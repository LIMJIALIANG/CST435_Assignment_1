# Start all 5 microservices (each on a different port)

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
Write-Host "Starting Service A (Port 50051)..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$scriptDir'; & '$venvActivate'; python service_a_mapreduce_cgpa.py"
Start-Sleep -Seconds 2

Write-Host "Starting Service B (Port 50052)..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$scriptDir'; & '$venvActivate'; python service_b_mapreduce_grade.py"
Start-Sleep -Seconds 2

Write-Host "Starting Service C (Port 50053)..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$scriptDir'; & '$venvActivate'; python service_c_mergesort_cgpa.py"
Start-Sleep -Seconds 2

Write-Host "Starting Service D (Port 50054)..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$scriptDir'; & '$venvActivate'; python service_d_mergesort_grade.py"
Start-Sleep -Seconds 2

Write-Host "Starting Service E (Port 50055)..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$scriptDir'; & '$venvActivate'; python service_e_statistics.py"
Start-Sleep -Seconds 2

Write-Host ""
Write-Host "All 5 services started!" -ForegroundColor Green
Write-Host "Service Chain: A(50051) → B(50052) → C(50053) → D(50054) → E(50055)" -ForegroundColor Cyan
Write-Host ""
Write-Host "Now run the client:" -ForegroundColor Yellow
Write-Host "  cd ..\client" -ForegroundColor White
Write-Host "  .\run_client.ps1" -ForegroundColor White
