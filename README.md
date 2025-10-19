# MapReduce Performance Comparison Project

## Overview
This project compares the performance of different distributed computing approaches:
- gRPC
- XML-RPC
- Python Multiprocessing
- MPI (Message Passing Interface)

## Project Structure
```
.
├── grpc_implementation/
│   ├── proto/
│   │   └── mapreduce.proto
│   ├── server.py
│   ├── client.py
│   ├── mapreduce_pb2.py (generated)
│   └── mapreduce_pb2_grpc.py (generated)
├── xmlrpc_implementation/
│   ├── server.py
│   └── client.py
├── multiprocessing_implementation/
│   └── mapreduce.py
├── mpi_implementation/
│   └── mapreduce.py
├── docker/
│   ├── Dockerfile.grpc
│   ├── Dockerfile.xmlrpc
│   ├── Dockerfile.mpi
│   └── docker-compose.yml
├── data/
│   └── sample_text.txt
├── performance_test.py
└── requirements.txt
```

## Setup Instructions

### Prerequisites
- Docker Desktop installed
- Python 3.9+
- Docker Compose

### Installation Steps

1. **Install Python dependencies (for local testing)**
   ```bash
   pip install -r requirements.txt
   ```

2. **Generate gRPC code**
   ```bash
   cd grpc_implementation
   python -m grpc_tools.protoc -I./proto --python_out=. --grpc_python_out=. proto/mapreduce.proto
   ```

3. **Build Docker images**
   ```bash
   docker-compose build
   ```

4. **Run tests**
   ```bash
   # Test gRPC
   docker-compose up grpc-test

   # Test XML-RPC
   docker-compose up xmlrpc-test

   # Test MPI
   docker-compose up mpi-test
   ```

## Performance Testing
Run the performance comparison:
```bash
python performance_test.py
```

## Expected Output
- Transaction duration for each approach
- Throughput (requests/second)
- Resource utilization
- Comparison charts
