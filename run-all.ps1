#
# Run all tests in parallel
#
start powershell {
    $host.ui.RawUI.WindowTitle = 'Firebird 2.5 (fdb)'
    .\.venv\Scripts\activate

    while ($true) {
        .\run-test.ps1 -Db 'fdb_fb25' -All
        pause
    }
}

start powershell {
    $host.ui.RawUI.WindowTitle = 'Firebird 3.0 (fdb)'
    .\.venv\Scripts\activate

    while ($true) {
        .\run-test.ps1 -Db 'fdb_fb30' -All
        pause
    }
}

start powershell {
    $host.ui.RawUI.WindowTitle = 'Firebird 3.0 (firebird)'
    .\.venv\Scripts\activate

    while ($true) {
        .\run-test.ps1 -Db 'firebird_fb30' -All
        pause
    }
}

start powershell {
    $host.ui.RawUI.WindowTitle = 'Firebird 4.0 (firebird)'
    .\.venv\Scripts\activate

    while ($true) {
        .\run-test.ps1 -Db 'firebird_fb40' -All
        pause
    }
}

start powershell {
    $host.ui.RawUI.WindowTitle = 'Firebird 5.0 (firebird)'
    .\.venv\Scripts\activate

    while ($true) {
        .\run-test.ps1 -Db 'firebird_fb50' -All
        pause
    }
}
