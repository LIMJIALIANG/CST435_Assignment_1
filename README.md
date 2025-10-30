# CST435 Assignment 1 - Student Marks Analysis with RPC Protocols

## Problem Statement
This project implements a distributed student marks analysis system using **gRPC microservices architecture** and **XML-RPC** for protocol comparison. The system performs:
1. **MapReduce**: Count CGPA ranges and grade distributions
2. **Merge Sort**: Rank students by grades
3. **Statistical Analysis**: Calculate average CGPA per faculty, grade distribution, and pass rates
4. **Protocol Comparison**: Performance analysis between gRPC (binary) and XML-RPC (text-based)

## Architecture

### gRPC Microservices Architecture (Service Chaining) ⭐
The gRPC implementation uses a **microservices architecture with service chaining**, where each service performs a specific task and forwards the request to the next service:

```
Client → Service A → Service B → Service C → Service D → Service E → Client
         (MapReduce  (MapReduce  (MergeSort  (MergeSort  (Statistics)
          CGPA)       Grade)      CGPA)       Grade)
```

**Service Chain Details:**
- **Service A** (Port 50051): MapReduce CGPA counting → forwards to Service B
- **Service B** (Port 50052): MapReduce Grade distribution → forwards to Service C
- **Service C** (Port 50053): MergeSort by CGPA → forwards to Service D
- **Service D** (Port 50054): MergeSort by Grade → forwards to Service E
- **Service E** (Port 50055): Statistical Analysis → returns aggregated results to client

**Key Features:**
- Each service is an independent server on a different port
- Services communicate via gRPC (Protocol Buffers)
- Data flows through the entire chain: Client calls Service A, which calls Service B, and so on
- **Result Aggregation**: Each service accumulates results and forwards them downstream
- **Complete Results**: Client receives results from all 5 services in a single response
- Simulates distributed containers across multiple servers
- Performance metrics captured for each service and end-to-end workflow

### XML-RPC Implementation (Text Protocol)
- **Protocol**: XML-RPC
- **Serialization**: XML (human-readable, verbose)
- **Transport**: HTTP/1.1
- **Port**: 8000
- **Use Case**: Legacy systems, simple integrations, protocol comparison

## Project Structure
```
.
📁 CST435_Assignment_1/
├── 🔧 grpc_implementation/      # gRPC Microservices Implementation
│   ├── proto/                   # Protocol Buffer definitions
│   │   └── student_service.proto
│   │
│   ├── server/                  # Microservices (A, B, C, D, E)
│   │   ├── service_a_mapreduce_cgpa.py    # Service A (Port 50051)
│   │   ├── service_b_mapreduce_grade.py   # Service B (Port 50052)
│   │   ├── service_c_mergesort_cgpa.py    # Service C (Port 50053)
│   │   ├── service_d_mergesort_grade.py   # Service D (Port 50054)
│   │   ├── service_e_statistics.py        # Service E (Port 50055)
│   │   ├── start_all_services.ps1/.bat    # Launch all services
│   │   └── generated/                     # Generated gRPC code
│   │
│   └── client/                  # Microservices Client
│       ├── microservices_client.py        # Initiates workflow at Service A
│       ├── run_client.ps1/.bat            # Run client script
│       └── generated/                     # Generated gRPC code
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
│   ├── Dockerfile.service_a              # Service A container
│   ├── Dockerfile.service_b              # Service B container
│   ├── Dockerfile.service_c              # Service C container
│   ├── Dockerfile.service_d              # Service D container
│   ├── Dockerfile.service_e              # Service E container
│   ├── Dockerfile.microservices_client   # Microservices client
│   ├── docker-compose.microservices.yml  # Docker Compose config
│   │
│   ├── Dockerfile.xmlrpc.server          # XML-RPC server container
│   ├── Dockerfile.xmlrpc.client          # XML-RPC client container
│   └── docker-compose.xmlrpc.yml         # XML-RPC Docker Compose
│
├── 🔧 tools/                    # Analysis and comparison tools
│   └── compare_protocols.py     # Compare gRPC vs XML-RPC performance
│
├── 📈 results/                  # Performance results
├── 📄 requirements.txt
└── 📖 README.md
```


