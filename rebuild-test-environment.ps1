$rootFolder = Join-Path $env:TEMP 'sqlalchemy-firebird-tests'

# Clear rootFolder
Remove-Item -Path $rootFolder -Force -Recurse -ErrorAction SilentlyContinue
mkdir $rootFolder | Out-Null

# Download Firebird binaries
Write-Warning 'Download Firebird binaries...'
git clone --quiet --depth 1 --single-branch https://github.com/fdcastel/Rebuild-Firebird $rootFolder

# Create empty databases
'fb25', 'fb30', 'fb40' | ForEach-Object {
    $engine = $_

    Write-Warning "Creating $engine database..."

    $engineFolder = Join-Path $rootFolder $engine
    $isql = Join-Path $engineFolder 'isql.exe'

    $database = Join-Path $rootFolder "test.$engine.fdb"
    Remove-Item $database -Force -ErrorAction SilentlyContinue

    @"
    CREATE DATABASE '$database'
        USER 'SYSDBA' PASSWORD 'masterkey'
        PAGE_SIZE 8192 DEFAULT CHARACTER SET UTF8;
"@ | & $isql -quiet | Out-Null

}

# Update setup.cfg
$setupFile = './setup.cfg'

$hasDbSection = Select-String -Path $setupFile -Pattern '\[db\]'
if ($hasDbSection) {
    return
}

@"
[db]
firebird_fb40 = firebird+firebird://SYSDBA@/$rootFolder\TEST.FB40.FDB?charset=UTF8&fb_client_library=$rootFolder\fb40\fbclient.dll
firebird_fb30 = firebird+firebird://SYSDBA@/$rootFolder\TEST.FB30.FDB?charset=UTF8&fb_client_library=$rootFolder\fb30\fbclient.dll

fdb_fb40 = firebird+fdb://SYSDBA@/$rootFolder\TEST.FB40.FDB?charset=UTF8&fb_library_name=$rootFolder\fb40\fbclient.dll
fdb_fb30 = firebird+fdb://SYSDBA@/$rootFolder\TEST.FB30.FDB?charset=UTF8&fb_library_name=$rootFolder\fb30\fbclient.dll
fdb_fb25 = firebird+fdb://SYSDBA@/$rootFolder\TEST.FB25.FDB?charset=UTF8&fb_library_name=$rootFolder\fb25\fbclient.dll
"@ | Add-Content -Path $setupFile