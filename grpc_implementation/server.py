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
    """Implementation of MapReduce gRPC service"""
    
    def Map(self, request, context):
        """
        Map phase: Count words in text chunk
        """
        start_time = time.time()
        
        # Convert text to lowercase and split into words
        words = re.findall(r'\b\w+\b', request.text_chunk.lower())
        
        # Count word occurrences
        word_counts = Counter(words)
        
        processing_time = time.time() - start_time
        
        print(f"Map - Chunk {request.chunk_id}: Processed {len(words)} words in {processing_time:.4f}s")
        
        return mapreduce_pb2.MapResponse(
            word_counts=dict(word_counts),
            chunk_id=request.chunk_id,
            processing_time=processing_time
        )
    
    def Reduce(self, request, context):
        """
        Reduce phase: Aggregate word counts
        """
        start_time = time.time()
        
        # Sum up all word counts
        final_counts = Counter(request.intermediate_counts)
        
        processing_time = time.time() - start_time
        
        print(f"Reduce: Aggregated {len(final_counts)} unique words in {processing_time:.4f}s")
        
        return mapreduce_pb2.ReduceResponse(
            final_counts=dict(final_counts),
            processing_time=processing_time
        )
    
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
