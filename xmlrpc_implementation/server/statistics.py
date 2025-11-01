"""
XML-RPC Statistics Service: Statistical Analysis (Final Service)
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


class StatisticsServiceHandler:
    """Statistics Service: Statistical Analysis (Terminal Service)"""
    
    def __init__(self):
        print(f"[Statistics Service] Initialized (Terminal Service)")
    
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
            print(f"[Statistics Service] Received from MergeSort Service")
            print(f"[Statistics Service] Processing {len(students_data)} students...")
            
            # Convert dictionaries to StudentObject instances
            students = [StudentObject(**student) for student in students_data]
            
            # Perform Statistical Analysis
            print(f"[Statistics] Comprehensive analysis")
            start_time = time.time()
            result = StatsService.calculate_statistics(students)
            processing_time = time.time() - start_time
            
            print(f"[Statistics] Analyzed {len(students_data)} students")
            print(f"[Statistics] Mean CGPA: {result['statistics']['cgpa']['mean']:.4f}")
            print(f"[Statistics] Processing time: {processing_time:.4f} seconds")
            
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
            accumulated_results['statistics'] = {
                'operation': 'statistical_analysis',
                'result': serializable_stats,
                'processing_time': processing_time
            }
            
            print(f"[Statistics Service] Completed in {processing_time:.4f}s")
            print(f"[Statistics Service] Statistics calculated")
            print(f"[Statistics Service] Chain complete: MapReduce, MergeSort, Statistics processed")
            print(f"[Statistics Service] Returning final results to client...")
            
            # Return all accumulated results (terminal service)
            return accumulated_results
            
        except Exception as e:
            print(f"[Statistics Service] Error: {str(e)}")
            raise


def main():
    """Start Statistics Service server"""
    host = os.getenv('STATISTICS_HOST', 'localhost')
    port = int(os.getenv('STATISTICS_PORT', '8005'))
    
    # Create server
    server = SimpleXMLRPCServer((host, port), allow_none=True, logRequests=False)
    server.register_introspection_functions()
    
    # Register service instance
    statistics_service = StatisticsServiceHandler()
    server.register_instance(statistics_service)
    
    print("="*70)
    print(f"Statistics Service (Statistical Analysis) started on {host}:{port}")
    print("Terminal Service - Returns final results")
    print("="*70)
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n[Statistics Service] Shutting down...")


if __name__ == '__main__':
    main()
