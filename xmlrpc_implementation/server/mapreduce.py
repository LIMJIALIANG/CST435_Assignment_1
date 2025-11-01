"""
XML-RPC MapReduce Service: CGPA and Grade Count
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


class MapReduceServiceHandler:
    """MapReduce Service: CGPA and Grade Count using MapReduce"""
    
    def __init__(self, next_service_url):
        self.next_service_url = next_service_url
        print(f"[MapReduce Service] Initialized. Next service: {next_service_url}")
    
    def process(self, students_data, accumulated_results):
        """
        Process CGPA classification and forward to next service
        Args:
            students_data: List of student dictionaries
            accumulated_results: Dictionary containing results from previous services
        Returns:
            Dictionary with accumulated results including this service's output
        """
        try:
            print(f"[MapReduce Service] Processing {len(students_data)} students...")
            
            # Convert dictionaries to StudentObject instances
            students = [StudentObject(**student) for student in students_data]
            
            # Perform MapReduce for CGPA classification
            print(f"[MapReduce] CGPA Classification")
            start_time = time.time()
            cgpa_result = MapReduceService.perform_mapreduce(students)
            processing_time = time.time() - start_time
            
            print(f"[MapReduce] Processed {len(students_data)} students")
            print(f"[MapReduce] Results: {cgpa_result['cgpa_classification']}")
            print(f"[MapReduce] Processing time: {processing_time:.4f} seconds")
            
            # Ensure all values are XML-RPC serializable
            cgpa_classification = {}
            for k, v in cgpa_result['cgpa_classification'].items():
                cgpa_classification[str(k)] = int(v)
            
            # Add this service's results to accumulated results
            accumulated_results['mapreduce'] = {
                'cgpa_classification': cgpa_classification,
                'processing_time': processing_time
            }
            
            print(f"[MapReduce Service] ✓ CGPA Classification completed in {processing_time:.4f}s")
            print(f"[MapReduce Service] Forwarding to MergeSort Service...")
            
            # Forward to next service in chain
            next_service = ServerProxy(self.next_service_url, allow_none=True)
            final_results = next_service.process(students_data, accumulated_results)
            
            return final_results
            
        except Exception as e:
            print(f"[MapReduce Service] Error: {str(e)}")
            raise


def main():
    """Start MapReduce Service server"""
    host = os.getenv('MAPREDUCE_HOST', 'localhost')
    port = int(os.getenv('MAPREDUCE_PORT', '8001'))
    mergesort_url = os.getenv('MERGESORT_URL', 'http://localhost:8003')
    
    # Create server
    server = SimpleXMLRPCServer((host, port), allow_none=True, logRequests=False)
    server.register_introspection_functions()
    
    # Register service instance
    mapreduce_service = MapReduceServiceHandler(mergesort_url)
    server.register_instance(mapreduce_service)
    
    print("="*70)
    print(f"MapReduce Service (CGPA + Grade Count) started on {host}:{port}")
    print(f"Next service: {mergesort_url}")
    print("Operations: CGPA Classification, Grade Distribution")
    print("="*70)
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n[MapReduce Service] Shutting down...")


if __name__ == '__main__':
    main()
