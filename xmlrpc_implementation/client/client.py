"""
XML-RPC Client Implementation
Triggers student analysis services and measures performance
"""

import sys
import os
import xmlrpc.client
import csv
import json
import time
from datetime import datetime


class StudentAnalysisClient:
    """
    XML-RPC Client for Student Analysis
    """
    
    def __init__(self, server_address='http://localhost:8000'):
        """Initialize client with server address"""
        self.server_address = server_address
        self.proxy = None
        self.performance_metrics = []
    
    def connect(self):
        """Establish connection to server"""
        print(f"[Client] Connecting to XML-RPC server at {self.server_address}...")
        self.proxy = xmlrpc.client.ServerProxy(self.server_address, allow_none=True)
        
        # Test connection
        try:
            methods = self.proxy.system.listMethods()
            print(f"[Client] Connected successfully!")
            print(f"[Client] Available methods: {len(methods)}")
            print(f"[Client] Connection established\n")
        except Exception as e:
            print(f"[Client] Connection failed: {str(e)}")
            raise
    
    def disconnect(self):
        """Close connection to server"""
        print("[Client] Disconnected from server")
    
    def load_students_from_csv(self, csv_path):
        """Load student data from CSV file"""
        students = []
        
        try:
            with open(csv_path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    student = {
                        'student_id': row['student_id'],
                        'name': row['name'],
                        'faculty': row['faculty'],
                        'cgpa': float(row['cgpa']),
                        'grade': row['grade']
                    }
                    students.append(student)
            
            print(f"[Client] Loaded {len(students)} students from {csv_path}\n")
            return students
            
        except Exception as e:
            print(f"[Client] Error loading CSV: {str(e)}")
            return []
    
    def call_mapreduce(self, students, operation):
        """Call MapReduce service"""
        print(f"{'='*60}")
        print(f"Calling MapReduce Service: {operation}")
        print(f"{'='*60}")
        
        start_time = time.time()
        
        try:
            response = self.proxy.perform_mapreduce(students, operation)
            
            end_time = time.time()
            total_time = end_time - start_time
            
            if response['success']:
                print(f"\n[Client] Results received:")
                
                if operation == "cgpa_count":
                    print("\nCGPA Range Distribution:")
                    for range_key, count in sorted(response['result'].items()):
                        print(f"  {range_key}: {count} students")
                elif operation == "grade_count":
                    print("\nGrade Distribution:")
                    for grade, count in sorted(response['result'].items()):
                        print(f"  Grade {grade}: {count} students")
                
                # Calculate network overhead
                server_time = response['processing_time']
                network_overhead = total_time - server_time
                
                print(f"\n[Client] Performance Metrics:")
                print(f"  Server Processing Time: {server_time:.6f} seconds")
                print(f"  Total Time (with network): {total_time:.6f} seconds")
                print(f"  Network Overhead: {network_overhead:.6f} seconds")
                print(f"{'='*60}\n")
                
                # Store metrics
                self.performance_metrics.append({
                    'service': 'MapReduce',
                    'operation': operation,
                    'server_time': server_time,
                    'total_time': total_time,
                    'network_overhead': network_overhead
                })
            else:
                print(f"[Client] Error: {response['error']}")
            
        except Exception as e:
            print(f"[Client] Error calling MapReduce: {str(e)}")
    
    def call_mergesort(self, students, sort_by):
        """Call MergeSort service"""
        print(f"{'='*60}")
        print(f"Calling MergeSort Service: sort by {sort_by}")
        print(f"{'='*60}")
        
        start_time = time.time()
        
        try:
            response = self.proxy.perform_mergesort(students, sort_by)
            
            end_time = time.time()
            total_time = end_time - start_time
            
            if response['success']:
                sorted_students = response['sorted_students']
                
                print(f"\n[Client] Received {len(sorted_students)} sorted students")
                print(f"\nTop 5 students (sorted by {sort_by}):")
                
                for i, student in enumerate(sorted_students[:5], 1):
                    print(f"  {i}. {student['name']:<30} "
                          f"CGPA: {student['cgpa']:.2f}  "
                          f"Grade: {student['grade']}")
                
                # Calculate network overhead
                server_time = response['processing_time']
                network_overhead = total_time - server_time
                
                print(f"\n[Client] Performance Metrics:")
                print(f"  Server Processing Time: {server_time:.6f} seconds")
                print(f"  Total Time (with network): {total_time:.6f} seconds")
                print(f"  Network Overhead: {network_overhead:.6f} seconds")
                print(f"{'='*60}\n")
                
                # Store metrics
                self.performance_metrics.append({
                    'service': 'MergeSort',
                    'operation': sort_by,
                    'server_time': server_time,
                    'total_time': total_time,
                    'network_overhead': network_overhead
                })
            else:
                print(f"[Client] Error: {response['error']}")
            
        except Exception as e:
            print(f"[Client] Error calling MergeSort: {str(e)}")
    
    def call_statistical_analysis(self, students):
        """Call Statistical Analysis service"""
        print(f"{'='*60}")
        print(f"Calling Statistical Analysis Service")
        print(f"{'='*60}")
        
        start_time = time.time()
        
        try:
            response = self.proxy.perform_statistical_analysis(students)
            
            end_time = time.time()
            total_time = end_time - start_time
            
            if response['success']:
                stats = response['statistics']
                
                print(f"\n[Client] Statistical Analysis Results:")
                print(f"\n  CGPA Statistics:")
                print(f"    Mean:     {stats['cgpa']['mean']:.4f}")
                print(f"    Median:   {stats['cgpa']['median']:.4f}")
                print(f"    Std Dev:  {stats['cgpa']['std_dev']:.4f}")
                print(f"    Min:      {stats['cgpa']['min']:.4f}")
                print(f"    Max:      {stats['cgpa']['max']:.4f}")
                
                print(f"\n  Student Distribution:")
                print(f"    Total Students: {stats['distribution']['total_students']}")
                print(f"    Total Faculties: {stats['distribution']['total_faculties']}")
                
                print(f"\n  Faculty Distribution:")
                for faculty, count in sorted(stats['distribution']['by_faculty'].items()):
                    print(f"    {faculty}: {count} students")
                
                # Calculate network overhead
                server_time = response['processing_time']
                network_overhead = total_time - server_time
                
                print(f"\n[Client] Performance Metrics:")
                print(f"  Server Processing Time: {server_time:.6f} seconds")
                print(f"  Total Time (with network): {total_time:.6f} seconds")
                print(f"  Network Overhead: {network_overhead:.6f} seconds")
                print(f"{'='*60}\n")
                
                # Store metrics
                self.performance_metrics.append({
                    'service': 'StatisticalAnalysis',
                    'operation': 'calculate_stats',
                    'server_time': server_time,
                    'total_time': total_time,
                    'network_overhead': network_overhead
                })
            else:
                print(f"[Client] Error: {response['error']}")
            
        except Exception as e:
            print(f"[Client] Error calling Statistical Analysis: {str(e)}")
    
    def call_filter(self, students, filter_type, value):
        """Call Filter service"""
        print(f"{'='*60}")
        print(f"Calling Filter Service: {filter_type} = {value}")
        print(f"{'='*60}")
        
        start_time = time.time()
        
        try:
            response = self.proxy.perform_filter(students, filter_type, value)
            
            end_time = time.time()
            total_time = end_time - start_time
            
            if response['success']:
                filtered_students = response['filtered_students']
                
                print(f"\n[Client] Found {len(filtered_students)} students matching criteria")
                
                if len(filtered_students) <= 10:
                    print(f"\nFiltered Results:")
                    for student in filtered_students:
                        print(f"  {student['name']:<30} "
                              f"Faculty: {student['faculty']:<15} "
                              f"CGPA: {student['cgpa']:.2f}  "
                              f"Grade: {student['grade']}")
                else:
                    print(f"\nShowing first 10 results:")
                    for student in filtered_students[:10]:
                        print(f"  {student['name']:<30} "
                              f"Faculty: {student['faculty']:<15} "
                              f"CGPA: {student['cgpa']:.2f}  "
                              f"Grade: {student['grade']}")
                
                # Calculate network overhead
                server_time = response['processing_time']
                network_overhead = total_time - server_time
                
                print(f"\n[Client] Performance Metrics:")
                print(f"  Server Processing Time: {server_time:.6f} seconds")
                print(f"  Total Time (with network): {total_time:.6f} seconds")
                print(f"  Network Overhead: {network_overhead:.6f} seconds")
                print(f"{'='*60}\n")
                
                # Store metrics
                self.performance_metrics.append({
                    'service': 'Filter',
                    'operation': f'{filter_type}={value}',
                    'server_time': server_time,
                    'total_time': total_time,
                    'network_overhead': network_overhead
                })
            else:
                print(f"[Client] Error: {response['error']}")
            
        except Exception as e:
            print(f"[Client] Error calling Filter: {str(e)}")
    
    def call_search(self, students, search_term):
        """Call Search service"""
        print(f"{'='*60}")
        print(f"Calling Search Service: {search_term}")
        print(f"{'='*60}")
        
        start_time = time.time()
        
        try:
            response = self.proxy.search_student(students, search_term)
            
            end_time = time.time()
            total_time = end_time - start_time
            
            if response['success']:
                found_students = response['found_students']
                
                print(f"\n[Client] Found {len(found_students)} students matching '{search_term}'")
                
                if found_students:
                    print(f"\nSearch Results:")
                    for student in found_students:
                        print(f"  ID: {student['student_id']:<15} "
                              f"Name: {student['name']:<30} "
                              f"CGPA: {student['cgpa']:.2f}")
                
                # Calculate network overhead
                server_time = response['processing_time']
                network_overhead = total_time - server_time
                
                print(f"\n[Client] Performance Metrics:")
                print(f"  Server Processing Time: {server_time:.6f} seconds")
                print(f"  Total Time (with network): {total_time:.6f} seconds")
                print(f"  Network Overhead: {network_overhead:.6f} seconds")
                print(f"{'='*60}\n")
                
                # Store metrics
                self.performance_metrics.append({
                    'service': 'Search',
                    'operation': search_term,
                    'server_time': server_time,
                    'total_time': total_time,
                    'network_overhead': network_overhead
                })
            else:
                print(f"[Client] Error: {response['error']}")
            
        except Exception as e:
            print(f"[Client] Error calling Search: {str(e)}")
    
    def save_performance_metrics(self, output_path):
        """Save performance metrics to JSON file"""
        try:
            # Calculate summary statistics
            avg_server_time = sum(m['server_time'] for m in self.performance_metrics) / len(self.performance_metrics)
            avg_total_time = sum(m['total_time'] for m in self.performance_metrics) / len(self.performance_metrics)
            avg_network_overhead = sum(m['network_overhead'] for m in self.performance_metrics) / len(self.performance_metrics)
            
            output = {
                'timestamp': datetime.now().isoformat(),
                'protocol': 'XML-RPC',
                'server_address': self.server_address,
                'summary': {
                    'total_requests': len(self.performance_metrics),
                    'avg_server_time': avg_server_time,
                    'avg_total_time': avg_total_time,
                    'avg_network_overhead': avg_network_overhead
                },
                'detailed_metrics': self.performance_metrics
            }
            
            with open(output_path, 'w') as f:
                json.dump(output, f, indent=2)
            
            print(f"[Client] Performance metrics saved to {output_path}")
            
        except Exception as e:
            print(f"[Client] Error saving metrics: {str(e)}")


def main():
    """Main client execution"""
    # Get configuration from environment or use defaults
    server_address = os.environ.get('SERVER_ADDRESS', 'http://localhost:8000')
    output_filename = os.environ.get('OUTPUT_FILE', 'xmlrpc_performance_metrics.json')
    wait_time = int(os.environ.get('WAIT_TIME', '0'))
    
    # Wait if specified (for Docker deployments)
    if wait_time > 0:
        print(f"[Client] Waiting {wait_time} seconds for server to be ready...")
        time.sleep(wait_time)
    
    # Determine paths
    current_dir = os.path.dirname(os.path.abspath(__file__))
    xmlrpc_impl_dir = os.path.dirname(current_dir)
    project_root = os.path.dirname(xmlrpc_impl_dir)
    
    csv_path = os.path.join(project_root, 'data', 'students.csv')
    results_dir = os.path.join(project_root, 'results')
    os.makedirs(results_dir, exist_ok=True)
    
    # Use environment variable for output path if it's an absolute path
    if os.path.isabs(output_filename):
        output_path = output_filename
    else:
        output_path = os.path.join(results_dir, output_filename)
    
    # Create client
    client = StudentAnalysisClient(server_address)
    
    try:
        # Connect to server
        client.connect()
        
        # Load student data
        students = client.load_students_from_csv(csv_path)
        
        if not students:
            print("[Client] No student data loaded. Exiting.")
            return
        
        # Call all services
        print("\n" + "="*60)
        print("Starting Student Analysis with XML-RPC")
        print(f"Server: {server_address}")
        print("="*60 + "\n")
        
        # 1. MapReduce - CGPA Count
        client.call_mapreduce(students, "cgpa_count")
        
        # 2. MapReduce - Grade Count
        client.call_mapreduce(students, "grade_count")
        
        # 3. MergeSort by CGPA
        client.call_mergesort(students, "cgpa")
        
        # 4. MergeSort by Name
        client.call_mergesort(students, "name")
        
        # 5. Statistical Analysis
        client.call_statistical_analysis(students)
        
        # Summary
        print("\n" + "="*60)
        print("Performance Summary")
        print("="*60)
        
        avg_server = sum(m['server_time'] for m in client.performance_metrics) / len(client.performance_metrics)
        avg_total = sum(m['total_time'] for m in client.performance_metrics) / len(client.performance_metrics)
        avg_network = sum(m['network_overhead'] for m in client.performance_metrics) / len(client.performance_metrics)
        
        print(f"\nTotal Service Calls: {len(client.performance_metrics)}")
        print(f"\nAverage Times:")
        print(f"  Server Processing: {avg_server:.6f} seconds")
        print(f"  Total Time:        {avg_total:.6f} seconds")
        print(f"  Network Overhead:  {avg_network:.6f} seconds")
        print(f"\nNetwork overhead is {(avg_network/avg_total)*100:.2f}% of total time")
        print("="*60 + "\n")
        
        # Save metrics
        client.save_performance_metrics(output_path)
        
    except Exception as e:
        print(f"[Client] Error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    finally:
        client.disconnect()


if __name__ == '__main__':
    main()
