# Docker Swarm Deployment Guide
# Step-by-step instructions for deploying with Docker Swarm

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Docker Swarm Deployment - Step by Step" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Step 1: Check if Swarm is already initialized
Write-Host "Step 1: Checking Docker Swarm status..." -ForegroundColor Yellow
$swarmStatus = docker info --format '{{.Swarm.LocalNodeState}}'
if ($swarmStatus -eq "active") {
    Write-Host "✓ Docker Swarm is already initialized" -ForegroundColor Green
} else {
    Write-Host "Initializing Docker Swarm..." -ForegroundColor Yellow
    docker swarm init
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ Docker Swarm initialized successfully" -ForegroundColor Green
    } else {
        Write-Host "✗ Failed to initialize Docker Swarm" -ForegroundColor Red
        exit 1
    }
}
Write-Host ""

# Step 2: Build Docker images
Write-Host "Step 2: Building Docker images..." -ForegroundColor Yellow
Write-Host "This may take a few minutes..." -ForegroundColor Gray
Set-Location $PSScriptRoot
docker-compose -f docker-compose.grpc.yml build
if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Docker images built successfully" -ForegroundColor Green
} else {
    Write-Host "✗ Failed to build Docker images" -ForegroundColor Red
    exit 1
}
Write-Host ""

# Step 3: Deploy stack to Swarm
Write-Host "Step 3: Deploying stack to Docker Swarm..." -ForegroundColor Yellow
docker stack deploy -c docker-compose.grpc.swarm.yml student-analysis
if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Stack deployed successfully" -ForegroundColor Green
} else {
    Write-Host "✗ Failed to deploy stack" -ForegroundColor Red
    exit 1
}
Write-Host ""

# Step 4: Wait for services to start
Write-Host "Step 4: Waiting for services to start..." -ForegroundColor Yellow
Start-Sleep -Seconds 5
Write-Host ""

# Step 5: Check service status
Write-Host "Step 5: Checking service status..." -ForegroundColor Yellow
docker service ls
Write-Host ""

# Step 6: View logs
Write-Host "Step 6: Viewing service logs..." -ForegroundColor Yellow
Write-Host "Server logs:" -ForegroundColor Cyan
docker service logs --tail 20 student-analysis_server
Write-Host ""
Write-Host "Client logs:" -ForegroundColor Cyan
docker service logs --tail 20 student-analysis_client
Write-Host ""

# Summary
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Deployment Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Useful commands:" -ForegroundColor Yellow
Write-Host "  docker service ls                              - List all services" -ForegroundColor Gray
Write-Host "  docker service logs student-analysis_server    - View server logs" -ForegroundColor Gray
Write-Host "  docker service logs student-analysis_client    - View client logs" -ForegroundColor Gray
Write-Host "  docker service ps student-analysis_server      - Check server tasks" -ForegroundColor Gray
Write-Host "  docker service ps student-analysis_client      - Check client tasks" -ForegroundColor Gray
Write-Host "  docker stack rm student-analysis               - Remove the stack" -ForegroundColor Gray
Write-Host "  docker swarm leave --force                     - Leave swarm mode" -ForegroundColor Gray
Write-Host ""
