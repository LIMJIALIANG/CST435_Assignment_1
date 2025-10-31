"""
Microservices Client
Initiates workflow: Client → MapReduce → MergeSort → Statistics → Client
Measures end-to-end performance
"""

import sys
import os
import grpc
import csv
import json
import time
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'generated'))

import student_service_pb2
import student_service_pb2_grpc


class MicroservicesClient:
    """Client that initiates the microservices chain"""
    
    def __init__(self):
        self.mapreduce_address = os.getenv('MAPREDUCE_ADDRESS', 'localhost:50051')
        self.students = []
        self.metrics = {
            'timestamp': datetime.now().isoformat(),
            'architecture': 'microservices_chained',
            'workflow': 'Client → MapReduce → MergeSort → Statistics → Client'
        }
    
    def load_students(self, csv_path):
        """Load student data"""
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
            
            self.students = students
            print(f"[Client] ✓ Loaded {len(students)} students\n")
            return students
        except Exception as e:
            print(f"[Client] ✗ Error loading CSV: {e}")
            return []
    
    def initiate_workflow(self):
        """Initiate the microservices workflow"""
        print("="*70)
        print("MICROSERVICES WORKFLOW")
        print("="*70)
        print("Chain: Client → MapReduce → MergeSort → Statistics → Client")
        print("="*70 + "\n")
        
        print(f"[Client] Starting workflow...")
        print(f"[Client] Sending request to MapReduce Service ({self.mapreduce_address})\n")
        
        try:
            # Connect to MapReduce Service (entry point)
            channel = grpc.insecure_channel(self.mapreduce_address)
            stub = student_service_pb2_grpc.StudentAnalysisServiceStub(channel)
            
            # Send chain request to MapReduce Service
            request = student_service_pb2.ChainRequest(
                students=self.students,
                partial_results=student_service_pb2.CombinedResponse()  # Empty initial results
            )
            
            workflow_start = time.time()
            combined_response = stub.ProcessChain(request, timeout=120)
            workflow_end = time.time()
            
            total_workflow_time = workflow_end - workflow_start
            
            channel.close()
            
            # Display ALL results from ALL services
            print("="*70)
            print("WORKFLOW COMPLETED - ALL RESULTS")
            print("="*70)
            
            # MapReduce Service Results
            print(f"\n[MapReduce Service] CGPA Classification (Time: {combined_response.mapreduce_time:.4f}s)")
            print("-" * 70)
            print(f"  CGPA Classification:")
            for cgpa_range in combined_response.cgpa_ranges:
                print(f"    {cgpa_range.range}: {cgpa_range.count} students")
            
            # MergeSort Service Results
            print(f"\n[MergeSort Service] Sort by CGPA (Time: {combined_response.mergesort_time:.4f}s)")
            print("-" * 70)
            print(f"  Top 10 students by CGPA:")
            for i, student in enumerate(combined_response.sorted_by_cgpa[:10], 1):
                print(f"    {i}. {student.name} - CGPA: {student.cgpa:.2f} ({student.grade})")
            
            # Statistics Service Results
            print(f"\n[Statistics Service] Statistical Analysis (Time: {combined_response.statistics_time:.4f}s)")
            print("-" * 70)
            print(f"  Pass Rate: {combined_response.pass_rate:.2f}%")
            print(f"\n  Faculty Statistics:")
            for faculty_stat in combined_response.faculty_stats:
                print(f"    {faculty_stat.faculty}: Avg CGPA {faculty_stat.average_cgpa:.2f} ({faculty_stat.student_count} students)")
            print(f"\n  Grade Distribution:")
            for grade_dist in combined_response.grade_distribution:
                print(f"    Grade {grade_dist.grade}: {grade_dist.count} students ({grade_dist.percentage:.1f}%)")
            
            # Performance Summary
            print(f"\n{'='*70}")
            print("PERFORMANCE SUMMARY")
            print("="*70)
            print(f"MapReduce Time:        {combined_response.mapreduce_time:.4f}s")
            print(f"MergeSort Time:        {combined_response.mergesort_time:.4f}s")
            print(f"Statistics Time:       {combined_response.statistics_time:.4f}s")
            print(f"Total Processing:      {combined_response.total_workflow_time:.4f}s")
            print(f"End-to-End Time:       {total_workflow_time:.4f}s")
            print(f"Network Overhead:      {(total_workflow_time - combined_response.total_workflow_time):.4f}s")
            
            # Store detailed metrics (matching XML-RPC format)
            network_overhead = total_workflow_time - combined_response.total_workflow_time
            
            self.metrics['workflow_time'] = total_workflow_time
            self.metrics['mapreduce_time'] = combined_response.mapreduce_time
            self.metrics['mergesort_time'] = combined_response.mergesort_time
            self.metrics['statistics_time'] = combined_response.statistics_time
            self.metrics['total_processing_time'] = combined_response.total_workflow_time
            self.metrics['network_overhead'] = network_overhead
            
            # Add summary statistics
            self.metrics['summary'] = {
                'total_services': 3,
                'avg_service_time': combined_response.total_workflow_time / 3,
                'overhead_percentage': (network_overhead / total_workflow_time) * 100
            }
            
            # Add detailed results
            self.metrics['detailed_results'] = {}
            
            # MapReduce results
            cgpa_classification = {}
            for cgpa_range in combined_response.cgpa_ranges:
                cgpa_classification[cgpa_range.range] = cgpa_range.count
            
            self.metrics['detailed_results']['mapreduce'] = {
                'cgpa_classification': cgpa_classification,
                'processing_time': combined_response.mapreduce_time
            }
            
            # MergeSort results
            top_10_students = []
            for student in combined_response.sorted_by_cgpa[:10]:
                top_10_students.append({
                    'student_id': student.student_id,
                    'name': student.name,
                    'faculty': student.faculty,
                    'cgpa': student.cgpa,
                    'grade': student.grade
                })
            
            self.metrics['detailed_results']['mergesort'] = {
                'sorted_count': len(combined_response.sorted_by_cgpa),
                'top_10': top_10_students,
                'processing_time': combined_response.mergesort_time
            }
            
            # Statistics results
            faculty_stats = {}
            for faculty_stat in combined_response.faculty_stats:
                faculty_stats[faculty_stat.faculty] = {
                    'average_cgpa': faculty_stat.average_cgpa,
                    'student_count': faculty_stat.student_count
                }
            
            grade_distribution = {}
            for grade_dist in combined_response.grade_distribution:
                grade_distribution[grade_dist.grade] = {
                    'count': grade_dist.count,
                    'percentage': grade_dist.percentage
                }
            
            self.metrics['detailed_results']['statistics'] = {
                'operation': 'statistical_analysis',
                'result': {
                    'pass_rate': combined_response.pass_rate,
                    'faculty_statistics': faculty_stats,
                    'grade_distribution': grade_distribution
                },
                'processing_time': combined_response.statistics_time
            }
            
            print(f"\n{'='*70}")
            print("✓ All services (MapReduce→MergeSort→Statistics) completed successfully!")
            print("="*70 + "\n")
            
            return True
            
        except Exception as e:
            print(f"[Client] ✗ Error: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def save_metrics(self, output_path):
        """Save performance metrics"""
        try:
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(self.metrics, f, indent=2)
            print(f"[Client] ✓ Metrics saved to: {output_path}\n")
        except Exception as e:
            print(f"[Client] ✗ Error saving metrics: {e}")


def main():
    """Main execution"""
    print("\n" + "="*70)
    print("MICROSERVICES CLIENT")
    print("="*70)
    print("Architecture: 3 Connected Services (MapReduce→MergeSort→Statistics)")
    print("="*70 + "\n")
    
    # Initialize client
    client = MicroservicesClient()
    
    # Load data
    current_dir = os.path.dirname(os.path.abspath(__file__))
    grpc_impl_dir = os.path.dirname(current_dir)
    project_root = os.path.dirname(grpc_impl_dir)
    csv_path = os.path.join(project_root, 'data', 'students.csv')
    
    client.load_students(csv_path)
    
    if not client.students:
        print("[Client] ✗ No students loaded. Exiting.")
        return
    
    # Run workflow
    success = client.initiate_workflow()
    
    if success:
        # Save metrics
        results_dir = os.path.join(project_root, 'results')
        output_file = os.getenv('OUTPUT_FILE', 'grpc_performance_metrics.json')
        output_path = os.path.join(results_dir, output_file)
        client.save_metrics(output_path)


if __name__ == '__main__':
    main()
