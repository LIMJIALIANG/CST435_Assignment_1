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
        print(f"[MergeSort Service] Initialized. Next service: {self.next_service}", flush=True)
    
    def ProcessChain(self, request, context):
        """Process CGPA sort, forward chain to Statistics Service"""
        print(f"[MergeSort Service] Received from MapReduce Service", flush=True)
        print(f"[MergeSort Service] Processing {len(request.students)} students...", flush=True)
        print(f"[MergeSort Service] Performing MergeSort by CGPA...", flush=True)
        
        try:
            # Sort by CGPA
            print(f"[MergeSort] Sort by CGPA", flush=True)
            start_time = time.time()
            cgpa_result = MergeSortService.perform_sort(list(request.students))
            processing_time = time.time() - start_time
            
            sorted_students = cgpa_result['sorted_students']
            print(f"[MergeSort] Sorted {len(sorted_students)} students", flush=True)
            if sorted_students:
                top_student = sorted_students[0]
                print(f"[MergeSort] Top student: {top_student.name} (CGPA: {top_student.cgpa:.2f})", flush=True)
            print(f"[MergeSort] Processing time: {processing_time:.4f} seconds", flush=True)
            
            # Get accumulated results from MapReduce Service
            combined = student_service_pb2.CombinedResponse()
            combined.CopyFrom(request.partial_results)
            
            # Add MergeSort Service results (CGPA sort only)
            for student in sorted_students:
                combined.sorted_by_cgpa.append(student)
            
            combined.mergesort_time = processing_time
            
            print(f"[MergeSort Service] Sort completed in {processing_time:.4f}s", flush=True)
            print(f"[MergeSort Service] Forwarding to Statistics Service...", flush=True)
            
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
                
                return final_response
                
            except Exception as e:
                print(f"[MergeSort Service] ✗ Failed to forward to Statistics Service: {e}", flush=True)
                return combined
            
        except Exception as e:
            print(f"[MergeSort Service] ✗ Error: {e}", flush=True)
            context.set_code(grpc.StatusCode.INTERNAL)
            return student_service_pb2.CombinedResponse()


def serve():
    """Start MergeSort Service"""
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    student_service_pb2_grpc.add_StudentAnalysisServiceServicer_to_server(
        MergeSortServiceHandler(), server
    )
    
    port = os.getenv('MERGESORT_PORT', '50053')
    statistics_addr = os.getenv('STATISTICS_ADDRESS', 'localhost:50055')
    server.add_insecure_port(f'0.0.0.0:{port}')
    server.start()
    
    print("="*60, flush=True)
    print(f"gRPC MERGESORT SERVICE: Sort CGPA + Grade", flush=True)
    print(f"Operations: Sort by CGPA, Sort by Grade", flush=True)
    print(f"Server running on 0.0.0.0:{port}", flush=True)
    print(f"Next service: {statistics_addr}", flush=True)
    print("="*60, flush=True)
    
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
