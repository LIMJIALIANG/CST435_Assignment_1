#!/usr/bin/env pwsh
# Run XML-RPC microservices client

Write-Host "="*70 -ForegroundColor Cyan
Write-Host "XML-RPC Microservices Client" -ForegroundColor Cyan
Write-Host "="*70 -ForegroundColor Cyan

# Set environment variables
$env:SERVICE_A_URL = "http://localhost:8001"
$env:CSV_PATH = "../../data/students.csv"
$env:OUTPUT_FILE = "../../results/xmlrpc_performance_metrics.json"

Write-Host "`nConfiguration:" -ForegroundColor Yellow
Write-Host "  Service A URL: $env:SERVICE_A_URL" -ForegroundColor White
Write-Host "  CSV Path: $env:CSV_PATH" -ForegroundColor White
Write-Host "  Output File: $env:OUTPUT_FILE" -ForegroundColor White
Write-Host ""

# Run client
python client.py

Write-Host "`n" + ("="*70) -ForegroundColor Cyan
Write-Host "Client execution completed" -ForegroundColor Green
Write-Host "="*70 -ForegroundColor Cyan
