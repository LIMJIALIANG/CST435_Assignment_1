# MapReduce Performance Comparison Project

## Overview
This project compares the performance of different distributed computing approaches:
- gRPC
- XML-RPC
- Request-Reply (ZeroMQ)
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
├── reqrep_implementation/
│   ├── server.py
│   └── client.py
├── mpi_implementation/
│   └── mapreduce.py
├── docker/
│   ├── Dockerfile.grpc
│   ├── Dockerfile.xmlrpc
│   ├── Dockerfile.reqrep
│   ├── Dockerfile.mpi
│   └── docker-compose.yml
├── data/
│   └── sample_text.txt
├── performance_test.py
├── requirements.txt
├── requirements-grpc.txt
├── requirements-reqrep.txt
└── requirements-mpi.txt
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
   docker-compose up grpc-client

   # Test XML-RPC
   docker-compose up xmlrpc-client

   # Test Request-Reply
   docker-compose up reqrep-client

   # Test MPI
   docker-compose run --rm mpi-runner
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
