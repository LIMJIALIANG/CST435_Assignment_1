# CST435 Assignment 1 - Student Marks Analysis with gRPC

## Problem Statement
This project implements a distributed student marks analysis system using gRPC for inter-service communication. The system performs:
1. **MapReduce**: Count CGPA ranges and grade distributions
2. **Merge Sort**: Rank students by grades
3. **Statistical Analysis**: Calculate average CGPA per faculty, grade distribution, and pass rates

## Architecture
The system uses a client-server architecture with gRPC protocol:
- **Server**: Provides multiple service endpoints for different operations
- **Client**: Triggers services and measures performance

## Project Structure
```
.
📁 CST435_Assignment_1/
├── 🔧 grpc_implementation/      # gRPC Protocol Implementation
│   ├── proto/                   # Protocol Buffer definitions
│   │   └── student_service.proto
│   ├── server/                  # gRPC Server
│   │   ├── server.py
│   │   └── generated/          # Generated gRPC code
│   ├── client/                  # gRPC Client
│   │   ├── client.py
│   │   └── generated/          # Generated gRPC code
│   ├── run_server.ps1/.bat     # Convenience scripts
│   └── run_client.ps1/.bat
│
├── 🔧 xmlrpc_implementation/    # XML-RPC Protocol Implementation (Future)
│   ├── server_xmlrpc/          # XML-RPC Server
│   └── client_xmlrpc/          # XML-RPC Client
│
├── 📦 services/                 # Shared Service Implementations
│   ├── mapreduce_service.py    # MapReduce logic (protocol-independent)
│   ├── mergesort_service.py    # MergeSort logic (protocol-independent)
│   └── stats_service.py        # Statistics logic (protocol-independent)
│
├── 📊 data/                     # Sample student data
│   └── students.csv
│
├── 🐳 docker/                   # Docker configurations
│   ├── Dockerfile.server
│   ├── Dockerfile.client
│   └── docker-compose.yml
│
├── 📈 results/                  # Performance results
├── 📄 requirements.txt
└── 📖 README.md
```


## Features
- **MapReduce Operations**: Parallel processing of CGPA and grade counting
- **Merge Sort**: Distributed sorting for student rankings
- **Statistical Analysis**: Grade distribution, pass rates, average CGPA per faculty
- **Performance Metrics**: Timing measurements for same-machine vs different-machine setups
- **Docker Support**: Containerization for easy deployment and testing

## Installation

### Prerequisites
- Python 3.13+ (or 3.8+)
- Docker (optional, for containerized testing)
- pip

### Setup
```powershell
# 1. Install dependencies (creates virtual environment automatically)
pip install -r requirements.txt

# 2. Generate gRPC code from proto files
python generate_proto.py
```

## Usage

### Option 1: gRPC Implementation (Primary) ⭐

#### Method 1: Using Convenience Scripts (EASIEST)
```powershell
# Terminal 1: Start gRPC server
cd grpc_implementation
.\run_server.ps1    # or run_server.bat

# Terminal 2: Run gRPC client
cd grpc_implementation
.\run_client.ps1    # or run_client.bat
```

#### Method 2: Activate Virtual Environment
```powershell
# Activate virtual environment (once per terminal session)
.\.venv\Scripts\Activate.ps1

# Terminal 1: Start gRPC server
cd grpc_implementation
python server/server.py

# Terminal 2: Run gRPC client
cd grpc_implementation
python client/client.py
```

### Option 2: XML-RPC Implementation (Future)
```powershell
# Coming soon - XML-RPC protocol implementation
cd xmlrpc_implementation
```

### Option 3: Protocol Comparison
```powershell
# Compare performance between gRPC and XML-RPC
python compare_protocols.py
```

## Docker Deployment

### Method 1: Docker Compose - Local Containers (⚠️ Windows DNS Issue)
**What it does**: Runs server and client in **separate containers on the same machine** using bridge networking.

**Note**: On Windows Docker Desktop, there's a known DNS resolution issue with bridge networks that may cause connection failures. **For reliable local testing, use native Python execution instead** (see Test 1 below).

