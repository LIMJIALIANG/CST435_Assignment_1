"""
MPI Server Implementation
Runs as a worker process that accepts tasks via MPI
"""
from mpi4py import MPI
import time
import re
from collections import Counter
import sys


class MPIServer:
    """MPI Server that processes text chunks"""
    
    def __init__(self):
        self.comm = MPI.COMM_WORLD
        self.rank = self.comm.Get_rank()
        self.size = self.comm.Get_size()
        
        if self.rank == 0:
            print(f"MPI Server initialized with {self.size} processes")
    
    def map_operation(self, text_chunk):
        """Map phase: Count words in text chunk"""
        words = re.findall(r'\b\w+\b', text_chunk.lower())
        word_counts = Counter(words)
        return dict(word_counts)
    
    def reduce_operation(self, word_counts):
        """Reduce phase: Aggregate word counts"""
        final_counts = Counter()
        final_counts.update(word_counts)
        return dict(final_counts)
    
    def sort_words(self, text_chunk):
        """Sort words alphabetically using merge sort"""
        words = list(set(re.findall(r'\b\w+\b', text_chunk.lower())))
        return sorted(words)
    
    def analyze_word_lengths(self, text_chunk):
        """Analyze word length distribution"""
        words = re.findall(r'\b\w+\b', text_chunk.lower())
        
        length_dist = Counter()
        for word in words:
            length_dist[len(word)] += 1
        
        if words:
            avg_length = sum(len(w) for w in words) / len(words)
            min_length = min(len(w) for w in words)
            max_length = max(len(w) for w in words)
        else:
            avg_length = min_length = max_length = 0
        
        return {
            'length_distribution': dict(length_dist),
            'average_length': avg_length,
            'min_length': min_length,
            'max_length': max_length,
            'total_words': len(words)
        }
    
    def health_check(self):
        """Health check"""
        return {
            'status': 'healthy',
            'rank': self.rank,
            'size': self.size
        }
    
    def run(self):
        """Run server - wait for commands from master"""
        if self.rank == 0:
            print(f"MPI Server (Master) ready on rank {self.rank}")
        else:
            print(f"MPI Server (Worker) ready on rank {self.rank}")
        
        # Server loop - in MPI, the client will coordinate via rank 0
        # Worker processes (rank > 0) will wait for scatter/gather operations
        while True:
            # Workers wait for tasks via MPI collective operations
            # This is handled by the client via scatter/gather
            try:
                # Keep process alive
                self.comm.Barrier()
            except KeyboardInterrupt:
                print(f"Server rank {self.rank} shutting down...")
                break


def main():
    """Run MPI server"""
    server = MPIServer()
    
    # For MPI, we don't need a traditional server loop
    # The processes stay alive and communicate via MPI primitives
    print(f"Rank {server.rank}: MPI Server process ready")
    
    # In MPI architecture, all processes are started together
    # and coordinate via the client's scatter/gather operations


if __name__ == '__main__':
    main()
