start powershell {
    $host.ui.RawUI.WindowTitle = 'Firebird 3.0 (firebird)'
    .\.venv\Scripts\activate

    while ($true) {
        .\run-test.ps1 -Db 'firebird_fb30' -Full
        pause
    }
}

start powershell {
    $host.ui.RawUI.WindowTitle = 'Firebird 4.0 (firebird)'
    .\.venv\Scripts\activate

    while ($true) {
        .\run-test.ps1 -Db 'firebird_fb40' -Full
        pause
    }
}
