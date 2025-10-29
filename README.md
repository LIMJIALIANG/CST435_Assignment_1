# CST435 Assignment 1 - Student Marks Analysis with RPC Protocols

## Problem Statement
This project implements a distributed student marks analysis system using **gRPC and XML-RPC** protocols for comparison. The system performs:
1. **MapReduce**: Count CGPA ranges and grade distributions
2. **Merge Sort**: Rank students by grades
3. **Statistical Analysis**: Calculate average CGPA per faculty, grade distribution, and pass rates
4. **Protocol Comparison**: Performance analysis between gRPC (binary) and XML-RPC (text-based)

## Architecture
The system uses a client-server architecture with **two protocol implementations**:

### gRPC Implementation (Binary Protocol)
- **Protocol**: gRPC with Protocol Buffers
- **Serialization**: Binary (compact, fast)
- **Transport**: HTTP/2
- **Port**: 50051
- **Use Case**: High-performance, production systems

### XML-RPC Implementation (Text Protocol)
- **Protocol**: XML-RPC
- **Serialization**: XML (human-readable, verbose)
- **Transport**: HTTP/1.1
- **Port**: 8000
- **Use Case**: Legacy systems, simple integrations

Both implementations use the **same shared business logic** (services folder) to ensure fair comparison.

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
├── 🔧 xmlrpc_implementation/    # XML-RPC Protocol Implementation
│   ├── server/                  # XML-RPC Server
│   │   └── server.py
│   ├── client/                  # XML-RPC Client
│   │   └── client.py
│   ├── run_server.ps1/.bat     # Convenience scripts
│   └── run_client.ps1/.bat
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
│   ├── Dockerfile.grpc.server         # gRPC server container
│   ├── Dockerfile.grpc.client         # gRPC client container
│   ├── docker-compose.grpc.yml        # gRPC Docker Compose
│   ├── docker-compose.grpc.swarm.yml  # gRPC Docker Swarm
│   ├── Dockerfile.xmlrpc.server       # XML-RPC server container
│   ├── Dockerfile.xmlrpc.client       # XML-RPC client container
│   ├── docker-compose.xmlrpc.yml      # XML-RPC Docker Compose
│   └── docker-compose.xmlrpc.swarm.yml # XML-RPC Docker Swarm
│
├── 🔧 tools/                    # Analysis and comparison tools
│   └── compare_protocols.py     # Compare gRPC vs XML-RPC performance
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

### Option 2: XML-RPC Implementation 🆕

#### Method 1: Using Convenience Scripts (EASIEST)
```powershell
# Terminal 1: Start XML-RPC server
cd xmlrpc_implementation
.\run_server.ps1    # or run_server.bat

# Terminal 2: Run XML-RPC client
cd xmlrpc_implementation
.\run_client.ps1    # or run_client.bat
```

#### Method 2: Manual Execution
```powershell
# Activate virtual environment
.\.venv\Scripts\Activate.ps1

# Terminal 1: Start XML-RPC server
cd xmlrpc_implementation\server
python server.py

# Terminal 2: Run XML-RPC client
cd xmlrpc_implementation\client
python client.py
```

### Option 3: Protocol Comparison 📊
After running both gRPC and XML-RPC clients, compare their performance:
```powershell
# Activate virtual environment
.\.venv\Scripts\Activate.ps1

# Run comparison tool
python tools\compare_protocols.py
```

This will generate:
- **Console output**: Detailed comparison tables
- **Charts**: Visual performance comparisons (PNG files)
- **Reports**: Text reports with analysis and recommendations

## Docker Deployment

Both gRPC and XML-RPC support Docker deployment with identical configurations.

### Method 1: Docker Compose - Local Containers

#### gRPC Deployment
```powershell
cd docker
docker-compose -f docker-compose.grpc.yml up --build
# Results saved to: results/grpc_docker_performance_metrics.json
```

#### XML-RPC Deployment
```powershell
cd docker
docker-compose -f docker-compose.xmlrpc.yml up --build
# Results saved to: results/xmlrpc_docker_performance_metrics.json
```

**Note**: Windows Docker Desktop may have DNS issues with bridge networks. Use Swarm for distributed testing.

---

### Method 2: Docker Swarm - Distributed Orchestration ⭐ (Recommended)

**What it does**: Simulates containers running on **different machines** using overlay networking.

#### gRPC Swarm Deployment
```powershell
# Initialize Swarm (one-time)
docker swarm init

# Build and deploy gRPC
cd docker
docker-compose -f docker-compose.grpc.yml build
docker stack deploy -c docker-compose.grpc.swarm.yml student-analysis

# View logs
docker service logs student-analysis_server --tail 50
docker service logs student-analysis_client --tail 50

# Results saved to: results/grpc_swarm_performance_metrics.json

# Cleanup
docker stack rm student-analysis
```

