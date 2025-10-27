"""
gRPC Server Implementation
Provides student analysis services via gRPC
"""

import sys
import os
import grpc
from concurrent import futures
import time

# Add paths for generated code
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'generated'))

# Import generated gRPC code
import student_service_pb2
import student_service_pb2_grpc

# Import service implementations
from services.mapreduce_service import MapReduceService
from services.mergesort_service import MergeSortService
from services.stats_service import StatsService


class StudentAnalysisServicer(student_service_pb2_grpc.StudentAnalysisServiceServicer):
    """
    gRPC Servicer implementation for Student Analysis
    """
    
    def PerformMapReduce(self, request, context):
        """Handle MapReduce requests"""
        print(f"\n[Server] Received MapReduce request: {request.operation}")
        print(f"[Server] Number of students: {len(request.students)}")
        
        try:
            # Perform MapReduce operation
            result = MapReduceService.perform_mapreduce(
                list(request.students),
                request.operation
            )
            
            # Build response
            response = student_service_pb2.MapReduceResponse()
            response.processing_time = result['processing_time']
            
            if request.operation == "cgpa_count":
                for range_key, count in result['result'].items():
                    cgpa_range = response.cgpa_ranges.add()
                    cgpa_range.range = range_key
                    cgpa_range.count = count
            elif request.operation == "grade_count":
                for grade, count in result['result'].items():
                    grade_count = response.grade_counts.add()
                    grade_count.grade = grade
                    grade_count.count = count
            
            print(f"[Server] MapReduce completed successfully\n")
            return response
            
        except Exception as e:
            print(f"[Server] Error in MapReduce: {str(e)}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"MapReduce error: {str(e)}")
            return student_service_pb2.MapReduceResponse()
    
    def PerformMergeSort(self, request, context):
        """Handle MergeSort requests"""
        print(f"\n[Server] Received MergeSort request: sort by {request.sort_by}")
        print(f"[Server] Number of students: {len(request.students)}")
        
        try:
            # Perform merge sort
            result = MergeSortService.perform_sort(
                list(request.students),
                request.sort_by
            )
            
            # Build response
            response = student_service_pb2.MergeSortResponse()
            response.processing_time = result['processing_time']
            
            for student in result['sorted_students']:
                response.sorted_students.append(student)
            
            print(f"[Server] MergeSort completed successfully\n")
            return response
            
        except Exception as e:
            print(f"[Server] Error in MergeSort: {str(e)}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"MergeSort error: {str(e)}")
            return student_service_pb2.MergeSortResponse()
    
    def PerformStatisticalAnalysis(self, request, context):
        """Handle Statistical Analysis requests"""
        print(f"\n[Server] Received Statistics request: {request.analysis_type}")
        print(f"[Server] Number of students: {len(request.students)}")
        
        try:
            # Perform statistical analysis
            result = StatsService.perform_analysis(
                list(request.students),
                request.analysis_type
            )
            
            # Build response
            response = student_service_pb2.StatsResponse()
            response.processing_time = result['processing_time']
            response.pass_rate = result['pass_rate']
            
            for faculty_stat in result['faculty_stats']:
                stat = response.faculty_stats.add()
                stat.faculty = faculty_stat['faculty']
                stat.average_cgpa = faculty_stat['average_cgpa']
                stat.student_count = faculty_stat['student_count']
            
            for grade_dist in result['grade_distribution']:
                dist = response.grade_distribution.add()
                dist.grade = grade_dist['grade']
                dist.count = grade_dist['count']
                dist.percentage = grade_dist['percentage']
            
            print(f"[Server] Statistics completed successfully\n")
            return response
            
        except Exception as e:
            print(f"[Server] Error in Statistics: {str(e)}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Statistics error: {str(e)}")
            return student_service_pb2.StatsResponse()


def serve(port=50051):
    """Start the gRPC server"""
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    student_service_pb2_grpc.add_StudentAnalysisServiceServicer_to_server(
        StudentAnalysisServicer(), server
    )
    
    server.add_insecure_port(f'[::]:{port}')
    server.start()
    
    print("=" * 60)
    print("Student Analysis gRPC Server")
    print("=" * 60)
    print(f"Server started on port {port}")
    print("Waiting for client requests...")
    print("Press Ctrl+C to stop\n")
    
    try:
        while True:
            time.sleep(86400)  # Keep server running
    except KeyboardInterrupt:
        print("\n[Server] Shutting down...")
        server.stop(0)


if __name__ == '__main__':
    serve()
