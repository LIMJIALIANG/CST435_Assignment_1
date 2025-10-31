"""
XML-RPC Service A: MapReduce - CGPA Count
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


class ServiceA:
    """Service A: CGPA Count using MapReduce"""
    
    def __init__(self, next_service_url):
        self.next_service_url = next_service_url
        print(f"[Service A] Initialized. Next service: {next_service_url}")
    
    def process(self, students_data, accumulated_results):
        """
        Process CGPA count and forward to next service
        Args:
            students_data: List of student dictionaries
            accumulated_results: Dictionary containing results from previous services
        Returns:
            Dictionary with accumulated results including this service's output
        """
        try:
            print(f"[Service A] Processing {len(students_data)} students...")
            start_time = time.time()
            
            # Convert dictionaries to StudentObject instances
            students = [StudentObject(**student) for student in students_data]
            
            # Perform MapReduce for CGPA count
            result = MapReduceService.perform_mapreduce(students, "cgpa_count")
            
            processing_time = time.time() - start_time
            
            # Ensure all values are XML-RPC serializable
            cgpa_result = {}
            for k, v in result['result'].items():
                cgpa_result[str(k)] = int(v)
            
            # Add this service's result to accumulated results
            accumulated_results['service_a'] = {
                'operation': 'cgpa_count',
                'result': cgpa_result,
                'processing_time': processing_time
            }
            
            print(f"[Service A] Completed in {processing_time:.4f}s")
            print(f"[Service A] Result: {result}")
            print(f"[Service A] Forwarding to Service B...")
            
            # Forward to next service in chain
            next_service = ServerProxy(self.next_service_url, allow_none=True)
            return next_service.process(students_data, accumulated_results)
            
        except Exception as e:
            print(f"[Service A] Error: {str(e)}")
            raise


def main():
    """Start Service A server"""
    host = os.getenv('SERVICE_A_HOST', 'localhost')
    port = int(os.getenv('SERVICE_A_PORT', '8001'))
    service_b_url = os.getenv('SERVICE_B_URL', 'http://localhost:8002')
    
    # Create server
    server = SimpleXMLRPCServer((host, port), allow_none=True, logRequests=False)
    server.register_introspection_functions()
    
    # Register service instance
    service = ServiceA(service_b_url)
    server.register_instance(service)
    
    print("="*70)
    print(f"Service A (CGPA Count) started on {host}:{port}")
    print(f"Next service: {service_b_url}")
    print("="*70)
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n[Service A] Shutting down...")


if __name__ == '__main__':
    main()
