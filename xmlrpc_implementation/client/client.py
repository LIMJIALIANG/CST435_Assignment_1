"""
XML-RPC Client for Chained Microservices Architecture
Calls only MapReduce Service, which triggers the entire chain
"""
from xmlrpc.client import ServerProxy
import json
import os
import sys
import time
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))


class ChainedXMLRPCClient:
    """Client for chained XML-RPC microservices"""
    
    def __init__(self, mapreduce_url):
        """
        Initialize client
        Args:
            mapreduce_url: URL of MapReduce Service (entry point)
        """
        self.mapreduce_url = mapreduce_url
        self.mapreduce_service = None
        print(f"[Client] Initialized with MapReduce Service URL: {mapreduce_url}")
    
    def connect(self):
        """Connect to MapReduce Service"""
        try:
            self.mapreduce_service = ServerProxy(self.mapreduce_url, allow_none=True)
            # Test connection
            self.mapreduce_service.system.listMethods()
            print(f"[Client] Connected to MapReduce Service at {self.mapreduce_url}")
        except Exception as e:
            print(f"[Client] Failed to connect to MapReduce Service: {str(e)}")
            raise
    
    def disconnect(self):
        """Disconnect from server"""
        if self.mapreduce_service:
            self.mapreduce_service = None
            print("[Client] Disconnected from MapReduce Service")
    
    def load_students_from_csv(self, csv_path):
        """
        Load students from CSV file
        Args:
            csv_path: Path to CSV file
        Returns:
            List of student dictionaries
        """
        try:
            print(f"[Client] Loading students from {csv_path}")
            students = []
            
            with open(csv_path, 'r') as file:
                lines = file.readlines()
                
                # Skip header (student_id,name,faculty,cgpa,grade)
                for line in lines[1:]:
                    parts = line.strip().split(',')
                    if len(parts) >= 5:
                        student = {
                            'student_id': parts[0].strip(),
                            'name': parts[1].strip(),
                            'faculty': parts[2].strip(),
                            'cgpa': float(parts[3].strip()),
                            'grade': parts[4].strip()
                        }
                        students.append(student)
            
            print(f"[Client] Loaded {len(students)} students")
            return students
            
        except Exception as e:
            print(f"[Client] Error loading CSV: {str(e)}")
            raise
    
    def start_workflow(self, students):
        """
        Start the microservices workflow by calling MapReduce Service
        MapReduce Service will automatically chain to MergeSort → Statistics
        
        Args:
            students: List of student dictionaries
        Returns:
            Dictionary containing all service results
        """
        try:
            print("\n[Client] Starting chained workflow...")
            print("[Client] Calling MapReduce Service...")
            
            # Call MapReduce Service with empty accumulated_results
            # MapReduce Service will chain through all services
            accumulated_results = {}
            
            workflow_start = time.time()
            final_results = self.mapreduce_service.process(students, accumulated_results)
            workflow_end = time.time()
            
            workflow_time = workflow_end - workflow_start
            
            print(f"\n[Client] Workflow completed in {workflow_time:.4f}s")
            
            return {
                'results': final_results,
                'workflow_time': workflow_time
            }
            
        except Exception as e:
            print(f"[Client] Error in workflow: {str(e)}")
            raise


def main():
    """Main execution"""
    # Configuration
    mapreduce_url = os.getenv('MAPREDUCE_URL', 'http://localhost:8001')
    csv_path = os.getenv('CSV_PATH', '../data/students.csv')
    output_file = os.getenv('OUTPUT_FILE', '../results/xmlrpc_performance_metrics.json')
    
    print("\n" + "="*70)
    print("XML-RPC CHAINED MICROSERVICES CLIENT")
    print("="*70)
    print(f"MapReduce Service URL: {mapreduce_url}")
    print(f"CSV Path: {csv_path}")
    print(f"Output File: {output_file}")
    print("="*70 + "\n")
    
    # Create output directory if it doesn't exist
    output_dir = os.path.dirname(output_file)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Create client
    client = ChainedXMLRPCClient(mapreduce_url)
    
    try:
        # Connect
        client.connect()
        
        # Load students
        students = client.load_students_from_csv(csv_path)
        
        if not students:
            print("[Client] No student data loaded. Exiting.")
            return
        
        # Display workflow
        print("\n" + "="*70)
        print("XML-RPC MICROSERVICES WORKFLOW")
        print("="*70)
        print("Architecture: Client → MapReduce → MergeSort → Statistics → Client")
        print("Operations: CGPA Classification → Sort by CGPA → Statistical Analysis")
        print("="*70 + "\n")
        
        # Start workflow (single call to MapReduce Service)
        workflow_result = client.start_workflow(students)
        
        # Extract results
        results = workflow_result['results']
        workflow_time = workflow_result['workflow_time']
        
        # Calculate metrics
        mapreduce_time = results['mapreduce']['processing_time']
        mergesort_time = results['mergesort']['processing_time']
        statistics_time = results['statistics']['processing_time']
        
        total_processing_time = mapreduce_time + mergesort_time + statistics_time
        network_overhead = workflow_time - total_processing_time
        
        # Display results
        print("\n" + "="*70)
        print("SERVICE RESULTS")
        print("="*70)
        print(f"\nMapReduce Service (CGPA Classification):")
        print(f"  Result: {results['mapreduce']['cgpa_classification']}")
        print(f"  Time: {mapreduce_time:.4f}s")
        
        print(f"\nMergeSort Service (Sort by CGPA):")
        print(f"  Sorted: {results['mergesort']['sorted_count']} students")
        print(f"  Time: {mergesort_time:.4f}s")
        
        print(f"\nStatistics Service:")
        print(f"  Result: {results['statistics']['result']}")
        print(f"  Time: {statistics_time:.4f}s")
        
        # Performance summary
        print("\n" + "="*70)
        print("PERFORMANCE SUMMARY")
        print("="*70)
        print(f"MapReduce Time:             {mapreduce_time:.4f}s")
        print(f"MergeSort Time:             {mergesort_time:.4f}s")
        print(f"Statistics Time:            {statistics_time:.4f}s")
        print(f"Total Processing:           {total_processing_time:.4f}s")
        print(f"End-to-End Time:            {workflow_time:.4f}s")
        print(f"Network Overhead:           {network_overhead:.4f}s")
        print(f"Overhead %:                 {(network_overhead/workflow_time*100):.2f}%")
        print("="*70 + "\n")
        
        # Save metrics
        metrics_output = {
            'timestamp': datetime.now().isoformat(),
            'protocol': 'XML-RPC',
            'architecture': 'microservices_chained',
            'mapreduce_url': mapreduce_url,
            'workflow_time': workflow_time,
            'mapreduce_time': mapreduce_time,
            'mergesort_time': mergesort_time,
            'statistics_time': statistics_time,
            'total_processing_time': total_processing_time,
            'network_overhead': network_overhead,
            'summary': {
                'total_services': 3,
                'avg_service_time': total_processing_time / 3,
                'overhead_percentage': (network_overhead / workflow_time) * 100
            },
            'detailed_results': results
        }
        
        output_path = os.path.abspath(output_file)
        with open(output_path, 'w') as f:
            json.dump(metrics_output, f, indent=2)
        
        print(f"[Client] Performance metrics saved to {output_path}")
        
    except Exception as e:
        print(f"[Client] Error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    finally:
        client.disconnect()


if __name__ == '__main__':
    main()
