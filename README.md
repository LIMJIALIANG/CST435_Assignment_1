# MapReduce Performance Comparison Project

## 📖 Overview
This project provides a **comprehensive performance comparison** of three distributed computing paradigms:
- **MPI** (Message Passing Interface) - HPC-grade parallel computing
- **gRPC** (Google Remote Procedure Call) - Modern microservices RPC  
- **XML-RPC** - Traditional web services RPC

**Key Finding**: MPI is 2-47x faster than RPC protocols, but RPC offers better fault tolerance and distributed system capabilities.

---

## 🎯 Quick Start

### 1. Prerequisites
- Docker Desktop installed and running
- Python 3.9+
- Docker Compose

### 2. Setup (One-Time)
```bash
# Install Python dependencies
pip install -r requirements.txt

# Build Docker images
cd docker
docker-compose build
cd ..

# Generate test datasets (1K to 1M words)
python generate_large_data.py
```

### 3. Start RPC Servers
```bash
cd docker
docker-compose up -d grpc-server-1 xmlrpc-server-1
cd ..
```

### 4. Run Tests
```bash
# Test all three protocols together
python performance_test.py --data data/large_50k.txt --protocol all
python performance_test.py --data data/huge_1m.txt --protocol all
```

---

## 📊 Performance Results Summary

### Complete Comparison (All Three Protocols)

| Dataset | MPI | XML-RPC | gRPC | Winner | MPI Advantage |
|---------|-----|---------|------|--------|---------------|
| 156 words (1.2 KB) | 0.002s | 0.017s | 0.041s | **MPI** âš¡ | **8-20x faster** |
| 10K words (91 KB) | 0.009s | 0.079s | 0.416s | **MPI** âš¡ | **8-47x faster** |
| 50K words (454 KB) | 0.044s | 0.151s | 0.218s | **MPI** âš¡ | **3.4-5.0x faster** |
| 1M words (8.9 MB) | 0.713s | 1.511s | 1.488s | **MPI** âš¡ | **2.1x faster** |

**Key Insights:**
- 🏆 **MPI dominates** at all dataset sizes (2-47x faster)
- 📉 **MPI advantage decreases** as data size increases (computation dominates over communication)
- ⚔️ **gRPC vs XML-RPC**: XML-RPC faster for small data (< 500 KB), gRPC faster for large data (> 1 MB)
- 🔄 **Crossover point**: ~500 KB - 1 MB where gRPC overtakes XML-RPC

---

## � Test Files Explanation

### `performance_test.py` (Recommended)
**Purpose:** Compare all three protocols with 3 containers/servers each

**Features:**
- âœ… Tests MPI (3 processes), gRPC (3 servers), XML-RPC (3 servers)
- âœ… Generates visual bar charts comparing all services
- âœ… Saves results to JSON for later analysis
- âœ… Shows winner and speedup comparisons

**Usage:**
```bash
python performance_test.py --data data/large_50k.txt --protocol all
```

**Output:**
- Console: Performance comparison table
- Visual: `performance_results/multi_server_comparison_*.png`
- Data: `performance_results/multi_server_results_*.json`

---

### `performance_test_single_server.py`
**Purpose:** Analyze container overhead by comparing single vs multi-container setups

**Features:**
- ✅ Tests gRPC single machine (local process)
- ✅ Tests gRPC multi-container (Docker)
- ✅ Tests XML-RPC and MPI
- ✅ Generates box plots and bar charts
- ✅ Analyzes container overhead percentage

**Usage:**
```bash
python performance_test_single_server.py
```

**Output:**
- Console: Detailed performance statistics
- Visual: `performance_results/performance_comparison_*.png`
- Data: `performance_results/results_*.json` and `results_*.csv`
- Analysis: Container overhead calculations

---

## �🚀 How to Run Each Protocol

### Option 1: Run All Three Protocols Together (Recommended)

```bash
# Test all protocols with different dataset sizes
python performance_test.py --data data/small_1k.txt --protocol all
python performance_test.py --data data/medium_10k.txt --protocol all
python performance_test.py --data data/large_50k.txt --protocol all
python performance_test.py --data data/huge_1m.txt --protocol all
```

