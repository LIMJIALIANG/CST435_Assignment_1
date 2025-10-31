"""
XML-RPC Service B: MapReduce - Grade Count
Chained Microservices Architecture
"""
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.client import ServerProxy
import sys
import os
import time

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from services.mapreduce_service import MapReduceService


class StudentObject:
    """Helper class to convert dict to object with attributes"""
    def __init__(self, student_id, name, cgpa, grade, faculty=None):
        self.student_id = student_id
        self.name = name
        self.cgpa = cgpa
        self.grade = grade
        self.faculty = faculty


class ServiceB:
    """Service B: Grade Count using MapReduce"""
    
    def __init__(self, next_service_url):
        self.next_service_url = next_service_url
        print(f"[Service B] Initialized. Next service: {next_service_url}")
    
    def process(self, students_data, accumulated_results):
        """
        Process Grade count and forward to next service
        Args:
            students_data: List of student dictionaries
            accumulated_results: Dictionary containing results from previous services
        Returns:
            Dictionary with accumulated results including this service's output
        """
        try:
            print(f"[Service B] Received from Service A")
            print(f"[Service B] Processing {len(students_data)} students...")
            start_time = time.time()
            
            # Convert dictionaries to StudentObject instances
            students = [StudentObject(**student) for student in students_data]
            
            # Perform MapReduce for Grade count
            result = MapReduceService.perform_mapreduce(students, "grade_count")
            
            processing_time = time.time() - start_time
            
            # Ensure all values are XML-RPC serializable
            grade_result = {}
            for k, v in result['result'].items():
                grade_result[str(k)] = int(v)
            
            # Add this service's result to accumulated results
            accumulated_results['service_b'] = {
                'operation': 'grade_count',
                'result': grade_result,
                'processing_time': processing_time
            }
            
            print(f"[Service B] Completed in {processing_time:.4f}s")
            print(f"[Service B] Result: {result}")
            print(f"[Service B] Forwarding to Service C...")
            
            # Forward to next service in chain
            next_service = ServerProxy(self.next_service_url, allow_none=True)
            return next_service.process(students_data, accumulated_results)
            
        except Exception as e:
            print(f"[Service B] Error: {str(e)}")
            raise


def main():
    """Start Service B server"""
    host = os.getenv('SERVICE_B_HOST', 'localhost')
    port = int(os.getenv('SERVICE_B_PORT', '8002'))
    service_c_url = os.getenv('SERVICE_C_URL', 'http://localhost:8003')
    
    # Create server
    server = SimpleXMLRPCServer((host, port), allow_none=True, logRequests=False)
    server.register_introspection_functions()
    
    # Register service instance
    service = ServiceB(service_c_url)
    server.register_instance(service)
    
    print("="*70)
    print(f"Service B (Grade Count) started on {host}:{port}")
    print(f"Next service: {service_c_url}")
    print("="*70)
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n[Service B] Shutting down...")


if __name__ == '__main__':
    main()
