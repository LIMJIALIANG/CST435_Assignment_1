"""
MapReduce Service: CGPA Classification
Port: 50051
Chains to: MergeSort Service (50053)
"""

import sys
import os
import grpc
from concurrent import futures
import time

# Add project paths
current_dir = os.path.dirname(os.path.abspath(__file__))
grpc_impl_dir = os.path.dirname(current_dir)
project_root = os.path.dirname(grpc_impl_dir)
sys.path.insert(0, project_root)
sys.path.insert(0, os.path.join(current_dir, 'generated'))

import student_service_pb2
import student_service_pb2_grpc
from services.mapreduce_service import MapReduceService


class MapReduceServiceHandler(student_service_pb2_grpc.StudentAnalysisServiceServicer):
    """MapReduce Service: Performs CGPA classification, forwards to MergeSort Service"""
    
    def __init__(self):
        self.next_service = os.getenv('MERGESORT_ADDRESS', 'localhost:50053')
        print(f"[MapReduce Service] Initialized. Next service: {self.next_service}", flush=True)
    
    def ProcessChain(self, request, context):
        """Process CGPA classification, forward chain to MergeSort Service"""
        print(f"[MapReduce Service] Processing {len(request.students)} students...", flush=True)
        
        try:
            # Process MapReduce CGPA Classification
            print(f"[MapReduce] CGPA Classification", flush=True)
            start_time = time.time()
            cgpa_result = MapReduceService.perform_mapreduce(list(request.students))
            processing_time = time.time() - start_time
            
            print(f"[MapReduce] Processed {len(request.students)} students", flush=True)
            print(f"[MapReduce] Results: {cgpa_result['cgpa_classification']}", flush=True)
            print(f"[MapReduce] Processing time: {processing_time:.4f} seconds", flush=True)
            
            # Create combined response with MapReduce Service results
            combined = student_service_pb2.CombinedResponse()
            
            # Add CGPA classification results
            for grade_key, count in cgpa_result['cgpa_classification'].items():
                cgpa_range = combined.cgpa_ranges.add()
                cgpa_range.range = grade_key
                cgpa_range.count = count
            
            combined.mapreduce_time = processing_time
            
            print(f"[MapReduce Service] ✓ CGPA Classification completed in {processing_time:.4f}s", flush=True)
            print(f"[MapReduce Service] Forwarding to MergeSort Service...", flush=True)
            
            # Forward to MergeSort Service with accumulated results
            try:
                channel = grpc.insecure_channel(self.next_service)
                stub = student_service_pb2_grpc.StudentAnalysisServiceStub(channel)
                
                next_request = student_service_pb2.ChainRequest(
                    students=request.students,
                    partial_results=combined
                )
                
                # Wait for and receive combined results from MergeSort Service (which includes Statistics)
                final_response = stub.ProcessChain(next_request, timeout=60)
                channel.close()
                
                return final_response
                
            except Exception as e:
                print(f"[MapReduce Service] ✗ Failed to forward to MergeSort Service: {e}", flush=True)
                # Return only MapReduce Service results if forwarding fails
                return combined
            
        except Exception as e:
            print(f"[MapReduce Service] ✗ Error: {e}", flush=True)
            context.set_code(grpc.StatusCode.INTERNAL)
            return student_service_pb2.CombinedResponse()


def serve():
    """Start MapReduce Service"""
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    student_service_pb2_grpc.add_StudentAnalysisServiceServicer_to_server(
        MapReduceServiceHandler(), server
    )
    
    port = os.getenv('MAPREDUCE_PORT', '50051')
    mergesort_addr = os.getenv('MERGESORT_ADDRESS', 'localhost:50053')
    server.add_insecure_port(f'0.0.0.0:{port}')
    server.start()
    
    print("="*70, flush=True)
    print(f"MapReduce Service (CGPA + Grade Count) started on 0.0.0.0:{port}", flush=True)
    print(f"Next service: {mergesort_addr}", flush=True)
    print("Operations: CGPA Classification, Grade Distribution", flush=True)
    print("="*70, flush=True)
    
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
