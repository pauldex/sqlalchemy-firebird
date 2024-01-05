#
# Run all tests in parallel (one process per driver/engine combination)
#

'fdb_fb25','fdb_fb30','firebird_fb30','firebird_fb40','firebird_fb50' | ForEach-Object {
    Start-Process 'powershell' ".\.venv\Scripts\activate ; while (`$true) { .\run-tests.ps1 -Db $_ ; pause }"
}
