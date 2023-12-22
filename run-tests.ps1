#
# Run all tests for a given driver/engine.
#
# By default, uses the same arguments from "launch.json".
#   Use -Db to force a specific driver/engine.
#   Use -All to force all tests to run (not the only ones specified in "launch.json")
#

Param(
    [string]$Db, 
    [switch]$All
)

Clear-Host   

#
# Get pytest arguments from "launch.json"
#
$launchJson = Get-Content '.\.vscode\launch.json' -Raw
$launchJson = $launchJson -replace '(?m)\s*//.*?$' -replace '(?ms)/\*.*?\*/'    # Remove comments -- https://stackoverflow.com/a/57092959
$launchValues = $launchJson | ConvertFrom-Json
$launchArgs = [System.Collections.ArrayList]$launchValues.configurations[0].args

# Get "--db" from "launch.json" arguments
$DbFromLaunch = $null
if ($launchArgs) {
    $indexDb = $launchArgs.IndexOf('--db')
    if ($indexDb -ne -1) {
        # Found "--db" in "launch.json": Use it and remove from $launchArgs
        $DbFromLaunch = $launchArgs[$indexDb + 1]

        $launchArgs.RemoveAt($indexDb + 1)
        $launchArgs.RemoveAt($indexDb)
    }
}

if (-not $Db) {
    # -Db not informed. Try to use from "launch.json"
    $Db = $DbFromLaunch

    if (-not $Db) {
        throw 'Database connection (--db) not found in "launch.json" args. You must inform a -Db argument.'
    }
}

Write-Warning "Using connection '$Db'"

if ($All) {
    # Ignore "launch.json" when running all tests.
    $launchArgs = $()
}

$driver, $engine = $Db.Split('_')

$rootFolder = Join-Path $env:TEMP 'sqlalchemy-firebird-tests'
$engineFolder = Join-Path $rootFolder $engine
$isql = Join-Path $engineFolder 'isql.exe'

$databaseFile = Join-Path $rootFolder "$($driver).$($engine).fdb"

#
# Recreate database
#
Remove-Item $databaseFile -Force -ErrorAction SilentlyContinue
Write-Warning "Creating '$engine' database..."
@"
    CREATE DATABASE '$databaseFile'
        USER 'SYSDBA' PASSWORD 'masterkey'
        PAGE_SIZE 8192 DEFAULT CHARACTER SET UTF8;
"@ | & $isql -quiet | Out-Null

#
# Run tests
#
$db = "$($driver)_$($engine)"

$extraArgs = @(
    '--tb=no',    # Disable tracebacks
    '--color=yes' # Force color in output. Pytest disables it because Tee-Object redirection
)

# Set console width in chars
[console]::WindowWidth=300

$host.ui.RawUI.WindowTitle = "[$db]: (Running...)"
& pytest $launchArgs --db $db $extraArgs 2>$null | Tee-Object -Variable testOutput
$pytestExitCode = $LASTEXITCODE
$summary1st = $testOutput[-1] -replace '\x1b\[\d+(;\d+)?m' -replace '='    # strip colors and '='
$host.ui.RawUI.WindowTitle = "[$db]: $summary1st (exit code = $pytestExitCode)"
