"""
XML-RPC Client for Chained Microservices Architecture
Calls only Service A, which triggers the entire chain
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
    
    def __init__(self, service_a_url):
        """
        Initialize client
        Args:
            service_a_url: URL of Service A (entry point)
        """
        self.service_a_url = service_a_url
        self.service_a = None
        print(f"[Client] Initialized with Service A URL: {service_a_url}")
    
    def connect(self):
        """Connect to Service A"""
        try:
            self.service_a = ServerProxy(self.service_a_url, allow_none=True)
            # Test connection
            self.service_a.system.listMethods()
            print(f"[Client] Connected to Service A at {self.service_a_url}")
        except Exception as e:
            print(f"[Client] Failed to connect to Service A: {str(e)}")
            raise
    
    def disconnect(self):
        """Disconnect from server"""
        if self.service_a:
            self.service_a = None
            print("[Client] Disconnected from Service A")
    
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
        Start the microservices workflow by calling Service A
        Service A will automatically chain to B → C → D → E
        
        Args:
            students: List of student dictionaries
        Returns:
            Dictionary containing all service results
        """
        try:
            print("\n[Client] Starting chained workflow...")
            print("[Client] Calling Service A...")
            
            # Call Service A with empty accumulated_results
            # Service A will chain through all services
            accumulated_results = {}
            
            workflow_start = time.time()
            final_results = self.service_a.process(students, accumulated_results)
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
    service_a_url = os.getenv('SERVICE_A_URL', 'http://localhost:8001')
    csv_path = os.getenv('CSV_PATH', '../data/students.csv')
    output_file = os.getenv('OUTPUT_FILE', '../results/xmlrpc_performance_metrics.json')
    
    print("\n" + "="*70)
    print("XML-RPC CHAINED MICROSERVICES CLIENT")
    print("="*70)
    print(f"Service A URL: {service_a_url}")
    print(f"CSV Path: {csv_path}")
    print(f"Output File: {output_file}")
    print("="*70 + "\n")
    
    # Create output directory if it doesn't exist
    output_dir = os.path.dirname(output_file)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Create client
    client = ChainedXMLRPCClient(service_a_url)
    
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
        print("Architecture: Client → A → B → C → D → E → Client")
        print("Operations: CGPA Count → Grade Count → Sort CGPA → Sort Grade → Statistics")
        print("="*70 + "\n")
        
        # Start workflow (single call to Service A)
        workflow_result = client.start_workflow(students)
        
        # Extract results
        results = workflow_result['results']
        workflow_time = workflow_result['workflow_time']
        
        # Calculate metrics
        service_a_time = results['service_a']['processing_time']
        service_b_time = results['service_b']['processing_time']
        service_c_time = results['service_c']['processing_time']
        service_d_time = results['service_d']['processing_time']
        service_e_time = results['service_e']['processing_time']
        
        total_processing_time = (service_a_time + service_b_time + 
                                service_c_time + service_d_time + service_e_time)
        network_overhead = workflow_time - total_processing_time
        
        # Display results
        print("\n" + "="*70)
        print("SERVICE RESULTS")
        print("="*70)
        print(f"\nService A (CGPA Count):")
        print(f"  Result: {results['service_a']['result']}")
        print(f"  Time: {service_a_time:.4f}s")
        
        print(f"\nService B (Grade Count):")
        print(f"  Result: {results['service_b']['result']}")
        print(f"  Time: {service_b_time:.4f}s")
        
        print(f"\nService C (Sort CGPA):")
        print(f"  Sorted: {results['service_c']['result']['sorted_count']} students")
        print(f"  Time: {service_c_time:.4f}s")
        
        print(f"\nService D (Sort Grade):")
        print(f"  Sorted: {results['service_d']['result']['sorted_count']} students")
        print(f"  Time: {service_d_time:.4f}s")
        
        print(f"\nService E (Statistics):")
        print(f"  Result: {results['service_e']['result']}")
        print(f"  Time: {service_e_time:.4f}s")
        
        # Performance summary
        print("\n" + "="*70)
        print("PERFORMANCE SUMMARY")
        print("="*70)
        print(f"Service A Time (CGPA):      {service_a_time:.4f}s")
        print(f"Service B Time (Grade):     {service_b_time:.4f}s")
        print(f"Service C Time (Sort CGPA): {service_c_time:.4f}s")
        print(f"Service D Time (Sort Grade):{service_d_time:.4f}s")
        print(f"Service E Time (Stats):     {service_e_time:.4f}s")
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
            'service_a_url': service_a_url,
            'workflow_time': workflow_time,
            'service_a_time': service_a_time,
            'service_b_time': service_b_time,
            'service_c_time': service_c_time,
            'service_d_time': service_d_time,
            'service_e_time': service_e_time,
            'total_processing_time': total_processing_time,
            'network_overhead': network_overhead,
            'summary': {
                'total_services': 5,
                'avg_service_time': total_processing_time / 5,
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
