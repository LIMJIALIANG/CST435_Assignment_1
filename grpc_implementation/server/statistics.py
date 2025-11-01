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
    
    def __init__(self):
        print(f"[Statistics Service] Initialized (Terminal Service)", flush=True)
    
    def ProcessChain(self, request, context):
        """Process statistics and return FINAL combined results"""
        print(f"[Statistics Service] Received from MergeSort Service", flush=True)
        print(f"[Statistics Service] Processing {len(request.students)} students...", flush=True)
        
        try:
            print(f"[Statistics] Comprehensive analysis", flush=True)
            start_time = time.time()
            result = StatsService.perform_analysis(list(request.students), "all")
            processing_time = time.time() - start_time
            
            # Calculate mean CGPA
            mean_cgpa = sum(s.cgpa for s in request.students) / len(request.students) if request.students else 0.0
            
            print(f"[Statistics] Analyzed {len(request.students)} students", flush=True)
            print(f"[Statistics] Mean CGPA: {mean_cgpa:.4f}", flush=True)
            print(f"[Statistics] Processing time: {processing_time:.4f} seconds", flush=True)
            
            # Get accumulated results from MapReduce, MergeSort Services
            combined = student_service_pb2.CombinedResponse()
            combined.CopyFrom(request.partial_results)
            
            # Add Statistics Service results (FINAL)
            combined.pass_rate = result['pass_rate']
            combined.mean_cgpa = mean_cgpa
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
            
            print(f"[Statistics Service] Completed in {processing_time:.4f}s", flush=True)
            print(f"[Statistics Service] Statistics calculated", flush=True)
            print(f"[Statistics Service] Chain complete: MapReduce, MergeSort, Statistics processed", flush=True)
            print(f"[Statistics Service] Returning final results to client...", flush=True)
            
            return combined
            
        except Exception as e:
            print(f"[Statistics Service] ✗ Error: {e}", flush=True)
            context.set_code(grpc.StatusCode.INTERNAL)
            return student_service_pb2.CombinedResponse()


def serve():
    """Start Statistics Service"""
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    student_service_pb2_grpc.add_StudentAnalysisServiceServicer_to_server(
        StatisticsServiceHandler(), server
    )
    
    port = os.getenv('STATISTICS_PORT', '50055')
    server.add_insecure_port(f'0.0.0.0:{port}')
    server.start()
    
    print("="*70, flush=True)
    print(f"Statistics Service (Statistical Analysis) started on 0.0.0.0:{port}", flush=True)
    print("Terminal Service - Returns final results", flush=True)
    print("="*70, flush=True)
    
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
