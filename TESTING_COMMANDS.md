# Quick Test Commands - gRPC vs XML-RPC Performance

## 🚀 Quick Start

### Generate Test Data
```bash
python generate_large_data.py
```

### Start All Servers (Docker)
```bash
cd docker
docker-compose up -d grpc-server-1 grpc-server-2 grpc-server-3 xmlrpc-server-1 xmlrpc-server-2 xmlrpc-server-3
```

---

## 📊 Run Performance Tests

### Test All Dataset Sizes

```bash
# Small (1K words, 9 KB) - XML-RPC wins ~2x
python performance_test_large.py --data data/small_1k.txt --protocol both

# Medium (10K words, 91 KB) - XML-RPC wins ~1.6x
python performance_test_large.py --data data/medium_10k.txt --protocol both

# Large (50K words, 454 KB) - XML-RPC wins ~1.5x
python performance_test_large.py --data data/large_50k.txt --protocol both

# X-Large (100K words, 907 KB) - XML-RPC wins ~1.4x
python performance_test_large.py --data data/xlarge_100k.txt --protocol both

# XX-Large (500K words, 4.44 MB) - Very close! XML-RPC wins 1.04x
python performance_test_large.py --data data/xxlarge_500k.txt --protocol both

# Huge (1M words, 8.87 MB) - gRPC FINALLY WINS! 1.05x
python performance_test_large.py --data data/huge_1m.txt --protocol both
```

---

## 🎯 Expected Results Summary

| Dataset | Winner | Speedup |
|---------|--------|---------|
| 1K words (9 KB) | XML-RPC | 1.8x |
| 10K words (91 KB) | XML-RPC | 1.6x |
| 50K words (454 KB) | XML-RPC | 1.56x |
| 100K words (907 KB) | XML-RPC | 1.46x |
| 500K words (4.44 MB) | XML-RPC | 1.04x |
| **1M words (8.87 MB)** | **gRPC** | **1.05x** ✅ |

**Crossover point: ~6-7 MB**

---

## 📈 Test Individual Protocols

### gRPC Only
```bash
python performance_test_large.py --data data/large_50k.txt --protocol grpc
```

### XML-RPC Only
```bash
python performance_test_large.py --data data/large_50k.txt --protocol xmlrpc
```

---

## 🔄 Test Single vs Multiple Servers

### Original Sample Text (156 words)

**gRPC:**
```bash
# Single server
cd grpc_implementation
python client_single_server.py

# Multiple servers (3)
python client_multi_servers.py
```

**XML-RPC:**
```bash
# Single server
cd xmlrpc_implementation
python client_single_server.py

# Multiple servers (3)
python client.py
```

---

## 🐳 Docker Commands

### Start Specific Servers
```bash
# gRPC only
docker-compose up -d grpc-server-1 grpc-server-2 grpc-server-3

# XML-RPC only
docker-compose up -d xmlrpc-server-1 xmlrpc-server-2 xmlrpc-server-3

# Single server of each
docker-compose up -d grpc-server-1 xmlrpc-server-1
```

### Check Server Status
```bash
docker-compose ps
```

### View Server Logs
```bash
docker-compose logs grpc-server-1
docker-compose logs xmlrpc-server-1
```

### Stop All Servers
```bash
docker-compose down
```

### Restart Servers
```bash
docker-compose restart grpc-server-1 grpc-server-2 grpc-server-3
docker-compose restart xmlrpc-server-1 xmlrpc-server-2 xmlrpc-server-3
```

---

## 📝 Available Test Files

After running `generate_large_data.py`:

```
data/
  sample_text.txt      -       156 words (  1.2 KB) - Original sample
  small_1k.txt         -     1,000 words (  9.0 KB) - Small test
  medium_10k.txt       -    10,000 words ( 91.2 KB) - Medium test
  large_50k.txt        -    50,000 words (453.8 KB) - Large test
  xlarge_100k.txt      -   100,000 words (907.5 KB) - X-Large test
  xxlarge_500k.txt     -   500,000 words (  4.4 MB) - XX-Large test
  huge_1m.txt          - 1,000,000 words (  8.9 MB) - Huge test ⭐
```

