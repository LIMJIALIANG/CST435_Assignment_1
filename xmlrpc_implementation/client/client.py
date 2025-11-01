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
    print("MICROSERVICES CLIENT")
    print("="*70)
    print(f"Architecture: 3 Connected Services (MapReduce→MergeSort→Statistics)")
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
        
        print(f"[Client] ✓ Loaded {len(students)} students")
        
        # Display workflow
        print("\n" + "="*70)
        print("MICROSERVICES WORKFLOW")
        print("="*70)
        print("Chain: Client → MapReduce → MergeSort → Statistics → Client")
        print("="*70 + "\n")
        
        print("[Client] Starting workflow...")
        print(f"[Client] Sending request to MapReduce Service ({mapreduce_url})")
        
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
        
        # Display results in consistent format
        print("\n" + "="*70)
        print("WORKFLOW COMPLETED - ALL RESULTS")
        print("="*70)
        
        # MapReduce Service Results
        print(f"\n[MapReduce Service] CGPA Classification (Time: {mapreduce_time:.4f}s)")
        print("-" * 70)
        print(f"  CGPA Classification:")
        for grade_range, count in results['mapreduce']['cgpa_classification'].items():
            print(f"    {grade_range}: {count} students")
        
        # MergeSort Service Results
        print(f"\n[MergeSort Service] Sort by CGPA (Time: {mergesort_time:.4f}s)")
        print("-" * 70)
        print(f"  Top 10 students by CGPA:")
        for i, student in enumerate(results['mergesort']['top_10'], 1):
            print(f"    {i}. {student['name']} - CGPA: {student['cgpa']:.2f} ({student['grade']})")
        
        # Statistics Service Results
        print(f"\n[Statistics Service] Statistical Analysis (Time: {statistics_time:.4f}s)")
        print("-" * 70)
        stats = results['statistics']['result']
        
        # Handle different statistics structure
        if 'cgpa' in stats and 'distribution' in stats:
            # Structure from calculate_statistics
            cgpa_stats = stats['cgpa']
            distribution = stats['distribution']
            
            # Display mean CGPA
            print(f"  Mean CGPA: {cgpa_stats['mean']:.4f}")
            
            # Calculate pass rate (CGPA >= 2.0)
            pass_rate = sum(1 for s in students if s['cgpa'] >= 2.0) / len(students) * 100 if students else 0.0
            print(f"  Pass Rate: {pass_rate:.2f}%")
            
            print(f"\n  Faculty Statistics:")
            # Calculate average CGPA per faculty
            faculty_cgpa = {}
            for student in students:
                faculty = student['faculty']
                if faculty not in faculty_cgpa:
                    faculty_cgpa[faculty] = []
                faculty_cgpa[faculty].append(student['cgpa'])
            
            for faculty in sorted(faculty_cgpa.keys()):
                cgpa_list = faculty_cgpa[faculty]
                avg_cgpa = sum(cgpa_list) / len(cgpa_list)
                count = distribution['by_faculty'][faculty]
                print(f"    {faculty}: Avg CGPA {avg_cgpa:.2f} ({count} students)")
            
            print(f"\n  Grade Distribution:")
            total_students = distribution['total_students']
            for grade in sorted(distribution['by_grade'].keys()):
                count = distribution['by_grade'][grade]
                percentage = (count / total_students * 100) if total_students > 0 else 0.0
                print(f"    Grade {grade}: {count} students ({percentage:.1f}%)")
        else:
            # Fallback for other structures
            print(f"  Statistics: {stats}")
        
        # Performance summary
        print(f"\n{'='*70}")
        print("PERFORMANCE SUMMARY")
        print("="*70)
        print(f"MapReduce Time:        {mapreduce_time:.4f}s")
        print(f"MergeSort Time:        {mergesort_time:.4f}s")
        print(f"Statistics Time:       {statistics_time:.4f}s")
        print(f"Total Processing:      {total_processing_time:.4f}s")
        print(f"End-to-End Time:       {workflow_time:.4f}s")
        print(f"Network Overhead:      {network_overhead:.4f}s")
        
        print(f"\n{'='*70}")
        print("✓ All services (MapReduce→MergeSort→Statistics) completed successfully!")
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