**This generates:**
- Console performance comparison table
- Visual charts: `performance_results/single_server_comparison_YYYYMMDD_HHMMSS.png`
- JSON results: `performance_results/single_server_results_YYYYMMDD_HHMMSS.json`

**Output:**
```
📊 PERFORMANCE COMPARISON
Service                        MPI             gRPC            XML-RPC
----------------------------------------------------------------------
Service 1 (Word Count)          0.0138s        0.0835s        0.0551s       âœ… MPI
Service 2 (Sorting)             0.0157s        0.0732s        0.0458s       âœ… MPI
Service 3 (Word Lengths)        0.0145s        0.0615s        0.0498s       âœ… MPI
TOTAL                           0.0440s        0.2181s        0.1508s       âœ… MPI

🏆 OVERALL WINNER: MPI (0.0440s)

Speedup Comparisons:
  MPI is 4.96x faster than gRPC
  MPI is 3.43x faster than XML-RPC
  XML-RPC is 1.45x faster than gRPC
```

### Option 2: Run Individual Protocols

#### MPI (Fastest - Batch Job)
```bash
# Using Docker (recommended)
cd docker
docker-compose run --rm mpi-runner
cd ..

# Test with specific data file
python performance_test.py --data data/large_50k.txt --protocol mpi

# Using local MPI (if installed)
cd mpi_implementation
mpiexec -n 3 python client.py
```

#### gRPC (Modern RPC)
```bash
# Make sure server is running
cd docker
docker-compose up -d grpc-server-1
cd ..

# Test gRPC
python performance_test.py --data data/large_50k.txt --protocol grpc

# Or run client directly
cd grpc_implementation
python client.py
```

#### XML-RPC (Traditional RPC)
```bash
# Make sure server is running
cd docker
docker-compose up -d xmlrpc-server-1
cd ..

# Test XML-RPC
python performance_test.py --data data/large_50k.txt --protocol xmlrpc

# Or run client directly
cd xmlrpc_implementation
python client.py
```

---

## âš™ï¸ Docker Server Setup

### Start RPC Servers
```bash
cd docker

# Start gRPC server
docker-compose up -d grpc-server-1

# Start XML-RPC server  
docker-compose up -d xmlrpc-server-1

# Or start both
docker-compose up -d grpc-server-1 xmlrpc-server-1

cd ..
```

### MPI (Docker Container)
```bash
# MPI runs as a batch job with multiple processes in one container
cd docker
docker-compose run --rm mpi-runner

# Or customize process count
docker run --rm -v "${PWD}/../:/app" docker-mpi-runner \
  mpiexec -n 5 --allow-run-as-root python mpi_implementation/client.py
```

**Note:** MPI runs all processes in one container (shared memory), unlike RPC which uses network communication to separate server containers.

---

## 📊 Comparison Tests

### Compare All Protocols
```bash
# Start servers first
cd docker
docker-compose up -d grpc-server-1 xmlrpc-server-1
cd ..

# Run comprehensive comparison with various dataset sizes
python performance_test.py --data data/small_1k.txt --protocol all
python performance_test.py --data data/medium_10k.txt --protocol all
python performance_test.py --data data/large_50k.txt --protocol all
python performance_test.py --data data/huge_1m.txt --protocol all
```

**This generates:**
- Console: Performance comparison table with speedup analysis
- Visual: `performance_results/single_server_comparison_*.png` (4-subplot bar chart)
- Data: `performance_results/single_server_results_*.json`

### Test Individual Protocols
```bash
# Test only gRPC
python performance_test.py --data data/large_50k.txt --protocol grpc

# Test only XML-RPC
python performance_test.py --data data/large_50k.txt --protocol xmlrpc

# Test only MPI
python performance_test.py --data data/large_50k.txt --protocol mpi
```

---

