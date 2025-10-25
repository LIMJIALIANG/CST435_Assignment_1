"""
gRPC Multi-Service Client
Tests 3 different distributed services:
1. Word Count (MapReduce)
2. Sorting (Merge Sort)
3. Prime Number Detection
"""
import grpc
import time
import sys
import os
from collections import Counter
import random

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import mapreduce_pb2
import mapreduce_pb2_grpc


class MultiServiceClient:
    """Client for testing all 3 distributed services"""
    
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
        print("\n" + "="*60)
        print("HEALTH CHECK")
        print("="*60)
        for i, stub in enumerate(self.stubs):
            try:
                response = stub.HealthCheck(
                    mapreduce_pb2.HealthCheckRequest(service_name="MapReduce")
                )
                print(f"✓ Server {i+1}: {response.message}")
            except grpc.RpcError as e:
                print(f"✗ Server {i+1}: UNHEALTHY - {e}")
                return False
        return True
    
    # SERVICE 1: Word Count
    def test_word_count(self, text):
        """
        Test word count service across multiple servers
        """
        print("\n" + "="*60)
        print("SERVICE 1: WORD COUNT (MapReduce)")
        print("="*60)
        
        start_time = time.time()
        
        # Split text into chunks
        chunks = self._split_text(text, len(self.stubs))
        
        # Map phase
        map_start = time.time()
        map_results = []
        
        for i, (chunk, stub) in enumerate(zip(chunks, self.stubs)):
            request = mapreduce_pb2.MapRequest(text_chunk=chunk, chunk_id=i)
            response = stub.Map(request)
            map_results.append(response.word_counts)
        
        map_duration = time.time() - map_start
        
        # Reduce phase
        reduce_start = time.time()
        combined_counts = Counter()
        for counts in map_results:
            combined_counts.update(counts)
        
        reduce_request = mapreduce_pb2.ReduceRequest(
            intermediate_counts=dict(combined_counts)
        )
        reduce_response = self.stubs[0].Reduce(reduce_request)
        reduce_duration = time.time() - reduce_start
        
        total_duration = time.time() - start_time
        
        # Display results
        print(f"Total Duration: {total_duration:.4f}s")
        print(f"Map Duration: {map_duration:.4f}s")
        print(f"Reduce Duration: {reduce_duration:.4f}s")
        print(f"\nTop 10 Words:")
        sorted_words = sorted(reduce_response.final_counts.items(), 
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
        chunks = self._split_text(text, len(self.stubs))
        
        print(f"Sorting words from text distributed across {len(self.stubs)} servers")
        
        # Send chunks to servers for sorting
        sorted_chunks = []
        for i, (chunk, stub) in enumerate(zip(chunks, self.stubs)):
            request = mapreduce_pb2.SortWordsRequest(text_chunk=chunk, chunk_id=i)
            response = stub.SortWords(request)
            sorted_chunks.append(list(response.sorted_words))
        
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
        print(f"Analyzing word lengths distributed across {len(self.stubs)} servers")
        
        start_time = time.time()
        
        # Split text into chunks
        chunks = self._split_text(text, len(self.stubs))
        
        # Send to servers for analysis
        all_distributions = Counter()
        total_avg = 0
        min_length = float('inf')
        max_length = 0
        
        for i, (chunk, stub) in enumerate(zip(chunks, self.stubs)):
            request = mapreduce_pb2.WordLengthRequest(text_chunk=chunk, chunk_id=i)
            response = stub.AnalyzeWordLengths(request)
            
            # Aggregate results
            all_distributions.update(response.length_distribution)
            total_avg += response.average_length
            min_length = min(min_length, response.min_length)
            max_length = max(max_length, response.max_length)
        
        avg_length = total_avg / len(self.stubs)
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
    
    def _merge_sorted_lists(self, sorted_lists):
        """Merge multiple sorted lists of numbers into one sorted list"""
        import heapq
        return list(heapq.merge(*sorted_lists))
    
    def _merge_sorted_string_lists(self, sorted_lists):
        """Merge multiple sorted lists of strings into one sorted list"""
        import heapq
        return list(heapq.merge(*sorted_lists))
    
    def close(self):
        """Close all gRPC channels"""
        for channel in self.channels:
            channel.close()


def main():
    """Test all three services"""
    # Server addresses
    servers = ['localhost:50051', 'localhost:50052', 'localhost:50053']
    
    if os.getenv('GRPC_SERVERS'):
        servers = os.getenv('GRPC_SERVERS').split(',')
    
    client = MultiServiceClient(servers)
    
    # Health check
    if not client.health_check():
        print("\n✗ Some servers are not healthy!")
        return
    
    print("\n" + "="*60)
    print("TESTING ALL 3 SERVICES WITH SAMPLE TEXT")
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
    print("PERFORMANCE SUMMARY")
    print("="*60)
    print(f"Service 1 (Word Count):         {time1:.4f}s")
    print(f"Service 2 (Alphabetical Sort):  {time2:.4f}s")
    print(f"Service 3 (Word Length Stats):  {time3:.4f}s")
    print(f"Total Time (All Services):      {time1 + time2 + time3:.4f}s")
    print(f"Number of Servers Used:         {len(client.stubs)}")
    
    client.close()


if __name__ == '__main__':
    main()
