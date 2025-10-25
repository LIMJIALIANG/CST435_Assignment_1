"""
XML-RPC Multi-Service Client
Tests 3 different distributed services:
1. Word Count (MapReduce)
2. Alphabetical Sorting (Merge Sort)
3. Word Length Analysis
"""
import xmlrpc.client
import time
import os
from collections import Counter
import heapq


class MultiServiceClient:
    """Client for distributed text-processing using XML-RPC"""
    
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
        print("\n" + "="*60)
        print("HEALTH CHECK")
        print("="*60)
        for i, proxy in enumerate(self.proxies):
            try:
                response = proxy.health_check()
                print(f"✓ Server {i+1}: {response['message']}")
            except Exception as e:
                print(f"✗ Server {i+1}: UNHEALTHY - {e}")
                return False
        return True
    
    # SERVICE 1: Word Count
    def test_word_count(self, text):
        """
        Execute MapReduce word count on the given text
        """
        print("\n" + "="*60)
        print("SERVICE 1: WORD COUNT (MapReduce)")
        print("="*60)
        
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
        
        # Reduce phase - aggregate results
        reduce_start = time.time()
        
        # Combine all map results
        combined_counts = Counter()
        for counts in map_results:
            combined_counts.update(counts)
        
        # Send to first server for final reduction
        reduce_response = self.proxies[0].reduce_operation(dict(combined_counts))
        
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
        Test alphabetical word sorting service across multiple servers
        """
        print("\n" + "="*60)
        print("SERVICE 2: ALPHABETICAL WORD SORTING (Merge Sort)")
        print("="*60)
        
        start_time = time.time()
        
        # Split text into chunks
        chunks = self._split_text(text, len(self.proxies))
        
        print(f"Sorting words from text distributed across {len(self.proxies)} servers")
        
        # Send chunks to servers for sorting
        sorted_chunks = []
        for i, (chunk, proxy) in enumerate(zip(chunks, self.proxies)):
            try:
                response = proxy.sort_words(chunk, i)
                sorted_chunks.append(response['sorted_words'])
            except Exception as e:
                print(f"Sort error on server {i+1}: {e}")
                raise
        
        # Merge sorted chunks (final merge)
        final_sorted = self._merge_sorted_string_lists(sorted_chunks)
        
        duration = time.time() - start_time
        
        # Display results
        print(f"Total Duration: {duration:.4f}s")
        print(f"Unique words sorted: {len(final_sorted)}")
        print(f"First 20 words (alphabetically):")
        for word in final_sorted[:20]:
            print(f"  {word}")
        if len(final_sorted) > 20:
            print(f"Last 10 words:")
            for word in final_sorted[-10:]:
                print(f"  {word}")
        
        return duration
    
    # SERVICE 3: Word Length Analysis
    def test_word_lengths(self, text):
        """
        Test word length analysis service across multiple servers
        """
        print("\n" + "="*60)
        print("SERVICE 3: WORD LENGTH ANALYSIS")
        print("="*60)
        print(f"Analyzing word lengths distributed across {len(self.proxies)} servers")
        
        start_time = time.time()
        
        # Split text into chunks
        chunks = self._split_text(text, len(self.proxies))
        
        # Send to servers for analysis
        all_distributions = Counter()
        total_avg = 0
        min_length = float('inf')
        max_length = 0
        
        for i, (chunk, proxy) in enumerate(zip(chunks, self.proxies)):
            try:
                response = proxy.analyze_word_lengths(chunk, i)
                
                # Aggregate results (convert list of pairs back to dict)
                for length, count in response['length_distribution']:
                    all_distributions[length] += count
                total_avg += response['average_length']
                min_length = min(min_length, response['min_length'])
                max_length = max(max_length, response['max_length'])
            except Exception as e:
                print(f"Analysis error on server {i+1}: {e}")
                raise
        
        avg_length = total_avg / len(self.proxies)
        duration = time.time() - start_time
        
        # Display results
        print(f"Total Duration: {duration:.4f}s")
        print(f"\nWord Length Statistics:")
        print(f"  Average Length: {avg_length:.2f} characters")
        print(f"  Minimum Length: {min_length} characters")
        print(f"  Maximum Length: {max_length} characters")
        print(f"\nLength Distribution:")
        for length in sorted(all_distributions.keys()):
            count = all_distributions[length]
            bar = '█' * min(50, count)
            print(f"  {length:2d} chars: {count:4d} words {bar}")
        
        return duration
    
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
    
    def _merge_sorted_string_lists(self, sorted_lists):
        """Merge multiple sorted lists of strings into one sorted list"""
        return list(heapq.merge(*sorted_lists))


def main():
    """Test all three services"""
    # Server URLs (modify based on your setup)
    servers = [
        'http://localhost:8000',
        'http://localhost:8001',
        'http://localhost:8002'
    ]
    
    # Override with environment variable if set
    if os.getenv('XMLRPC_SERVERS'):
        servers = os.getenv('XMLRPC_SERVERS').split(',')
    
    client = MultiServiceClient(servers)
    
    # Health check
    if not client.health_check():
        print("\n✗ Some servers are not healthy!")
        return
    
    print("\n" + "="*60)
    print("TESTING ALL 3 SERVICES WITH SAMPLE TEXT")
    print("="*60)
    
    # Read input text
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
    print("PERFORMANCE SUMMARY")
    print("="*60)
    print(f"Service 1 (Word Count):         {time1:.4f}s")
    print(f"Service 2 (Alphabetical Sort):  {time2:.4f}s")
    print(f"Service 3 (Word Length Stats):  {time3:.4f}s")
    print(f"Total Time (All Services):      {time1 + time2 + time3:.4f}s")
    print(f"Number of Servers Used:         {len(client.proxies)}")


if __name__ == '__main__':
    main()
