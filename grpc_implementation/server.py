"""
gRPC MapReduce Server
Implements Map and Reduce operations as gRPC services
"""
import grpc
from concurrent import futures
import time
import re
from collections import Counter
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import mapreduce_pb2
import mapreduce_pb2_grpc


class MapReduceServicer(mapreduce_pb2_grpc.MapReduceServiceServicer):
    """Implementation of MapReduce gRPC service with 3 different algorithms"""
    
    def Map(self, request, context):
        """
        Service 1: Word Count - Map phase
        Count words in text chunk
        """
        start_time = time.time()
        
        # Convert text to lowercase and split into words
        words = re.findall(r'\b\w+\b', request.text_chunk.lower())
        
        # Count word occurrences
        word_counts = Counter(words)
        
        processing_time = time.time() - start_time
        
        print(f"[WordCount] Map - Chunk {request.chunk_id}: Processed {len(words)} words in {processing_time:.4f}s")
        
        return mapreduce_pb2.MapResponse(
            word_counts=dict(word_counts),
            chunk_id=request.chunk_id,
            processing_time=processing_time
        )
    
    def Reduce(self, request, context):
        """
        Service 1: Word Count - Reduce phase
        Aggregate word counts
        """
        start_time = time.time()
        
        # Sum up all word counts
        final_counts = Counter(request.intermediate_counts)
        
        processing_time = time.time() - start_time
        
        print(f"[WordCount] Reduce: Aggregated {len(final_counts)} unique words in {processing_time:.4f}s")
        
        return mapreduce_pb2.ReduceResponse(
            final_counts=dict(final_counts),
            processing_time=processing_time
        )
    
    def Sort(self, request, context):
        """
        Service 2: Alphabetical Word Sorting
        Extracts and sorts unique words from text alphabetically
        """
        start_time = time.time()
        
        # Extract words from text
        words = re.findall(r'\b\w+\b', request.text_chunk.lower())
        
        # Get unique words and sort alphabetically using merge sort
        unique_words = list(set(words))
        sorted_words = self._merge_sort_strings(unique_words)
        
        processing_time = time.time() - start_time
        
        print(f"[AlphaSort] Chunk {request.chunk_id}: Sorted {len(sorted_words)} unique words in {processing_time:.4f}s")
        
        return mapreduce_pb2.SortWordsResponse(
            sorted_words=sorted_words,
            chunk_id=request.chunk_id,
            word_count=len(sorted_words),
            processing_time=processing_time
        )
    
    def FindPrimes(self, request, context):
        """
        Service 3: Word Length Analysis
        Analyzes the distribution of word lengths in text
        """
        start_time = time.time()
        
        # Extract words from text
        words = re.findall(r'\b\w+\b', request.text_chunk.lower())
        
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
        
        print(f"[WordLength] Chunk {request.chunk_id}: Analyzed {len(words)} words, "
              f"avg length={avg_length:.2f} in {processing_time:.4f}s")
        
        return mapreduce_pb2.WordLengthResponse(
            length_distribution=dict(length_dist),
            average_length=avg_length,
            min_length=min_length,
            max_length=max_length,
            chunk_id=request.chunk_id,
            processing_time=processing_time
        )
    
    def SortWords(self, request, context):
        """
        Alias for Sort method for compatibility
        """
        return self.Sort(request, context)
    
    def AnalyzeWordLengths(self, request, context):
        """
        Alias for FindPrimes method for compatibility
        """
        return self.FindPrimes(request, context)
    
    def _merge_sort(self, arr):
        """
        Merge sort algorithm implementation for numbers
        """
        if len(arr) <= 1:
            return arr
        
        mid = len(arr) // 2
        left = self._merge_sort(arr[:mid])
        right = self._merge_sort(arr[mid:])
        
        return self._merge(left, right)
    
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
    
    def _merge(self, left, right):
        """
        Merge two sorted arrays of numbers
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
    
    
    def HealthCheck(self, request, context):
        """
        Health check endpoint
        """
        return mapreduce_pb2.HealthCheckResponse(
            status=True,
            message=f"MapReduce service is healthy"
        )


def serve(port=50051):
    """
    Start gRPC server
    """
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    mapreduce_pb2_grpc.add_MapReduceServiceServicer_to_server(
        MapReduceServicer(), server
    )
    
    server.add_insecure_port(f'[::]:{port}')
    server.start()
    
    print(f"gRPC MapReduce Server started on port {port}")
    
    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        print("\nServer stopped by user")
        server.stop(0)


if __name__ == '__main__':
    port = int(os.getenv('GRPC_PORT', '50051'))
    serve(port)
