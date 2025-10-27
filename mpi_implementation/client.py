"""
MPI Client Implementation
Coordinates MPI worker processes for distributed text processing
Matches gRPC/XML-RPC client interface for fair comparison
"""
from mpi4py import MPI
import time
import re
import os
import sys
from collections import Counter
import heapq


class MPIClient:
    """
    MPI Client that coordinates worker processes
    Note: In MPI, the "client" is actually the master process (rank 0)
    that coordinates with worker processes (rank 1, 2, 3, ...)
    """
    
    def __init__(self):
        self.comm = MPI.COMM_WORLD
        self.rank = self.comm.Get_rank()
        self.size = self.comm.Get_size()
        
        if self.rank == 0:
            print(f"MPI Client initialized with {self.size} processes (1 master + {self.size-1} workers)")
    
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
    
    def health_check(self):
        """Check if all MPI processes are healthy"""
        print("\n" + "="*60)
        print("HEALTH CHECK")
        print("="*60)
        
        # In MPI, all processes are already running
        # We can verify by doing a simple barrier
        try:
            self.comm.Barrier()
            for i in range(self.size):
                print(f"✓ Process {i}: HEALTHY")
            return True
        except Exception as e:
            print(f"✗ MPI processes UNHEALTHY: {e}")
            return False
    
    def test_word_count(self, text):
        """
        Service 1: Word Count (MapReduce)
        Distributes text across MPI processes for parallel word counting
        """
        if self.rank == 0:
            print("\n" + "="*60)
            print("SERVICE 1: WORD COUNT (MapReduce)")
            print("="*60)
        
        start_time = time.time()
        
        # Master splits text, workers receive None
        if self.rank == 0:
            chunks = self._split_text(text, self.size)
        else:
            chunks = None
        
        # Scatter chunks to all processes (including rank 0)
        chunk = self.comm.scatter(chunks, root=0)
        
        # Map phase - each process counts words in its chunk
        words = re.findall(r'\b\w+\b', chunk.lower())
        local_counts = dict(Counter(words))
        
        # Gather results back to master
        all_counts = self.comm.gather(local_counts, root=0)
        
        # Reduce phase - master aggregates
        if self.rank == 0:
            final_counts = Counter()
            for counts in all_counts:
                if counts:
                    final_counts.update(counts)
            
            duration = time.time() - start_time
            
            # Display results
            print(f"Total Duration: {duration:.4f}s")
            print(f"\nTop 10 Words:")
            sorted_words = sorted(final_counts.items(), key=lambda x: x[1], reverse=True)
            for word, count in sorted_words[:10]:
                print(f"  {word}: {count}")
            
            return duration
        else:
            return 0.0
    
    def test_sorting(self, text):
        """
        Service 2: Alphabetical Word Sorting (Merge Sort)
        Distributes text across MPI processes for parallel sorting
        """
        if self.rank == 0:
            print("\n" + "="*60)
            print("SERVICE 2: ALPHABETICAL WORD SORTING (Merge Sort)")
            print("="*60)
            print(f"Sorting words distributed across {self.size} MPI processes")
        
        start_time = time.time()
        
        # Master splits text, workers receive None
        if self.rank == 0:
            chunks = self._split_text(text, self.size)
        else:
            chunks = None
        
        # Scatter chunks to all processes
        chunk = self.comm.scatter(chunks, root=0)
        
        # Each process sorts its chunk
        words = list(set(re.findall(r'\b\w+\b', chunk.lower())))
        local_sorted = sorted(words)
        
        # Gather sorted chunks
        all_sorted = self.comm.gather(local_sorted, root=0)
        
        # Master merges sorted lists
        if self.rank == 0:
            final_sorted = list(heapq.merge(*all_sorted))
            
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
        else:
            return 0.0
    
    def test_word_lengths(self, text):
        """
        Service 3: Word Length Analysis
        Distributes text across MPI processes for parallel analysis
        """
        if self.rank == 0:
            print("\n" + "="*60)
            print("SERVICE 3: WORD LENGTH ANALYSIS")
            print("="*60)
            print(f"Analyzing word lengths distributed across {self.size} MPI processes")
        
        start_time = time.time()
        
        # Master splits text, workers receive None
        if self.rank == 0:
            chunks = self._split_text(text, self.size)
        else:
            chunks = None
        
        # Scatter chunks to all processes
        chunk = self.comm.scatter(chunks, root=0)
        
        # Each process analyzes its chunk
        words = re.findall(r'\b\w+\b', chunk.lower())
        
        length_dist = Counter()
        for word in words:
            length_dist[len(word)] += 1
        
        if words:
            avg_length = sum(len(w) for w in words) / len(words)
            min_length = min(len(w) for w in words)
            max_length = max(len(w) for w in words)
        else:
            avg_length = min_length = max_length = 0
        
        local_result = {
            'length_distribution': dict(length_dist),
            'average_length': avg_length,
            'min_length': min_length,
            'max_length': max_length,
            'total_words': len(words)
        }
        
        # Gather results
        all_results = self.comm.gather(local_result, root=0)
        
        # Master aggregates
        if self.rank == 0:
            all_distributions = Counter()
            total_avg = 0
            min_length = float('inf')
            max_length = 0
            
            for result in all_results:
                if result:
                    all_distributions.update(result['length_distribution'])
                    total_avg += result['average_length']
                    min_length = min(min_length, result['min_length'])
                    max_length = max(max_length, result['max_length'])
            
            avg_length = total_avg / len(all_results)
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
        else:
            return 0.0


def main():
    """Test all three services with MPI"""
    # Initialize MPI
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()
    
    # All processes create a client (but only rank 0 prints)
    client = MPIClient()
    
    # Master process acts as coordinator and prints output
    if rank == 0:
        # Health check - all processes participate in Barrier
        if not client.health_check():
            print("\n✗ Some MPI processes are not healthy!")
            return
        
        print("\n" + "="*60)
        print("TESTING ALL 3 SERVICES WITH SAMPLE TEXT")
        print("="*60)
        
        # Load sample text
        data_file = os.path.join(os.path.dirname(__file__), '..', 'data', 'sample_text.txt')
        try:
            with open(data_file, 'r') as f:
                text = f.read()
        except FileNotFoundError:
            data_file = '../data/sample_text.txt'
            with open(data_file, 'r') as f:
                text = f.read()
        
        print(f"Text loaded: {len(text)} characters, {len(text.split())} words")
        
        # Test all 3 services
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
        print(f"Number of MPI Processes:        {client.size}")
    else:
        # Worker processes must participate in all collective operations
        # Health check barrier
        client.health_check()
        
        # Service 1: Word count
        client.test_word_count(None)
        
        # Service 2: Sorting
        client.test_sorting(None)
        
        # Service 3: Word lengths
        client.test_word_lengths(None)


if __name__ == '__main__':
    main()
