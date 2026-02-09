# Guardian Test Mode
$ErrorActionPreference = "Continue"

$CLI_PATH = "C:\Users\Administrator\Desktop\CLIProxyAPI_6.7.46_windows_amd64\cli-proxy-api.exe"
$CLI_DIR = "C:\Users\Administrator\Desktop\CLIProxyAPI_6.7.46_windows_amd64"

Write-Host "Checking CLIProxyAPI..."
if (Test-Path $CLI_PATH) {
    Write-Host "Path exists: $CLI_PATH"
} else {
    Write-Host "ERROR: Path NOT found!"
}

$cli = Get-Process -Name "cli-proxy-api" -ErrorAction SilentlyContinue
if ($cli) {
    Write-Host "Process is running."
} else {
    Write-Host "Process is NOT running."
}

Write-Host "Done."
