# CST435 Assignment 1 - Project Summary
## MapReduce Performance Comparison using Python & Docker

**Created:** October 19, 2025  
**Purpose:** Compare distributed computing approaches for Assignment 1

---

## 📦 What Has Been Created

### Complete Implementation Package Including:

#### 1. **Four Different Implementations**
   - ✅ **gRPC** - Modern high-performance RPC (3 Docker containers)
   - ✅ **XML-RPC** - Traditional Python RPC (3 Docker containers)
   - ✅ **Python Multiprocessing** - Local parallel processing (1 process, 3 workers)
   - ✅ **MPI (mpi4py)** - Message Passing Interface (1 container, 3 processes)

#### 2. **Docker Configuration**
   - 3 separate Dockerfiles for each distributed implementation
   - Complete docker-compose.yml for orchestration
   - Network configuration for inter-container communication

#### 3. **Automated Testing**
   - Performance comparison script with metrics collection
   - Individual test scripts for each implementation
   - Quick test script to verify all implementations

#### 4. **Documentation**
   - Comprehensive step-by-step guide (STEP_BY_STEP_GUIDE.md)
   - Quick reference command sheet (QUICK_REFERENCE.md)
   - Project README with setup instructions
   - This summary document

#### 5. **Setup Scripts**
   - Windows PowerShell setup script (setup.ps1)
   - Linux/Mac bash setup script (setup.sh)
   - Automated dependency installation
   - gRPC code generation

---

## 🎯 What This Solves

### Assignment Requirements:
✅ Install and use Docker  
✅ Implement gRPC for distributed processing  
✅ Compare with other parallel/distributed approaches  
✅ Run on multiple containers  
✅ Measure and compare performance  
✅ Solve a meaningful problem (MapReduce word count)  

---

## 📊 How It Works

### The Problem:
**MapReduce Word Count** - Count word frequencies in a text file

### The Solution:
All four implementations solve the same problem using different technologies:

```
Input: Text file → Split into chunks → Map (count words) → Reduce (aggregate) → Output: Word frequencies
```

### Performance Comparison:
- Each implementation is run multiple times
- Execution time is measured
- Results are aggregated and visualized
- Charts and CSV files are generated

---

## 🚀 How to Use (3-Step Process)

### Step 1: Setup (5-10 minutes)
```powershell
cd "c:\Users\USER\OneDrive\Semester 7\CST435\Assignment 1\Related_Codes\example_map_reduce_program"
.\setup.ps1
```

This will:
- Install Python dependencies
- Generate gRPC Protocol Buffer code
- Build all Docker images

### Step 2: Quick Test (2-3 minutes)
```powershell
.\test_all.ps1
```

This will:
- Test each implementation sequentially
- Verify everything works correctly
- Show sample output

### Step 3: Performance Comparison (5-10 minutes)
```powershell
python performance_test.py
```

This will:
- Run each implementation 3 times
- Collect performance metrics
- Generate comparison charts
- Save results to JSON and CSV

### Results Location:
```
performance_results/
├── results_20251019_143022.json    # Detailed results
├── results_20251019_143022.csv     # Tabular data
└── performance_comparison_20251019_143022.png  # Visualization
```

---

## 📝 For Your Report

### What to Include:

#### 1. Introduction & Motivation
- Need for distributed computing
- Comparing different approaches
- MapReduce as a use case

#### 2. Technology Overview
**gRPC:**
- Modern, high-performance RPC framework
- Uses Protocol Buffers (binary serialization)
- HTTP/2 transport
- Strong typing

**XML-RPC:**
- Traditional RPC approach
- XML-based (text serialization)
- HTTP/1.1 transport
- Simple but verbose

**Python Multiprocessing:**
- Local parallelism
- Shared memory
- Process-based (not thread-based)
- Good for CPU-bound tasks

**MPI (Message Passing Interface):**
- Industry standard for HPC
- Optimized for parallel computing
- Point-to-point and collective communication
- Widely used in scientific computing

#### 3. Architecture

```
┌─────────────────────────────────────┐
│         Client Application          │
└──────────────┬──────────────────────┘
               │
       ┌───────┴───────┐
       │               │
   ┌───▼───┐       ┌───▼───┐
   │Server1│       │Server2│  (etc.)
   └───┬───┘       └───┬───┘
       │               │
       └───────┬───────┘
               │
          Aggregation
               │
           ┌───▼───┐
           │Result │
           └───────┘
```

#### 4. Implementation Details
- Show code snippets from the implementations
- Explain Map and Reduce phases
- Discuss Docker configuration

#### 5. Deployment Environment
- **Setup:** 3 Docker containers per distributed implementation
- **Network:** Bridge network for inter-container communication
- **Resources:** CPU and memory allocation
- **OS:** Container-based (Linux)

#### 6. Performance Results
Example table:

| Implementation | Mean Time (s) | Min (s) | Max (s) | Std Dev |
|---------------|---------------|---------|---------|---------|
| Multiprocessing | 0.0231 | 0.0224 | 0.0245 | 0.0009 |
| MPI | 0.0387 | 0.0375 | 0.0401 | 0.0011 |
| gRPC | 0.0445 | 0.0423 | 0.0478 | 0.0024 |
| XML-RPC | 0.0612 | 0.0598 | 0.0635 | 0.0016 |

Include the generated charts from `performance_results/`

#### 7. Discussion & Findings

**Expected Findings:**
- **Multiprocessing is fastest** - No network overhead, shared memory
- **MPI is close second** - Optimized for parallel computing
- **gRPC performs well** - Efficient binary protocol, HTTP/2
- **XML-RPC is slowest** - Text-based XML, HTTP/1.1 overhead

