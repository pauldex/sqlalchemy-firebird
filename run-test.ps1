param([string]$Db, [switch]$Full) 

#
# Get pytest arguments from launch.json
#
$launchFile = '.\.vscode\launch.json'
$launchJson = Get-Content $launchFile -Raw
# Remove comments -- https://stackoverflow.com/a/57092959
$launchJson = $launchJson -replace '(?m)\s*//.*?$' -replace '(?ms)/\*.*?\*/'
$launch = $launchJson | ConvertFrom-Json

$launchArgs = [System.Collections.ArrayList]$launch.configurations[0].args
$indexDb = $launchArgs.IndexOf('--db')


if (-not $Db) {
    if ($indexDb -ne -1) {
        $Db = $launchArgs[$indexDb + 1]
        $launchArgs.RemoveAt($indexDb + 1)
        $launchArgs.RemoveAt($indexDb)
    }
}

if (-not $Db) {
    throw 'You must inform a -Db argument.'
}
Write-Warning "Using connection '$Db'"

if ($Full) {
    $launchArgs = $()
}


$driver, $engine = $Db.Split('_')

$rootFolder = Join-Path $env:TEMP 'sqlalchemy-firebird-tests'
$engineFolder = Join-Path $rootFolder $engine
$isql = Join-Path $engineFolder 'isql.exe'

$database = Join-Path $rootFolder "test.$engine.fdb"

#
# Recreate database
#
Remove-Item $database -Force -ErrorAction SilentlyContinue
Write-Warning "Creating '$engine' database..."
@"
    CREATE DATABASE '$database'
        USER 'SYSDBA' PASSWORD 'masterkey'
        PAGE_SIZE 8192 DEFAULT CHARACTER SET UTF8;
"@ | & $isql -quiet | Out-Null


#
# Run tests
#
clear
$db = "$($driver)_$($engine)"
$host.ui.RawUI.WindowTitle = $db
& pytest $launchArgs --db $db
