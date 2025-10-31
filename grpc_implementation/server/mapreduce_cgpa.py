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
        print(f"[MapReduce Service] Next service: {self.next_service}")
    
    def ProcessChain(self, request, context):
        """Process CGPA classification, forward chain to MergeSort Service"""
        print(f"\n[MapReduce Service] ✓ Chain request received")
        print(f"[MapReduce Service] Processing {len(request.students)} students")
        
        try:
            # Process MapReduce CGPA Classification
            start_time = time.time()
            cgpa_result = MapReduceService.perform_mapreduce(list(request.students))
            processing_time = time.time() - start_time
            
            # Create combined response with MapReduce Service results
            combined = student_service_pb2.CombinedResponse()
            
            # Add CGPA classification results
            for grade_key, count in cgpa_result['cgpa_classification'].items():
                cgpa_range = combined.cgpa_ranges.add()
                cgpa_range.range = grade_key
                cgpa_range.count = count
            
            combined.mapreduce_time = processing_time
            
            print(f"[MapReduce Service] ✓ CGPA Classification completed in {processing_time:.4f}s")
            print(f"[MapReduce Service] → Forwarding to MergeSort Service...")
            
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
                
                print(f"[MapReduce Service] ✓ Received combined results from downstream services\n")
                return final_response
                
            except Exception as e:
                print(f"[MapReduce Service] ✗ Failed to forward to MergeSort Service: {e}\n")
                # Return only MapReduce Service results if forwarding fails
                return combined
            
        except Exception as e:
            print(f"[MapReduce Service] ✗ Error: {e}")
            context.set_code(grpc.StatusCode.INTERNAL)
            return student_service_pb2.CombinedResponse()


def serve():
    port = int(os.getenv('SERVICE_PORT', '50051'))
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    student_service_pb2_grpc.add_StudentAnalysisServiceServicer_to_server(MapReduceServiceHandler(), server)
    server.add_insecure_port(f'[::]:{port}')
    server.start()
    
    print("="*60)
    print("MAPREDUCE SERVICE: CGPA Classification")
    print("="*60)
    print(f"Port: {port}")
    print("Status: RUNNING")
    print("Operation: CGPA Classification")
    print("="*60 + "\n")
    
    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        print("\n[MapReduce Service] Shutting down...")
        server.stop(0)


if __name__ == '__main__':
    serve()
