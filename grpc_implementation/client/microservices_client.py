"""
Microservices Client
Initiates workflow: Client → A → B → C → D → E → Client
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
        self.service_a_address = os.getenv('SERVICE_A_ADDRESS', 'localhost:50051')
        self.students = []
        self.metrics = {
            'timestamp': datetime.now().isoformat(),
            'architecture': 'microservices_chained',
            'workflow': 'Client → A → B → C → D → E → Client'
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
        print("Chain: Client → A → B → C → D → E → Client")
        print("="*70 + "\n")
        
        print(f"[Client] Starting workflow...")
        print(f"[Client] Sending request to Service A ({self.service_a_address})\n")
        
        try:
            # Connect to Service A (entry point)
            channel = grpc.insecure_channel(self.service_a_address)
            stub = student_service_pb2_grpc.StudentAnalysisServiceStub(channel)
            
            # Send chain request to Service A
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
            
            # Service A Results
            print(f"\n[Service A] MapReduce CGPA Count (Time: {combined_response.service_a_time:.4f}s)")
            print("-" * 70)
            for cgpa_range in combined_response.cgpa_ranges:
                print(f"  {cgpa_range.range}: {cgpa_range.count} students")
            
            # Service B Results
            print(f"\n[Service B] MapReduce Grade Distribution (Time: {combined_response.service_b_time:.4f}s)")
            print("-" * 70)
            for grade_count in combined_response.grade_counts:
                print(f"  Grade {grade_count.grade}: {grade_count.count} students")
            
            # Service C Results
            print(f"\n[Service C] MergeSort by CGPA (Time: {combined_response.service_c_time:.4f}s)")
            print("-" * 70)
            print(f"  Top 5 students by CGPA:")
            for i, student in enumerate(combined_response.sorted_by_cgpa[:5], 1):
                print(f"    {i}. {student.name} - CGPA: {student.cgpa:.2f} ({student.grade})")
            
            # Service D Results
            print(f"\n[Service D] MergeSort by Grade (Time: {combined_response.service_d_time:.4f}s)")
            print("-" * 70)
            print(f"  Top 5 students by Grade:")
            for i, student in enumerate(combined_response.sorted_by_grade[:5], 1):
                print(f"    {i}. {student.name} - Grade: {student.grade} (CGPA: {student.cgpa:.2f})")
            
            # Service E Results
            print(f"\n[Service E] Statistical Analysis (Time: {combined_response.service_e_time:.4f}s)")
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
            print(f"Service A Time:        {combined_response.service_a_time:.4f}s")
            print(f"Service B Time:        {combined_response.service_b_time:.4f}s")
            print(f"Service C Time:        {combined_response.service_c_time:.4f}s")
            print(f"Service D Time:        {combined_response.service_d_time:.4f}s")
            print(f"Service E Time:        {combined_response.service_e_time:.4f}s")
            print(f"Total Processing:      {combined_response.total_workflow_time:.4f}s")
            print(f"End-to-End Time:       {total_workflow_time:.4f}s")
            print(f"Network Overhead:      {(total_workflow_time - combined_response.total_workflow_time):.4f}s")
            
            # Store metrics
            self.metrics['workflow_time'] = total_workflow_time
            self.metrics['service_a_time'] = combined_response.service_a_time
            self.metrics['service_b_time'] = combined_response.service_b_time
            self.metrics['service_c_time'] = combined_response.service_c_time
            self.metrics['service_d_time'] = combined_response.service_d_time
            self.metrics['service_e_time'] = combined_response.service_e_time
            self.metrics['total_processing_time'] = combined_response.total_workflow_time
            self.metrics['network_overhead'] = total_workflow_time - combined_response.total_workflow_time
            
            print(f"\n{'='*70}")
            print("✓ All services (A→B→C→D→E) completed successfully!")
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
    print("Architecture: 5 Connected Services (A→B→C→D→E)")
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
        output_file = os.getenv('OUTPUT_FILE', 'microservices_performance_metrics.json')
        output_path = os.path.join(results_dir, output_file)
        client.save_metrics(output_path)


if __name__ == '__main__':
    main()
