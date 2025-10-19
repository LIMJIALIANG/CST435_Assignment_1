# Architecture Diagrams

## Overall System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    Performance Test Script                       │
│                  (performance_test.py)                           │
└────────┬────────────┬────────────┬─────────────┬────────────────┘
         │            │            │             │
         │            │            │             │
    ┌────▼────┐  ┌───▼────┐  ┌────▼────┐  ┌────▼─────┐
    │  gRPC   │  │XML-RPC │  │   MPI   │  │Multi-    │
    │  Test   │  │  Test  │  │  Test   │  │processing│
    └────┬────┘  └───┬────┘  └────┬────┘  └────┬─────┘
         │            │            │             │
         ▼            ▼            ▼             ▼
    Performance   Performance Performance  Performance
      Metrics       Metrics      Metrics      Metrics
         │            │            │             │
         └────────────┴────────────┴─────────────┘
                           │
                           ▼
              ┌────────────────────────┐
              │  Results & Comparison  │
              │  - JSON, CSV, Charts   │
              └────────────────────────┘
```

---

## 1. gRPC Implementation

```
┌──────────────────────────────────────────────────────────────┐
│                      gRPC Client                              │
│  (grpc_implementation/client.py)                             │
└─────┬─────────────┬─────────────┬──────────────────────────┘
      │             │             │
      │ gRPC Call   │ gRPC Call   │ gRPC Call
      ▼             ▼             ▼
┌──────────┐  ┌──────────┐  ┌──────────┐
│ gRPC     │  │ gRPC     │  │ gRPC     │
│ Server 1 │  │ Server 2 │  │ Server 3 │
│ :50051   │  │ :50052   │  │ :50053   │
└────┬─────┘  └────┬─────┘  └────┬─────┘
     │             │             │
     │ Map()       │ Map()       │ Map()
     ▼             ▼             ▼
  Word Count   Word Count   Word Count
  (Chunk 1)    (Chunk 2)    (Chunk 3)
     │             │             │
     └─────────────┴─────────────┘
                   │
                   ▼
            Reduce (Server 1)
                   │
                   ▼
            Final Word Counts
```

**Data Flow:**
1. Client reads text file
2. Splits into 3 chunks
3. Sends each chunk to a different server via gRPC
4. Each server performs Map (word count)
5. Client collects results
6. Client sends to Server 1 for Reduce
7. Final aggregated counts returned

**Protocol Buffers:**
```protobuf
service MapReduceService {
    rpc Map(MapRequest) returns (MapResponse);
    rpc Reduce(ReduceRequest) returns (ReduceResponse);
}
```

---

## 2. XML-RPC Implementation

```
┌──────────────────────────────────────────────────────────────┐
│                    XML-RPC Client                             │
│  (xmlrpc_implementation/client.py)                           │
└─────┬─────────────┬─────────────┬──────────────────────────┘
      │             │             │
      │ XML-RPC     │ XML-RPC     │ XML-RPC
      ▼             ▼             ▼
┌──────────┐  ┌──────────┐  ┌──────────┐
│ XML-RPC  │  │ XML-RPC  │  │ XML-RPC  │
│ Server 1 │  │ Server 2 │  │ Server 3 │
│ :8000    │  │ :8001    │  │ :8002    │
└────┬─────┘  └────┬─────┘  └────┬─────┘
     │             │             │
     │map_operation│map_operation│map_operation
     ▼             ▼             ▼
  Word Count   Word Count   Word Count
     │             │             │
     └─────────────┴─────────────┘
                   │
                   ▼
        reduce_operation (Server 1)
                   │
                   ▼
            Final Word Counts
```

**Protocol:** HTTP/1.1 + XML
**Format:** Text-based (verbose)

---

## 3. MPI Implementation

```
┌────────────────────────────────────────────────────────┐
│              MPI Coordinator (Rank 0)                  │
│  (mpi_implementation/mapreduce.py)                    │
└───┬──────────────┬──────────────┬────────────────────┘
    │              │              │
    │ Scatter      │ Scatter      │ Scatter
    │ Chunk 1      │ Chunk 2      │ Chunk 3
    ▼              ▼              ▼
