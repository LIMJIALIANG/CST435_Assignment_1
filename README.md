# CST435 Assignment 1 - Student Marks Analysis with RPC Protocols

## Problem Statement
This project implements a distributed student marks analysis system using **gRPC microservices architecture** and **XML-RPC** for protocol comparison. The system performs:
1. **MapReduce**: Count CGPA-based grade classifications and grade distributions
2. **Merge Sort**: Rank students by CGPA and grades
3. **Statistical Analysis**: Calculate average CGPA per faculty, grade distribution, and pass rates
4. **Protocol Comparison**: Performance analysis between gRPC (binary) and XML-RPC (text-based)

### Grading Scale
Based on official university grading system (descending order):
| Grade | Marks Range | CGPA Point | Classification |
|-------|-------------|------------|----------------|
| A     | 80-100     | 4.00       | Pass with distinction |
| B+    | 70-79      | 3.67       | Pass with credit |
| B     | 58-63      | 3.00       | Satisfactory pass |
| B-    | 65-69      | 2.67       | Satisfactory pass |
| C+    | 55-59      | 2.33       | Fail (for core courses) |
| C     | 50-54      | 2.00       | Pass (for elective courses) |
| C-    | 47-49      | 1.67       | |
| D+    | 44-46      | 1.33       | |
| D     | 40-43      | 1.00       | Fail |
| D-    | 30-39      | 0.67       | Fail |
| F     | 0-24       | 0.00       | Fail |

**Note**: MapReduce service uses CGPA thresholds to classify students into grade categories.

## Architecture

### gRPC Microservices Architecture (Service Chaining) ⭐
The gRPC implementation uses a **microservices architecture with service chaining**, where each service performs a specific task and forwards the request to the next service:

```
Client → MapReduce → MergeSort → Statistics → Client
         (CGPA +     (CGPA +      (Statistical
          Grade       Grade        Analysis)
          Classification) Sorting)
```

**Service Chain Details:**
- **MapReduce Service** (Port 50051): CGPA-based Grade Classification + Grade Distribution → forwards to MergeSort
- **MergeSort Service** (Port 50053): Sort by CGPA + Sort by Grade → forwards to Statistics
- **Statistics Service** (Port 50055): Statistical Analysis → returns aggregated results to client

**Key Features:**
- Each service is an independent server on a different port
- Services communicate via gRPC (Protocol Buffers)
- Data flows through the entire chain: Client calls MapReduce, which calls MergeSort, then Statistics
- **Result Aggregation**: Each service accumulates results and forwards them downstream
- **Complete Results**: Client receives results from all 3 services in a single response
- Simulates distributed containers across multiple servers
- Performance metrics captured for each service and end-to-end workflow

### XML-RPC Microservices Architecture (Service Chaining)
The XML-RPC implementation uses the **same chained microservices architecture** as gRPC for fair comparison:

```
Client → MapReduce → MergeSort → Statistics → Client
         (CGPA +     (CGPA +      (Statistical
          Grade       Grade        Analysis)
          Classification) Sorting)   Port 8005
         Port 8001)  Port 8003)
```

**Service Chain Details:**
- **MapReduce Service** (Port 8001): CGPA-based Grade Classification + Grade Distribution → forwards to MergeSort
- **MergeSort Service** (Port 8003): Sort by CGPA + Sort by Grade → forwards to Statistics
- **Statistics Service** (Port 8005): Statistical Analysis → returns aggregated results to client

**Key Features:**
- **Identical Architecture to gRPC**: Both use chained microservices pattern
- **Protocol**: XML-RPC over HTTP
- **Serialization**: XML (text-based, human-readable)
- **Transport**: HTTP/1.1
- **Port Range**: 8001, 8003, 8005
- **Use Case**: Protocol performance comparison with identical architecture

