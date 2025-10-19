"""
Python Multiprocessing MapReduce
Local parallel processing for comparison
"""
import time
import re
from collections import Counter
from multiprocessing import Pool, cpu_count
import os


def map_function(chunk_data):
    """
    Map phase: Count words in text chunk
    Args:
        chunk_data: Tuple of (text_chunk, chunk_id)
    """
    text_chunk, chunk_id = chunk_data
    start_time = time.time()
    
    # Convert text to lowercase and split into words
    words = re.findall(r'\b\w+\b', text_chunk.lower())
    
    # Count word occurrences
    word_counts = Counter(words)
    
    processing_time = time.time() - start_time
    
    print(f"Map - Chunk {chunk_id}: Processed {len(words)} words in {processing_time:.4f}s")
    
    return dict(word_counts)


def reduce_function(word_counts_list):
    """
    Reduce phase: Aggregate word counts
    Args:
        word_counts_list: List of word count dictionaries
    """
    start_time = time.time()
    
    # Combine all word counts
    final_counts = Counter()
    for counts in word_counts_list:
        final_counts.update(counts)
    
    processing_time = time.time() - start_time
    
    print(f"Reduce: Aggregated {len(final_counts)} unique words in {processing_time:.4f}s")
    
    return dict(final_counts)


class MapReduceMultiprocessing:
    """MapReduce using Python multiprocessing"""
    
    def __init__(self, num_workers=None):
        """
        Initialize with number of worker processes
        Args:
            num_workers: Number of processes (defaults to CPU count)
        """
        self.num_workers = num_workers or min(cpu_count(), 3)
        print(f"Initialized with {self.num_workers} worker processes")
    
    def map_reduce(self, text):
        """
        Execute MapReduce on the given text
        """
        start_time = time.time()
        
        # Split text into chunks
        chunks = self._split_text(text, self.num_workers)
        chunk_data = [(chunk, i) for i, chunk in enumerate(chunks)]
        
        # Map phase - parallel processing
        map_start = time.time()
        
        with Pool(processes=self.num_workers) as pool:
            map_results = pool.map(map_function, chunk_data)
        
        map_duration = time.time() - map_start
        print(f"Map phase completed in {map_duration:.4f}s")
        
        # Reduce phase - aggregate results
        reduce_start = time.time()
        final_counts = reduce_function(map_results)
        reduce_duration = time.time() - reduce_start
        print(f"Reduce phase completed in {reduce_duration:.4f}s")
        
        total_duration = time.time() - start_time
        
        return {
            'word_counts': final_counts,
            'total_duration': total_duration,
            'map_duration': map_duration,
            'reduce_duration': reduce_duration,
            'num_workers': self.num_workers
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
    """Test the multiprocessing MapReduce"""
    # Number of workers (simulating 3 containers)
    num_workers = 3
    
    mapreduce = MapReduceMultiprocessing(num_workers=num_workers)
    
    # Read input text
    data_file = os.path.join(os.path.dirname(__file__), '..', 'data', 'sample_text.txt')
    with open(data_file, 'r') as f:
        text = f.read()
    
    print(f"\nProcessing text with {len(text)} characters...")
    
    # Execute MapReduce
    result = mapreduce.map_reduce(text)
    
    # Display results
    print(f"\n{'='*60}")
    print("RESULTS:")
    print(f"{'='*60}")
    print(f"Total Duration: {result['total_duration']:.4f}s")
    print(f"Map Duration: {result['map_duration']:.4f}s")
    print(f"Reduce Duration: {result['reduce_duration']:.4f}s")
    print(f"Number of Workers: {result['num_workers']}")
    print(f"\nTop 10 Words:")
    
    sorted_words = sorted(result['word_counts'].items(), key=lambda x: x[1], reverse=True)
    for word, count in sorted_words[:10]:
        print(f"  {word}: {count}")


if __name__ == '__main__':
    main()
