#!/usr/bin/env pwsh
# Start all XML-RPC microservices

Write-Host "="*70 -ForegroundColor Cyan
Write-Host "Starting XML-RPC Microservices" -ForegroundColor Cyan
Write-Host "="*70 -ForegroundColor Cyan

# Set environment variables for service communication
$env:MAPREDUCE_HOST = "localhost"
$env:MAPREDUCE_PORT = "8001"
$env:MERGESORT_HOST = "localhost"
$env:MERGESORT_PORT = "8003"
$env:STATISTICS_HOST = "localhost"
$env:STATISTICS_PORT = "8005"

$env:MERGESORT_URL = "http://localhost:8003"
$env:STATISTICS_URL = "http://localhost:8005"

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

# Start services in order (Statistics first, then MergeSort, then MapReduce)
# This ensures downstream services are ready when upstream services start
Write-Host "`nStarting services (from end to start of chain)...`n" -ForegroundColor Green

Start-Service -ServiceName "Statistics Service" -ScriptPath "statistics.py" -Port "8005"
Start-Service -ServiceName "MergeSort Service (Sort CGPA + Grade)" -ScriptPath "mergesort.py" -Port "8003"
Start-Service -ServiceName "MapReduce Service (CGPA + Grade Count)" -ScriptPath "mapreduce.py" -Port "8001"

Write-Host "`n" + ("="*70) -ForegroundColor Cyan
Write-Host "All services started!" -ForegroundColor Green
Write-Host "="*70 -ForegroundColor Cyan
Write-Host "`nService Chain:" -ForegroundColor Yellow
Write-Host "  Client → MapReduce (8001) → MergeSort (8003) → Statistics (8005) → Client" -ForegroundColor White
Write-Host "`nTo run the client:" -ForegroundColor Yellow
Write-Host "  cd client" -ForegroundColor White
Write-Host "  .\run_client.ps1" -ForegroundColor White
Write-Host "`nTo stop all services, close the PowerShell windows or press Ctrl+C in each`n" -ForegroundColor Yellow

