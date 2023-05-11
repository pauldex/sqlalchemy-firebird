Param(
    [string]$Db, 
    [switch]$All, 
    [switch]$RebuildDbOnly
)

clear

#
# Get pytest arguments from launch.json
#
$launchFile = '.\.vscode\launch.json'
$launchJson = Get-Content $launchFile -Raw
# Remove comments -- https://stackoverflow.com/a/57092959
$launchJson = $launchJson -replace '(?m)\s*//.*?$' -replace '(?ms)/\*.*?\*/'
$launch = $launchJson | ConvertFrom-Json

$launchArgs = [System.Collections.ArrayList]$launch.configurations[0].args

$DbFromLaunch = $null
if ($launchArgs) {
    $indexDb = $launchArgs.IndexOf('--db')
    if ($indexDb -ne -1) {
        # "--db" in args from launch.json: Save it and remove from $launchArgs
        $DbFromLaunch = $launchArgs[$indexDb + 1]

        $launchArgs.RemoveAt($indexDb + 1)
        $launchArgs.RemoveAt($indexDb)
    }

}

if (-not $Db) {
    # -Db not informed. Try to use from launch.json
    $Db = $DbFromLaunch

    if (-not $Db) {
        throw 'Database connection (--db) not found in "launch.json" args. You must inform a -Db argument.'
    }
}

Write-Warning "Using connection '$Db'"

if ($All) {
    # Run all tests. Ignore "launch.json".
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

if ($RebuildDbOnly) {
    return
}


#
# Run tests
#

$db = "$($driver)_$($engine)"

$extraArgs = ""
if ($All) {
    # When running all tests, reduce log output.
    $extraArgs = "--log-info="
}



# Run "not hanging" tests first
$testOutput = $null
$host.ui.RawUI.WindowTitle = "$($db): Running 1st..."
& pytest $launchArgs --db $db -m "not hanging" $extraArgs | Tee-Object -Variable testOutput
$summary1st = $testOutput[-1].replace('=', '')
$host.ui.RawUI.WindowTitle = "$($db): $summary1st"

if ($?) {
    # Tests passed. Run "hanging" tests.
    $testOutput = $null
    $host.ui.RawUI.WindowTitle = "$($db): $summary1st / Running 2nd..."
    & pytest $launchArgs --db $db -m "hanging" $extraArgs | Tee-Object -Variable testOutput
    $summary2nd = $testOutput[-1].replace('=', '')
    $host.ui.RawUI.WindowTitle = "$($db): $summary1st / $summary2nd"
}
