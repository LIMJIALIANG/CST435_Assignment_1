"""
Service B: MapReduce Grade Count
Port: 50052
Chains to: Service C (50053)
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
from services.mapreduce_service import MapReduceService


class ServiceB(student_service_pb2_grpc.StudentAnalysisServiceServicer):
    """Service B: Performs grade counting and forwards to Service C"""
    
    def __init__(self):
        self.next_service = os.getenv('SERVICE_C_ADDRESS', 'localhost:50053')
        print(f"[Service B] Next service: {self.next_service}")
    
    def ProcessChain(self, request, context):
        """Process grade count and forward chain to Service C"""
        print(f"\n[Service B] ✓ Chain request received from Service A")
        print(f"[Service B] Processing {len(request.students)} students")
        
        try:
            start_time = time.time()
            result = MapReduceService.perform_mapreduce(list(request.students), "grade_count")
            processing_time = time.time() - start_time
            
            # Get accumulated results from Service A
            combined = student_service_pb2.CombinedResponse()
            combined.CopyFrom(request.partial_results)
            
            # Add Service B results
            for grade, count in result['result'].items():
                grade_count = combined.grade_counts.add()
                grade_count.grade = grade
                grade_count.count = count
            combined.service_b_time = processing_time
            
            print(f"[Service B] ✓ Completed in {processing_time:.4f}s")
            print(f"[Service B] → Forwarding to Service C...")
            
            # Forward to Service C
            try:
                channel = grpc.insecure_channel(self.next_service)
                stub = student_service_pb2_grpc.StudentAnalysisServiceStub(channel)
                
                next_request = student_service_pb2.ChainRequest(
                    students=request.students,
                    partial_results=combined
                )
                
                # Wait for combined results from Service C (which includes D, E)
                final_response = stub.ProcessChain(next_request, timeout=60)
                channel.close()
                
                print(f"[Service B] ✓ Received combined results from downstream services\n")
                return final_response
                
            except Exception as e:
                print(f"[Service B] ✗ Failed to forward to Service C: {e}\n")
                return combined
            
        except Exception as e:
            print(f"[Service B] ✗ Error: {e}")
            context.set_code(grpc.StatusCode.INTERNAL)
            return student_service_pb2.CombinedResponse()


def serve():
    port = int(os.getenv('SERVICE_PORT', '50052'))
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    student_service_pb2_grpc.add_StudentAnalysisServiceServicer_to_server(ServiceB(), server)
    server.add_insecure_port(f'[::]:{port}')
    server.start()
    
    print("="*60)
    print("SERVICE B: MapReduce Grade Count")
    print("="*60)
    print(f"Port: {port}")
    print("Status: RUNNING")
    print("="*60 + "\n")
    
    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        print("\n[Service B] Shutting down...")
        server.stop(0)


if __name__ == '__main__':
    serve()