#### XML-RPC Swarm Deployment
```powershell
# Build and deploy XML-RPC
cd docker
docker-compose -f docker-compose.xmlrpc.yml build
docker stack deploy -c docker-compose.xmlrpc.swarm.yml xmlrpc-analysis

# View logs
docker service logs xmlrpc-analysis_xmlrpc-server --tail 50
docker service logs xmlrpc-analysis_xmlrpc-client --tail 50

# Results saved to: results/xmlrpc_swarm_performance_metrics.json

# Cleanup
docker stack rm xmlrpc-analysis
```

#### Compare Both Protocols in Swarm
```powershell
# After running both deployments, compare results
python tools\compare_protocols.py
```


## Performance Testing & Comparison

### Test Scenarios

#### Test 1: Native Python (Same Machine) - Baseline
Run each protocol natively for baseline performance:

**gRPC:**
```powershell
# Terminal 1: gRPC Server
cd grpc_implementation\server
.\run_server.ps1

# Terminal 2: gRPC Client
cd grpc_implementation\client
.\run_client.ps1
```
Results: `results/grpc_performance_metrics.json`

**XML-RPC:**
```powershell
# Terminal 1: XML-RPC Server
cd xmlrpc_implementation
.\run_server.ps1

# Terminal 2: XML-RPC Client
cd xmlrpc_implementation
.\run_client.ps1
```
Results: `results/xmlrpc_performance_metrics.json`

**Expected**: Lowest latency, baseline for each protocol

---

#### Test 2: Docker Compose (Containerized, Same Machine)
Run both protocols in Docker containers:

**gRPC:**
```powershell
cd docker
docker-compose -f docker-compose.grpc.yml up --build
```
Results: `results/grpc_docker_performance_metrics.json`

**XML-RPC:**
```powershell
cd docker
docker-compose -f docker-compose.xmlrpc.yml up --build
```
Results: `results/xmlrpc_docker_performance_metrics.json`

**Expected**: Containerization overhead added

---

#### Test 3: Docker Swarm (Distributed Simulation) ⭐ Recommended
Simulate distributed systems with overlay networking:

**gRPC:**
```powershell
docker swarm init
cd docker
docker-compose -f docker-compose.grpc.yml build
docker stack deploy -c docker-compose.grpc.swarm.yml student-analysis
```
Results: `results/grpc_swarm_performance_metrics.json`

**XML-RPC:**
```powershell
cd docker
docker-compose -f docker-compose.xmlrpc.yml build
docker stack deploy -c docker-compose.xmlrpc.swarm.yml xmlrpc-analysis
```
Results: `results/xmlrpc_swarm_performance_metrics.json`

**Expected**: Realistic network overhead from overlay networking

---

### Performance Comparison

After running tests for both protocols, analyze results:

```powershell
# Activate virtual environment
.\.venv\Scripts\Activate.ps1

# Run comparison tool
python tools\compare_protocols.py
```

**Generates:**
1. **Console Output**: Detailed comparison tables
2. **Charts**: 
   - `native_comparison.png` - Native execution comparison
   - `docker_comparison.png` - Docker comparison
   - `swarm_comparison.png` - Swarm comparison
3. **Reports**:
   - `native_comparison_report.txt`
   - `docker_comparison_report.txt`
   - `swarm_comparison_report.txt`

### Key Performance Metrics

Each test measures:
- **Server Processing Time**: Pure computation time
- **Total Request Time**: End-to-end including network
- **Network Overhead**: Serialization + transmission time
- **Protocol Efficiency**: gRPC (binary) vs XML-RPC (text)

### Expected Performance Characteristics

| Aspect | gRPC | XML-RPC |
|--------|------|---------|
| **Serialization** | Binary (Protocol Buffers) | Text (XML) |
| **Message Size** | Smaller | Larger |
| **Speed** | Faster | Slower |
| **Readability** | Not human-readable | Human-readable |
| **Overhead** | Lower | Higher |
| **Best For** | Production, microservices | Legacy, debugging |

### Performance Metrics
The client automatically measures and records:
- **Server processing time**: Time taken by server to process the request
- **Total request time**: End-to-end time including network latency
- **Network overhead**: Difference between total time and server processing time
- **Summary statistics**: Average times across all requests

Results are saved in `results/performance_metrics.json`

### Sample Performance Results

**gRPC Metrics:**
```json
{
  "timestamp": "2025-10-30T...",
  "protocol": "gRPC",
  "server_address": "localhost:50051",
  "summary": {
    "total_requests": 5,
    "avg_server_time": 0.0021,
    "avg_total_time": 0.0067,
    "avg_network_overhead": 0.0046
  }
}
```

