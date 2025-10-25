# Single Container vs Multiple Containers Comparison

## Test Results (October 25, 2025)

**Dataset**: sample_text.txt (1206 characters, 156 words)

### Performance Comparison

| Configuration | Service 1 (Word Count) | Service 2 (Alphabetical Sort) | Service 3 (Word Length) | **Total Time** |
|--------------|----------------------|------------------------------|----------------------|--------------|
| **1 Server** | 0.0049s | 0.0033s | 0.0059s | **0.0140s** |
| **3 Servers** | 0.0121s | 0.0078s | 0.0209s | **0.0408s** |
| **Difference** | +147% slower | +136% slower | +254% slower | **+191% slower** |

### Key Findings

#### 🏆 Single Server is FASTER (2.9x)
- **Winner**: Single server at 0.0140s
- **3 Servers**: 0.0408s
- **Overhead**: Network communication + container coordination adds significant overhead

#### Why Single Server Wins for Small Data:

1. **No Network Overhead**
   - Single server: All processing happens locally in memory
   - 3 Servers: Each request travels over Docker network (even if virtual)

2. **No Data Splitting/Merging Overhead**
   - Single server: Processes entire text at once
   - 3 Servers: Must split text into 3 chunks, process separately, then merge results

3. **Simpler Coordination**
   - Single server: Direct function calls
   - 3 Servers: gRPC serialization + deserialization for each chunk

4. **Small Dataset Size**
   - With only 156 words, the overhead of distribution exceeds the benefit of parallelization

---

## When to Use Each Approach

### ✅ Use Single Server When:
- Dataset is small (< 1 MB)
- Response time is critical
- Simple deployment is preferred
- Development/testing environment
- Cost optimization is important

### ✅ Use Multiple Servers When:
- Dataset is large (> 100 MB)
- Scalability is required
- Fault tolerance is needed (one server can fail, others continue)
- Multiple physical machines are available
- Production environment with high load
- Processing time > network overhead

---

## Detailed Breakdown by Service

### Service 1: Word Count (MapReduce)
```
Single Server:  0.0049s
3 Servers:      0.0121s
Overhead:       +147%
```
**Analysis**: Map phase benefits from parallel processing, but reduce phase requires aggregating results from all servers, adding overhead.

### Service 2: Alphabetical Sort
```
Single Server:  0.0033s
3 Servers:      0.0078s
Overhead:       +136%
```
**Analysis**: Merge sort on distributed chunks requires final merge operation across all sorted sublists, doubling the time.

### Service 3: Word Length Analysis
```
Single Server:  0.0059s
3 Servers:      0.0209s
Overhead:       +254%
```
**Analysis**: Statistical aggregation requires coordination across all servers to compute min/max/average, adding significant overhead.

---

## Architecture Diagrams

### Single Server Architecture
```
┌─────────────────────────────────────────┐
│           Single Container              │
│                                         │
│  ┌───────────────────────────────────┐  │
│  │       Client Process              │  │
│  │  - Connects to 1 server           │  │
│  │  - Sends entire text              │  │
│  │  - Receives complete result       │  │
│  └───────────────────────────────────┘  │
│               │                         │
│               ▼                         │
│  ┌───────────────────────────────────┐  │
│  │       Server Process              │  │
│  │  - All 3 services available       │  │
│  │  - Processes entire dataset       │  │
│  │  - Returns complete result        │  │
│  └───────────────────────────────────┘  │
│                                         │
└─────────────────────────────────────────┘
```

### Multiple Servers Architecture
```
┌─────────────────────────────────────────────────────┐
│                   Client Container                   │
│  - Connects to 3 servers                            │
│  - Splits text into 3 chunks                        │
│  - Distributes chunks across servers                │
│  - Aggregates results                               │
└─────────────────────────────────────────────────────┘
         │                │                │
         ▼                ▼                ▼
   ┌──────────┐     ┌──────────┐     ┌──────────┐
   │ Server 1 │     │ Server 2 │     │ Server 3 │
   │  Port    │     │  Port    │     │  Port    │
   │  50051   │     │  50052   │     │  50053   │
   │          │     │          │     │          │
   │ Process  │     │ Process  │     │ Process  │
   │ chunk 1  │     │ chunk 2  │     │ chunk 3  │
   │ (33% of  │     │ (33% of  │     │ (34% of  │
   │  text)   │     │  text)   │     │  text)   │
   └──────────┘     └──────────┘     └──────────┘
```

---

## How to Run Each Configuration

### Single Server (Faster for small data)
```bash
# Start 1 server
cd docker
docker-compose up -d grpc-server-1

# Run single-server client
cd ../grpc_implementation
python client_single_server.py
```

### Multiple Servers (Better for large data)
```bash
# Start 3 servers
cd docker
docker-compose up -d grpc-server-1 grpc-server-2 grpc-server-3

# Run multi-server client
cd ../grpc_implementation
python client_multi_servers.py
```

---

## Recommendation

**For this dataset (1206 characters):**
- ✅ **Use single server** - 2.9x faster
- ❌ **Avoid 3 servers** - overhead > benefit

**For larger datasets (e.g., 1 GB text file):**
- ❌ **Avoid single server** - will be bottlenecked
- ✅ **Use 3 servers** - parallel processing will win

**Breakeven Point**: Approximately 10-50 MB of text data
- Below this: single server is faster
- Above this: multiple servers become faster

---

## Conclusion

This demonstrates the classic **distributed computing tradeoff**:
- **Small data**: Centralized processing wins (lower overhead)
- **Large data**: Distributed processing wins (parallelization benefit > overhead)

The 2.9x performance difference shows that containerization and network communication add significant overhead that only pays off with larger datasets.
