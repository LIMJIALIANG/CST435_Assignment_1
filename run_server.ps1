# Run gRPC Server
Write-Host "Starting gRPC Server..." -ForegroundColor Green
& "$PSScriptRoot\.venv\Scripts\python.exe" "$PSScriptRoot\server\server.py"
