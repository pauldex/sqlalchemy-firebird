start powershell {
    $host.ui.RawUI.WindowTitle = 'Firebird 2.5 (fdb)'
    .\.venv\Scripts\activate

    while ($true) {
        .\run-test.ps1 -Db 'fdb_fb25' -Full
        pause
    }
}

start powershell {
    $host.ui.RawUI.WindowTitle = 'Firebird 3.0 (fdb)'
    .\.venv\Scripts\activate

    while ($true) {
        .\run-test.ps1 -Db 'fdb_fb30' -Full
        pause
    }
}

start powershell {
    $host.ui.RawUI.WindowTitle = 'Firebird 4.0 (fdb)'
    .\.venv\Scripts\activate

    while ($true) {
        .\run-test.ps1 -Db 'fdb_fb40' -Full
        pause
    }
}
