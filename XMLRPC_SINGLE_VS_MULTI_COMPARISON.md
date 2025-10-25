# Single vs Multiple Container Comparison - XML-RPC

## Test Results (October 26, 2025)

**Dataset**: sample_text.txt (1206 characters, 156 words)

---

## XML-RPC Performance Comparison

### Single Server vs Multiple Servers

| Service | Single Server | 3 Servers | Difference |
|---------|--------------|-----------|------------|
| **Service 1 (Word Count)** | 0.0043s | 0.0077s | +79% slower |
| **Service 2 (Alphabetical Sort)** | 0.0021s | 0.0039s | +86% slower |
| **Service 3 (Word Length Analysis)** | 0.0013s | 0.0049s | +277% slower |
| **Total Time** | **0.0077s** | **0.0165s** | **+114% slower** |

### 🏆 Winner: Single Server (2.1x faster)

---

## Complete Comparison: gRPC vs XML-RPC

### Single Server Performance

| Service | gRPC (1 server) | XML-RPC (1 server) | Winner |
|---------|----------------|-------------------|---------|
| Service 1 | 0.0049s | 0.0043s | XML-RPC (1.1x) |
| Service 2 | 0.0033s | 0.0021s | XML-RPC (1.6x) |
| Service 3 | 0.0059s | 0.0013s | XML-RPC (4.5x) |
| **Total** | **0.0140s** | **0.0077s** | **XML-RPC (1.8x)** ✅ |

### Multiple Servers Performance

| Service | gRPC (3 servers) | XML-RPC (3 servers) | Winner |
|---------|-----------------|-------------------|---------|
| Service 1 | 0.0121s | 0.0077s | XML-RPC (1.6x) |
| Service 2 | 0.0078s | 0.0039s | XML-RPC (2.0x) |
| Service 3 | 0.0209s | 0.0049s | XML-RPC (4.3x) |
| **Total** | **0.0408s** | **0.0165s** | **XML-RPC (2.5x)** ✅ |

---

## Key Findings

### 🚀 Single Server is Faster for Both

**XML-RPC:**
- Single server: 0.0077s
- 3 servers: 0.0165s
- **Overhead: +114%** (multiple servers are 2.1x slower)

**gRPC:**
- Single server: 0.0140s
- 3 servers: 0.0408s
- **Overhead: +191%** (multiple servers are 2.9x slower)

**Conclusion:** For small datasets, distribution overhead exceeds parallelization benefits.

---

### 🎯 XML-RPC is Faster in Docker!

**Surprising Result:** In Docker containers with optimized networking, XML-RPC outperforms gRPC!

**Why XML-RPC wins in this test:**
1. **Small dataset** (156 words) - no benefit from binary serialization
2. **Optimized Docker networking** - eliminates XML parsing penalty
3. **Simpler protocol** - less connection overhead for tiny payloads
4. **Python-native XML** - efficient in Python runtime

**Why gRPC's advantages don't show here:**
1. **Binary format** - wasted on tiny data (overhead > savings)
2. **HTTP/2 complexity** - connection setup slower for one request
3. **Protocol Buffer overhead** - schema validation adds latency
4. **Small payloads** - binary encoding benefit negligible

---

## Detailed Analysis

### Single Server Performance

```
XML-RPC Single Server (FASTEST):
Service 1:  0.0043s  ████
Service 2:  0.0021s  ██
Service 3:  0.0013s  █
Total:      0.0077s  ███████

gRPC Single Server:
Service 1:  0.0049s  █████
Service 2:  0.0033s  ███
Service 3:  0.0059s  ██████
Total:      0.0140s  ██████████████

XML-RPC 3 Servers:
Service 1:  0.0077s  ████████
Service 2:  0.0039s  ████
Service 3:  0.0049s  █████
Total:      0.0165s  ████████████████

gRPC 3 Servers (SLOWEST):
Service 1:  0.0121s  ████████████
Service 2:  0.0078s  ████████
Service 3:  0.0209s  █████████████████████
Total:      0.0408s  ████████████████████████████████████████
```

---

## When to Use Each Configuration

### ✅ Single Server - Best For:
- **Small datasets** (< 1 MB)
- **Development/testing**
- **Low latency requirements**
- **Simple deployments**
- **Cost optimization**
- Both gRPC and XML-RPC benefit