## Project Structure
```
.
📁 CST435_Assignment_1/
├── 🔧 grpc_implementation/      # gRPC Microservices Implementation
│   ├── proto/                   # Protocol Buffer definitions
│   │   └── student_service.proto
│   │
│   ├── server/                  # Microservices (MapReduce, MergeSort, Statistics)
│   │   ├── mapreduce_cgpa.py       # MapReduce service (Port 50051)
│   │   ├── mergesort_cgpa.py       # MergeSort service (Port 50053)
│   │   ├── statistics.py          # Statistics service (Port 50055)
│   │   ├── start_all_services.ps1/.bat    # Launch all services
│   │   └── generated/                     # Generated gRPC code
│   │
│   └── client/                  # Microservices Client
│       ├── client.py                      # Initiates workflow at MapReduce Service
│       ├── run_client.ps1/.bat            # Run client script
│       └── generated/                     # Generated gRPC code
│
├── 🔧 xmlrpc_implementation/    # XML-RPC Microservices Implementation
│   ├── server/                  # XML-RPC Microservices (MapReduce, MergeSort, Statistics)
│   │   ├── mapreduce.py         # MapReduce Service (Port 8001)
│   │   ├── mergesort.py         # MergeSort Service (Port 8003)
│   │   ├── statistics.py        # Statistics Service (Port 8005)
│   │   ├── start_all_services.ps1  # Launch all 3 services
│   │   └── start_all_services.bat
│   └── client/                  # XML-RPC Client
│       ├── client.py
│       ├── run_client.ps1       # Run client script
│       └── run_client.bat
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
│   ├── Dockerfile.grpc.mapreduce          # gRPC MapReduce service container
│   ├── Dockerfile.grpc.mergesort          # gRPC MergeSort service container
│   ├── Dockerfile.grpc.statistics         # gRPC Statistics service container
│   ├── Dockerfile.grpc.client   # gRPC client container
│   ├── docker-compose.grpc.yml  # gRPC Docker Compose
│   │
│   ├── Dockerfile.xmlrpc.mapreduce       # XML-RPC MapReduce service container
│   ├── Dockerfile.xmlrpc.mergesort       # XML-RPC MergeSort service container
│   ├── Dockerfile.xmlrpc.statistics      # XML-RPC Statistics service container
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
- **Microservices Architecture**: 3 independent services simulating distributed containers
- **Service Chaining with Result Aggregation**: Data and results flow sequentially MapReduce → MergeSort → Statistics
- **Complete Result Visibility**: Client receives aggregated results from all 3 services
- **MapReduce Operations**: Parallel processing of CGPA and grade counting
- **Merge Sort**: Distributed sorting for student rankings
- **Statistical Analysis**: Grade distribution, pass rates, average CGPA per faculty
- **Detailed Performance Metrics**: Individual service times, total processing time, network overhead
- **Two Deployment Methods**: Native Python, Docker Compose
- **Protocol Comparison**: Compare gRPC vs XML-RPC with identical microservices architecture

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

This method runs all 3 services locally on different ports, simulating distributed containers.

```powershell
# Terminal 1: Start all 3 microservices
cd grpc_implementation\server
.\start_all_services.ps1    # or start_all_services.bat

# This will open 3 terminal windows:
# - MapReduce Service: localhost:50051 (CGPA-based Grade Classification)
# - MergeSort Service: localhost:50053 (Sort by CGPA + Grade)
# - Statistics Service: localhost:50055 (Statistical Analysis)

# Terminal 2: Run the microservices client
cd grpc_implementation\client
.\run_client.ps1    # or run_client.bat

# Results saved to: results/grpc_performance_metrics.json
```

**What happens:**
1. Client calls MapReduce Service with the initial request
2. MapReduce Service processes CGPA-based Grade Classification + Grade Distribution → forwards accumulated results to MergeSort
3. MergeSort Service processes Sort by CGPA + Sort by Grade → forwards accumulated results to Statistics
4. Statistics Service performs Statistical Analysis → returns **complete aggregated results** from all services
5. Client displays results from all 3 services and measures performance metrics

**Results displayed:**
- MapReduce Service: Grade classification count (A, B+, B, B-, C+, C, C-, D+, D, D-, F) + Grade distribution
- MergeSort Service: Top students sorted by CGPA + Top students sorted by grade
- Statistics Service: Statistical analysis (pass rate, faculty averages)
- Performance: Individual service times + total workflow time + network overhead

---

### Method 2: Docker Compose (Containerized) 🐳

This method runs all 5 services in separate Docker containers with bridge networking.

```powershell
cd docker

