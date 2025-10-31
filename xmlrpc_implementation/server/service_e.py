"""
XML-RPC Service E: Statistical Analysis (Final Service)
Chained Microservices Architecture
"""
from xmlrpc.server import SimpleXMLRPCServer
import sys
import os
import time

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from services.stats_service import StatsService


class StudentObject:
    """Helper class to convert dict to object with attributes"""
    def __init__(self, student_id, name, cgpa, grade, faculty=None):
        self.student_id = student_id
        self.name = name
        self.cgpa = cgpa
        self.grade = grade
        self.faculty = faculty


class ServiceE:
    """Service E: Statistical Analysis (Terminal Service)"""
    
    def __init__(self):
        print(f"[Service E] Initialized (Terminal Service)")
    
    def process(self, students_data, accumulated_results):
        """
        Process statistical analysis and return final results
        Args:
            students_data: List of student dictionaries
            accumulated_results: Dictionary containing results from previous services
        Returns:
            Dictionary with all accumulated results including this service's output
        """
        try:
            print(f"[Service E] Received from Service D")
            print(f"[Service E] Processing {len(students_data)} students...")
            start_time = time.time()
            
            # Convert dictionaries to StudentObject instances
            students = [StudentObject(**student) for student in students_data]
            
            # Perform Statistical Analysis
            result = StatsService.calculate_statistics(students)
            
            processing_time = time.time() - start_time
            
            # Ensure statistics are XML-RPC serializable
            stats = result['statistics']
            serializable_stats = {}
            for key, value in stats.items():
                if isinstance(value, dict):
                    # Convert nested dictionaries (e.g., faculty_avg_cgpa)
                    serializable_stats[str(key)] = {str(k): v for k, v in value.items()}
                else:
                    serializable_stats[str(key)] = value
            
            # Add this service's result to accumulated results
            accumulated_results['service_e'] = {
                'operation': 'statistical_analysis',
                'result': serializable_stats,
                'processing_time': processing_time
            }
            
            print(f"[Service E] Completed in {processing_time:.4f}s")
            print(f"[Service E] Statistics calculated")
            print(f"[Service E] Returning final results to client...")
            
            # Return all accumulated results (terminal service)
            return accumulated_results
            
        except Exception as e:
            print(f"[Service E] Error: {str(e)}")
            raise


def main():
    """Start Service E server"""
    host = os.getenv('SERVICE_E_HOST', 'localhost')
    port = int(os.getenv('SERVICE_E_PORT', '8005'))
    
    # Create server
    server = SimpleXMLRPCServer((host, port), allow_none=True, logRequests=False)
    server.register_introspection_functions()
    
    # Register service instance
    service = ServiceE()
    server.register_instance(service)
    
    print("="*70)
    print(f"Service E (Statistical Analysis) started on {host}:{port}")
    print("Terminal Service - Returns final results")
    print("="*70)
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n[Service E] Shutting down...")


if __name__ == '__main__':
    main()
