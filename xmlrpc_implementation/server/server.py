"""
XML-RPC Server Implementation
Provides student analysis services via XML-RPC
"""

import sys
import os
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
import time

# Add project root to path for shared services
current_dir = os.path.dirname(os.path.abspath(__file__))
xmlrpc_impl_dir = os.path.dirname(current_dir)
project_root = os.path.dirname(xmlrpc_impl_dir)
sys.path.insert(0, project_root)

# Import service implementations from shared services folder
from services.mapreduce_service import MapReduceService
from services.mergesort_service import MergeSortService
from services.stats_service import StatsService


class StudentObject:
    """Helper class to convert dict to object with attributes"""
    def __init__(self, data):
        self.student_id = data['student_id']
        self.name = data['name']
        self.faculty = data['faculty']
        self.cgpa = float(data['cgpa'])
        self.grade = data['grade']


class RequestHandler(SimpleXMLRPCRequestHandler):
    """Custom request handler to restrict to specific paths"""
    rpc_paths = ('/RPC2',)


class StudentAnalysisServer:
    """
    XML-RPC Server implementation for Student Analysis
    """
    
    def perform_mapreduce(self, students_data, operation):
        """
        Handle MapReduce requests
        
        Args:
            students_data: List of student dictionaries
            operation: "cgpa_count" or "grade_count"
        
        Returns:
            Dictionary with results and processing_time
        """
        print(f"\n[XML-RPC Server] Received MapReduce request: {operation}")
        print(f"[XML-RPC Server] Number of students: {len(students_data)}")
        
        try:
            # Convert dictionaries to objects
            students = [StudentObject(s) for s in students_data]
            
            # Perform MapReduce operation
            result = MapReduceService.perform_mapreduce(students, operation)
            
            print(f"[XML-RPC Server] MapReduce completed successfully\n")
            
            return {
                'success': True,
                'result': result['result'],
                'processing_time': result['processing_time']
            }
            
        except Exception as e:
            print(f"[XML-RPC Server] Error in MapReduce: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'processing_time': 0.0
            }
    
    def perform_mergesort(self, students_data, sort_by):
        """
        Handle MergeSort requests
        
        Args:
            students_data: List of student dictionaries
            sort_by: "cgpa" or "name"
        
        Returns:
            Dictionary with sorted students and processing_time
        """
        print(f"\n[XML-RPC Server] Received MergeSort request: sort by {sort_by}")
        print(f"[XML-RPC Server] Number of students: {len(students_data)}")
        
        try:
            # Convert dictionaries to objects
            students = [StudentObject(s) for s in students_data]
            
            # Perform merge sort
            result = MergeSortService.perform_sort(students, sort_by)
            
            # Convert sorted students back to dictionaries
            sorted_students_dict = []
            for student in result['sorted_students']:
                sorted_students_dict.append({
                    'student_id': student.student_id,
                    'name': student.name,
                    'faculty': student.faculty,
                    'cgpa': student.cgpa,
                    'grade': student.grade
                })
            
            print(f"[XML-RPC Server] MergeSort completed successfully\n")
            
            return {
                'success': True,
                'sorted_students': sorted_students_dict,
                'processing_time': result['processing_time']
            }
            
        except Exception as e:
            print(f"[XML-RPC Server] Error in MergeSort: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'processing_time': 0.0
            }
    
    def perform_statistical_analysis(self, students_data):
        """
        Handle Statistical Analysis requests
        
        Args:
            students_data: List of student dictionaries
        
        Returns:
            Dictionary with statistics and processing_time
        """
        print(f"\n[XML-RPC Server] Received Statistical Analysis request")
        print(f"[XML-RPC Server] Number of students: {len(students_data)}")
        
        try:
            # Convert dictionaries to objects
            students = [StudentObject(s) for s in students_data]
            
            # Perform statistical analysis
            result = StatsService.calculate_statistics(students)
            
            print(f"[XML-RPC Server] Statistical Analysis completed successfully\n")
            
            return {
                'success': True,
                'statistics': result['statistics'],
                'processing_time': result['processing_time']
            }
            
        except Exception as e:
            print(f"[XML-RPC Server] Error in Statistical Analysis: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'processing_time': 0.0
            }
    
    def perform_filter(self, students_data, filter_type, value):
        """
        Handle Filter requests
        
        Args:
            students_data: List of student dictionaries
            filter_type: "faculty", "grade", or "min_cgpa"
            value: Filter value (faculty name, grade, or minimum CGPA)
        
        Returns:
            Dictionary with filtered students and processing_time
        """
        print(f"\n[XML-RPC Server] Received Filter request: {filter_type} = {value}")
        print(f"[XML-RPC Server] Number of students: {len(students_data)}")
        
        try:
            # Convert dictionaries to objects
            students = [StudentObject(s) for s in students_data]
            
            start_time = time.time()
            
            # Perform filtering
            if filter_type == "faculty":
                filtered = [s for s in students if s.faculty == value]
            elif filter_type == "grade":
                filtered = [s for s in students if s.grade == value]
            elif filter_type == "min_cgpa":
                filtered = [s for s in students if s.cgpa >= float(value)]
            else:
                raise ValueError(f"Unknown filter type: {filter_type}")
            
            processing_time = time.time() - start_time
            
            # Convert filtered students back to dictionaries
            filtered_dict = []
            for student in filtered:
                filtered_dict.append({
                    'student_id': student.student_id,
                    'name': student.name,
                    'faculty': student.faculty,
                    'cgpa': student.cgpa,
                    'grade': student.grade
                })
            
            print(f"[XML-RPC Server] Filter completed successfully\n")
            
            return {
                'success': True,
                'filtered_students': filtered_dict,
                'processing_time': processing_time
            }
            
        except Exception as e:
            print(f"[XML-RPC Server] Error in Filter: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'processing_time': 0.0
            }
    
    def search_student(self, students_data, search_term):
        """
        Handle Search requests
        
        Args:
            students_data: List of student dictionaries
            search_term: Student ID or name to search for
        
        Returns:
            Dictionary with found students and processing_time
        """
        print(f"\n[XML-RPC Server] Received Search request: {search_term}")
        print(f"[XML-RPC Server] Number of students: {len(students_data)}")
        
        try:
            # Convert dictionaries to objects
            students = [StudentObject(s) for s in students_data]
            
            start_time = time.time()
            
            # Perform search
            found = []
            search_lower = search_term.lower()
            for student in students:
                if (search_lower in student.student_id.lower() or 
                    search_lower in student.name.lower()):
                    found.append(student)
            
            processing_time = time.time() - start_time
            
            # Convert found students back to dictionaries
            found_dict = []
            for student in found:
                found_dict.append({
                    'student_id': student.student_id,
                    'name': student.name,
                    'faculty': student.faculty,
                    'cgpa': student.cgpa,
                    'grade': student.grade
                })
            
            print(f"[XML-RPC Server] Search completed successfully\n")
            
            return {
                'success': True,
                'found_students': found_dict,
                'processing_time': processing_time
            }
            
        except Exception as e:
            print(f"[XML-RPC Server] Error in Search: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'processing_time': 0.0
            }


def serve(host='0.0.0.0', port=8000):
    """Start the XML-RPC server"""
    print("="*60)
    print("Student Analysis XML-RPC Server")
    print("="*60)
    print(f"Starting server on {host}:{port}...")
    
    # Create server
    server = SimpleXMLRPCServer(
        (host, port),
        requestHandler=RequestHandler,
        allow_none=True
    )
    
    # Register introspection functions
    server.register_introspection_functions()
    
    # Register service instance
    service = StudentAnalysisServer()
    server.register_instance(service)
    
    print(f"Server is ready and listening on {host}:{port}")
    print("Available methods:")
    print("  - perform_mapreduce(students, operation)")
    print("  - perform_mergesort(students, sort_by)")
    print("  - perform_statistical_analysis(students)")
    print("  - perform_filter(students, filter_type, value)")
    print("  - search_student(students, search_term)")
    print("\nPress Ctrl+C to stop the server")
    print("="*60 + "\n")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n[XML-RPC Server] Shutting down...")
        server.server_close()


if __name__ == '__main__':
    serve()
