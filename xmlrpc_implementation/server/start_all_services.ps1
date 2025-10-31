#!/usr/bin/env pwsh
# Start all XML-RPC microservices

Write-Host "="*70 -ForegroundColor Cyan
Write-Host "Starting XML-RPC Microservices" -ForegroundColor Cyan
Write-Host "="*70 -ForegroundColor Cyan

# Set environment variables for service URLs
$env:SERVICE_A_HOST = "localhost"
$env:SERVICE_A_PORT = "8001"
$env:SERVICE_B_HOST = "localhost"
$env:SERVICE_B_PORT = "8002"
$env:SERVICE_C_HOST = "localhost"
$env:SERVICE_C_PORT = "8003"
$env:SERVICE_D_HOST = "localhost"
$env:SERVICE_D_PORT = "8004"
$env:SERVICE_E_HOST = "localhost"
$env:SERVICE_E_PORT = "8005"

$env:SERVICE_B_URL = "http://localhost:8002"
$env:SERVICE_C_URL = "http://localhost:8003"
$env:SERVICE_D_URL = "http://localhost:8004"
$env:SERVICE_E_URL = "http://localhost:8005"

# Function to start a service in a new terminal
function Start-Service {
    param(
        [string]$ServiceName,
        [string]$ScriptPath,
        [string]$Port
    )
    
    Write-Host "Starting $ServiceName on port $Port..." -ForegroundColor Yellow
    
    # Start in new PowerShell window
    Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PSScriptRoot'; python '$ScriptPath'"
    
    # Wait a bit for service to start
    Start-Sleep -Seconds 2
}

# Start services in order (E first, then D, C, B, A)
# This ensures downstream services are ready when upstream services start
Write-Host "`nStarting services (from end to start of chain)...`n" -ForegroundColor Green

Start-Service -ServiceName "Service E (Statistics)" -ScriptPath "service_e.py" -Port "8005"
Start-Service -ServiceName "Service D (Sort Grade)" -ScriptPath "service_d.py" -Port "8004"
Start-Service -ServiceName "Service C (Sort CGPA)" -ScriptPath "service_c.py" -Port "8003"
Start-Service -ServiceName "Service B (Grade Count)" -ScriptPath "service_b.py" -Port "8002"
Start-Service -ServiceName "Service A (CGPA Count)" -ScriptPath "service_a.py" -Port "8001"

Write-Host "`n" + ("="*70) -ForegroundColor Cyan
Write-Host "All services started!" -ForegroundColor Green
Write-Host "="*70 -ForegroundColor Cyan
Write-Host "`nService Chain:" -ForegroundColor Yellow
Write-Host "  Client → Service A (8001) → Service B (8002) → Service C (8003) → Service D (8004) → Service E (8005) → Client" -ForegroundColor White
Write-Host "`nTo run the client:" -ForegroundColor Yellow
Write-Host "  cd client" -ForegroundColor White
Write-Host "  .\run_client.ps1" -ForegroundColor White
Write-Host "`nTo stop all services, close the PowerShell windows or press Ctrl+C in each`n" -ForegroundColor Yellow
