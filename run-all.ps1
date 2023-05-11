#
# Run all tests in parallel
#
start powershell {
    .\.venv\Scripts\activate
    while ($true) {
        .\run-test.ps1 -Db 'fdb_fb25' -All
        pause
    }
}

start powershell {
    .\.venv\Scripts\activate
    while ($true) {
        .\run-test.ps1 -Db 'fdb_fb30' -All
        pause
    }
}

start powershell {
    .\.venv\Scripts\activate

    while ($true) {
        .\run-test.ps1 -Db 'firebird_fb30' -All
        pause
    }
}

start powershell {
    .\.venv\Scripts\activate
    while ($true) {
        .\run-test.ps1 -Db 'firebird_fb40' -All
        pause
    }
}

start powershell {
    .\.venv\Scripts\activate
    while ($true) {
        .\run-test.ps1 -Db 'firebird_fb50' -All
        pause
    }
}
