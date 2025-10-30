# Run microservices client

Write-Host "Running Microservices Client..." -ForegroundColor Green
Write-Host ""

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$projectRoot = Split-Path -Parent (Split-Path -Parent $scriptDir)

# Activate virtual environment
$venvActivate = Join-Path $projectRoot ".venv\Scripts\Activate.ps1"
if (Test-Path $venvActivate) {
    Write-Host "Activating virtual environment..." -ForegroundColor Cyan
    & $venvActivate
}

# Run client
Write-Host "Initiating workflow: Client → A → B → C → D → E" -ForegroundColor Yellow
Write-Host ""
python "$scriptDir\microservices_client.py"
