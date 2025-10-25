"""
XML-RPC Multi-Service Client - Single Server Version
Tests all 3 services using only ONE server (no distribution)
"""
import xmlrpc.client
import time
import os
from collections import Counter


class SingleServerClient:
    """Client for testing all 3 services on a single XML-RPC server"""
    
    def __init__(self, server_url):
        """
        Initialize client with single server URL
        Args:
            server_url: 'http://host:port' string
        """
        self.server_url = server_url
        self.proxy = xmlrpc.client.ServerProxy(server_url, allow_none=True)
        
        print(f"Connected to XML-RPC server at {server_url}")
    
    def health_check(self):
        """Check if server is healthy"""
        print("\n" + "="*60)
        print("HEALTH CHECK")
        print("="*60)
        try:
            response = self.proxy.health_check()
            print(f"✓ Server: {response['message']}")
            return True
        except Exception as e:
            print(f"✗ Server: UNHEALTHY - {e}")
            return False
    
    # SERVICE 1: Word Count
    def test_word_count(self, text):
        """
        Test word count service on single server
        """
        print("\n" + "="*60)
        print("SERVICE 1: WORD COUNT (MapReduce)")
        print("="*60)
        
        start_time = time.time()
        
        # Map phase - send entire text to one server
        map_start = time.time()
        response = self.proxy.map_operation(text, 0)
        map_duration = time.time() - map_start
        
        # Reduce phase
        reduce_start = time.time()
        reduce_response = self.proxy.reduce_operation(response['word_counts'])
        reduce_duration = time.time() - reduce_start
        
        total_duration = time.time() - start_time
        
        # Display results
        print(f"Total Duration: {total_duration:.4f}s")
        print(f"Map Duration: {map_duration:.4f}s")
        print(f"Reduce Duration: {reduce_duration:.4f}s")
        print(f"\nTop 10 Words:")
        sorted_words = sorted(reduce_response['final_counts'].items(), 
                            key=lambda x: x[1], reverse=True)
        for word, count in sorted_words[:10]:
            print(f"  {word}: {count}")
        
        return total_duration
    
    # SERVICE 2: Alphabetical Word Sorting
    def test_sorting(self, text):
        """
        Test alphabetical word sorting service on single server
        """
        print("\n" + "="*60)
        print("SERVICE 2: ALPHABETICAL WORD SORTING (Merge Sort)")
        print("="*60)
        
        start_time = time.time()
        
        # Send entire text to one server
        response = self.proxy.sort_words(text, 0)
        
        duration = time.time() - start_time
        
        sorted_words = response['sorted_words']
        
        # Display results
        print(f"Total Duration: {duration:.4f}s")
        print(f"Unique words sorted: {len(sorted_words)}")
        print(f"First 20 words (alphabetically):")
        for word in sorted_words[:20]:
            print(f"  {word}")
        if len(sorted_words) > 20:
            print(f"Last 10 words:")
            for word in sorted_words[-10:]:
                print(f"  {word}")
        
        return duration
    
    # SERVICE 3: Word Length Analysis
    def test_word_lengths(self, text):
        """
        Test word length analysis service on single server
        """
        print("\n" + "="*60)
        print("SERVICE 3: WORD LENGTH ANALYSIS")
        print("="*60)
        
        start_time = time.time()
        
        # Send entire text to one server
        response = self.proxy.analyze_word_lengths(text, 0)
        
        duration = time.time() - start_time
        
        # Display results
        print(f"Total Duration: {duration:.4f}s")
        print(f"\nWord Length Statistics:")
        print(f"  Average Length: {response['average_length']:.2f} characters")
        print(f"  Minimum Length: {response['min_length']} characters")
        print(f"  Maximum Length: {response['max_length']} characters")
        print(f"\nLength Distribution:")
        for length, count in response['length_distribution']:
            bar = '█' * min(50, count)
            print(f"  {length:2d} chars: {count:4d} words {bar}")
        
        return duration


def main():
    """Test all three services on single server"""
    # Single server URL
    server = 'http://localhost:8000'
    
    if os.getenv('XMLRPC_SERVERS'):
        # Use first server from environment if available
        servers = os.getenv('XMLRPC_SERVERS').split(',')
        server = servers[0]
    
    client = SingleServerClient(server)
    
    # Health check
    if not client.health_check():
        print("\n✗ Server is not healthy!")
        return
    
    print("\n" + "="*60)
    print("TESTING ALL 3 SERVICES WITH SAMPLE TEXT (SINGLE SERVER)")
    print("="*60)
    
    # Load sample text
    data_file = os.path.join(os.path.dirname(__file__), '..', 'data', 'sample_text.txt')
    with open(data_file, 'r') as f:
        text = f.read()
    
    print(f"Text loaded: {len(text)} characters, {len(text.split())} words")
    
    # Test all 3 services with the same text
    time1 = client.test_word_count(text)
    time2 = client.test_sorting(text)
    time3 = client.test_word_lengths(text)
    
    # Summary
    print("\n" + "="*60)
    print("PERFORMANCE SUMMARY (SINGLE SERVER)")
    print("="*60)
    print(f"Service 1 (Word Count):         {time1:.4f}s")
    print(f"Service 2 (Alphabetical Sort):  {time2:.4f}s")
    print(f"Service 3 (Word Length Stats):  {time3:.4f}s")
    print(f"Total Time (All Services):      {time1 + time2 + time3:.4f}s")
    print(f"Number of Servers Used:         1")


if __name__ == '__main__':
    main()
