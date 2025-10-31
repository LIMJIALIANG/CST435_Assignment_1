"""
Statistics Service: Statistical Analysis
Port: 50055
FINAL SERVICE - Returns results to client
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
from services.stats_service import StatsService


class StatisticsServiceHandler(student_service_pb2_grpc.StudentAnalysisServiceServicer):
    """Statistics Service: Performs statistical analysis (FINAL SERVICE)"""
    
    def ProcessChain(self, request, context):
        """Process statistics and return FINAL combined results"""
        print(f"\n[Statistics Service] ✓ Chain request received from MergeSort Service")
        print(f"[Statistics Service] Analyzing {len(request.students)} students")
        print(f"[Statistics Service] This is the FINAL service in the chain")
        
        try:
            start_time = time.time()
            result = StatsService.perform_analysis(list(request.students), "all")
            processing_time = time.time() - start_time
            
            # Get accumulated results from MapReduce, MergeSort Services
            combined = student_service_pb2.CombinedResponse()
            combined.CopyFrom(request.partial_results)
            
            # Add Statistics Service results (FINAL)
            combined.pass_rate = result['pass_rate']
            combined.statistics_time = processing_time
            
            for faculty_stat in result['faculty_stats']:
                stat = combined.faculty_stats.add()
                stat.faculty = faculty_stat['faculty']
                stat.average_cgpa = faculty_stat['average_cgpa']
                stat.student_count = faculty_stat['student_count']
            
            for grade_dist in result['grade_distribution']:
                dist = combined.grade_distribution.add()
                dist.grade = grade_dist['grade']
                dist.count = grade_dist['count']
                dist.percentage = grade_dist['percentage']
            
            # Calculate total workflow time
            combined.total_workflow_time = (
                combined.mapreduce_time + 
                combined.mergesort_time + 
                combined.statistics_time
            )
            
            print(f"[Statistics Service] ✓ Completed in {processing_time:.4f}s")
            
            # Print detailed statistics
            print(f"[Statistics Service] Pass Rate: {result['pass_rate']:.2f}%")
            
            print(f"[Statistics Service] Faculty Distribution:")
            for faculty_stat in result['faculty_stats']:
                print(f"[Statistics Service]   {faculty_stat['faculty']}: {faculty_stat['student_count']} students (Avg CGPA: {faculty_stat['average_cgpa']:.2f})")
            
            print(f"[Statistics Service] Grade Distribution:")
            for grade_dist in result['grade_distribution']:
                print(f"[Statistics Service]   {grade_dist['grade']}: {grade_dist['count']} students ({grade_dist['percentage']:.1f}%)")
            
            print(f"[Statistics Service] ✓ All services completed! Chain: MapReduce→MergeSort→Statistics")
            print(f"[Statistics Service] ✓ Returning FINAL combined results to client\n")
            
            return combined
            
        except Exception as e:
            print(f"[Statistics Service] ✗ Error: {e}")
            context.set_code(grpc.StatusCode.INTERNAL)
            return student_service_pb2.CombinedResponse()


def serve():
    port = int(os.getenv('SERVICE_PORT', '50055'))
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    student_service_pb2_grpc.add_StudentAnalysisServiceServicer_to_server(StatisticsServiceHandler(), server)
    server.add_insecure_port(f'[::]:{port}')
    server.start()
    
    print("="*60)
    print("STATISTICS SERVICE: Statistical Analysis (FINAL)")
    print("="*60)
    print(f"Port: {port}")
    print("Status: RUNNING")
    print("="*60 + "\n")
    
    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        print("\n[Statistics Service] Shutting down...")
        server.stop(0)


if __name__ == '__main__':
    serve()