### ✅ Multiple Servers - Best For:
- **Large datasets** (> 100 MB)
- **True parallel processing**
- **Fault tolerance** (one server fails, others continue)
- **Scalability testing**
- **Production workloads**
- gRPC and XML-RPC both scale

---

## Protocol Comparison for This Workload

### XML-RPC Advantages (Small Data in Docker):
- ✅ Simpler connection setup
- ✅ Native Python XML parsing (fast)
- ✅ Less protocol overhead
- ✅ Faster for tiny payloads

### gRPC Advantages (Would shine with larger data):
- 🔧 Binary serialization (wasted on 156 words)
- 🔧 HTTP/2 multiplexing (wasted on single request)
- 🔧 Strong typing (no runtime benefit here)
- 🔧 Streaming (not used in this test)

---

## The Overhead Breakdown

### Distribution Overhead Analysis

**Single to Multiple Server Cost:**

| Protocol | Single | Multi | Overhead |
|----------|--------|-------|----------|
| XML-RPC | 0.0077s | 0.0165s | +0.0088s (114%) |
| gRPC | 0.0140s | 0.0408s | +0.0268s (191%) |

**Where the overhead comes from:**
1. **Data splitting**: Divide text into 3 chunks
2. **Network requests**: 3x the connections
3. **Result aggregation**: Merge results from 3 servers
4. **Coordination**: Managing 3 servers vs 1

**gRPC has higher overhead because:**
- HTTP/2 connection multiplexing adds complexity
- Protocol Buffer encoding/decoding per chunk
- More robust error handling and retries
- Stronger type validation

---

## Real-World Implications

### For This Dataset (1206 characters):
```
Ranking (Fastest to Slowest):
1. XML-RPC Single Server:   0.0077s  ⭐⭐⭐⭐⭐
2. gRPC Single Server:      0.0140s  ⭐⭐⭐⭐
3. XML-RPC 3 Servers:       0.0165s  ⭐⭐⭐
4. gRPC 3 Servers:          0.0408s  ⭐⭐
```

### For Larger Datasets (Projected):

**10 MB text file:**
- Single server becomes bottleneck
- Multiple servers start to win
- gRPC's binary format saves bandwidth
- Distribution overhead becomes worthwhile

**1 GB text file:**
- Multiple servers essential
- gRPC pulls ahead (efficient binary encoding)
- XML-RPC struggles with large XML parsing
- Network bandwidth becomes critical

---

## Running the Tests

### XML-RPC Single Server:
```bash
cd docker
docker-compose up -d xmlrpc-server-1
docker run --rm --network docker_mapreduce-net \
  -e XMLRPC_SERVERS=http://xmlrpc-server-1:8000 \
  -v "$(pwd)/../:/app" docker-xmlrpc-client \
  python xmlrpc_implementation/client_single_server.py
```

### XML-RPC Multiple Servers:
```bash
cd docker
docker-compose up xmlrpc-server-1 xmlrpc-server-2 xmlrpc-server-3 xmlrpc-client
```

### gRPC Single Server:
```bash
cd docker
docker-compose up -d grpc-server-1
cd ../grpc_implementation
python client_single_server.py
```

### gRPC Multiple Servers:
```bash
cd docker
docker-compose up grpc-server-1 grpc-server-2 grpc-server-3 grpc-client
```

---

## Conclusion

### For Small Datasets in Docker:
✅ **XML-RPC Single Server is the winner** (1.8x faster than gRPC single, 5.3x faster than gRPC multi)

### Key Insights:
1. **Distribution overhead is significant** - For tiny data, single server always wins
2. **Protocol overhead matters less** - With small payloads, XML vs binary doesn't matter
3. **Docker networking is efficient** - Eliminates the huge performance gap seen on Windows
4. **gRPC's advantages need scale** - Binary format and HTTP/2 shine with larger datasets

### Recommendation:
- **< 10 MB**: Use single server (any protocol)
- **10-100 MB**: Test both configurations
- **> 100 MB**: Use multiple servers + gRPC

### The Surprising Truth:
For this specific workload (156 words in Docker), the "slower" XML-RPC protocol actually outperforms the "faster" gRPC by 2.5x! This shows that **protocol efficiency matters less than workload characteristics and deployment environment**.
