"""
XML-RPC MergeSort Service: Sort by CGPA and Grade
Chained Microservices Architecture
"""
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.client import ServerProxy
import sys
import os
import time

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from services.mergesort_service import MergeSortService


class StudentObject:
    """Helper class to convert dict to object with attributes"""
    def __init__(self, student_id, name, cgpa, grade, faculty=None):
        self.student_id = student_id
        self.name = name
        self.cgpa = cgpa
        self.grade = grade
        self.faculty = faculty


class MergeSortServiceHandler:
    """MergeSort Service: Sort by CGPA and Grade using MergeSort"""
    
    def __init__(self, next_service_url):
        self.next_service_url = next_service_url
        print(f"[MergeSort Service] Initialized. Next service: {next_service_url}")
    
    def process(self, students_data, accumulated_results):
        """
        Process sort by CGPA and forward to next service
        Args:
            students_data: List of student dictionaries
            accumulated_results: Dictionary containing results from previous services
        Returns:
            Dictionary with accumulated results including this service's output
        """
        try:
            print(f"[MergeSort Service] Received from MapReduce Service")
            print(f"[MergeSort Service] Processing {len(students_data)} students...")
            
            # Convert dictionaries to StudentObject instances
            students = [StudentObject(**student) for student in students_data]
            
            # Perform MergeSort by CGPA
            print(f"[MergeSort Service] Performing MergeSort by CGPA...")
            print(f"[MergeSort] Sort by CGPA")
            start_time = time.time()
            sort_result = MergeSortService.perform_sort(students)
            sorted_students = sort_result['sorted_students']
            processing_time = time.time() - start_time
            
            print(f"[MergeSort] Sorted {len(sorted_students)} students")
            if sorted_students:
                print(f"[MergeSort] Top student: {sorted_students[0].name} (CGPA: {sorted_students[0].cgpa:.2f})")
            print(f"[MergeSort] Processing time: {processing_time:.4f} seconds")
            
            # Convert sorted students to dictionaries (Top 10 for display)
            sorted_data = [
                {
                    'student_id': str(s.student_id),
                    'name': str(s.name),
                    'faculty': str(s.faculty) if hasattr(s, 'faculty') and s.faculty else '',
                    'cgpa': float(s.cgpa),
                    'grade': str(s.grade)
                }
                for s in sorted_students[:10]
            ]
            
            # Add MergeSort Service result to accumulated results
            accumulated_results['mergesort'] = {
                'sorted_count': len(sorted_students),
                'top_10': sorted_data,
                'processing_time': processing_time
            }
            
            print(f"[MergeSort Service] Sort completed in {processing_time:.4f}s")
            print(f"[MergeSort Service] Forwarding to Statistics Service...")
            
            # Forward to next service in chain
            next_service = ServerProxy(self.next_service_url, allow_none=True)
            final_results = next_service.process(students_data, accumulated_results)
            
            return final_results
            
        except Exception as e:
            print(f"[MergeSort Service] Error: {str(e)}")
            raise


def main():
    """Start MergeSort Service server"""
    host = os.getenv('MERGESORT_HOST', 'localhost')
    port = int(os.getenv('MERGESORT_PORT', '8003'))
    statistics_url = os.getenv('STATISTICS_URL', 'http://localhost:8005')
    
    # Create server
    server = SimpleXMLRPCServer((host, port), allow_none=True, logRequests=False)
    server.register_introspection_functions()
    
    # Register MergeSort Service
    mergesort_service = MergeSortServiceHandler(statistics_url)
    server.register_instance(mergesort_service)
    
    print("=" * 60)
    print("XML-RPC MERGESORT SERVICE: Sort CGPA + Grade")
    print("Operations: Sort by CGPA, Sort by Grade")
    print(f"Server running on {host}:{port}")
    print(f"Next service: {statistics_url}")
    print("=" * 60)
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n[MergeSort Service] Shutting down...")


if __name__ == '__main__':
    main()