---

## 🎓 Educational Insights

### Key Findings:

1. **XML-RPC is faster for small data** (< 5 MB)
   - Lower protocol overhead
   - Python's optimized XML parsing
   - Docker network eliminates latency penalty

2. **gRPC becomes faster at large scale** (> 8 MB)
   - Binary serialization saves bandwidth
   - HTTP/2 multiplexing helps
   - Efficiency scales with data size

3. **Crossover point: ~6-7 MB**
   - Both protocols perform similarly
   - Choice depends on other factors (tooling, ecosystem, etc.)

### Service-Specific Patterns:

- **Word Count**: XML-RPC advantage persists even at 1M words
- **Sorting**: gRPC wins at 500K+ words (binary arrays are efficient)
- **Word Lengths**: gRPC wins at 500K+ words (numerical data benefits)

---

## 🔬 Advanced Testing

### Custom Data Size
```bash
# Modify generate_large_data.py and add:
create_dataset('custom_250k.txt', 250_000)  # 2.2 MB

python generate_large_data.py
python performance_test_large.py --data data/custom_250k.txt --protocol both
```

### Different Server Counts
```bash
# Modify performance_test_large.py to use 2 servers
python performance_test_large.py --data data/large_50k.txt --protocol both --servers 2

# Or 4 servers (requires starting server-4 in Docker)
python performance_test_large.py --data data/large_50k.txt --protocol both --servers 4
```

---

## 📚 Documentation Files

- `LARGE_DATASET_COMPARISON.md` - Complete analysis with all results
- `XMLRPC_SINGLE_VS_MULTI_COMPARISON.md` - XML-RPC configuration comparison
- `SINGLE_VS_MULTIPLE_COMPARISON.md` - gRPC configuration comparison
- `GRPC_TEXT_SERVICES.md` - gRPC service documentation
- `README.md` - Project overview

---

## 🐛 Troubleshooting

### Servers Not Starting
```bash
docker-compose down
docker-compose up -d grpc-server-1 grpc-server-2 grpc-server-3 xmlrpc-server-1 xmlrpc-server-2 xmlrpc-server-3
sleep 3  # Wait for servers to initialize
```

### Port Conflicts
```bash
# Check what's using ports
netstat -ano | findstr "50051"  # gRPC
netstat -ano | findstr "8000"   # XML-RPC

# Kill process if needed
taskkill /PID <process_id> /F
```

### Performance Test Fails
```bash
# Make sure servers are running
docker-compose ps

# Check server health
docker-compose logs grpc-server-1
docker-compose logs xmlrpc-server-1

# Rebuild if needed
docker-compose build
```

---

## ⚡ One-Command Full Test Suite

Run all tests sequentially:

```bash
python generate_large_data.py && python performance_test_large.py --data data/small_1k.txt --protocol both && python performance_test_large.py --data data/medium_10k.txt --protocol both && python performance_test_large.py --data data/large_50k.txt --protocol both && python performance_test_large.py --data data/xlarge_100k.txt --protocol both && python performance_test_large.py --data data/xxlarge_500k.txt --protocol both && python performance_test_large.py --data data/huge_1m.txt --protocol both
```

PowerShell version:
```powershell
python generate_large_data.py ; python performance_test_large.py --data data/small_1k.txt --protocol both ; python performance_test_large.py --data data/medium_10k.txt --protocol both ; python performance_test_large.py --data data/large_50k.txt --protocol both ; python performance_test_large.py --data data/xlarge_100k.txt --protocol both ; python performance_test_large.py --data data/xxlarge_500k.txt --protocol both ; python performance_test_large.py --data data/huge_1m.txt --protocol both
```