```powershell
# Navigate to docker directory
cd docker

# Build and run with docker-compose
docker-compose up --build

# To stop
docker-compose down
```

**When to use**: Linux/Mac users, or if you want to test containerization overhead.

---

### Method 2: Docker Swarm - Distributed Orchestration ⭐ (Recommended for Assignment)
**What it does**: Simulates **containers running on different machines** using overlay networking. This represents a **true distributed system** scenario.

**Why use this**: Demonstrates network overhead and latency when services communicate across different hosts (even though they're on the same physical machine).

```powershell
# Step 1: Remove any existing bridge networks (important!)
docker network rm docker_student-network student-analysis_student-network

# Step 2: Initialize Docker Swarm (one-time setup)
docker swarm init

# Step 3: Build Docker images
cd docker
docker-compose build

# Step 4: Deploy stack to Swarm (uses overlay network)
docker stack deploy -c docker-compose.swarm.yml student-analysis

# Step 5: Check services status
docker service ls

# Step 6: View logs
docker service logs student-analysis_server --tail 50
docker service logs student-analysis_client --tail 50

# Step 7: Check service tasks (verify completion)
docker service ps student-analysis_client

# Cleanup: Remove stack
docker stack rm student-analysis

# Optional: Leave swarm mode
docker swarm leave --force
```

**Performance Note**: Swarm uses overlay networking which adds realistic network latency, simulating communication between different physical machines.


## Performance Testing

### Test Scenarios

#### Test 1: Same Machine (No Containers)
Run server and client directly on your machine using virtual environment:
```powershell
# Terminal 1
cd grpc_implementation
.\run_server.ps1

# Terminal 2
cd grpc_implementation
.\run_client.ps1
```
**Expected Results**: Lowest latency, baseline performance

#### Test 2: Docker Containers (Same Machine)
Run both services in separate containers:
```powershell
cd docker
docker-compose up --build
```
**Expected Results**: Slight overhead from containerization and virtual networking
**Note**: May have DNS issues on Windows. Use Swarm instead for distributed testing.

#### Test 3: Docker Swarm (Simulated Different Machines) ⭐ Recommended
Deploy using Docker Swarm with overlay networking:
```powershell
# Remove old networks first
docker network rm docker_student-network student-analysis_student-network 2>$null

docker swarm init
cd docker
docker-compose build
docker stack deploy -c docker-compose.swarm.yml student-analysis
```
**Expected Results**: Additional network overhead from overlay networking, most realistic distributed scenario. Shows communication latency between "different machines".

### Performance Metrics
The client automatically measures and records:
- **Server processing time**: Time taken by server to process the request
- **Total request time**: End-to-end time including network latency
- **Network overhead**: Difference between total time and server processing time
- **Summary statistics**: Average times across all requests

Results are saved in `results/performance_metrics.json`

### Sample Output
```json
{
  "timestamp": "2025-10-27T...",
  "server_address": "localhost:50051",
  "metrics": [...],
  "summary": {
    "total_requests": 5,
    "avg_server_time": 0.0023,
    "avg_total_time": 0.0156,
    "avg_network_overhead": 0.0133
  }
}
```

## Project Files

- `run_server.ps1` / `run_server.bat` - Convenient server startup scripts
- `run_client.ps1` / `run_client.bat` - Convenient client startup scripts
- `generate_proto.py` - Generates gRPC code from .proto files
- `requirements.txt` - Python dependencies (gRPC, protobuf, numpy, pandas)

## Troubleshooting

### Port Already in Use
```powershell
# Find process using port 50051
netstat -ano | findstr :50051

# Kill process (use PID from above)
taskkill /PID <PID> /F
```

### gRPC Version Mismatch
```powershell
# Reinstall packages
pip install --upgrade grpcio grpcio-tools

# Regenerate proto files
python generate_proto.py
```

### Virtual Environment Issues
```powershell
# Recreate virtual environment
Remove-Item -Recurse -Force .venv
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python generate_proto.py
```

## References
- [gRPC Documentation](https://grpc.io)
- [Docker Documentation](https://docs.docker.com/)
- [Protocol Buffers](https://developers.google.com/protocol-buffers)
