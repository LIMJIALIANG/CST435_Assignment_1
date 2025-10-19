#!/bin/bash
# Setup Script for MapReduce Performance Comparison Project (Linux/Mac)

echo "MapReduce Performance Comparison - Setup Script"
echo "============================================================"

# Check if Docker is running
echo -e "\nChecking Docker..."
docker --version
if [ $? -ne 0 ]; then
    echo "Error: Docker is not installed or not running!"
    exit 1
fi

# Check if Docker Compose is available
docker-compose --version
if [ $? -ne 0 ]; then
    echo "Error: Docker Compose is not available!"
    exit 1
fi

echo -e "\nDocker is ready!"

# Install Python dependencies (for local testing)
echo -e "\nInstalling Python dependencies..."
pip install -r requirements.txt

# Generate gRPC code
echo -e "\nGenerating gRPC code..."
cd grpc_implementation
python -m grpc_tools.protoc -I./proto --python_out=. --grpc_python_out=. proto/mapreduce.proto
cd ..

echo -e "\ngRPC code generated!"

# Build Docker images
echo -e "\nBuilding Docker images..."
echo "This may take a few minutes..."

cd docker
docker-compose build
cd ..

if [ $? -eq 0 ]; then
    echo -e "\nDocker images built successfully!"
else
    echo -e "\nError building Docker images!"
    exit 1
fi

echo -e "\n============================================================"
echo "Setup completed successfully!"
echo "============================================================"

echo -e "\nNext steps:"
echo "1. Test individual implementations:"
echo "   - gRPC:           cd docker && docker-compose up grpc-client"
echo "   - XML-RPC:        cd docker && docker-compose up xmlrpc-client"
echo "   - MPI:            cd docker && docker-compose run --rm mpi-runner"
echo "   - Multiprocessing: python multiprocessing_implementation/mapreduce.py"
echo ""
echo "2. Run performance comparison:"
echo "   python performance_test.py"
echo ""
