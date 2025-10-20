"""
ZeroMQ Request-Reply MapReduce Server
Demonstrates request-reply messaging pattern
"""
import zmq
import time
import re
import json
from collections import Counter
import os


class MapReduceReqRepServer:
    """Request-Reply server for MapReduce operations"""
    
    def __init__(self, port):
        """Initialize ZeroMQ Request-Reply server"""
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REP)
        self.socket.bind(f"tcp://*:{port}")
        self.port = port
        print(f"Request-Reply Server started on port {port}")
    
    def map_operation(self, text_chunk, chunk_id):
        """Map phase: Count words in text chunk"""
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
        """Reduce phase: Aggregate word counts"""
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
            'message': f'Request-Reply MapReduce service is healthy on port {self.port}'
        }
    
    def run(self):
        """Main server loop"""
        try:
            while True:
                # Wait for request
                message = self.socket.recv_json()
                
                operation = message.get('operation')
                
                if operation == 'health_check':
                    response = self.health_check()
                
                elif operation == 'map':
                    text_chunk = message.get('text_chunk')
                    chunk_id = message.get('chunk_id')
                    response = self.map_operation(text_chunk, chunk_id)
                
                elif operation == 'reduce':
                    intermediate_counts = message.get('intermediate_counts')
                    response = self.reduce_operation(intermediate_counts)
                
                else:
                    response = {
                        'error': f'Unknown operation: {operation}'
                    }
                
                # Send reply
                self.socket.send_json(response)
        
        except KeyboardInterrupt:
            print("\nServer stopped by user")
        finally:
            self.socket.close()
            self.context.term()


if __name__ == '__main__':
    port = int(os.getenv('REQREP_PORT', '5555'))
    server = MapReduceReqRepServer(port)
    server.run()
