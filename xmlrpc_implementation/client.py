"""
XML-RPC MapReduce Client
Distributes work across multiple XML-RPC servers
"""
import xmlrpc.client
import time
import os
from collections import Counter


class MapReduceClient:
    """Client for distributed MapReduce using XML-RPC"""
    
    def __init__(self, server_urls):
        """
        Initialize client with list of server URLs
        Args:
            server_urls: List of 'http://host:port' strings
        """
        self.server_urls = server_urls
        self.proxies = []
        
        # Create proxy for each server
        for url in server_urls:
            proxy = xmlrpc.client.ServerProxy(url, allow_none=True)
            self.proxies.append(proxy)
        
        print(f"Connected to {len(self.proxies)} XML-RPC servers")
    
    def health_check(self):
        """Check if all servers are healthy"""
        for i, proxy in enumerate(self.proxies):
            try:
                response = proxy.health_check()
                print(f"Server {i+1}: {response['message']}")
            except Exception as e:
                print(f"Server {i+1}: UNHEALTHY - {e}")
                return False
        return True
    
    def map_reduce(self, text):
        """
        Execute MapReduce on the given text
        """
        start_time = time.time()
        
        # Split text into chunks (one per server)
        chunks = self._split_text(text, len(self.proxies))
        
        # Map phase - distribute to servers
        map_start = time.time()
        map_results = []
        
        for i, (chunk, proxy) in enumerate(zip(chunks, self.proxies)):
            try:
                response = proxy.map_operation(chunk, i)
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
        reduce_response = self.proxies[0].reduce_operation(dict(combined_counts))
        
        reduce_duration = time.time() - reduce_start
        print(f"Reduce phase completed in {reduce_duration:.4f}s")
        
        total_duration = time.time() - start_time
        
        return {
            'word_counts': reduce_response['final_counts'],
            'total_duration': total_duration,
            'map_duration': map_duration,
            'reduce_duration': reduce_duration,
            'num_servers': len(self.proxies)
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


def main():
    """Test the XML-RPC MapReduce client"""
    # Server URLs (modify based on your setup)
    servers = [
        'http://localhost:8000',
        'http://localhost:8001',
        'http://localhost:8002'
    ]
    
    # Override with environment variable if set
    if os.getenv('XMLRPC_SERVERS'):
        servers = os.getenv('XMLRPC_SERVERS').split(',')
    
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


if __name__ == '__main__':
    main()
