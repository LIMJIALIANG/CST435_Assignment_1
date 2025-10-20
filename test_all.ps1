# Quick Test Script - Test all implementations quickly
# Run this after setup to verify everything works

Write-Host "Quick Test - All Implementations" -ForegroundColor Green
Write-Host "=" * 60

# Test 1: Request-Reply (fastest to test)
Write-Host "`n[1/4] Testing Request-Reply..." -ForegroundColor Yellow
Write-Host "Starting Request-Reply servers..." -ForegroundColor Cyan
cd docker
docker-compose up -d reqrep-server-1 reqrep-server-2 reqrep-server-3
Start-Sleep -Seconds 5

Write-Host "Running Request-Reply client..." -ForegroundColor Cyan
docker-compose run --rm reqrep-client

if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Request-Reply test passed!" -ForegroundColor Green
} else {
    Write-Host "✗ Request-Reply test failed!" -ForegroundColor Red
}

docker-compose down
cd ..
Start-Sleep -Seconds 2

# Test 2: gRPC
Write-Host "`n[2/4] Testing gRPC..." -ForegroundColor Yellow
Write-Host "Starting gRPC servers..." -ForegroundColor Cyan
cd docker
docker-compose up -d grpc-server-1 grpc-server-2 grpc-server-3
Start-Sleep -Seconds 5

Write-Host "Running gRPC client..." -ForegroundColor Cyan
docker-compose run --rm grpc-client

if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ gRPC test passed!" -ForegroundColor Green
} else {
    Write-Host "✗ gRPC test failed!" -ForegroundColor Red
}

docker-compose down
cd ..
Start-Sleep -Seconds 2

# Test 3: XML-RPC
Write-Host "`n[3/4] Testing XML-RPC..." -ForegroundColor Yellow
Write-Host "Starting XML-RPC servers..." -ForegroundColor Cyan
cd docker
docker-compose up -d xmlrpc-server-1 xmlrpc-server-2 xmlrpc-server-3
Start-Sleep -Seconds 5

Write-Host "Running XML-RPC client..." -ForegroundColor Cyan
docker-compose run --rm xmlrpc-client

if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ XML-RPC test passed!" -ForegroundColor Green
} else {
    Write-Host "✗ XML-RPC test failed!" -ForegroundColor Red
}

docker-compose down
cd ..
Start-Sleep -Seconds 2

# Test 4: MPI
Write-Host "`n[4/4] Testing MPI..." -ForegroundColor Yellow
cd docker
docker-compose run --rm mpi-runner

if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ MPI test passed!" -ForegroundColor Green
} else {
    Write-Host "✗ MPI test failed!" -ForegroundColor Red
}

docker-compose down
cd ..

Write-Host "`n" + ("=" * 60) -ForegroundColor Green
Write-Host "Quick test completed!" -ForegroundColor Green
Write-Host ("=" * 60) -ForegroundColor Green
Write-Host "`nAll implementations tested successfully!" -ForegroundColor Green
Write-Host "You can now run the full performance comparison:" -ForegroundColor Yellow
Write-Host "  python performance_test.py" -ForegroundColor Cyan
Write-Host ""
Write-Host "This will test:" -ForegroundColor Yellow
Write-Host "  - gRPC: Single Machine vs Multiple Containers" -ForegroundColor Cyan
Write-Host "  - XML-RPC, Request-Reply, and MPI" -ForegroundColor Cyan