# Build and run all microservices + client
docker-compose -f docker-compose.grpc.yml up --build

# Results saved to: results/grpc_docker_performance_metrics.json

# To stop and remove containers:
docker-compose -f docker-compose.grpc.yml down
```

**Container architecture:**
- 5 service containers (service-a, service-b, service-c, service-d, service-e)
- 1 client container
- Bridge network for inter-service communication
- Environment variables for service addresses

---

## Usage - XML-RPC Microservices

The XML-RPC implementation now uses the **same chained microservices architecture** as gRPC for fair protocol comparison.

### Method 1: Native Python (Convenience Scripts) ⭐ EASIEST

```powershell
# Terminal 1: Start all 5 XML-RPC microservices
cd xmlrpc_implementation\server
.\start_all_services.ps1

# This will open 5 terminal windows:
# - MapReduce Service: localhost:8001 (CGPA-based Grade Classification + Grade Distribution)
# - MergeSort Service: localhost:8003 (Sort CGPA + Sort Grade)
# - Statistics Service: localhost:8005 (Statistical Analysis)

# Terminal 2: Run XML-RPC client
cd xmlrpc_implementation\client
.\run_client.ps1

# Results saved to: results/xmlrpc_performance_metrics.json
```

**What happens:**
1. Client calls MapReduce Service (port 8001) with the initial request
2. MapReduce Service processes CGPA-based Grade Classification + Grade Distribution → forwards to MergeSort
3. MergeSort Service processes Sort by CGPA + Sort by Grade → forwards to Statistics
4. Statistics Service performs Statistical Analysis → returns **complete aggregated results**
5. Client displays results from all 3 services and measures performance

---

### Method 2: Docker Compose (Containerized) 🐳

This method runs all 5 XML-RPC services in separate Docker containers with bridge networking.

```powershell
cd docker

# Build and run all XML-RPC microservices + client
docker-compose -f docker-compose.xmlrpc.yml up --build

# Results saved to: results/xmlrpc_docker_performance_metrics.json

# To stop and remove containers:
docker-compose -f docker-compose.xmlrpc.yml down
```

**Container architecture:**
- 3 service containers (xmlrpc-mapreduce, xmlrpc-mergesort, xmlrpc-statistics)
- 1 client container
- Bridge network for inter-service communication
- Services start in reverse order (Statistics→MergeSort→MapReduce) to ensure downstream services are ready
- Environment variables for service addresses (e.g., SERVICE_C_URL=http://xmlrpc-mergesort:8003)

---

### Method 3: Manual Execution

```powershell
# Activate virtual environment
.\.venv\Scripts\Activate.ps1

# Terminal 1: Start Statistics service (terminal service first)
cd xmlrpc_implementation\server
python statistics.py

# Terminal 2: Start MergeSort service
python mergesort.py

# Terminal 3: Start MapReduce service (entry point)
python mapreduce.py

# Terminal 4: Run client
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
- Serialization format (Binary Protocol Buffers vs XML)
- Network overhead
- Latency per operation
- End-to-end workflow time
- **Fair Architecture**: Both use identical chained microservices (MapReduce → MergeSort → Statistics)
- **Protocol Performance**: Pure comparison of gRPC vs XML-RPC protocols

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

**XML-RPC Microservices:**
```powershell
# Terminal 1: Start all 5 services
cd xmlrpc_implementation\server
.\start_all_services.ps1

# Terminal 2: Run client
cd xmlrpc_implementation\client
.\run_client.ps1
```
Results: `results/xmlrpc_performance_metrics.json`

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
docker-compose -f docker-compose.grpc.yml up --build
```
Results: `results/grpc_docker_performance_metrics.json`

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
  "workflow": "Client → MapReduce → MergeSort → Statistics → Client",
  "workflow_time": 0.1284,
  "mapreduce_time": 0.0112,
  "mergesort_time": 0.0004,
  "statistics_time": 0.0002,
  "total_processing_time": 0.0118,
  "network_overhead": 0.1166
}
```

