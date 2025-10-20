# MapReduce Performance Comparison Project

## Overview
This project compares the performance of different distributed computing approaches:
- **gRPC** (Single Machine vs Multiple Containers)
- XML-RPC
- Request-Reply (ZeroMQ)
- MPI (Message Passing Interface)

**Key Feature**: Compares gRPC performance running on a single computer versus multiple containers to demonstrate the trade-offs between local and distributed processing.

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

### Compare All Implementations
Run the comprehensive performance comparison:
```bash
python performance_test.py
```

This tests:
- **gRPC Single Machine** - Local process without containers
- **gRPC Multiple Containers** - Distributed across 3 Docker containers
- XML-RPC (3 containers)
- Request-Reply/ZeroMQ (3 containers)
- MPI (1 container, 3 processes)

### Expected Output

**Console Output:**
```
PERFORMANCE COMPARISON REPORT
============================================================
Execution Times (seconds):
Implementation       Mean       Min        Max        Runs      
------------------------------------------------------------
grpc_single         2.3450     2.2100     2.4500     3         
grpc_multi          2.6700     2.5200     2.7900     3         
xmlrpc              3.1200     2.9800     3.2400     3         
reqrep              2.8900     2.7500     3.0100     3         
mpi                 3.0100     2.8900     3.1500     3         

============================================================
gRPC: Single Machine vs Multiple Containers
============================================================
Single Machine:       2.3450s
Multiple Containers:  2.6700s
Container Overhead:   +13.86%
Result: Single machine is 1.14x faster
Recommendation: Use single machine for small datasets
```

**Generated Files:**
- `performance_results/results_YYYYMMDD_HHMMSS.json` - Detailed results
- `performance_results/results_YYYYMMDD_HHMMSS.csv` - Tabular data
- `performance_results/performance_comparison_YYYYMMDD_HHMMSS.png` - Charts

### Key Findings

**Single Machine Advantages:**
- Lower latency (no network overhead)
- No containerization overhead
- Better for small datasets (< 100MB)
- Simpler setup for development

**Multiple Containers Advantages:**
- Scalability for large datasets
- Fault tolerance (container failure isolation)
- Resource isolation
- Production-ready deployment
- Can distribute across multiple physical machines
