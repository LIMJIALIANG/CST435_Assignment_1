"""
ZeroMQ Request-Reply MapReduce Client
Distributes work using request-reply pattern
"""
import zmq
import time
import os
from collections import Counter


class MapReduceReqRepClient:
    """Client for distributed MapReduce using Request-Reply pattern"""
    
    def __init__(self, server_addresses):
        """
        Initialize client with list of server addresses
        Args:
            server_addresses: List of 'tcp://host:port' strings
        """
        self.server_addresses = server_addresses
        self.context = zmq.Context()
        self.sockets = []
        
        # Create socket for each server
        for address in server_addresses:
            socket = self.context.socket(zmq.REQ)
            socket.connect(address)
            self.sockets.append(socket)
        
        print(f"Connected to {len(self.sockets)} Request-Reply servers")
    
    def health_check(self):
        """Check if all servers are healthy"""
        all_healthy = True
        for i, socket in enumerate(self.sockets):
            try:
                # Send health check request
                socket.send_json({'operation': 'health_check'})
                
                # Wait for reply
                response = socket.recv_json()
                print(f"Server {i+1}: {response.get('message', 'OK')}")
            except Exception as e:
                print(f"Server {i+1}: UNHEALTHY - {e}")
                all_healthy = False
        
        return all_healthy
    
    def map_reduce(self, text):
        """
        Execute MapReduce on the given text
        """
        start_time = time.time()
        
        # Split text into chunks (one per server)
        chunks = self._split_text(text, len(self.sockets))
        
        # Map phase - send requests to servers
        map_start = time.time()
        map_results = []
        
        for i, (chunk, socket) in enumerate(zip(chunks, self.sockets)):
            try:
                # Send map request
                request = {
                    'operation': 'map',
                    'text_chunk': chunk,
                    'chunk_id': i
                }
                socket.send_json(request)
                
                # Wait for reply
                response = socket.recv_json()
                map_results.append(response['word_counts'])
            except Exception as e:
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
        reduce_request = {
            'operation': 'reduce',
            'intermediate_counts': dict(combined_counts)
        }
        self.sockets[0].send_json(reduce_request)
        reduce_response = self.sockets[0].recv_json()
        
        reduce_duration = time.time() - reduce_start
        print(f"Reduce phase completed in {reduce_duration:.4f}s")
        
        total_duration = time.time() - start_time
        
        return {
            'word_counts': reduce_response['final_counts'],
            'total_duration': total_duration,
            'map_duration': map_duration,
            'reduce_duration': reduce_duration,
            'num_servers': len(self.sockets)
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
        """Close all ZeroMQ sockets"""
        for socket in self.sockets:
            socket.close()
        self.context.term()


def main():
    """Test the Request-Reply MapReduce client"""
    # Server addresses (modify based on your setup)
    servers = [
        'tcp://localhost:5555',
        'tcp://localhost:5556',
        'tcp://localhost:5557'
    ]
    
    # Override with environment variable if set
    if os.getenv('REQREP_SERVERS'):
        servers = os.getenv('REQREP_SERVERS').split(',')
    
    client = MapReduceReqRepClient(servers)
    
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