┌─────────┐    ┌─────────┐    ┌─────────┐
│ MPI     │    │ MPI     │    │ MPI     │
│ Rank 0  │    │ Rank 1  │    │ Rank 2  │
│ (Master)│    │ (Worker)│    │ (Worker)│
└────┬────┘    └────┬────┘    └────┬────┘
     │              │              │
     │ map_function │ map_function │ map_function
     ▼              ▼              ▼
  Count Words   Count Words   Count Words
     │              │              │
     │    Gather    │    Gather    │
     └──────────────┴──────────────┘
                    │
                    ▼
              ┌─────────┐
              │ Rank 0  │
              │ Reduce  │
              └────┬────┘
                   ▼
            Final Word Counts
```

**Communication:** Point-to-point and collective
**Topology:** Master-Worker pattern

**MPI Operations Used:**
- `scatter()` - Distribute chunks
- `gather()` - Collect results
- `Get_rank()` - Process identification
- `Get_size()` - Total processes

---

## 4. Python Multiprocessing Implementation

```
┌────────────────────────────────────────────────────────┐
│           Main Process (Master)                        │
│  (multiprocessing_implementation/mapreduce.py)        │
└───┬──────────────┬──────────────┬────────────────────┘
    │              │              │
    │              │              │
    │ Pool.map()   │              │
    ▼              ▼              ▼
┌─────────┐    ┌─────────┐    ┌─────────┐
│ Worker  │    │ Worker  │    │ Worker  │
│ Process │    │ Process │    │ Process │
│    1    │    │    2    │    │    3    │
└────┬────┘    └────┬────┘    └────┬────┘
     │              │              │
     │map_function  │map_function  │map_function
     ▼              ▼              ▼
  Count Words   Count Words   Count Words
     │              │              │
     └──────────────┴──────────────┘
                    │
                    ▼
            ┌───────────────┐
            │ Main Process  │
            │reduce_function│
            └───────┬───────┘
                    ▼
            Final Word Counts
```

**Features:**
- Shared memory space
- Process pool
- No network overhead
- CPU-bound optimization

---

## Docker Container Architecture

### gRPC Setup
```
┌─────────────────────────────────────────────────────┐
│              Docker Network (Bridge)                 │
│                                                      │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐   │
│  │ Container  │  │ Container  │  │ Container  │   │
│  │  gRPC-1    │  │  gRPC-2    │  │  gRPC-3    │   │
│  │            │  │            │  │            │   │
│  │ Server:    │  │ Server:    │  │ Server:    │   │
│  │ Port 50051 │  │ Port 50051 │  │ Port 50051 │   │
│  │            │  │            │  │            │   │
│  │ Host Port: │  │ Host Port: │  │ Host Port: │   │
│  │   50051    │  │   50052    │  │   50053    │   │
│  └────────────┘  └────────────┘  └────────────┘   │
│                                                      │
│  ┌────────────────────────────────────────────┐    │
│  │         Client Container                    │    │
│  │  Connects to: grpc-server-1:50051          │    │
│  │               grpc-server-2:50051          │    │
│  │               grpc-server-3:50051          │    │
│  └────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────┘
```

### XML-RPC Setup
```
┌─────────────────────────────────────────────────────┐
│              Docker Network (Bridge)                 │
│                                                      │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐   │
│  │ Container  │  │ Container  │  │ Container  │   │
│  │ XMLRPC-1   │  │ XMLRPC-2   │  │ XMLRPC-3   │   │
│  │            │  │            │  │            │   │
│  │ Port 8000  │  │ Port 8000  │  │ Port 8000  │   │
│  │ Host:8000  │  │ Host:8001  │  │ Host:8002  │   │
│  └────────────┘  └────────────┘  └────────────┘   │
└─────────────────────────────────────────────────────┘
```

---

## Performance Testing Flow

```
                    START
                      │
                      ▼
            ┌─────────────────┐
            │  Load Test Data │
            └────────┬────────┘
                     │
        ┌────────────┼────────────┐
        │            │            │
        ▼            ▼            ▼
    ┌───────┐   ┌───────┐   ┌───────┐
    │ Test  │   │ Test  │   │ Test  │ ...
    │  #1   │   │  #2   │   │  #3   │
    └───┬───┘   └───┬───┘   └───┬───┘
        │           │           │
        └───────────┴───────────┘
                    │
                    ▼
        ┌───────────────────────┐
        │  Collect Metrics:     │
        │  - Execution time     │
        │  - Map duration       │
        │  - Reduce duration    │
        │  - Throughput         │
        └───────────┬───────────┘
                    │
                    ▼
        ┌───────────────────────┐
        │  Statistical Analysis │
        │  - Mean               │
        │  - Min/Max            │
        │  - Std Dev            │
        └───────────┬───────────┘
                    │
        ┌───────────┴───────────┐
        │                       │
        ▼                       ▼
  ┌──────────┐          ┌──────────┐
  │   JSON   │          │   CSV    │
  │  Export  │          │  Export  │
  └──────────┘          └──────────┘
        │                       │
        └───────────┬───────────┘
                    ▼
          ┌─────────────────┐
          │  Generate Chart │
          └────────┬────────┘
                   │
                   ▼
               COMPLETE
