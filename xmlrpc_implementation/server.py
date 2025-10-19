"""
XML-RPC MapReduce Server
Simple RPC implementation for comparison
"""
from xmlrpc.server import SimpleXMLRPCServer
import time
import re
from collections import Counter
import os


class MapReduceService:
    """MapReduce operations exposed via XML-RPC"""
    
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
        
        print(f"Map - Chunk {chunk_id}: Processed {len(words)} words in {processing_time:.4f}s")
        
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
        
        print(f"Reduce: Aggregated {len(final_counts)} unique words in {processing_time:.4f}s")
        
        return {
            'final_counts': dict(final_counts),
            'processing_time': processing_time
        }
    
    def health_check(self):
        """Health check endpoint"""
        return {
            'status': True,
            'message': 'XML-RPC MapReduce service is healthy'
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
