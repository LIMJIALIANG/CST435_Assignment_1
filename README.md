## Files Used
- `docker-compose.grpc-services.yml` – Docker Compose configuration for gRPC services  
- `Dockerfile.grpc.client` – Dockerfile to build the gRPC client  

## Setup and Run (Same Machine)

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

## Setup and Run (Different Machine)

### 1. Download Oracle VM and also the 
Orcale VM: https://www.virtualbox.org/wiki/Downloads (Window Host)
Ubuntu: https://ubuntu.com/download/server 

### 2. Open the downloaded VM and insert the downloaded Ubuntu .iso file into the part of ISO image


### 3. Configuration of the machine: 
- CPU: 2
- GB: 2
- The rest as default

### 4. Configuration of the machine's network
- Click the Settings button (the gear icon).
- Go to the Network section.
- On the Adapter 1 tab, change the "Attached to:" dropdown menu from NAT to Bridged Adapter.
- Click OK.


### 5. Create the machine (wait for around 5 minutes)

### 6. After finish, run this command to download related dependency
```bash
# Update package lists
sudo apt update

# Install Docker, Git, and SSH Server
sudo apt install docker.io docker-compose git openssh-server
```

### 7. Git clone... then git switch 

### 8. Go to the docker, run the docker-compose

```bash
docker-compose -f docker-compose.grpc-services.yml up -d
```

### 9. Go to the local VS code terminal, and run the Dockerfile.grpc.client
- change this:

// Set the default environment variables
// Test it locally
// ENV SERVICE_A_ADDRESS=docker-grpc-service-a:50051
// Test it in different machine, use "ip a" to find the dynamic IP address in the terminal of VM
ENV SERVICE_A_ADDRESS=192.168.0.161:50051

