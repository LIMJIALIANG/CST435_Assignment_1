"""
Service A: MapReduce CGPA Count
Port: 50051
Chains to: Service B (50052)
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


class ServiceA(student_service_pb2_grpc.StudentAnalysisServiceServicer):
    """Service A: Performs CGPA counting and forwards to Service B"""
    
    def __init__(self):
        self.next_service = os.getenv('SERVICE_B_ADDRESS', 'localhost:50052')
        print(f"[Service A] Next service: {self.next_service}")
    
    def ProcessChain(self, request, context):
        """Process CGPA count and forward chain to Service B"""
        print(f"\n[Service A] ✓ Chain request received")
        print(f"[Service A] Processing {len(request.students)} students")
        
        try:
            # Process MapReduce CGPA
            start_time = time.time()
            result = MapReduceService.perform_mapreduce(list(request.students), "cgpa_count")
            processing_time = time.time() - start_time
            
            # Create combined response with Service A results
            combined = student_service_pb2.CombinedResponse()
            
            # Add Service A results
            for range_key, count in result['result'].items():
                cgpa_range = combined.cgpa_ranges.add()
                cgpa_range.range = range_key
                cgpa_range.count = count
            combined.service_a_time = processing_time
            
            print(f"[Service A] ✓ Completed in {processing_time:.4f}s")
            print(f"[Service A] → Forwarding to Service B...")
            
            # Forward to Service B with accumulated results
            try:
                channel = grpc.insecure_channel(self.next_service)
                stub = student_service_pb2_grpc.StudentAnalysisServiceStub(channel)
                
                next_request = student_service_pb2.ChainRequest(
                    students=request.students,
                    partial_results=combined
                )
                
                # Wait for and receive combined results from Service B (which includes C, D, E)
                final_response = stub.ProcessChain(next_request, timeout=60)
                channel.close()
                
                print(f"[Service A] ✓ Received combined results from downstream services\n")
                return final_response
                
            except Exception as e:
                print(f"[Service A] ✗ Failed to forward to Service B: {e}\n")
                # Return only Service A results if forwarding fails
                return combined
            
        except Exception as e:
            print(f"[Service A] ✗ Error: {e}")
            context.set_code(grpc.StatusCode.INTERNAL)
            return student_service_pb2.CombinedResponse()


def serve():
    port = int(os.getenv('SERVICE_PORT', '50051'))
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    student_service_pb2_grpc.add_StudentAnalysisServiceServicer_to_server(ServiceA(), server)
    server.add_insecure_port(f'[::]:{port}')
    server.start()
    
    print("="*60)
    print("SERVICE A: MapReduce CGPA Count")
    print("="*60)
    print(f"Port: {port}")
    print("Status: RUNNING")
    print("="*60 + "\n")
    
    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        print("\n[Service A] Shutting down...")
        server.stop(0)


if __name__ == '__main__':
    serve()
