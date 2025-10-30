"""
Service D: MergeSort by Grade
Port: 50054
Chains to: Service E (50055)
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


class ServiceD(student_service_pb2_grpc.StudentAnalysisServiceServicer):
    """Service D: Sorts by grade and forwards to Service E"""
    
    def __init__(self):
        self.next_service = os.getenv('SERVICE_E_ADDRESS', 'localhost:50055')
        print(f"[Service D] Next service: {self.next_service}")
    
    def ProcessChain(self, request, context):
        """Process grade sort and forward chain to Service E (final)"""
        print(f"\n[Service D] ✓ Chain request received from Service C")
        print(f"[Service D] Sorting {len(request.students)} students by grade")
        
        try:
            start_time = time.time()
            result = MergeSortService.perform_sort(list(request.students), "grade")
            processing_time = time.time() - start_time
            
            # Get accumulated results from Services A, B, C
            combined = student_service_pb2.CombinedResponse()
            combined.CopyFrom(request.partial_results)
            
            # Add Service D results
            for student in result['sorted_students']:
                combined.sorted_by_grade.append(student)
            combined.service_d_time = processing_time
            
            print(f"[Service D] ✓ Completed in {processing_time:.4f}s")
            print(f"[Service D] → Forwarding to Service E (FINAL)...")
            
            # Forward to Service E (final service)
            try:
                channel = grpc.insecure_channel(self.next_service)
                stub = student_service_pb2_grpc.StudentAnalysisServiceStub(channel)
                
                next_request = student_service_pb2.ChainRequest(
                    students=request.students,
                    partial_results=combined
                )
                
                # Wait for final combined results from Service E
                final_response = stub.ProcessChain(next_request, timeout=60)
                channel.close()
                
                print(f"[Service D] ✓ Received FINAL combined results from Service E\n")
                return final_response
                
            except Exception as e:
                print(f"[Service D] ✗ Failed to forward to Service E: {e}\n")
                return combined
            
        except Exception as e:
            print(f"[Service D] ✗ Error: {e}")
            context.set_code(grpc.StatusCode.INTERNAL)
            return student_service_pb2.CombinedResponse()


def serve():
    port = int(os.getenv('SERVICE_PORT', '50054'))
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    student_service_pb2_grpc.add_StudentAnalysisServiceServicer_to_server(ServiceD(), server)
    server.add_insecure_port(f'[::]:{port}')
    server.start()
    
    print("="*60)
    print("SERVICE D: MergeSort by Grade")
    print("="*60)
    print(f"Port: {port}")
    print("Status: RUNNING")
    print("="*60 + "\n")
    
    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        print("\n[Service D] Shutting down...")
        server.stop(0)


if __name__ == '__main__':
    serve()
