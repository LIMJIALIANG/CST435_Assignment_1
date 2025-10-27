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
├── proto/                  # Protocol Buffer definitions
│   └── student_service.proto
├── server/                 # gRPC Server implementation
│   ├── server.py
│   ├── services/
│   │   ├── mapreduce_service.py
│   │   ├── mergesort_service.py
│   │   └── stats_service.py
│   └── generated/         # Generated gRPC code
├── client/                # gRPC Client implementation
│   ├── client.py
│   └── generated/         # Generated gRPC code
├── data/                  # Sample student data
│   └── students.csv
├── docker/                # Docker configurations
│   ├── Dockerfile.server
│   ├── Dockerfile.client
│   └── docker-compose.yml
├── results/               # Performance results
├── requirements.txt
└── README.md
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

### Method 1: Using Convenience Scripts (EASIEST) ⭐
```powershell
# Terminal 1: Start server
.\run_server.ps1    # or run_server.bat

# Terminal 2: Run client
.\run_client.ps1    # or run_client.bat
```

### Method 2: Activate Virtual Environment
```powershell
# Activate virtual environment (once per terminal session)
.\.venv\Scripts\Activate.ps1

# Terminal 1: Start server
python server/server.py

# Terminal 2: Run client
python client/client.py
```

### Method 3: Using Full Virtual Environment Path
```powershell
# Terminal 1: Start server
& ".\.venv\Scripts\python.exe" server/server.py

# Terminal 2: Run client
& ".\.venv\Scripts\python.exe" client/client.py
```

## Docker Deployment

### Running with Docker Compose (Same Machine, Different Containers)
```powershell
# Navigate to docker directory
cd docker

# Build and run with docker-compose
docker-compose up --build

# To stop
docker-compose down
```

### Running with Docker Swarm (Simulated Different Machines)
```powershell
# Initialize Docker Swarm
docker swarm init

# Deploy stack
cd docker
docker stack deploy -c docker-compose.yml student-analysis

# Check services
docker service ls

# View logs
docker service logs student-analysis_server
docker service logs student-analysis_client

# Remove stack
docker stack rm student-analysis

# Leave swarm
docker swarm leave --force
```

## Performance Testing

### Test Scenarios

#### Test 1: Same Machine (No Containers)
Run server and client directly on your machine using virtual environment:
```powershell
# Terminal 1
.\run_server.ps1

# Terminal 2
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

#### Test 3: Docker Swarm (Simulated Different Machines)
Deploy using Docker Swarm:
```powershell
docker swarm init
cd docker
docker stack deploy -c docker-compose.yml student-analysis
```
**Expected Results**: Additional network overhead, most realistic distributed scenario

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
