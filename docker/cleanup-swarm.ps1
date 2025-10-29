# Docker Swarm Cleanup Script
# Removes the stack and optionally leaves swarm mode

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Docker Swarm Cleanup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Step 1: Remove stack
Write-Host "Step 1: Removing stack..." -ForegroundColor Yellow
docker stack rm student-analysis
if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Stack removed successfully" -ForegroundColor Green
    Write-Host "Waiting for services to shut down..." -ForegroundColor Gray
    Start-Sleep -Seconds 5
} else {
    Write-Host "✗ Failed to remove stack (it may not exist)" -ForegroundColor Yellow
}
Write-Host ""

# Step 2: Ask about leaving swarm
Write-Host "Step 2: Leave swarm mode?" -ForegroundColor Yellow
$response = Read-Host "Do you want to leave Docker Swarm mode? (y/n)"
if ($response -eq "y" -or $response -eq "Y") {
    docker swarm leave --force
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ Left swarm mode successfully" -ForegroundColor Green
    } else {
        Write-Host "✗ Failed to leave swarm mode" -ForegroundColor Red
    }
} else {
    Write-Host "Swarm mode still active" -ForegroundColor Gray
}
Write-Host ""

Write-Host "Cleanup complete!" -ForegroundColor Green