## ðŸ“ Project Structure
```
.
â”œâ”€â”€ grpc_implementation/
â”‚   â”œâ”€â”€ proto/
â”‚   â”‚   â””â”€â”€ mapreduce.proto
â”‚   â”œâ”€â”€ server.py
â”‚   â”œâ”€â”€ client.py
â”‚   â”œâ”€â”€ mapreduce_pb2.py (generated)
â”‚   â””â”€â”€ mapreduce_pb2_grpc.py (generated)
â”œâ”€â”€ xmlrpc_implementation/
â”‚   â”œâ”€â”€ server.py
â”‚   â””â”€â”€ client.py
â”œâ”€â”€ mpi_implementation/
â”‚   â”œâ”€â”€ client.py
â”‚   â””â”€â”€ server.py
â”œâ”€â”€ docker/
â”‚   â”œâ”€â”€ Dockerfile.grpc
â”‚   â”œâ”€â”€ Dockerfile.xmlrpc
â”‚   â”œâ”€â”€ Dockerfile.mpi
â”‚   â””â”€â”€ docker-compose.yml
â”œâ”€â”€ data/
â”‚   â””â”€â”€ sample_text.txt
â”œâ”€â”€ performance_test.py          # Performance comparison with visualizations
â”œâ”€â”€ generate_large_data.py       # Dataset generator
â”œâ”€â”€ requirements.txt
â”œâ”€â”€ requirements-grpc.txt
â””â”€â”€ requirements-mpi.txt
```

---

## ðŸ“ Project Structure

```
.
â”œâ”€â”€ grpc_implementation/
â”‚   â”œâ”€â”€ proto/
â”‚   â”‚   â””â”€â”€ mapreduce.proto          # gRPC service definitions
â”‚   â”œâ”€â”€ server.py                     # gRPC server
â”‚   â”œâ”€â”€ client.py                     # gRPC multi-server client
â”‚   â”œâ”€â”€ client_single_server.py       # gRPC single-server client
â”‚   â”œâ”€â”€ mapreduce_pb2.py             # Generated Protocol Buffers
â”‚   â””â”€â”€ mapreduce_pb2_grpc.py        # Generated gRPC code
â”œâ”€â”€ xmlrpc_implementation/
â”‚   â”œâ”€â”€ server.py                     # XML-RPC server
â”‚   â”œâ”€â”€ client.py                     # XML-RPC multi-server client
â”‚   â””â”€â”€ client_single_server.py       # XML-RPC single-server client
â”œâ”€â”€ mpi_implementation/
â”‚   â”œâ”€â”€ client.py                     # MPI client (master + workers)
â”‚   â””â”€â”€ server.py                     # MPI server helper
â”œâ”€â”€ docker/
â”‚   â”œâ”€â”€ Dockerfile.grpc              # gRPC Docker image
â”‚   â”œâ”€â”€ Dockerfile.xmlrpc            # XML-RPC Docker image
â”‚   â”œâ”€â”€ Dockerfile.mpi               # MPI Docker image
â”‚   â””â”€â”€ docker-compose.yml           # Docker orchestration
â”œâ”€â”€ data/
â”‚   â”œâ”€â”€ sample_text.txt              # Original sample (156 words)
â”‚   â”œâ”€â”€ small_1k.txt                 # 1K words (9 KB)
â”‚   â”œâ”€â”€ medium_10k.txt               # 10K words (91 KB)
â”‚   â”œâ”€â”€ large_50k.txt                # 50K words (454 KB)
â”‚   â”œâ”€â”€ xlarge_100k.txt              # 100K words (907 KB)
â”‚   â”œâ”€â”€ xxlarge_500k.txt             # 500K words (4.4 MB)
â”‚   â””â”€â”€ huge_1m.txt                  # 1M words (8.9 MB)
â”œâ”€â”€ performance_test.py              # Performance comparison with visualizations
â”œâ”€â”€ generate_large_data.py           # Dataset generator
â”œâ”€â”€ requirements.txt                 # Python dependencies
â”œâ”€â”€ requirements-grpc.txt            # gRPC-specific dependencies
â”œâ”€â”€ requirements-mpi.txt             # MPI-specific dependencies
â””â”€â”€ README.md                        # This file
```

---

## ðŸ—ï¸ Architecture Comparison

### MPI: Tightly Coupled Parallel Computing
```
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚         MPI Container                   â”‚
â”‚  â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”  â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”  â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â” â”‚
â”‚  â”‚ Rank 0  â”‚  â”‚ Rank 1  â”‚  â”‚ Rank 2  â”‚ â”‚
â”‚  â”‚ Master  â”‚  â”‚ Worker  â”‚  â”‚ Worker  â”‚ â”‚
â”‚  â””â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”˜  â””â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”˜  â””â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”˜ â”‚
â”‚       â””â”€â”€â”€â”€â”€â”€â”€â”€â”¼â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜       â”‚
â”‚         Shared Memory (MPI Comm)        â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
         Batch Job (Runs & Exits)
```