**XML-RPC Microservices Metrics:**
```json
{
  "timestamp": "2025-10-30T...",
  "protocol": "XML-RPC",
  "architecture": "microservices_chained",
  "mapreduce_url": "http://localhost:8001",
  "workflow_time": 0.1234,
  "mapreduce_time": 0.0357,
  "mergesort_time": 0.0801,
  "statistics_time": 0.0567,
  "total_processing_time": 0.1725,
  "network_overhead": 0.0109,
  "summary": {
    "total_services": 3,
    "avg_service_time": 0.0575,
    "overhead_percentage": 8.83
  }
}
```

**Comparison Summary:**
- Both use **identical chained microservices architecture** (MapReduce → MergeSort → Statistics)
- gRPC uses binary Protocol Buffers serialization
- XML-RPC uses text-based XML serialization
- **Fair protocol comparison** with same architecture and operations
- Each service's contribution to total time is visible
- Network overhead in microservices includes inter-service communication
- XML-RPC monolithic has simpler metrics but less visibility into operations
- Binary serialization (gRPC) vs text (XML-RPC) affects message sizes

## Project Files

### gRPC Microservices Implementation
- `grpc_implementation/proto/student_service.proto` - Protocol Buffer definitions with CombinedResponse
- `grpc_implementation/server/mapreduce_cgpa.py` - MapReduce Service (CGPA + Grade Classification)
- `grpc_implementation/server/mergesort_cgpa.py` - MergeSort Service (Sort CGPA + Grade)
- `grpc_implementation/server/statistics.py` - Statistics Service (Statistical Analysis)
- `grpc_implementation/client/client.py` - Microservices client
- `generate_proto.py` - Generates gRPC code from .proto files

### XML-RPC Implementation
- `xmlrpc_implementation/server/mapreduce.py` - MapReduce Service (Port 8001)
- `xmlrpc_implementation/server/mergesort.py` - MergeSort Service (Port 8003)
- `xmlrpc_implementation/server/statistics.py` - Statistics Service (Port 8005)
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

#### Ports Already in Use (8001-8005)
```powershell
# Find processes using XML-RPC ports
netstat -ano | findstr ":8001 :8002 :8003 :8004 :8005"

# Kill specific process (use PID from above)
taskkill /PID <PID> /F

# Or kill all Python processes
taskkill /F /IM python.exe
```

#### Services Not Starting in Chain
```powershell
# Start services in reverse order (E first, then D, C, B, A)
# This ensures downstream services are ready when upstream tries to connect

# Check if all 5 services are listening:
netstat -ano | findstr ":8001 :8002 :8003 :8004 :8005"
# All should show LISTENING status
```

#### Connection Refused
```powershell
# Ensure all 5 services are running before starting client
# Use start_all_services.ps1 to launch them properly
# Wait 2 seconds between each service start
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

---

## Quick Reference - Docker Commands

### gRPC Microservices (Docker)
```powershell
# Build and run
cd docker
docker-compose -f docker-compose.grpc.yml up --build

# Stop and remove
docker-compose -f docker-compose.grpc.yml down

# View logs
docker-compose -f docker-compose.grpc.yml logs -f

# Rebuild specific service
docker-compose -f docker-compose.grpc.yml build service-a
```

### XML-RPC Microservices (Docker)
```powershell
# Build and run
cd docker
docker-compose -f docker-compose.xmlrpc.yml up --build

# Stop and remove
docker-compose -f docker-compose.xmlrpc.yml down

# View logs (specific service)
docker logs xmlrpc-service-a -f

# View logs (all services)
docker-compose -f docker-compose.xmlrpc.yml logs -f

# Restart specific service
docker restart xmlrpc-service-a
```

### Docker Troubleshooting
```powershell
# Check running containers
docker ps

# Check all containers (including stopped)
docker ps -a

# Remove all stopped containers
docker container prune -f

# Remove all unused images
docker image prune -a -f

# View resource usage
docker stats

# Clean everything (containers, networks, images, volumes)
docker system prune -a --volumes -f
```

---

## References
- [gRPC Documentation](https://grpc.io)
- [Docker Documentation](https://docs.docker.com/)
- [Protocol Buffers](https://developers.google.com/protocol-buffers)

