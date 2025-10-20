# Quick Reference Card
## MapReduce Performance Comparison - Command Cheat Sheet

---

## 🚀 Setup (One-time)
```powershell
# Windows
.\setup.ps1

# Linux/Mac
chmod +x setup.sh && ./setup.sh
```

---

## 🧪 Quick Test All
```powershell
.\test_all.ps1
```

---

## 🔧 Individual Implementation Commands

### gRPC (3 containers)
```powershell
# Start servers
cd docker
docker-compose up -d grpc-server-1 grpc-server-2 grpc-server-3

# Run client
docker-compose run --rm grpc-client

# Stop
docker-compose down
cd ..
```

### XML-RPC (3 containers)
```powershell
# Start servers
cd docker
docker-compose up -d xmlrpc-server-1 xmlrpc-server-2 xmlrpc-server-3

# Run client
docker-compose run --rm xmlrpc-client

# Stop
docker-compose down
cd ..
```

### MPI (1 container, 3 processes)
```powershell
cd docker
docker-compose run --rm mpi-runner
cd ..
```

### Request-Reply (ZeroMQ) (3 containers)
```powershell
# Start servers
cd docker
docker-compose up -d reqrep-server-1 reqrep-server-2 reqrep-server-3

# Run client
docker-compose run --rm reqrep-client

# Stop
docker-compose down
cd ..
```

---

## 📊 Performance Testing
```powershell
# Run automated comparison
python performance_test.py

# Results saved to:
# - performance_results/results_*.json
# - performance_results/results_*.csv
# - performance_results/performance_comparison_*.png
```

---

## 🐛 Troubleshooting Commands

### View running containers
```powershell
docker ps
```

### View all containers (including stopped)
```powershell
docker ps -a
```

### Stop all containers
```powershell
docker-compose -f docker/docker-compose.yml down
```

### Remove all stopped containers
```powershell
docker container prune
```

### View container logs
```powershell
docker logs grpc-server-1
docker logs xmlrpc-server-1
```

### Rebuild Docker images
```powershell
cd docker
docker-compose build --no-cache
cd ..
```

### Check Python dependencies
```powershell
pip list | findstr grpc
pip list | findstr mpi4py
```

### Regenerate gRPC code
```powershell
cd grpc_implementation
python -m grpc_tools.protoc -I./proto --python_out=. --grpc_python_out=. proto/mapreduce.proto
cd ..
```

---

## 📁 Important Files

| File | Purpose |
|------|---------|
| `setup.ps1` / `setup.sh` | Initial setup |
| `test_all.ps1` | Quick test all implementations |
| `performance_test.py` | Automated performance comparison |
| `docker/docker-compose.yml` | Container orchestration |
| `data/sample_text.txt` | Sample input data |
| `STEP_BY_STEP_GUIDE.md` | Detailed instructions |

---

## 🎯 Typical Workflow

1. **Initial Setup** (once)
   ```powershell
   .\setup.ps1
   ```

2. **Quick Verification**
   ```powershell
   .\test_all.ps1
   ```

3. **Performance Testing**
   ```powershell
   python performance_test.py
   ```

4. **Analyze Results**
   - Check `performance_results/` folder
   - Review charts and CSV files

5. **Write Report**
   - Use screenshots from output
   - Include performance charts
   - Discuss findings

---

## 📈 Expected Performance Order

1. 🥇 **Request-Reply (ZeroMQ)** - Fast (lightweight messaging, binary protocol)
2. 🥈 **MPI** - Fast (optimized message passing)
3. 🥉 **gRPC** - Good (efficient binary protocol)
4. 🏃 **XML-RPC** - Slower (text-based protocol)

---

## ⚠️ Common Issues & Fixes

| Issue | Fix |
|-------|-----|
| Port already in use | `docker-compose down` |
| Docker not running | Start Docker Desktop |
| gRPC code missing | Re-run `setup.ps1` |
| Permission denied | `chmod +x setup.sh` (Linux/Mac) |
| Container won't stop | `docker rm -f <container_name>` |

---

## 📞 Need Help?

1. Check `STEP_BY_STEP_GUIDE.md` for detailed instructions
2. Review `README.md` for project overview
3. Examine logs: `docker logs <container_name>`
4. Verify Docker: `docker --version`
5. Check Python: `python --version`

---

## 🎓 For Your Report

**Performance Metrics to Record:**
- Total execution time
- Map phase duration
- Reduce phase duration
- Number of workers/containers
- Throughput (operations/second)

**Screenshots to Capture:**
- Setup completion
- Each implementation running
- Performance comparison chart
- Docker containers running
- Final results table

**Discussion Points:**
- Why is Request-Reply fast compared to RPC?
- Network overhead impact
- Serialization efficiency
- Scalability considerations
- Real-world applications

---

**Quick Start:** `.\setup.ps1` → `.\test_all.ps1` → `python performance_test.py` ✅
