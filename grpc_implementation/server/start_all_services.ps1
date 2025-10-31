# Start all 3 microservices (each on a different port)

Write-Host "Starting Microservices..." -ForegroundColor Green
Write-Host ""

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$projectRoot = Split-Path -Parent (Split-Path -Parent $scriptDir)

# Activate virtual environment
$venvActivate = Join-Path $projectRoot ".venv\Scripts\Activate.ps1"
if (Test-Path $venvActivate) {
    Write-Host "Activating virtual environment..." -ForegroundColor Cyan
    & $venvActivate
}

# Start each service in a separate terminal
Write-Host "Starting MapReduce Service (Port 50051) - CGPA + Grade Classification..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$scriptDir'; & '$venvActivate'; python mapreduce_cgpa.py"
Start-Sleep -Seconds 2

Write-Host "Starting MergeSort Service (Port 50053) - Sort CGPA + Grade..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$scriptDir'; & '$venvActivate'; python mergesort_cgpa.py"
Start-Sleep -Seconds 2

Write-Host "Starting Statistics Service (Port 50055) - Statistical Analysis..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$scriptDir'; & '$venvActivate'; python statistics.py"
Start-Sleep -Seconds 2

Write-Host ""
Write-Host "All 3 services started!" -ForegroundColor Green
Write-Host "Service Chain: MapReduce(50051) → MergeSort(50053) → Statistics(50055)" -ForegroundColor Cyan
Write-Host ""
Write-Host "Now run the client:" -ForegroundColor Yellow
Write-Host "  cd ..\client" -ForegroundColor White
Write-Host "  .\run_client.ps1" -ForegroundColor White

