$rootFolder = Join-Path $env:TEMP 'sqlalchemy-firebird-tests'

# Clear rootFolder
Remove-Item -Path $rootFolder -Force -Recurse -ErrorAction SilentlyContinue
mkdir $rootFolder | Out-Null

# Download Firebird binaries
Write-Warning 'Download Firebird binaries...'
git clone --quiet --depth 1 --single-branch https://github.com/fdcastel/firebird-binaries $rootFolder

# Create empty databases
& "$rootFolder\Rebuild-Databases.ps1" -Verbose -DbPath $rootFolder -DbPrefix 'firebird'
& "$rootFolder\Rebuild-Databases.ps1" -Verbose -DbPath $rootFolder -DbPrefix 'fdb'

# Update setup.cfg
$setupFile = './setup.cfg'

$hasDbSection = Select-String -Path $setupFile -Pattern '\[db\]'
if ($hasDbSection) {
    return
}

@"

[db]
firebird_fb50 = firebird+firebird://SYSDBA@/$rootFolder\FIREBIRD.FB50.FDB?charset=UTF8&fb_client_library=$rootFolder\fb50\fbclient.dll
firebird_fb40 = firebird+firebird://SYSDBA@/$rootFolder\FIREBIRD.FB40.FDB?charset=UTF8&fb_client_library=$rootFolder\fb40\fbclient.dll
firebird_fb30 = firebird+firebird://SYSDBA@/$rootFolder\FIREBIRD.FB30.FDB?charset=UTF8&fb_client_library=$rootFolder\fb30\fbclient.dll

fdb_fb50 = firebird+fdb://SYSDBA@/$rootFolder\FDB.FB50.FDB?charset=UTF8&fb_library_name=$rootFolder\fb50\fbclient.dll
fdb_fb40 = firebird+fdb://SYSDBA@/$rootFolder\FDB.FB40.FDB?charset=UTF8&fb_library_name=$rootFolder\fb40\fbclient.dll
fdb_fb30 = firebird+fdb://SYSDBA@/$rootFolder\FDB.FB30.FDB?charset=UTF8&fb_library_name=$rootFolder\fb30\fbclient.dll
fdb_fb25 = firebird+fdb://SYSDBA@/$rootFolder\FDB.FB25.FDB?charset=UTF8&fb_library_name=$rootFolder\fb25\fbclient.dll
"@ | Add-Content -Path $setupFile

