"""
XML-RPC Service D: MergeSort by Grade
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


class ServiceD:
    """Service D: Sort by Grade using MergeSort"""
    
    def __init__(self, next_service_url):
        self.next_service_url = next_service_url
        print(f"[Service D] Initialized. Next service: {next_service_url}")
    
    def process(self, students_data, accumulated_results):
        """
        Process sort by Grade and forward to next service
        Args:
            students_data: List of student dictionaries
            accumulated_results: Dictionary containing results from previous services
        Returns:
            Dictionary with accumulated results including this service's output
        """
        try:
            print(f"[Service D] Received from Service C")
            print(f"[Service D] Processing {len(students_data)} students...")
            start_time = time.time()
            
            # Convert dictionaries to StudentObject instances
            students = [StudentObject(**student) for student in students_data]
            
            # Perform MergeSort by Grade
            result = MergeSortService.perform_sort(students, "grade")
            sorted_students = result['sorted_students']
            
            processing_time = time.time() - start_time
            
            # Convert sorted students back to dictionaries for transmission
            sorted_data = [
                {
                    'student_id': str(s.student_id),
                    'name': str(s.name),
                    'faculty': str(s.faculty) if hasattr(s, 'faculty') and s.faculty else '',
                    'cgpa': float(s.cgpa),
                    'grade': str(s.grade)
                }
                for s in sorted_students[:5]  # Top 5 for display
            ]
            
            # Add this service's result to accumulated results
            accumulated_results['service_d'] = {
                'operation': 'sort_by_grade',
                'result': {
                    'sorted_count': len(sorted_students),
                    'top_5': sorted_data
                },
                'processing_time': processing_time
            }
            
            print(f"[Service D] Completed in {processing_time:.4f}s")
            print(f"[Service D] Sorted {len(sorted_students)} students by Grade")
            print(f"[Service D] Forwarding to Service E...")
            
            # Forward to next service in chain (final service)
            next_service = ServerProxy(self.next_service_url, allow_none=True)
            return next_service.process(students_data, accumulated_results)
            
        except Exception as e:
            print(f"[Service D] Error: {str(e)}")
            raise


def main():
    """Start Service D server"""
    host = os.getenv('SERVICE_D_HOST', 'localhost')
    port = int(os.getenv('SERVICE_D_PORT', '8004'))
    service_e_url = os.getenv('SERVICE_E_URL', 'http://localhost:8005')
    
    # Create server
    server = SimpleXMLRPCServer((host, port), allow_none=True, logRequests=False)
    server.register_introspection_functions()
    
    # Register service instance
    service = ServiceD(service_e_url)
    server.register_instance(service)
    
    print("="*70)
    print(f"Service D (Sort by Grade) started on {host}:{port}")
    print(f"Next service: {service_e_url}")
    print("="*70)
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n[Service D] Shutting down...")


if __name__ == '__main__':
    main()