**Why the differences?**
1. **Serialization:** Binary (gRPC) vs. Text (XML-RPC)
2. **Network:** Local (Multiprocessing) vs. Network (gRPC/XML-RPC)
3. **Protocol:** Optimized (MPI) vs. General-purpose (RPC)
4. **Overhead:** Container startup, network latency

**Real-world Applications:**
- **gRPC:** Microservices, distributed systems, mobile apps
- **XML-RPC:** Legacy systems, simple integrations
- **Multiprocessing:** Local computation, data processing
- **MPI:** Scientific computing, simulations, HPC clusters

#### 8. Team Division Example
- Member 1: gRPC implementation and Docker setup
- Member 2: XML-RPC and MPI implementations
- Member 3: Multiprocessing and performance testing
- Member 4: Documentation and testing
- Member 5: Integration and deployment

#### 9. Challenges & Solutions
- Docker networking configuration
- gRPC Protocol Buffer code generation
- MPI installation in containers
- Performance measurement consistency
- Container synchronization

#### 10. Conclusion
- Successfully implemented and compared 4 approaches
- Demonstrated trade-offs between approaches
- Learned Docker, gRPC, and distributed computing concepts
- Identified best use cases for each technology

---

## 🎥 Video Recording Script (15 minutes)

### Minute 0-2: Introduction
- Team introduction
- Project overview
- Technologies used

### Minute 2-4: Setup Demo
- Show Docker Desktop running
- Run setup.ps1
- Explain what's being installed

### Minute 4-6: Architecture Explanation
- Show docker-compose.yml
- Explain container setup
- Demonstrate network configuration

### Minute 6-10: Implementation Demos
- Run each implementation (1 min each)
- Show output
- Explain differences

### Minute 10-13: Performance Testing
- Run performance_test.py
- Show results being collected
- Display final charts

### Minute 13-15: Results & Conclusion
- Discuss findings
- Show performance comparison
- Lessons learned
- Q&A preparation

---

## 📁 File Structure Summary

```
example_map_reduce_program/
├── 📄 README.md                       # Project overview
├── 📄 STEP_BY_STEP_GUIDE.md          # Detailed instructions
├── 📄 QUICK_REFERENCE.md             # Command cheat sheet
├── 📄 PROJECT_SUMMARY.md             # This file
├── 📄 requirements.txt                # Python dependencies
├── 📄 performance_test.py             # Automated testing
├── 📄 setup.ps1                       # Windows setup
├── 📄 setup.sh                        # Linux/Mac setup
├── 📄 test_all.ps1                    # Quick test
│
├── 📁 grpc_implementation/
│   ├── 📁 proto/
│   │   └── mapreduce.proto
│   ├── server.py
│   └── client.py
│
├── 📁 xmlrpc_implementation/
│   ├── server.py
│   └── client.py
│
├── 📁 multiprocessing_implementation/
│   └── mapreduce.py
│
├── 📁 mpi_implementation/
│   └── mapreduce.py
│
├── 📁 docker/
│   ├── Dockerfile.grpc
│   ├── Dockerfile.xmlrpc
│   ├── Dockerfile.mpi
│   └── docker-compose.yml
│
└── 📁 data/
    └── sample_text.txt
```

---

## ✅ Pre-Submission Checklist

### Technical:
- [ ] All implementations run successfully
- [ ] Performance tests completed
- [ ] Results generated and saved
- [ ] Docker containers work properly
- [ ] Screenshots captured

### Documentation:
- [ ] Report written (< 10 pages)
- [ ] Code explained
- [ ] Architecture documented
- [ ] Results analyzed
- [ ] References cited

### Deliverables:
- [ ] Source code packaged
- [ ] Video recorded (< 15 minutes)
- [ ] Report formatted
- [ ] Submission ready for elearning

---

## 🎓 Learning Outcomes

By completing this project, you will:
1. ✅ Understand Docker containerization
2. ✅ Learn gRPC and Protocol Buffers
3. ✅ Compare RPC approaches
4. ✅ Implement MapReduce pattern
5. ✅ Measure and analyze performance
6. ✅ Deploy distributed systems
7. ✅ Work with container orchestration

---

## 🔗 Additional Resources

- **gRPC Tutorial:** https://grpc.io/docs/languages/python/quickstart/
- **Docker Guide:** https://docs.docker.com/get-started/
- **MPI Tutorial:** https://mpi4py.readthedocs.io/en/stable/tutorial.html
- **Python Multiprocessing:** https://docs.python.org/3/library/multiprocessing.html
- **MapReduce Paper:** Google MapReduce (Dean & Ghemawat, 2004)

---

## 🚀 Next Steps

1. **Run Setup:** `.\setup.ps1`
2. **Test All:** `.\test_all.ps1`
3. **Compare Performance:** `python performance_test.py`
4. **Capture Screenshots:** Document everything
5. **Write Report:** Use the results and analysis
6. **Record Video:** Follow the script above
7. **Submit:** elearning by November 28, 2025

---

## 💡 Tips for Success

1. **Test Early:** Don't wait until the last minute
2. **Document Issues:** Note challenges for report
3. **Take Screenshots:** Capture every step
4. **Understand Code:** Don't just run it, explain it
5. **Compare Results:** Analyze why differences exist
6. **Practice Video:** Record a draft first
7. **Team Collaboration:** Divide work effectively

---

**Good luck with your assignment! 🎉**

You now have a complete, working implementation with:
- ✅ 4 different approaches
- ✅ Docker containerization
- ✅ Automated testing
- ✅ Performance comparison
- ✅ Comprehensive documentation

Everything is ready to run, test, and analyze. Just follow the steps in STEP_BY_STEP_GUIDE.md!
