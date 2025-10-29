# Run XML-RPC Server
Write-Host "Starting XML-RPC Server..." -ForegroundColor Green
& "$PSScriptRoot\..\.venv\Scripts\python.exe" "$PSScriptRoot\server\server.py"
