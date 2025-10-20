# Detailed Step-by-Step Guide
## CST435 Assignment 1 - MapReduce Performance Comparison

---

## 📋 Table of Contents
1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Project Structure](#project-structure)
4. [Installation Steps](#installation-steps)
5. [Running Individual Tests](#running-individual-tests)
6. [Performance Comparison](#performance-comparison)
7. [Understanding the Results](#understanding-the-results)
8. [Troubleshooting](#troubleshooting)

---

## 🎯 Overview

This project compares **4 different distributed computing approaches**:

| Implementation | Technology | Containers | Purpose |
|---------------|------------|------------|---------|
| **gRPC** | Modern RPC framework | 3 servers | High-performance RPC |
| **XML-RPC** | Traditional RPC | 3 servers | Simple RPC baseline |
| **Request-Reply** | ZeroMQ messaging | 3 servers | Message-based communication |
| **MPI** | Message Passing | 1 (3 processes) | HPC standard |

All implementations solve the same problem: **MapReduce Word Count**

---

## ✅ Prerequisites

### Required Software:
1. **Docker Desktop** (Windows/Mac) or Docker Engine (Linux)
   - Download: https://www.docker.com/products/docker-desktop
   - Verify: `docker --version` and `docker-compose --version`

2. **Python 3.9+**
   - Download: https://www.python.org/downloads/
   - Verify: `python --version`

3. **Git** (optional, for version control)
   - Download: https://git-scm.com/downloads

### System Requirements:
- **RAM**: 4GB minimum (8GB recommended)
- **Disk Space**: 2GB free space
- **OS**: Windows 10/11, macOS 10.14+, or Linux

---

## 📁 Project Structure

```
example_map_reduce_program/
├── grpc_implementation/          # gRPC MapReduce
│   ├── proto/
│   │   └── mapreduce.proto       # Protocol Buffer definition
│   ├── server.py                 # gRPC server
│   ├── client.py                 # gRPC client
│   ├── mapreduce_pb2.py          # Generated (auto-created)
│   └── mapreduce_pb2_grpc.py     # Generated (auto-created)
│
├── xmlrpc_implementation/         # XML-RPC MapReduce
│   ├── server.py                 # XML-RPC server
│   └── client.py                 # XML-RPC client
│
├── reqrep_implementation/         # Request-Reply (ZeroMQ) MapReduce
│   ├── server.py                 # Request-Reply server
│   └── client.py                 # Request-Reply client
│
├── mpi_implementation/            # MPI MapReduce
│   └── mapreduce.py              # MPI implementation
│
├── docker/                        # Docker configuration
│   ├── Dockerfile.grpc           # gRPC Docker image
│   ├── Dockerfile.xmlrpc         # XML-RPC Docker image
│   ├── Dockerfile.reqrep         # Request-Reply Docker image
│   ├── Dockerfile.mpi            # MPI Docker image
│   └── docker-compose.yml        # Multi-container orchestration
│
├── data/
│   └── sample_text.txt           # Sample data for word count
│
├── performance_results/           # Auto-generated results
│   ├── results_YYYYMMDD_HHMMSS.json
│   ├── results_YYYYMMDD_HHMMSS.csv
│   └── performance_comparison_YYYYMMDD_HHMMSS.png
│
├── performance_test.py            # Automated performance testing
├── requirements.txt               # Python dependencies
├── requirements-grpc.txt          # gRPC-specific dependencies
├── requirements-reqrep.txt        # Request-Reply dependencies
├── requirements-mpi.txt           # MPI dependencies
├── setup.ps1                      # Windows setup script
├── setup.sh                       # Linux/Mac setup script
├── test_all.ps1                   # Quick test script
└── README.md                      # This file
```

---

## 🚀 Installation Steps

### Step 1: Navigate to Project Directory
```powershell
cd "c:\Users\USER\OneDrive\Semester 7\CST435\Assignment 1\Related_Codes\example_map_reduce_program"
```

### Step 2: Run Setup Script

**For Windows (PowerShell):**
```powershell
.\setup.ps1
```

**For Linux/Mac (Bash):**
```bash
chmod +x setup.sh
./setup.sh
```

**What the setup script does:**
1. ✓ Checks Docker installation
2. ✓ Installs Python dependencies
3. ✓ Generates gRPC Protocol Buffer code
4. ✓ Builds all Docker images

**Expected output:**
```
MapReduce Performance Comparison - Setup Script
============================================================
Checking Docker...
Docker version 24.0.x ...
Docker Compose version 2.x.x ...
Docker is ready!

Installing Python dependencies...
Successfully installed grpcio-1.60.0 ...

Generating gRPC code...
gRPC code generated!

Building Docker images...
Successfully built grpc-server
Successfully built xmlrpc-server
Successfully built mpi-runner

============================================================
Setup completed successfully!
============================================================
```

### Step 3: Verify Installation

Run quick test to verify all implementations:
```powershell
.\test_all.ps1
```

This will test each implementation sequentially.

---

## 🧪 Running Individual Tests

### 1. Test gRPC Implementation

**Start 3 gRPC servers:**
```powershell
cd docker
```for first time set-up server
docker-compose build grpc-server-1
```then
docker-compose up -d grpc-server-1 grpc-server-2 grpc-server-3
```

**Run client:**
```powershell
docker-compose run --rm grpc-client
```

**Expected output:**
```
Connected to 3 gRPC servers
Server 1: MapReduce service is healthy
Server 2: MapReduce service is healthy
Server 3: MapReduce service is healthy

Processing text with 1234 characters...
Map - Chunk 0: Processed 45 words in 0.0012s
Map - Chunk 1: Processed 47 words in 0.0011s
Map - Chunk 2: Processed 46 words in 0.0013s
Map phase completed in 0.0245s
Reduce: Aggregated 89 unique words in 0.0008s
Reduce phase completed in 0.0015s

============================================================
RESULTS:
============================================================
Total Duration: 0.0345s
Map Duration: 0.0245s
Reduce Duration: 0.0015s
Number of Servers: 3

Top 10 Words:
  the: 12
  is: 8
  and: 7
  ...
```

**Stop servers:**
```powershell
docker-compose down
cd ..
```

---

### 2. Test XML-RPC Implementation

**Start 3 XML-RPC servers:**
```powershell
cd docker
```for first time set-up this server
docker-compose build xmlrpc-server-1
```then
docker-compose up -d xmlrpc-server-1 xmlrpc-server-2 xmlrpc-server-3
```

**Run client:**
```powershell
docker-compose run --rm xmlrpc-client
```

**Stop servers:**
```powershell
docker-compose down
cd ..
```

---

### 3. Test Request-Reply Implementation

**Start 3 Request-Reply servers:**
```powershell
cd docker
docker-compose build reqrep-server-1
docker-compose up -d reqrep-server-1 reqrep-server-2 reqrep-server-3
```

**Run client:**
```powershell
docker-compose run --rm reqrep-client
```

**Expected output:**
```
Connected to 3 Request-Reply servers
Server 1: Request-Reply MapReduce service is healthy on port 5555
Server 2: Request-Reply MapReduce service is healthy on port 5555
Server 3: Request-Reply MapReduce service is healthy on port 5555

Processing text with 1206 characters...
Map phase completed in 0.0198s
Reduce phase completed in 0.0015s

============================================================
RESULTS:
============================================================
Total Duration: 0.0285s
Map Duration: 0.0198s
Reduce Duration: 0.0015s
Number of Servers: 3

Top 10 Words:
  is: 6
  performance: 5
  ...
```

**Stop servers:**
```powershell
docker-compose down
cd ..
```

---

### 4. Test MPI Implementation

**Run MPI (single container, 3 processes):**
```powershell
cd docker
docker-compose run --rm mpi-runner
cd ..
```

**Expected output:**
```
MPI MapReduce with 3 processes
Processing text with 1234 characters...
Rank 0 - Processed 45 words in 0.0015s
Rank 1 - Processed 47 words in 0.0014s
Rank 2 - Processed 46 words in 0.0016s

Map phase completed in 0.0234s
Reduce: Aggregated 89 unique words in 0.0009s
...
```

---

### 4. Test MPI Implementation

**Run MPI (single container, 3 processes):**
```powershell
cd docker
docker-compose run --rm mpi-runner
cd ..
```

**Expected output:**
```
MPI MapReduce with 3 processes
Processing text with 1234 characters...
Rank 0 - Processed 45 words in 0.0015s
Rank 1 - Processed 47 words in 0.0014s
Rank 2 - Processed 46 words in 0.0016s

Map phase completed in 0.0234s
Reduce: Aggregated 89 unique words in 0.0009s
...
```

---

## 📊 Performance Comparison

### Running Automated Performance Tests

**Execute the performance test script:**
```powershell
python performance_test.py
```

**What it does:**
1. Runs each implementation **3 times** (configurable)
2. Measures execution time for each run
3. Calculates statistics (mean, min, max)
4. Generates comparison charts
5. Saves results to JSON and CSV

**Process:**
```
Testing gRPC Implementation
Run 1/3
Starting gRPC servers...
Duration: 0.0456s
...

Testing XML-RPC Implementation
Run 1/3
Starting XML-RPC servers...
Duration: 0.0623s
...

Testing Request-Reply Implementation
Run 1/3
Starting Request-Reply servers...
Duration: 0.0298s
...

Testing MPI Implementation
Run 1/3
Duration: 0.0389s
...

PERFORMANCE COMPARISON REPORT
============================================================
Execution Times (seconds):
Implementation       Mean       Min        Max        Runs      
------------------------------------------------------------
grpc                0.0445     0.0423     0.0478     3         
xmlrpc              0.0612     0.0598     0.0635     3         
reqrep              0.0298     0.0285     0.0312     3         
mpi                 0.0387     0.0375     0.0401     3         

Chart saved to: performance_results/performance_comparison_20251019_143022.png
Results saved to: performance_results/results_20251019_143022.json
CSV saved to: performance_results/results_20251019_143022.csv
```

### Output Files

**1. JSON File** (`results_YYYYMMDD_HHMMSS.json`)
```json
{
  "timestamp": "20251019_143022",
  "statistics": {
    "grpc": {
      "mean": 0.0445,
      "min": 0.0423,
      "max": 0.0478,
      "runs": 3
    },
    ...
  },
  "raw_results": { ... }
}
```

**2. CSV File** (`results_YYYYMMDD_HHMMSS.csv`)
```csv
Implementation,Run,Duration
grpc,1,0.0445
grpc,2,0.0423
grpc,3,0.0478
...
```

**3. Chart** (PNG image with bar chart and box plot)

---

## 📈 Understanding the Results

### Key Metrics to Analyze:

1. **Total Duration**: End-to-end execution time
   - Includes network overhead, serialization, processing

2. **Map Duration**: Time for parallel word counting
   - Shows distribution efficiency

3. **Reduce Duration**: Time for aggregation
   - Usually minimal for small datasets

4. **Throughput**: Operations per second
   - Higher is better

### Expected Performance Order (typically):
1. **Request-Reply (ZeroMQ)** - Fast (lightweight messaging, binary protocol)
2. **MPI** - Fast (optimized for HPC)
3. **gRPC** - Good (binary protocol, efficient)
4. **XML-RPC** - Slowest (text-based XML, overhead)

### Factors Affecting Performance:
- **Network latency**: Docker networking overhead
- **Serialization**: Protocol efficiency (binary vs. text)
- **Container startup**: Docker container initialization
- **Data size**: Larger datasets show more differences
- **Number of workers**: Scaling efficiency

---

## 🔧 Troubleshooting

### Issue 1: Docker not running
**Error:** `Cannot connect to Docker daemon`

**Solution:**
1. Start Docker Desktop
2. Wait for Docker to fully initialize
3. Verify: `docker ps`

---

### Issue 2: Port already in use
**Error:** `Bind for 0.0.0.0:50051 failed: port is already allocated`

**Solution:**
1. Stop all containers: `docker-compose down`
2. Kill process using port: `netstat -ano | findstr :50051`
3. Or change port in `docker-compose.yml`

---

### Issue 3: gRPC code not generated
**Error:** `ModuleNotFoundError: No module named 'mapreduce_pb2'`

**Solution:**
```powershell
cd grpc_implementation
python -m grpc_tools.protoc -I./proto --python_out=. --grpc_python_out=. proto/mapreduce.proto
cd ..
```

---

### Issue 4: MPI build fails
**Error:** `Unable to install mpi4py`

**Solution:**
- MPI runs in Docker container (no local installation needed)
- If testing locally, install MPI:
  - Windows: Download MS-MPI
  - Linux: `sudo apt-get install libopenmpi-dev`
  - Mac: `brew install open-mpi`

---

### Issue 5: Permission denied (Linux/Mac)
**Error:** `Permission denied: './setup.sh'`

**Solution:**
```bash
chmod +x setup.sh
chmod +x test_all.ps1
```

---

## 📝 Tips for Your Report

### What to Include:

1. **Problem Statement**
   - Word count MapReduce problem
   - Need for distributed processing

2. **Installation Process**
   - Docker setup steps
   - Challenges faced
   - Screenshots of successful installation

3. **Implementation Details**
   - Explain each approach
   - Code snippets (from this project)
   - Architecture diagrams

4. **Deployment Environment**
   - 3 Docker containers per implementation
   - Network configuration
   - Resource allocation

5. **Performance Results**
   - Tables with execution times
   - Charts (from performance_results/)
   - Analysis of differences

6. **Findings & Discussion**
   - Which approach is fastest? Why?
   - Overhead comparison
   - Scalability considerations
   - Real-world applications

7. **Team Division**
   - Who worked on what
   - Collaboration process

### Screenshots to Capture:
- [ ] Docker Desktop running
- [ ] Successful setup output
- [ ] Each implementation running
- [ ] Performance comparison chart
- [ ] Container logs
- [ ] Final results table

---

## 🎥 Video Recording Tips

**Content to Cover (15 minutes):**
1. **Introduction** (2 min)
   - Team introduction
   - Project overview

2. **Demo Setup** (3 min)
   - Show Docker Desktop
   - Run setup script
   - Explain architecture

3. **Individual Tests** (5 min)
   - Demonstrate each implementation
   - Show output
   - Explain differences

4. **Performance Comparison** (3 min)
   - Run performance_test.py
   - Show results
   - Discuss findings

5. **Conclusion** (2 min)
   - Summary
   - Lessons learned
   - Q&A preparation

---

## 📚 Additional Resources

- **gRPC Documentation**: https://grpc.io/docs/languages/python/
- **Docker Documentation**: https://docs.docker.com/
- **MPI Tutorial**: https://mpi4py.readthedocs.io/
- **Python Multiprocessing**: https://docs.python.org/3/library/multiprocessing.html

---

## ✅ Checklist Before Submission

- [ ] All implementations run successfully
- [ ] Performance tests completed
- [ ] Results saved and documented
- [ ] Screenshots captured
- [ ] Video recorded (< 15 minutes)
- [ ] Report written (< 10 pages)
- [ ] Source code attached
- [ ] References cited

---

**Good luck with your assignment! 🚀**

For questions or issues, document them in your report as part of the learning experience.