**XML-RPC Metrics:**
```json
{
  "timestamp": "2025-10-30T...",
  "protocol": "XML-RPC",
  "server_address": "http://localhost:8000",
  "summary": {
    "total_requests": 5,
    "avg_server_time": 0.0023,
    "avg_total_time": 0.0089,
    "avg_network_overhead": 0.0066
  }
}
```

**Comparison Summary:**
- gRPC is typically **20-40% faster** than XML-RPC
- Binary serialization reduces message size significantly
- Network overhead is lower with Protocol Buffers
- XML-RPC is more verbose but easier to debug

## Project Files

### gRPC Implementation
- `grpc_implementation/proto/student_service.proto` - Protocol Buffer definitions
- `grpc_implementation/server/server.py` - gRPC server
- `grpc_implementation/client/client.py` - gRPC client
- `generate_proto.py` - Generates gRPC code from .proto files

### XML-RPC Implementation
- `xmlrpc_implementation/server/server.py` - XML-RPC server
- `xmlrpc_implementation/client/client.py` - XML-RPC client

### Shared Components
- `services/mapreduce_service.py` - MapReduce logic (protocol-independent)
- `services/mergesort_service.py` - MergeSort logic (protocol-independent)
- `services/stats_service.py` - Statistics logic (protocol-independent)

### Tools & Scripts
- `tools/compare_protocols.py` - Performance comparison analyzer
- `run_server.ps1/.bat` - Convenience server startup scripts
- `run_client.ps1/.bat` - Convenience client startup scripts
- `requirements.txt` - Python dependencies

## Troubleshooting

### gRPC Issues

#### Port Already in Use (50051)
```powershell
# Find process using port 50051
netstat -ano | findstr :50051

# Kill process (use PID from above)
taskkill /PID <PID> /F
```

#### gRPC Version Mismatch
```powershell
# Reinstall packages
pip install --upgrade grpcio grpcio-tools

# Regenerate proto files
python generate_proto.py
```

### XML-RPC Issues

#### Port Already in Use (8000)
```powershell
# Find process using port 8000
netstat -ano | findstr :8000

# Kill process (use PID from above)
taskkill /PID <PID> /F
```

#### Connection Refused
```powershell
# Ensure server is running first
# Check firewall settings
# Verify server address (localhost or 0.0.0.0)
```

### General Issues

#### Virtual Environment Issues
```powershell
# Recreate virtual environment
Remove-Item -Recurse -Force .venv
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python generate_proto.py  # For gRPC only
```

#### Docker Issues
```powershell
# Remove all containers and networks
docker-compose down -v
docker system prune -f

# For Swarm issues
docker stack rm student-analysis xmlrpc-analysis
docker swarm leave --force
```

## Protocol Comparison Summary

### When to Use gRPC
✅ **Advantages:**
- High performance (20-40% faster than XML-RPC)
- Binary protocol (smaller messages)
- Built-in streaming support
- Modern, actively maintained
- Type-safe with Protocol Buffers
- Better for microservices

❌ **Disadvantages:**
- Steeper learning curve
- Not human-readable (debugging harder)
- Requires code generation
- More complex setup

**Best for:** Production systems, microservices, real-time applications

---

### When to Use XML-RPC
✅ **Advantages:**
- Simple to implement
- Human-readable XML format
- Easy debugging
- Wide language support
- No code generation needed
- Good for legacy systems

❌ **Disadvantages:**
- Slower performance
- Larger message sizes
- Higher network overhead
- No streaming support
- Older technology

**Best for:** Legacy integration, simple RPC, debugging, educational purposes

---

### Performance Comparison

| Metric | gRPC | XML-RPC | Winner |
|--------|------|---------|--------|
| Speed | ⚡ Fast | 🐢 Slower | gRPC (20-40% faster) |
| Message Size | 📦 Small | 📦📦 Large | gRPC |
| Network Overhead | ⬇️ Low | ⬆️ Higher | gRPC |
| Readability | ❌ Binary | ✅ Text | XML-RPC |
| Debugging | 🔧 Hard | 🔧 Easy | XML-RPC |
| Setup Complexity | 😰 Complex | 😊 Simple | XML-RPC |
| Streaming | ✅ Yes | ❌ No | gRPC |
| Type Safety | ✅ Strong | ❌ Weak | gRPC |

---

### For This Assignment

Run **both protocols** in all three deployment scenarios:
1. **Native** (baseline)
2. **Docker Compose** (containerization overhead)
3. **Docker Swarm** (distributed system simulation)

Then use the comparison tool to generate:
- Performance charts
- Detailed reports
- Analysis for your assignment report

This provides comprehensive data showing:
- Protocol differences (gRPC vs XML-RPC)
- Deployment overhead (native vs containers)
- Network impact (single-host vs overlay networking)

## References
- [gRPC Documentation](https://grpc.io)
- [Docker Documentation](https://docs.docker.com/)
- [Protocol Buffers](https://developers.google.com/protocol-buffers)