## Features
- **Microservices Architecture**: 5 independent services simulating distributed containers
- **Service Chaining with Result Aggregation**: Data and results flow sequentially A → B → C → D → E
- **Complete Result Visibility**: Client receives aggregated results from all 5 services
- **MapReduce Operations**: Parallel processing of CGPA and grade counting
- **Merge Sort**: Distributed sorting for student rankings
- **Statistical Analysis**: Grade distribution, pass rates, average CGPA per faculty
- **Detailed Performance Metrics**: Individual service times, total processing time, network overhead
- **Two Deployment Methods**: Native Python, Docker Compose
- **Protocol Comparison**: Compare gRPC microservices vs XML-RPC monolithic

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

## Usage - gRPC Microservices

The gRPC implementation offers **two deployment methods** to test different scenarios:

### Method 1: Native Python (Convenience Scripts) ⭐ EASIEST

This method runs all 5 services locally on different ports, simulating distributed containers.

```powershell
# Terminal 1: Start all 5 microservices
cd grpc_implementation\server
.\start_all_services.ps1    # or start_all_services.bat

# This will open 5 terminal windows:
# - Service A: localhost:50051 (MapReduce CGPA)
# - Service B: localhost:50052 (MapReduce Grade)
# - Service C: localhost:50053 (MergeSort CGPA)
# - Service D: localhost:50054 (MergeSort Grade)
# - Service E: localhost:50055 (Statistics)

# Terminal 2: Run the microservices client
cd grpc_implementation\client
.\run_client.ps1    # or run_client.bat

# Results saved to: results/grpc_performance_metrics.json
```

**What happens:**
1. Client calls Service A with the initial request
2. Service A processes MapReduce CGPA → forwards accumulated results to Service B
3. Service B processes MapReduce Grade → forwards accumulated results to Service C
4. Service C processes MergeSort CGPA → forwards accumulated results to Service D
5. Service D processes MergeSort Grade → forwards accumulated results to Service E
6. Service E processes Statistics → returns **complete aggregated results** from all services
7. Client displays results from all 5 services and measures performance metrics

**Results displayed:**
- Service A: CGPA count by ranges
- Service B: Grade distribution
- Service C: Top students sorted by CGPA
- Service D: Top students sorted by grade
- Service E: Statistical analysis (pass rate, faculty averages)
- Performance: Individual service times + total workflow time + network overhead

---

### Method 2: Docker Compose (Containerized) 🐳

This method runs all 5 services in separate Docker containers with bridge networking.

```powershell
cd docker

# Build and run all microservices + client
docker-compose -f docker-compose.microservices.yml up --build

# Results saved to: results/microservices_docker_performance_metrics.json

# To stop and remove containers:
docker-compose -f docker-compose.microservices.yml down
```

**Container architecture:**
- 5 service containers (service-a, service-b, service-c, service-d, service-e)
- 1 client container
- Bridge network for inter-service communication
- Environment variables for service addresses

---

## Usage - XML-RPC Implementation

The XML-RPC implementation maintains a monolithic server-client architecture for comparison.

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

---

## Protocol Comparison 📊

After running both gRPC microservices and XML-RPC implementations, compare their performance:

```powershell
# Activate virtual environment
.\.venv\Scripts\Activate.ps1

# Run comparison tool
python tools\compare_protocols.py
```

**Generates:**
- **Console output**: Detailed comparison tables
- **Charts**: Visual performance comparisons (PNG files)
- **Reports**: Analysis of latency, throughput, and overhead

**Comparison aspects:**
- Serialization format (Binary vs XML)
- Network overhead
- Latency per operation
- End-to-end workflow time
- Architecture complexity (Microservices with chaining vs Monolithic)
- Result aggregation in microservices vs single response in monolithic

---

## Performance Testing Scenarios

### Test 1: Native Python (Same Machine) - Baseline

**gRPC Microservices:**
```powershell
# Terminal 1: Start all services
cd grpc_implementation\server
.\start_all_services.ps1

# Terminal 2: Run client
cd grpc_implementation\client
.\run_client.ps1
```
Results: `results/grpc_performance_metrics.json`

**XML-RPC:**
```powershell
# Terminal 1: Start server
cd xmlrpc_implementation
.\run_server.ps1

# Terminal 2: Run client
cd xmlrpc_implementation
.\run_client.ps1
```
Results: `results/xmlrpc_performance_metrics.json`

**Expected**: Lowest latency baseline for each protocol

---

### Test 2: Docker Compose (Containerized, Same Machine)

**gRPC Microservices:**
```powershell
cd docker
docker-compose -f docker-compose.microservices.yml up --build
```
Results: `results/microservices_docker_performance_metrics.json`