**Characteristics:**
- âœ… Maximum performance (zero network overhead)
- âœ… Optimized collective operations (scatter, gather, barrier)
- âŒ Tightly coupled (all processes must run together)
- âŒ Limited fault tolerance
- **Use for:** HPC, scientific computing, maximum speed

### gRPC: Modern Microservices RPC
```
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”    HTTP/2 + Protobuf    â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚          â”‚ â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€> â”‚ Server 1 â”‚
â”‚          â”‚ â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€> â”‚ Server 2 â”‚
â”‚  Client  â”‚ â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€> â”‚ Server 3 â”‚
â”‚          â”‚ <â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€ â”‚   ...    â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜       Network            â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
                Binary Protocol
```

**Characteristics:**
- âœ… Production-ready, fault tolerant
- âœ… Strong typing (Protocol Buffers)
- âœ… Efficient for large data (> 1 MB)
- âš ï¸ Network overhead
- **Use for:** Microservices, cloud-native apps, large-scale data

### XML-RPC: Traditional Web Services
```
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”    HTTP/1.1 + XML       â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚          â”‚ â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€> â”‚ Server 1 â”‚
â”‚          â”‚ â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€> â”‚ Server 2 â”‚
â”‚  Client  â”‚ â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€> â”‚ Server 3 â”‚
â”‚          â”‚ <â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€ â”‚   ...    â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜       Network            â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
               Text-based Protocol
```

**Characteristics:**
- âœ… Simple, human-readable
- âœ… Wide language support
- âœ… Efficient for small data (< 500 KB)
- âš ï¸ Higher overhead than gRPC at scale
- **Use for:** Legacy systems, simple services, prototyping

---

## ðŸŽ“ When to Use Each Protocol

| Protocol | Best For | Avoid For |
|----------|----------|-----------|
| **MPI** | â€¢ HPC & scientific computing<br>â€¢ Maximum performance needed<br>â€¢ Batch processing<br>â€¢ Single machine/HPC cluster | â€¢ Distributed systems across networks<br>â€¢ Microservices<br>â€¢ Long-running services<br>â€¢ Web applications |
| **gRPC** | â€¢ Microservices architecture<br>â€¢ Production distributed systems<br>â€¢ Large data (> 1 MB)<br>â€¢ Real-time streaming<br>â€¢ Cross-language support | â€¢ Simple prototypes<br>â€¢ Very small data<br>â€¢ Browser clients |
| **XML-RPC** | â€¢ Legacy system integration<br>â€¢ Simple web services<br>â€¢ Small data (< 500 KB)<br>â€¢ Rapid prototyping<br>â€¢ Human-readable debugging | â€¢ Large data transfers<br>â€¢ Performance-critical apps<br>â€¢ Modern microservices |

---

## ðŸ”§ Docker Commands Reference

### Start/Stop Servers
```bash
# Start RPC servers
cd docker
docker-compose up -d grpc-server-1 xmlrpc-server-1

# Stop all servers
docker-compose down

# Check server status
docker-compose ps

# View server logs
docker-compose logs grpc-server-1
docker-compose logs xmlrpc-server-1

# Restart servers
docker-compose restart grpc-server-1 xmlrpc-server-1
```

### MPI Commands
```bash
# Run with default 3 processes
docker-compose run --rm mpi-runner

# Run with custom process count
docker run --rm -v "${PWD}/../:/app" docker-mpi-runner \
  mpiexec -n 5 --allow-run-as-root python mpi_implementation/client.py
```

### Rebuild Images
```bash
cd docker
docker-compose build
```

---

## ðŸ› Troubleshooting

### Servers Not Starting
```bash
docker-compose down
docker-compose up -d grpc-server-1 xmlrpc-server-1
# Wait 2-3 seconds for servers to initialize
```

### Port Conflicts (Windows)
```powershell
# Check what's using ports
netstat -ano | findstr "50051"  # gRPC
netstat -ano | findstr "8000"   # XML-RPC

# Kill process if needed
taskkill /PID <process_id> /F
```

