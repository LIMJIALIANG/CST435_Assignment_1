"""
XML-RPC Multi-Service Server
Provides 3 text-processing services for comparison with gRPC
"""
from xmlrpc.server import SimpleXMLRPCServer
import time
import re
from collections import Counter
import os


class MapReduceService:
    """Multi-service operations exposed via XML-RPC"""
    
    # SERVICE 1: Word Count (MapReduce)
    def map_operation(self, text_chunk, chunk_id):
        """
        Map phase: Count words in text chunk
        """
        start_time = time.time()
        
        # Convert text to lowercase and split into words
        words = re.findall(r'\b\w+\b', text_chunk.lower())
        
        # Count word occurrences
        word_counts = dict(Counter(words))
        
        processing_time = time.time() - start_time
        
        print(f"[WordCount] Chunk {chunk_id}: Processed {len(words)} words in {processing_time:.4f}s")
        
        return {
            'word_counts': word_counts,
            'chunk_id': chunk_id,
            'processing_time': processing_time
        }
    
    def reduce_operation(self, intermediate_counts):
        """
        Reduce phase: Aggregate word counts
        """
        start_time = time.time()
        
        # Sum up all word counts
        final_counts = Counter(intermediate_counts)
        
        processing_time = time.time() - start_time
        
        print(f"[WordCount] Reduce: Aggregated {len(final_counts)} unique words in {processing_time:.4f}s")
        
        return {
            'final_counts': dict(final_counts),
            'processing_time': processing_time
        }
    
    # SERVICE 2: Alphabetical Word Sorting
    def sort_words(self, text_chunk, chunk_id):
        """
        Service 2: Alphabetical Word Sorting
        Extracts and sorts unique words from text alphabetically
        """
        start_time = time.time()
        
        # Extract words from text
        words = re.findall(r'\b\w+\b', text_chunk.lower())
        
        # Get unique words and sort alphabetically using merge sort
        unique_words = list(set(words))
        sorted_words = self._merge_sort_strings(unique_words)
        
        processing_time = time.time() - start_time
        
        print(f"[AlphaSort] Chunk {chunk_id}: Sorted {len(sorted_words)} unique words in {processing_time:.4f}s")
        
        return {
            'sorted_words': sorted_words,
            'chunk_id': chunk_id,
            'word_count': len(sorted_words),
            'processing_time': processing_time
        }
    
    # SERVICE 3: Word Length Analysis
    def analyze_word_lengths(self, text_chunk, chunk_id):
        """
        Service 3: Word Length Analysis
        Analyzes the distribution of word lengths in text
        """
        start_time = time.time()
        
        # Extract words from text
        words = re.findall(r'\b\w+\b', text_chunk.lower())
        
        # Calculate length distribution
        length_dist = Counter(len(word) for word in words)
        
        # Calculate statistics
        if words:
            avg_length = sum(len(word) for word in words) / len(words)
            min_length = min(len(word) for word in words)
            max_length = max(len(word) for word in words)
        else:
            avg_length = min_length = max_length = 0
        
        processing_time = time.time() - start_time
        
        print(f"[WordLength] Chunk {chunk_id}: Analyzed {len(words)} words, "
              f"avg length={avg_length:.2f} in {processing_time:.4f}s")
        
        # Return as list of [length, count] pairs for XML-RPC compatibility
        return {
            'length_distribution': [[k, v] for k, v in sorted(length_dist.items())],
            'average_length': avg_length,
            'min_length': int(min_length),
            'max_length': int(max_length),
            'chunk_id': chunk_id,
            'processing_time': processing_time
        }
    
    def _merge_sort_strings(self, arr):
        """
        Merge sort algorithm implementation for strings
        """
        if len(arr) <= 1:
            return arr
        
        mid = len(arr) // 2
        left = self._merge_sort_strings(arr[:mid])
        right = self._merge_sort_strings(arr[mid:])
        
        return self._merge_strings(left, right)
    
    def _merge_strings(self, left, right):
        """
        Merge two sorted arrays of strings
        """
        result = []
        i = j = 0
        
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
        
        result.extend(left[i:])
        result.extend(right[j:])
        return result
    
    def health_check(self):
        """Health check endpoint"""
        return {
            'status': True,
            'message': 'XML-RPC Multi-Service server is healthy'
        }


def serve(port=8000):
    """Start XML-RPC server"""
    server = SimpleXMLRPCServer(('0.0.0.0', port), allow_none=True)
    server.register_instance(MapReduceService())
    
    print(f"XML-RPC MapReduce Server started on port {port}")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped by user")


if __name__ == '__main__':
    port = int(os.getenv('XMLRPC_PORT', '8000'))
    serve(port)
