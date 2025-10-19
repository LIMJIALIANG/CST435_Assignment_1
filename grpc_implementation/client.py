"""
gRPC MapReduce Client
Distributes work across multiple gRPC servers
"""
import grpc
import time
import sys
import os
from collections import Counter

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import mapreduce_pb2
import mapreduce_pb2_grpc


class MapReduceClient:
    """Client for distributed MapReduce using gRPC"""
    
    def __init__(self, server_addresses):
        """
        Initialize client with list of server addresses
        Args:
            server_addresses: List of 'host:port' strings
        """
        self.server_addresses = server_addresses
        self.channels = []
        self.stubs = []
        
        # Create channels and stubs for each server
        for address in server_addresses:
            channel = grpc.insecure_channel(address)
            stub = mapreduce_pb2_grpc.MapReduceServiceStub(channel)
            self.channels.append(channel)
            self.stubs.append(stub)
        
        print(f"Connected to {len(self.stubs)} gRPC servers")
    
    def health_check(self):
        """Check if all servers are healthy"""
        for i, stub in enumerate(self.stubs):
            try:
                response = stub.HealthCheck(
                    mapreduce_pb2.HealthCheckRequest(service_name="MapReduce")
                )
                print(f"Server {i+1}: {response.message}")
            except grpc.RpcError as e:
                print(f"Server {i+1}: UNHEALTHY - {e}")
                return False
        return True
    
    def map_reduce(self, text):
        """
        Execute MapReduce on the given text
        """
        start_time = time.time()
        
        # Split text into chunks (one per server)
        chunks = self._split_text(text, len(self.stubs))
        
        # Map phase - distribute to servers
        map_start = time.time()
        map_results = []
        
        for i, (chunk, stub) in enumerate(zip(chunks, self.stubs)):
            try:
                request = mapreduce_pb2.MapRequest(
                    text_chunk=chunk,
                    chunk_id=i
                )
                response = stub.Map(request)
                map_results.append(response.word_counts)
            except grpc.RpcError as e:
                print(f"Map error on server {i+1}: {e}")
                raise
        
        map_duration = time.time() - map_start
        print(f"Map phase completed in {map_duration:.4f}s")
        
        # Reduce phase - aggregate results
        reduce_start = time.time()
        
        # Combine all map results
        combined_counts = Counter()
        for counts in map_results:
            combined_counts.update(counts)
        
        # Send to first server for final reduction
        reduce_request = mapreduce_pb2.ReduceRequest(
            intermediate_counts=dict(combined_counts)
        )
        reduce_response = self.stubs[0].Reduce(reduce_request)
        
        reduce_duration = time.time() - reduce_start
        print(f"Reduce phase completed in {reduce_duration:.4f}s")
        
        total_duration = time.time() - start_time
        
        return {
            'word_counts': dict(reduce_response.final_counts),
            'total_duration': total_duration,
            'map_duration': map_duration,
            'reduce_duration': reduce_duration,
            'num_servers': len(self.stubs)
        }
    
    def _split_text(self, text, num_chunks):
        """Split text into roughly equal chunks"""
        lines = text.strip().split('\n')
        chunk_size = max(1, len(lines) // num_chunks)
        
        chunks = []
        for i in range(num_chunks):
            start = i * chunk_size
            end = start + chunk_size if i < num_chunks - 1 else len(lines)
            chunk = '\n'.join(lines[start:end])
            chunks.append(chunk)
        
        return chunks
    
    def close(self):
        """Close all gRPC channels"""
        for channel in self.channels:
            channel.close()


def main():
    """Test the gRPC MapReduce client"""
    # Server addresses (modify based on your setup)
    servers = [
        'localhost:50051',
        'localhost:50052',
        'localhost:50053'
    ]
    
    # Override with environment variable if set
    if os.getenv('GRPC_SERVERS'):
        servers = os.getenv('GRPC_SERVERS').split(',')
    
    client = MapReduceClient(servers)
    
    # Health check
    if not client.health_check():
        print("Some servers are not healthy!")
        return
    
    # Read input text
    data_file = os.path.join(os.path.dirname(__file__), '..', 'data', 'sample_text.txt')
    with open(data_file, 'r') as f:
        text = f.read()
    
    print(f"\nProcessing text with {len(text)} characters...")
    
    # Execute MapReduce
    result = client.map_reduce(text)
    
    # Display results
    print(f"\n{'='*60}")
    print("RESULTS:")
    print(f"{'='*60}")
    print(f"Total Duration: {result['total_duration']:.4f}s")
    print(f"Map Duration: {result['map_duration']:.4f}s")
    print(f"Reduce Duration: {result['reduce_duration']:.4f}s")
    print(f"Number of Servers: {result['num_servers']}")
    print(f"\nTop 10 Words:")
    
    sorted_words = sorted(result['word_counts'].items(), key=lambda x: x[1], reverse=True)
    for word, count in sorted_words[:10]:
        print(f"  {word}: {count}")
    
    client.close()


if __name__ == '__main__':
    main()