### Port Conflicts (Linux/Mac)
```bash
# Check what's using ports
lsof -i :50051  # gRPC
lsof -i :8000   # XML-RPC

# Kill process if needed
kill -9 <PID>
```

### MPI Test Fails
```bash
# Make sure Docker is running
docker --version

# Rebuild MPI image
cd docker
docker-compose build mpi-runner
```

### Performance Test Connection Errors
```bash
# Verify servers are running
docker-compose ps

# Check server logs for errors
docker-compose logs grpc-server-1
docker-compose logs xmlrpc-server-1

# Restart if needed
docker-compose restart grpc-server-1 xmlrpc-server-1
```

---

## ðŸ“ˆ Expected Test Results

### Small Dataset (156 words)
```
Protocol          | Time    | Speedup
------------------|---------|---------
MPI               | 0.002s  | 1.0x (baseline - FASTEST!)
XML-RPC (1 srv)   | 0.008s  | 4.0x slower
XML-RPC (3 srv)   | 0.017s  | 8.5x slower
gRPC (1 srv)      | 0.014s  | 7.0x slower
gRPC (3 srv)      | 0.041s  | 20.5x slower
```

### Large Dataset (50K words)
```
Protocol          | Time    | Speedup
------------------|---------|---------
MPI               | 0.044s  | 1.0x (baseline - FASTEST!)
XML-RPC (3 srv)   | 0.151s  | 3.4x slower
gRPC (3 srv)      | 0.218s  | 5.0x slower
```

### Huge Dataset (1M words)
```
Protocol          | Time    | Speedup
------------------|---------|---------
MPI               | 0.713s  | 1.0x (baseline - FASTEST!)
gRPC (3 srv)      | 1.488s  | 2.1x slower
XML-RPC (3 srv)   | 1.511s  | 2.1x slower
```

**Note:** gRPC overtakes XML-RPC at ~500 KB - 1 MB crossover point!

---

## ðŸ’¡ Key Takeaways

1. **MPI is always fastest** (2-47x faster than RPC)
   - Zero network overhead (shared memory)
   - Optimized for HPC workloads
   - Best for batch processing on single machine/cluster

2. **Single container beats multiple for small data**
   - Distribution overhead > parallelization benefit
   - Use single server for < 1 MB data

3. **gRPC vs XML-RPC depends on data size**
   - XML-RPC faster for small data (< 500 KB)
   - gRPC faster for large data (> 1 MB)
   - Crossover at ~500 KB - 1 MB

4. **Choose based on architecture needs, not just speed**
   - MPI: Maximum performance, tightly coupled
   - gRPC: Production-ready, fault tolerant, scalable
   - XML-RPC: Simple, legacy-friendly, good for small data

---

## ðŸ“š Services Implemented

All three implementations provide the same services:

1. **Word Count (MapReduce)**
   - Splits text into chunks
   - Counts word frequencies in parallel
   - Aggregates results
   - Returns top 10 most frequent words

2. **Alphabetical Word Sorting**
   - Distributes text chunks to workers
   - Each worker sorts their chunk
   - Merges sorted results
   - Returns unique sorted words

3. **Word Length Analysis**
   - Analyzes word lengths across chunks
   - Computes statistics (min, max, average)
   - Aggregates length distribution
   - Returns complete analysis

---

## ðŸ“ Requirements

### Python Dependencies
```txt
grpcio==1.58.0
grpcio-tools==1.58.0
mpi4py==3.1.4
```

### System Requirements
- Docker Desktop
- Python 3.9+
- 2GB RAM minimum
- 5GB disk space for Docker images

---

## ðŸŽ¯ Conclusion

This project demonstrates that **different tools exist for different problems**:

- **Need maximum speed?** â†’ Use MPI
- **Building microservices?** â†’ Use gRPC  
- **Simple web service?** â†’ Use XML-RPC
- **Small data?** â†’ Single container wins
- **Large data?** â†’ Multiple containers win

**The best choice depends on your specific use case, not just raw performance!**

---

*Last Updated: October 26, 2025*  
*Test Environment: Windows 10, Docker Desktop, Python 3.9+*

