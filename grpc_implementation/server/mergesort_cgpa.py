"""
MergeSort Service: Sort by CGPA
Port: 50053
Chains to: Statistics Service (50055)
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


class MergeSortServiceHandler(student_service_pb2_grpc.StudentAnalysisServiceServicer):
    """MergeSort Service: Sorts by CGPA, forwards to Statistics Service"""
    
    def __init__(self):
        self.next_service = os.getenv('STATISTICS_ADDRESS', 'localhost:50055')
        print(f"[MergeSort Service] Next service: {self.next_service}")
    
    def ProcessChain(self, request, context):
        """Process CGPA sort, forward chain to Statistics Service"""
        print(f"\n[MergeSort Service] ✓ Chain request received from MapReduce Service")
        print(f"[MergeSort Service] Sorting {len(request.students)} students")
        
        try:
            # Sort by CGPA
            start_time = time.time()
            cgpa_result = MergeSortService.perform_sort(list(request.students))
            processing_time = time.time() - start_time
            
            # Get accumulated results from MapReduce Service
            combined = student_service_pb2.CombinedResponse()
            combined.CopyFrom(request.partial_results)
            
            # Add MergeSort Service results (CGPA sort only)
            for student in cgpa_result['sorted_students']:
                combined.sorted_by_cgpa.append(student)
            
            combined.mergesort_time = processing_time
            
            # Print top 10 results
            print(f"[MergeSort Service] ✓ Sort completed in {processing_time:.4f}s")
            print(f"[MergeSort Service] Top 10 students by CGPA:")
            for i, student in enumerate(cgpa_result['sorted_students'][:10], 1):
                print(f"[MergeSort Service]   {i}. {student.name} - CGPA: {student.cgpa:.2f} ({student.grade})")
            print(f"[MergeSort Service] → Forwarding to Statistics Service...")
            
            # Forward to Statistics Service
            try:
                channel = grpc.insecure_channel(self.next_service)
                stub = student_service_pb2_grpc.StudentAnalysisServiceStub(channel)
                
                next_request = student_service_pb2.ChainRequest(
                    students=request.students,
                    partial_results=combined
                )
                
                # Wait for combined results from Statistics Service
                final_response = stub.ProcessChain(next_request, timeout=60)
                channel.close()
                
                print(f"[MergeSort Service] ✓ Received combined results from downstream services\n")
                return final_response
                
            except Exception as e:
                print(f"[MergeSort Service] ✗ Failed to forward to Statistics Service: {e}\n")
                return combined
            
        except Exception as e:
            print(f"[MergeSort Service] ✗ Error: {e}")
            context.set_code(grpc.StatusCode.INTERNAL)
            return student_service_pb2.CombinedResponse()


def serve():
    port = int(os.getenv('SERVICE_PORT', '50053'))
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    student_service_pb2_grpc.add_StudentAnalysisServiceServicer_to_server(MergeSortServiceHandler(), server)
    server.add_insecure_port(f'[::]:{port}')
    server.start()
    
    print("="*60)
    print("MERGESORT SERVICE: Sort by CGPA")
    print("="*60)
    print(f"Port: {port}")
    print("Status: RUNNING")
    print("Operation: Sort by CGPA")
    print("="*60 + "\n")
    
    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        print("\n[MergeSort Service] Shutting down...")
        server.stop(0)


if __name__ == '__main__':
    serve()
