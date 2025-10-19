"""
MPI MapReduce
Message Passing Interface implementation for comparison
"""
from mpi4py import MPI
import time
import re
from collections import Counter
import os
import sys


def map_function(text_chunk, rank):
    """
    Map phase: Count words in text chunk
    """
    start_time = time.time()
    
    # Convert text to lowercase and split into words
    words = re.findall(r'\b\w+\b', text_chunk.lower())
    
    # Count word occurrences
    word_counts = Counter(words)
    
    processing_time = time.time() - start_time
    
    print(f"Rank {rank} - Processed {len(words)} words in {processing_time:.4f}s")
    
    return dict(word_counts)


def reduce_function(word_counts_list):
    """
    Reduce phase: Aggregate word counts
    """
    start_time = time.time()
    
    # Combine all word counts
    final_counts = Counter()
    for counts in word_counts_list:
        if counts:  # Skip None values
            final_counts.update(counts)
    
    processing_time = time.time() - start_time
    
    print(f"Reduce: Aggregated {len(final_counts)} unique words in {processing_time:.4f}s")
    
    return dict(final_counts)


def split_text(text, num_chunks):
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
    """MPI MapReduce main function"""
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()
    
    start_time = time.time()
    
    # Master process (rank 0)
    if rank == 0:
        print(f"\nMPI MapReduce with {size} processes")
        
        # Read input text
        data_file = os.path.join(os.path.dirname(__file__), '..', 'data', 'sample_text.txt')
        try:
            with open(data_file, 'r') as f:
                text = f.read()
        except FileNotFoundError:
            # Try alternative path
            data_file = 'data/sample_text.txt'
            with open(data_file, 'r') as f:
                text = f.read()
        
        print(f"Processing text with {len(text)} characters...")
        
        # Split text into chunks
        chunks = split_text(text, size)
        
        map_start = time.time()
    else:
        chunks = None
        map_start = None
    
    # Scatter chunks to all processes
    chunk = comm.scatter(chunks, root=0)
    
    # Map phase - each process counts words in its chunk
    local_counts = map_function(chunk, rank)
    
    # Gather results back to master
    all_counts = comm.gather(local_counts, root=0)
    
    # Master performs reduce
    if rank == 0:
        map_duration = time.time() - map_start
        print(f"\nMap phase completed in {map_duration:.4f}s")
        
        # Reduce phase
        reduce_start = time.time()
        final_counts = reduce_function(all_counts)
        reduce_duration = time.time() - reduce_start
        print(f"Reduce phase completed in {reduce_duration:.4f}s")
        
        total_duration = time.time() - start_time
        
        # Display results
        print(f"\n{'='*60}")
        print("RESULTS:")
        print(f"{'='*60}")
        print(f"Total Duration: {total_duration:.4f}s")
        print(f"Map Duration: {map_duration:.4f}s")
        print(f"Reduce Duration: {reduce_duration:.4f}s")
        print(f"Number of Processes: {size}")
        print(f"\nTop 10 Words:")
        
        sorted_words = sorted(final_counts.items(), key=lambda x: x[1], reverse=True)
        for word, count in sorted_words[:10]:
            print(f"  {word}: {count}")
        
        return {
            'word_counts': final_counts,
            'total_duration': total_duration,
            'map_duration': map_duration,
            'reduce_duration': reduce_duration,
            'num_processes': size
        }


if __name__ == '__main__':
    main()
