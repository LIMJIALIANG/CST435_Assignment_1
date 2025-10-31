## Files Used
- `docker-compose.grpc-services.yml` – Docker Compose configuration for gRPC services  
- `Dockerfile.grpc.client` – Dockerfile to build the gRPC client  

## Setup and Run

### 1. Start gRPC Services
Open a terminal and run:

```bash
docker-compose -f docker-compose.grpc-services.yml up --build

### 2. Start client 
Open another terminal and run:
- Build the client image:
```bash
docker build -t grpc-client-image -f Dockerfile.grpc.client ..
```
- Run the client container:
```bash 
docker run -d --network=docker_grpc-network --name my-grpc-client grpc-client-image
```