```

---

## MapReduce Data Flow

```
INPUT TEXT FILE
      │
      ▼
┌─────────────┐
│   SPLIT     │  Split into N chunks
└──────┬──────┘  (N = number of workers)
       │
   ┌───┴───┬───────┬───────┐
   │       │       │       │
   ▼       ▼       ▼       ▼
Chunk1  Chunk2  Chunk3  ...
   │       │       │       │
   │ MAP   │ MAP   │ MAP   │
   ▼       ▼       ▼       ▼
{the:3}  {is:2}  {and:4}  ...
{fox:1}  {a:1}   {the:2}
   │       │       │       │
   └───────┴───┬───┴───────┘
               │
          SHUFFLE/COMBINE
               │
               ▼
        ┌──────────────┐
        │    REDUCE    │
        │  Aggregate   │
        │  all counts  │
        └──────┬───────┘
               │
               ▼
      FINAL WORD COUNTS
      {the: 15, is: 10,
       and: 8, fox: 3, ...}
```

---

## Comparison Matrix

```
┌──────────────┬─────────┬─────────┬─────────┬──────────────┐
│ Feature      │  gRPC   │XML-RPC  │   MPI   │Multi-        │
│              │         │         │         │processing    │
├──────────────┼─────────┼─────────┼─────────┼──────────────┤
│ Protocol     │ HTTP/2  │ HTTP/1.1│ Custom  │ Local (IPC)  │
├──────────────┼─────────┼─────────┼─────────┼──────────────┤
│ Serialization│ ProtoBuf│   XML   │  Binary │ Pickle       │
├──────────────┼─────────┼─────────┼─────────┼──────────────┤
│ Speed        │  Fast   │  Slow   │Very Fast│ Fastest      │
├──────────────┼─────────┼─────────┼─────────┼──────────────┤
│ Network      │   Yes   │   Yes   │   Yes*  │    No        │
├──────────────┼─────────┼─────────┼─────────┼──────────────┤
│ Containers   │    3    │    3    │    1    │     1        │
├──────────────┼─────────┼─────────┼─────────┼──────────────┤
│ Processes    │    3    │    3    │    3    │     3        │
├──────────────┼─────────┼─────────┼─────────┼──────────────┤
│ Overhead     │ Medium  │  High   │   Low   │   Minimal    │
├──────────────┼─────────┼─────────┼─────────┼──────────────┤
│ Use Case     │Microserv│ Legacy  │   HPC   │ Local Comp.  │
└──────────────┴─────────┴─────────┴─────────┴──────────────┘

* Can work across network but optimized for shared memory
```

---

## Timeline / Sequence Diagram

### gRPC Request Flow
```
Client          Server1         Server2         Server3
  │                │               │               │
  │─── Map(C1) ───>│               │               │
  │                │─ Process ─>   │               │
  │<── Result1 ────│               │               │
  │                                │               │
  │─────── Map(C2) ────────────────>│              │
  │                                │─ Process ─>   │
  │<────── Result2 ─────────────────│              │
  │                                                 │
  │────────── Map(C3) ──────────────────────────────>
  │                                                 │─ Process ─>
  │<───────── Result3 ──────────────────────────────│
  │                │               │               │
  │── Reduce() ───>│               │               │
  │                │─ Aggregate >  │               │
  │<── Final ──────│               │               │
  │                │               │               │
```

---

## Summary

This architecture provides:
- ✅ Distributed processing across containers
- ✅ Multiple implementation approaches
- ✅ Performance comparison capability
- ✅ Scalable design
- ✅ Docker-based deployment
- ✅ Automated testing framework

Each implementation demonstrates different trade-offs:
- **gRPC**: Best for modern microservices
- **XML-RPC**: Good for simple, compatible systems
- **MPI**: Optimal for HPC and scientific computing
- **Multiprocessing**: Best for local, CPU-intensive tasks
