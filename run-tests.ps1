#
# Run all tests for a given driver/engine.
#

[CmdletBinding()]
param(
    [Parameter(Mandatory=$true)]
    [ValidateScript({
        if (Get-Content 'setup.cfg' | Select-String -Pattern "^$_\s*=") { return $true }
        throw [System.Management.Automation.ValidationMetadataException] "The database '$_' was not found in 'setup.cfg'."
    })]
    [string]$Database
)

if (-not $env:VIRTUAL_ENV) {
    throw "Virtual environment not detected. Please run '.venv/scripts/activate' first."
}

# Set console width
[console]::WindowWidth=260

Clear-Host   
Write-Warning "Using connection '$Database'..."

# Recreate test database
rebuild-test-databases $Database

# pytest: do not truncate error messages -- https://github.com/pytest-dev/pytest/issues/9920
$env:CI = 'True' 

# pytest additional parameters
$extraParams = @(
    '--tb=no',    # Disable tracebacks
    '--color=yes' # Force color in output. Pytest disables it because Tee-Object redirection.
)

# Run pytest
$host.ui.RawUI.WindowTitle = "[$Database]: (Running...)"
& pytest --db $Database $extraParams 2>$null | Tee-Object -Variable testOutput
$pytestExitCode = $LASTEXITCODE

# Update window title with test results
$summary1st = $testOutput[-1] -replace '\x1b\[\d+(;\d+)?m' -replace '='    # strip colors and '='
$host.ui.RawUI.WindowTitle = "[$Database]: $summary1st (exit code = $pytestExitCode)"
