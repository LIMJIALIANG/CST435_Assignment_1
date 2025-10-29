"""
gRPC Client Implementation
Triggers student analysis services and measures performance
"""

import sys
import os
import grpc
import csv
import json
import time
from datetime import datetime

# Add paths for generated code
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'generated'))

# Import generated gRPC code
import student_service_pb2
import student_service_pb2_grpc


class StudentAnalysisClient:
    """
    gRPC Client for Student Analysis
    """
    
    def __init__(self, server_address='localhost:50051'):
        """Initialize client with server address"""
        self.server_address = server_address
        self.channel = None
        self.stub = None
        self.performance_metrics = []
    
    def connect(self):
        """Establish connection to server"""
        print(f"[Client] Connecting to server at {self.server_address}...")
        self.channel = grpc.insecure_channel(self.server_address)
        self.stub = student_service_pb2_grpc.StudentAnalysisServiceStub(self.channel)
        print(f"[Client] Connected successfully!\n")
    
    def disconnect(self):
        """Close connection to server"""
        if self.channel:
            self.channel.close()
            print("[Client] Disconnected from server")
    
    def load_students_from_csv(self, csv_path):
        """Load student data from CSV file"""
        students = []
        
        try:
            with open(csv_path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    student = student_service_pb2.Student(
                        student_id=row['student_id'],
                        name=row['name'],
                        faculty=row['faculty'],
                        cgpa=float(row['cgpa']),
                        grade=row['grade']
                    )
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
        
        request = student_service_pb2.MapReduceRequest(
            students=students,
            operation=operation
        )
        
        start_time = time.time()
        
        try:
            response = self.stub.PerformMapReduce(request)
            
            end_time = time.time()
            total_time = end_time - start_time
            
            print(f"\n[Client] Results received:")
            
            if operation == "cgpa_count":
                print("\nCGPA Range Distribution:")
                for cgpa_range in response.cgpa_ranges:
                    print(f"  {cgpa_range.range}: {cgpa_range.count} students")
            elif operation == "grade_count":
                print("\nGrade Distribution:")
                for grade_count in sorted(response.grade_counts, key=lambda x: x.grade):
                    print(f"  Grade {grade_count.grade}: {grade_count.count} students")
            
            print(f"\n[Client] Server processing time: {response.processing_time:.4f} seconds")
            print(f"[Client] Total request time: {total_time:.4f} seconds")
            print(f"[Client] Network overhead: {(total_time - response.processing_time):.4f} seconds\n")
            
            # Record metrics
            self.performance_metrics.append({
                'service': 'MapReduce',
                'operation': operation,
                'server_time': response.processing_time,
                'total_time': total_time,
                'network_overhead': total_time - response.processing_time
            })
            
            return response
            
        except grpc.RpcError as e:
            print(f"[Client] RPC Error: {e.code()} - {e.details()}")
            return None
    
    def call_mergesort(self, students, sort_by):
        """Call MergeSort service"""
        print(f"{'='*60}")
        print(f"Calling MergeSort Service: sort by {sort_by}")
        print(f"{'='*60}")
        
        request = student_service_pb2.MergeSortRequest(
            students=students,
            sort_by=sort_by
        )
        
        start_time = time.time()
        
        try:
            response = self.stub.PerformMergeSort(request)
            
            end_time = time.time()
            total_time = end_time - start_time
            
            print(f"\n[Client] Results received:")
            print(f"\nTop 10 Students (sorted by {sort_by}):")
            for i, student in enumerate(response.sorted_students[:10], 1):
                print(f"  {i}. {student.name} - {student.faculty} - Grade: {student.grade} - CGPA: {student.cgpa:.2f}")
            
            print(f"\n[Client] Server processing time: {response.processing_time:.4f} seconds")
            print(f"[Client] Total request time: {total_time:.4f} seconds")
            print(f"[Client] Network overhead: {(total_time - response.processing_time):.4f} seconds\n")
            
            # Record metrics
            self.performance_metrics.append({
                'service': 'MergeSort',
                'operation': sort_by,
                'server_time': response.processing_time,
                'total_time': total_time,
                'network_overhead': total_time - response.processing_time
            })
            
            return response
            
        except grpc.RpcError as e:
            print(f"[Client] RPC Error: {e.code()} - {e.details()}")
            return None
    
    def call_statistics(self, students, analysis_type):
        """Call Statistical Analysis service"""
        print(f"{'='*60}")
        print(f"Calling Statistics Service: {analysis_type}")
        print(f"{'='*60}")
        
        request = student_service_pb2.StatsRequest(
            students=students,
            analysis_type=analysis_type
        )
        
        start_time = time.time()
        
        try:
            response = self.stub.PerformStatisticalAnalysis(request)
            
            end_time = time.time()
            total_time = end_time - start_time
            
            print(f"\n[Client] Results received:")
            
            if response.faculty_stats:
                print("\nAverage CGPA by Faculty:")
                for stat in response.faculty_stats:
                    print(f"  {stat.faculty}: {stat.average_cgpa:.2f} (n={stat.student_count})")
            
            if response.grade_distribution:
                print("\nGrade Distribution:")
                for dist in response.grade_distribution:
                    print(f"  Grade {dist.grade}: {dist.count} students ({dist.percentage:.1f}%)")
            
            if response.pass_rate > 0:
                print(f"\nPass Rate (CGPA >= 2.0): {response.pass_rate:.2f}%")
            
            print(f"\n[Client] Server processing time: {response.processing_time:.4f} seconds")
            print(f"[Client] Total request time: {total_time:.4f} seconds")
            print(f"[Client] Network overhead: {(total_time - response.processing_time):.4f} seconds\n")
            
            # Record metrics
            self.performance_metrics.append({
                'service': 'Statistics',
                'operation': analysis_type,
                'server_time': response.processing_time,
                'total_time': total_time,
                'network_overhead': total_time - response.processing_time
            })
            
            return response
            
        except grpc.RpcError as e:
            print(f"[Client] RPC Error: {e.code()} - {e.details()}")
            return None
    
    def save_performance_metrics(self, output_path):
        """Save performance metrics to JSON file"""
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        metrics_data = {
            'timestamp': datetime.now().isoformat(),
            'protocol': 'gRPC',
            'server_address': self.server_address,
            'summary': {
                'total_requests': len(self.performance_metrics),
                'avg_server_time': sum(m['server_time'] for m in self.performance_metrics) / len(self.performance_metrics) if self.performance_metrics else 0,
                'avg_total_time': sum(m['total_time'] for m in self.performance_metrics) / len(self.performance_metrics) if self.performance_metrics else 0,
                'avg_network_overhead': sum(m['network_overhead'] for m in self.performance_metrics) / len(self.performance_metrics) if self.performance_metrics else 0,
            },
            'detailed_metrics': self.performance_metrics
        }
        
        with open(output_path, 'w') as f:
            json.dump(metrics_data, f, indent=2)
        
        print(f"\n[Client] Performance metrics saved to: {output_path}")
        print(f"\nPerformance Summary:")
        print(f"  Total requests: {metrics_data['summary']['total_requests']}")
        print(f"  Average server processing time: {metrics_data['summary']['avg_server_time']:.4f} seconds")
        print(f"  Average total request time: {metrics_data['summary']['avg_total_time']:.4f} seconds")
        print(f"  Average network overhead: {metrics_data['summary']['avg_network_overhead']:.4f} seconds")



def main():
    """Main client execution"""
    print("=" * 60)
    print("Student Analysis gRPC Client")
    print("=" * 60)
    
    # Determine server address
    server_address = os.getenv('SERVER_ADDRESS', 'localhost:50051')
    
    # Get output filename from environment variable or use default
    output_filename = os.getenv('OUTPUT_FILE', 'grpc_performance_metrics.json')
    
    # Get data file path - navigate to project root (2 levels up)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    grpc_impl_dir = os.path.dirname(current_dir)
    project_root = os.path.dirname(grpc_impl_dir)
    csv_path = os.path.join(project_root, 'data', 'students.csv')
    
    # Initialize client
    client = StudentAnalysisClient(server_address)
    
    try:
        # Connect to server
        client.connect()
        
        # Load student data
        students = client.load_students_from_csv(csv_path)
        
        if not students:
            print("[Client] No student data loaded. Exiting.")
            return
        
        # Test all services
        print("\n" + "=" * 60)
        print("TESTING ALL SERVICES")
        print("=" * 60 + "\n")
        
        # 1. MapReduce - CGPA Count
        client.call_mapreduce(students, "cgpa_count")
        time.sleep(0.5)
        
        # 2. MapReduce - Grade Count
        client.call_mapreduce(students, "grade_count")
        time.sleep(0.5)
        
        # 3. MergeSort - by CGPA
        client.call_mergesort(students, "cgpa")
        time.sleep(0.5)
        
        # 4. MergeSort - by Grade
        client.call_mergesort(students, "grade")
        time.sleep(0.5)
        
        # 5. Statistics - All analysis
        client.call_statistics(students, "all")
        
        # Determine output path
        results_dir = os.path.join(project_root, 'results')
        os.makedirs(results_dir, exist_ok=True)
        
        # Use environment variable for output path if it's an absolute path
        if os.path.isabs(output_filename):
            output_path = output_filename
        else:
            output_path = os.path.join(results_dir, output_filename)
        
        # Save performance metrics
        client.save_performance_metrics(output_path)
        
    except Exception as e:
        print(f"[Client] Error: {str(e)}")
    
    finally:
        # Disconnect
        client.disconnect()


if __name__ == '__main__':
    main()
