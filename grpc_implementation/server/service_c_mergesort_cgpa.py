"""
Service C: MergeSort by CGPA
Port: 50053
Chains to: Service D (50054)
"""

import sys
import os
import grpc
from concurrent import futures
import time

current_dir = os.path.dirname(os.path.abspath(__file__))
grpc_impl_dir = os.path.dirname(current_dir)
project_root = os.path.dirname(grpc_impl_dir)
sys.path.insert(0, project_root)
sys.path.insert(0, os.path.join(current_dir, 'generated'))

import student_service_pb2
import student_service_pb2_grpc
from services.mergesort_service import MergeSortService


class ServiceC(student_service_pb2_grpc.StudentAnalysisServiceServicer):
    """Service C: Sorts by CGPA and forwards to Service D"""
    
    def __init__(self):
        self.next_service = os.getenv('SERVICE_D_ADDRESS', 'localhost:50054')
        print(f"[Service C] Next service: {self.next_service}")
    
    def ProcessChain(self, request, context):
        """Process CGPA sort and forward chain to Service D"""
        print(f"\n[Service C] ✓ Chain request received from Service B")
        print(f"[Service C] Sorting {len(request.students)} students by CGPA")
        
        try:
            start_time = time.time()
            result = MergeSortService.perform_sort(list(request.students), "cgpa")
            processing_time = time.time() - start_time
            
            # Get accumulated results from Services A & B
            combined = student_service_pb2.CombinedResponse()
            combined.CopyFrom(request.partial_results)
            
            # Add Service C results
            for student in result['sorted_students']:
                combined.sorted_by_cgpa.append(student)
            combined.service_c_time = processing_time
            
            print(f"[Service C] ✓ Completed in {processing_time:.4f}s")
            print(f"[Service C] → Forwarding to Service D...")
            
            # Forward to Service D
            try:
                channel = grpc.insecure_channel(self.next_service)
                stub = student_service_pb2_grpc.StudentAnalysisServiceStub(channel)
                
                next_request = student_service_pb2.ChainRequest(
                    students=request.students,
                    partial_results=combined
                )
                
                # Wait for combined results from Service D (which includes E)
                final_response = stub.ProcessChain(next_request, timeout=60)
                channel.close()
                
                print(f"[Service C] ✓ Received combined results from downstream services\n")
                return final_response
                
            except Exception as e:
                print(f"[Service C] ✗ Failed to forward to Service D: {e}\n")
                return combined
            
        except Exception as e:
            print(f"[Service C] ✗ Error: {e}")
            context.set_code(grpc.StatusCode.INTERNAL)
            return student_service_pb2.CombinedResponse()


def serve():
    port = int(os.getenv('SERVICE_PORT', '50053'))
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    student_service_pb2_grpc.add_StudentAnalysisServiceServicer_to_server(ServiceC(), server)
    server.add_insecure_port(f'[::]:{port}')
    server.start()
    
    print("="*60)
    print("SERVICE C: MergeSort by CGPA")
    print("="*60)
    print(f"Port: {port}")
    print("Status: RUNNING")
    print("="*60 + "\n")
    
    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        print("\n[Service C] Shutting down...")
        server.stop(0)


if __name__ == '__main__':
    serve()