**XML-RPC:**
```powershell
cd docker
docker-compose -f docker-compose.xmlrpc.yml up --build
```
Results: `results/xmlrpc_docker_performance_metrics.json`

**Expected**: Added containerization overhead

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
3. **Reports**:
   - `native_comparison_report.txt`
   - `docker_comparison_report.txt`

### Key Performance Metrics

**gRPC Microservices measures:**
- **Individual Service Times**: Processing time for each service (A, B, C, D, E)
- **Total Processing Time**: Sum of all service processing times
- **End-to-End Time**: Complete workflow time including network calls
- **Network Overhead**: Inter-service communication overhead
- **Result Aggregation**: Time to combine results from all services

**XML-RPC Monolithic measures:**
- **Server Processing Time**: Pure computation time
- **Total Request Time**: End-to-end including network
- **Network Overhead**: Serialization + transmission time
- **Protocol Efficiency**: Binary vs text-based serialization

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

**gRPC Microservices Metrics:**
```json
{
  "timestamp": "2025-10-30T...",
  "architecture": "microservices_chained",
  "workflow": "Client → A → B → C → D → E → Client",
  "workflow_time": 0.1284,
  "service_a_time": 0.0065,
  "service_b_time": 0.0047,
  "service_c_time": 0.0002,
  "service_d_time": 0.0002,
  "service_e_time": 0.0002,
  "total_processing_time": 0.0118,
  "network_overhead": 0.1166
}
```

**XML-RPC Monolithic Metrics:**
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
- gRPC microservices show **distributed processing** across 5 services
- Each service's contribution to total time is visible
- Network overhead in microservices includes inter-service communication
- XML-RPC monolithic has simpler metrics but less visibility into operations
- Binary serialization (gRPC) vs text (XML-RPC) affects message sizes

## Project Files

### gRPC Microservices Implementation
- `grpc_implementation/proto/student_service.proto` - Protocol Buffer definitions with CombinedResponse
- `grpc_implementation/server/service_a_mapreduce_cgpa.py` - Service A (MapReduce CGPA)
- `grpc_implementation/server/service_b_mapreduce_grade.py` - Service B (MapReduce Grade)
- `grpc_implementation/server/service_c_mergesort_cgpa.py` - Service C (MergeSort CGPA)
- `grpc_implementation/server/service_d_mergesort_grade.py` - Service D (MergeSort Grade)
- `grpc_implementation/server/service_e_statistics.py` - Service E (Statistics)
- `grpc_implementation/client/microservices_client.py` - Microservices client
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

#### Port Already in Use (50051-50055)
If services fail to start with "Failed to bind to address" error, ports are already in use.

**Quick Fix - Kill All Service Ports:**
```powershell
# Find all processes using service ports
netstat -ano | findstr "5005"

# Kill all service processes at once (replace PIDs with actual values)
taskkill /PID <PID1> /F; taskkill /PID <PID2> /F; taskkill /PID <PID3> /F; taskkill /PID <PID4> /F; taskkill /PID <PID5> /F
```

**Alternative - Kill All Python Processes:**
```powershell
# WARNING: This kills ALL Python processes
Get-Process python | Stop-Process -Force
```

**Step-by-Step Method:**
```powershell
# 1. Find process using a specific port (e.g., 50051)
netstat -ano | findstr :50051

# 2. Kill the specific process (use PID from above)
taskkill /PID <PID> /F

# 3. Verify port is free
netstat -ano | findstr :50051
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

**Docker Daemon Not Running:**
```powershell
# Error: "error during connect: this error may indicate that the docker daemon is not running"

# Solution: Start Docker Desktop
# 1. Press Windows Key
# 2. Search for "Docker Desktop"
# 3. Launch Docker Desktop
# 4. Wait for green indicator in system tray (30-60 seconds)
# 5. Verify Docker is running:
docker info
```

**Clean Up Containers and Networks:**
```powershell
# Remove all containers and networks
docker-compose down -v
docker system prune -f
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

Run **both protocols** in both deployment scenarios:
1. **Native** (baseline)
2. **Docker Compose** (containerization overhead)

Then use the comparison tool to generate:
- Performance charts
- Detailed reports
- Analysis for your assignment report

This provides comprehensive data showing:
- Protocol differences (gRPC vs XML-RPC)
- Deployment overhead (native vs containers)

## References
- [gRPC Documentation](https://grpc.io)
- [Docker Documentation](https://docs.docker.com/)
- [Protocol Buffers](https://developers.google.com/protocol-buffers)
