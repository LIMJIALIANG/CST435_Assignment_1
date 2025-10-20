# Setup Script for MapReduce Performance Comparison Project
# This script will set up the entire environment

Write-Host "MapReduce Performance Comparison - Setup Script" -ForegroundColor Green
Write-Host "=" * 60

# Check if Docker is running
Write-Host "`nChecking Docker..." -ForegroundColor Yellow
docker --version
if ($LASTEXITCODE -ne 0) {
    Write-Host "Error: Docker is not installed or not running!" -ForegroundColor Red
    exit 1
}

# Check if Docker Compose is available
docker-compose --version
if ($LASTEXITCODE -ne 0) {
    Write-Host "Error: Docker Compose is not available!" -ForegroundColor Red
    exit 1
}

Write-Host "`nDocker is ready!" -ForegroundColor Green

# Install Python dependencies (for local testing)
Write-Host "`nInstalling Python dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt

# Generate gRPC code
Write-Host "`nGenerating gRPC code..." -ForegroundColor Yellow
cd grpc_implementation
python -m grpc_tools.protoc -I./proto --python_out=. --grpc_python_out=. proto/mapreduce.proto
cd ..

Write-Host "`ngRPC code generated!" -ForegroundColor Green

# Build Docker images
Write-Host "`nBuilding Docker images..." -ForegroundColor Yellow
Write-Host "This may take a few minutes..." -ForegroundColor Cyan

cd docker
docker-compose build
cd ..

if ($LASTEXITCODE -eq 0) {
    Write-Host "`nDocker images built successfully!" -ForegroundColor Green
} else {
    Write-Host "`nError building Docker images!" -ForegroundColor Red
    exit 1
}

Write-Host "`n" + ("=" * 60) -ForegroundColor Green
Write-Host "Setup completed successfully!" -ForegroundColor Green
Write-Host ("=" * 60) -ForegroundColor Green

Write-Host "`nNext steps:" -ForegroundColor Yellow
Write-Host "1. Test individual implementations:"
Write-Host "   - gRPC:           cd docker; docker-compose up grpc-client"
Write-Host "   - XML-RPC:        cd docker; docker-compose up xmlrpc-client"
Write-Host "   - Request-Reply:  cd docker; docker-compose run --rm reqrep-client"
Write-Host "   - MPI:            cd docker; docker-compose run --rm mpi-runner"
Write-Host ""
Write-Host "2. Run performance comparison (includes single vs multi):"
Write-Host "   python performance_test.py"
Write-Host "   Note: Tests gRPC on single machine AND multiple containers"
Write-Host ""
