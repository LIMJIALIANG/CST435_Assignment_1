"""
Protocol Comparison Tool
Compares performance metrics between gRPC and XML-RPC implementations
"""

import json
import os
import sys
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np


class ProtocolComparator:
    """
    Compares performance between different RPC protocols
    """
    
    def __init__(self, results_dir='../results'):
        """Initialize comparator with results directory"""
        self.results_dir = results_dir
        self.grpc_metrics = None
        self.xmlrpc_metrics = None
    
    def load_metrics(self, grpc_file, xmlrpc_file):
        """Load metrics from both protocols"""
        try:
            # Load gRPC metrics
            grpc_path = os.path.join(self.results_dir, grpc_file)
            with open(grpc_path, 'r') as f:
                self.grpc_metrics = json.load(f)
            print(f"✓ Loaded gRPC metrics from {grpc_file}")
            
            # Load XML-RPC metrics
            xmlrpc_path = os.path.join(self.results_dir, xmlrpc_file)
            with open(xmlrpc_path, 'r') as f:
                self.xmlrpc_metrics = json.load(f)
            print(f"✓ Loaded XML-RPC metrics from {xmlrpc_file}")
            
            return True
            
        except Exception as e:
            print(f"✗ Error loading metrics: {str(e)}")
            return False
    
    def print_summary_comparison(self):
        """Print summary comparison of both protocols"""
        print("\n" + "="*80)
        print("PERFORMANCE COMPARISON: gRPC Microservices vs XML-RPC Monolithic")
        print("="*80)
        
        # Architecture comparison
        print(f"\n{'Architecture':<30} {'gRPC':<25} {'XML-RPC':<25}")
        print("-" * 80)
        print(f"{'Type':<30} {self.grpc_metrics['architecture']:<25} {self.xmlrpc_metrics['architecture']:<25}")
        print(f"{'Workflow':<30} {'Chained Services':<25} {'Individual Calls':<25}")
        
        # Performance metrics
        print(f"\n{'Metric':<30} {'gRPC':<25} {'XML-RPC':<25}")
        print("-" * 80)
        
        # Individual service times
        print(f"{'Service A (CGPA Count)':<30} {self.grpc_metrics['service_a_time']:<25.6f} {self.xmlrpc_metrics['service_a_time']:<25.6f}")
        print(f"{'Service B (Grade Count)':<30} {self.grpc_metrics['service_b_time']:<25.6f} {self.xmlrpc_metrics['service_b_time']:<25.6f}")
        print(f"{'Service C (Sort CGPA)':<30} {self.grpc_metrics['service_c_time']:<25.6f} {self.xmlrpc_metrics['service_c_time']:<25.6f}")
        print(f"{'Service D (Sort Grade)':<30} {self.grpc_metrics['service_d_time']:<25.6f} {self.xmlrpc_metrics['service_d_time']:<25.6f}")
        print(f"{'Service E (Statistics)':<30} {self.grpc_metrics['service_e_time']:<25.6f} {self.xmlrpc_metrics['service_e_time']:<25.6f}")
        print("-" * 80)
        print(f"{'Total Processing Time':<30} {self.grpc_metrics['total_processing_time']:<25.6f} {self.xmlrpc_metrics['total_processing_time']:<25.6f}")
        print(f"{'End-to-End Workflow Time':<30} {self.grpc_metrics['workflow_time']:<25.6f} {self.xmlrpc_metrics['workflow_time']:<25.6f}")
        print(f"{'Network Overhead':<30} {self.grpc_metrics['network_overhead']:<25.6f} {self.xmlrpc_metrics['network_overhead']:<25.6f}")
        
        print("\n" + "="*80)
        print("PERFORMANCE ANALYSIS")
        print("="*80)
        
        # Calculate differences
        grpc_total = self.grpc_metrics['total_processing_time']
        xmlrpc_total = self.xmlrpc_metrics['total_processing_time']
        
        grpc_workflow = self.grpc_metrics['workflow_time']
        xmlrpc_workflow = self.xmlrpc_metrics['workflow_time']
        
        grpc_network = self.grpc_metrics['network_overhead']
        xmlrpc_network = self.xmlrpc_metrics['network_overhead']
        
        processing_diff = ((xmlrpc_total - grpc_total) / grpc_total) * 100 if grpc_total > 0 else 0
        workflow_diff = ((xmlrpc_workflow - grpc_workflow) / grpc_workflow) * 100 if grpc_workflow > 0 else 0
        network_diff = ((xmlrpc_network - grpc_network) / grpc_network) * 100 if grpc_network > 0 else 0
        
        print(f"\nTotal Processing Time:")
        if grpc_total < xmlrpc_total:
            print(f"  ✓ gRPC is {abs(processing_diff):.2f}% FASTER than XML-RPC")
        else:
            print(f"  ✗ gRPC is {abs(processing_diff):.2f}% SLOWER than XML-RPC")
        
        print(f"\nEnd-to-End Workflow Time:")
        if grpc_workflow < xmlrpc_workflow:
            print(f"  ✓ gRPC is {abs(workflow_diff):.2f}% FASTER than XML-RPC")
        else:
            print(f"  ✗ gRPC is {abs(workflow_diff):.2f}% SLOWER than XML-RPC")
        
        print(f"\nNetwork Overhead:")
        if grpc_network < xmlrpc_network:
            print(f"  ✓ gRPC has {abs(network_diff):.2f}% LESS overhead than XML-RPC")
        else:
            print(f"  ✗ gRPC has {abs(network_diff):.2f}% MORE overhead than XML-RPC")
        
        # Network overhead percentage
        grpc_overhead_pct = (grpc_network / grpc_workflow) * 100 if grpc_workflow > 0 else 0
        xmlrpc_overhead_pct = (xmlrpc_network / xmlrpc_workflow) * 100 if xmlrpc_workflow > 0 else 0
        
        print(f"\nNetwork Overhead as % of Total Time:")
        print(f"  gRPC:    {grpc_overhead_pct:.2f}%")
        print(f"  XML-RPC: {xmlrpc_overhead_pct:.2f}%")
        
        # Architecture impact
        print(f"\nArchitecture Impact:")
        print(f"  gRPC:    Chained microservices (A→B→C→D→E→Client)")
        print(f"  XML-RPC: Independent service calls (Client→Server per operation)")
        
        print("\n" + "="*80)
    
    def print_detailed_comparison(self):
        """Print detailed per-service comparison"""
        print("\n" + "="*80)
        print("DETAILED SERVICE-BY-SERVICE COMPARISON")
        print("="*80)
        
        # Support both 'detailed_metrics' and 'metrics' keys for backward compatibility
        grpc_details = self.grpc_metrics.get('detailed_metrics') or self.grpc_metrics.get('metrics', [])
        xmlrpc_details = self.xmlrpc_metrics.get('detailed_metrics') or self.xmlrpc_metrics.get('metrics', [])
        
        # Group by service
        services = {}
        
        for metric in grpc_details:
            key = f"{metric['service']}_{metric['operation']}"
            if key not in services:
                services[key] = {'grpc': None, 'xmlrpc': None}
            services[key]['grpc'] = metric
        
        for metric in xmlrpc_details:
            key = f"{metric['service']}_{metric['operation']}"
            if key not in services:
                services[key] = {'grpc': None, 'xmlrpc': None}
            services[key]['xmlrpc'] = metric
        
        # Print comparison for each service
        for service_key, data in services.items():
            if data['grpc'] and data['xmlrpc']:
                grpc_m = data['grpc']
                xmlrpc_m = data['xmlrpc']
                
                print(f"\n{grpc_m['service']} - {grpc_m['operation']}")
                print("-" * 80)
                
                print("{:<30} {:<20} {:<20}".format("", "gRPC", "XML-RPC"))
                print("{:<30} {:<20.6f} {:<20.6f}".format(
                    "Server Time (s)",
                    grpc_m['server_time'],
                    xmlrpc_m['server_time']
                ))
                print("{:<30} {:<20.6f} {:<20.6f}".format(
                    "Total Time (s)",
                    grpc_m['total_time'],
                    xmlrpc_m['total_time']
                ))
                print("{:<30} {:<20.6f} {:<20.6f}".format(
                    "Network Overhead (s)",
                    grpc_m['network_overhead'],
                    xmlrpc_m['network_overhead']
                ))
                
                # Calculate speedup
                if grpc_m['total_time'] < xmlrpc_m['total_time']:
                    speedup = xmlrpc_m['total_time'] / grpc_m['total_time']
                    print(f"\n  → gRPC is {speedup:.2f}x faster")
                else:
                    speedup = grpc_m['total_time'] / xmlrpc_m['total_time']
                    print(f"\n  → XML-RPC is {speedup:.2f}x faster")
        
        print("\n" + "="*80)
    
    def generate_comparison_chart(self, output_file='protocol_comparison.png'):
        """Generate visual comparison chart"""
        try:
            # Check if we have the new format with individual service times
            has_service_times = ('service_a_time' in self.grpc_metrics and 
                                'service_a_time' in self.xmlrpc_metrics)
            
            if has_service_times:
                # New format: Generate detailed service-by-service comparison
                self._generate_detailed_chart(output_file)
            else:
                # Old format: Generate summary chart
                self._generate_summary_chart(output_file)
                
        except Exception as e:
            print(f"\n✗ Error generating chart: {str(e)}")
            import traceback
            traceback.print_exc()
    
    def _generate_detailed_chart(self, output_file):
        """Generate detailed chart with individual service comparisons"""
        # Prepare data for charts
        services = ['Service A\n(CGPA)', 'Service B\n(Grade)', 'Service C\n(Sort CGPA)', 
                   'Service D\n(Sort Grade)', 'Service E\n(Stats)']
        
        grpc_service_times = [
            self.grpc_metrics['service_a_time'],
            self.grpc_metrics['service_b_time'],
            self.grpc_metrics['service_c_time'],
            self.grpc_metrics['service_d_time'],
            self.grpc_metrics['service_e_time']
        ]
        
        xmlrpc_service_times = [
            self.xmlrpc_metrics['service_a_time'],
            self.xmlrpc_metrics['service_b_time'],
            self.xmlrpc_metrics['service_c_time'],
            self.xmlrpc_metrics['service_d_time'],
            self.xmlrpc_metrics['service_e_time']
        ]
        
        # Create figure with subplots
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
        
        # 1. Individual Service Times Comparison
        x = np.arange(len(services))
        width = 0.35
        
        bars1 = ax1.bar(x - width/2, grpc_service_times, width, label='gRPC', color='#4285F4')
        bars2 = ax1.bar(x + width/2, xmlrpc_service_times, width, label='XML-RPC', color='#EA4335')
        
        ax1.set_xlabel('Services', fontsize=10)
        ax1.set_ylabel('Time (seconds)', fontsize=10)
        ax1.set_title('Individual Service Processing Times', fontsize=12, fontweight='bold')
        ax1.set_xticks(x)
        ax1.set_xticklabels(services, fontsize=8)
        ax1.legend()
        ax1.grid(axis='y', alpha=0.3)
        
        # Add value labels on bars
        for bars in [bars1, bars2]:
            for bar in bars:
                height = bar.get_height()
                ax1.annotate(f'{height:.4f}',
                            xy=(bar.get_x() + bar.get_width() / 2, height),
                            xytext=(0, 3),
                            textcoords="offset points",
                            ha='center', va='bottom',
                            fontsize=7)
        
        # 2. Total Processing vs Workflow Time
        metrics = ['Total\nProcessing', 'Workflow\nTime', 'Network\nOverhead']
        grpc_totals = [
            self.grpc_metrics['total_processing_time'],
            self.grpc_metrics['workflow_time'],
            self.grpc_metrics['network_overhead']
        ]
        xmlrpc_totals = [
            self.xmlrpc_metrics['total_processing_time'],
            self.xmlrpc_metrics['workflow_time'],
            self.xmlrpc_metrics['network_overhead']
        ]
        
        x2 = np.arange(len(metrics))
        bars3 = ax2.bar(x2 - width/2, grpc_totals, width, label='gRPC', color='#4285F4')
        bars4 = ax2.bar(x2 + width/2, xmlrpc_totals, width, label='XML-RPC', color='#EA4335')
        
        ax2.set_xlabel('Metrics', fontsize=10)
        ax2.set_ylabel('Time (seconds)', fontsize=10)
        ax2.set_title('Overall Performance Metrics', fontsize=12, fontweight='bold')
        ax2.set_xticks(x2)
        ax2.set_xticklabels(metrics)
        ax2.legend()
        ax2.grid(axis='y', alpha=0.3)
        
        # Add value labels
        for bars in [bars3, bars4]:
            for bar in bars:
                height = bar.get_height()
                ax2.annotate(f'{height:.4f}',
                            xy=(bar.get_x() + bar.get_width() / 2, height),
                            xytext=(0, 3),
                            textcoords="offset points",
                            ha='center', va='bottom',
                            fontsize=8)
        
        # 3. Network Overhead Percentage
        grpc_overhead_pct = (self.grpc_metrics['network_overhead'] / self.grpc_metrics['workflow_time']) * 100
        xmlrpc_overhead_pct = (self.xmlrpc_metrics['network_overhead'] / self.xmlrpc_metrics['workflow_time']) * 100
        
        protocols = ['gRPC', 'XML-RPC']
        overhead_pcts = [grpc_overhead_pct, xmlrpc_overhead_pct]
        colors = ['#4285F4', '#EA4335']
        
        bars5 = ax3.bar(protocols, overhead_pcts, color=colors, width=0.6)
        ax3.set_ylabel('Network Overhead (%)', fontsize=10)
        ax3.set_title('Network Overhead as % of Workflow Time', fontsize=12, fontweight='bold')
        ax3.grid(axis='y', alpha=0.3)
        
        for bar in bars5:
            height = bar.get_height()
            ax3.annotate(f'{height:.2f}%',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),
                        textcoords="offset points",
                        ha='center', va='bottom',
                        fontsize=10,
                        fontweight='bold')
        
        # 4. Performance Comparison Summary
        ax4.axis('off')
        summary_text = f"""
PERFORMANCE SUMMARY

gRPC Microservices (Chained):
  Total Processing:  {self.grpc_metrics['total_processing_time']:.4f}s
  Workflow Time:     {self.grpc_metrics['workflow_time']:.4f}s
  Network Overhead:  {self.grpc_metrics['network_overhead']:.4f}s ({grpc_overhead_pct:.2f}%)

XML-RPC Monolithic (Individual Calls):
  Total Processing:  {self.xmlrpc_metrics['total_processing_time']:.4f}s
  Workflow Time:     {self.xmlrpc_metrics['workflow_time']:.4f}s
  Network Overhead:  {self.xmlrpc_metrics['network_overhead']:.4f}s ({xmlrpc_overhead_pct:.2f}%)

Speed Comparison:
"""
        if self.grpc_metrics['workflow_time'] < self.xmlrpc_metrics['workflow_time']:
            speedup = ((self.xmlrpc_metrics['workflow_time'] - self.grpc_metrics['workflow_time']) 
                      / self.grpc_metrics['workflow_time']) * 100
            summary_text += f"  gRPC is {speedup:.2f}% FASTER than XML-RPC"
        else:
            speedup = ((self.grpc_metrics['workflow_time'] - self.xmlrpc_metrics['workflow_time']) 
                      / self.xmlrpc_metrics['workflow_time']) * 100
            summary_text += f"  XML-RPC is {speedup:.2f}% FASTER than gRPC"
        
        ax4.text(0.1, 0.5, summary_text, transform=ax4.transAxes,
                fontsize=10, verticalalignment='center',
                fontfamily='monospace',
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.3))
        
        plt.tight_layout()
        
        # Save chart
        output_path = os.path.join(self.results_dir, output_file)
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"\n✓ Detailed comparison chart saved to {output_file}")
        
        plt.close()
    
    def _generate_summary_chart(self, output_file):
        """Generate summary chart for old format metrics"""
        grpc_summary = self.grpc_metrics['summary']
        xmlrpc_summary = self.xmlrpc_metrics['summary']
        
        # Data for plotting
        categories = ['Server Time', 'Network Overhead', 'Total Time']
        grpc_times = [
            grpc_summary['avg_server_time'],
            grpc_summary['avg_network_overhead'],
            grpc_summary['avg_total_time']
        ]
        xmlrpc_times = [
            xmlrpc_summary['avg_server_time'],
            xmlrpc_summary['avg_network_overhead'],
            xmlrpc_summary['avg_total_time']
        ]
        
        # Create figure with subplots
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # Bar chart comparison
        x = np.arange(len(categories))
        width = 0.35
        
        bars1 = ax1.bar(x - width/2, grpc_times, width, label='gRPC', color='#4285F4')
        bars2 = ax1.bar(x + width/2, xmlrpc_times, width, label='XML-RPC', color='#EA4335')
        
        ax1.set_xlabel('Metrics')
        ax1.set_ylabel('Time (seconds)')
        ax1.set_title('Performance Comparison: gRPC vs XML-RPC')
        ax1.set_xticks(x)
        ax1.set_xticklabels(categories)
        ax1.legend()
        ax1.grid(axis='y', alpha=0.3)
        
        # Add value labels on bars
        for bars in [bars1, bars2]:
            for bar in bars:
                height = bar.get_height()
                ax1.annotate(f'{height:.6f}',
                            xy=(bar.get_x() + bar.get_width() / 2, height),
                            xytext=(0, 3),
                            textcoords="offset points",
                            ha='center', va='bottom',
                            fontsize=8)
        
        # Pie chart for overhead percentage
        grpc_overhead_pct = (grpc_summary['avg_network_overhead'] / grpc_summary['avg_total_time']) * 100
        xmlrpc_overhead_pct = (xmlrpc_summary['avg_network_overhead'] / xmlrpc_summary['avg_total_time']) * 100
        
        overhead_data = [grpc_overhead_pct, xmlrpc_overhead_pct]
        labels = [f'gRPC\n{grpc_overhead_pct:.2f}%', f'XML-RPC\n{xmlrpc_overhead_pct:.2f}%']
        colors = ['#4285F4', '#EA4335']
        
        ax2.pie(overhead_data, labels=labels, colors=colors, autopct='', startangle=90)
        ax2.set_title('Network Overhead as % of Total Time')
        
        plt.tight_layout()
        
        # Save chart
        output_path = os.path.join(self.results_dir, output_file)
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"\n✓ Summary comparison chart saved to {output_file}")
        
        plt.close()
    
    def generate_report(self, output_file='comparison_report.txt'):
        """Generate detailed text report"""
        try:
            output_path = os.path.join(self.results_dir, output_file)
            
            with open(output_path, 'w', encoding='utf-8') as f:
                # Redirect stdout to file
                original_stdout = sys.stdout
                sys.stdout = f
                
                print("="*80)
                print("PROTOCOL PERFORMANCE COMPARISON REPORT")
                print("="*80)
                print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                print(f"gRPC Test: {self.grpc_metrics['timestamp']}")
                print(f"XML-RPC Test: {self.xmlrpc_metrics['timestamp']}")
                print("="*80)
                
                # Print all comparisons
                self.print_summary_comparison()
                self.print_detailed_comparison()
                
                print("\n" + "="*80)
                print("KEY FINDINGS")
                print("="*80)
                
                # Extract values from metrics (handle both with and without summary)
                grpc_total = self.grpc_metrics.get('workflow_time', 0)
                xmlrpc_total = self.xmlrpc_metrics.get('workflow_time', 0)
                
                grpc_overhead = self.grpc_metrics.get('network_overhead', 0)
                xmlrpc_overhead = self.xmlrpc_metrics.get('network_overhead', 0)
                
                grpc_processing = self.grpc_metrics.get('total_processing_time', 0)
                xmlrpc_processing = self.xmlrpc_metrics.get('total_processing_time', 0)
                
                print("\n1. PROTOCOL EFFICIENCY:")
                if grpc_total < xmlrpc_total:
                    speedup = xmlrpc_total / grpc_total
                    print(f"   gRPC is {speedup:.2f}x faster overall than XML-RPC")
                    print(f"   Time saved per request: {(xmlrpc_total - grpc_total)*1000:.3f} milliseconds")
                else:
                    speedup = grpc_total / xmlrpc_total
                    print(f"   XML-RPC is {speedup:.2f}x faster overall than gRPC")
                    print(f"   Time saved per request: {(grpc_total - xmlrpc_total)*1000:.3f} milliseconds")
                
                print("\n2. NETWORK OVERHEAD:")
                grpc_overhead_pct = (grpc_overhead / grpc_total) * 100 if grpc_total > 0 else 0
                xmlrpc_overhead_pct = (xmlrpc_overhead / xmlrpc_total) * 100 if xmlrpc_total > 0 else 0
                print(f"   gRPC network overhead: {grpc_overhead_pct:.2f}% of total time")
                print(f"   XML-RPC network overhead: {xmlrpc_overhead_pct:.2f}% of total time")
                
                print("\n3. SERIALIZATION:")
                print("   gRPC uses Protocol Buffers (binary)")
                print("   XML-RPC uses XML (text-based)")
                if grpc_overhead < xmlrpc_overhead:
                    print("   → Protocol Buffers show better network efficiency")
                
                print("\n4. RECOMMENDATIONS:")
                print("   • Use gRPC for:")
                print("     - High-performance requirements")
                print("     - Binary data transmission")
                print("     - Streaming support needed")
                print("     - Microservices architecture")
                print("\n   • Use XML-RPC for:")
                print("     - Simple request/response patterns")
                print("     - Human-readable messages")
                print("     - Legacy system integration")
                print("     - Debugging and development")
                
                print("\n" + "="*80)
                print("END OF REPORT")
                print("="*80)
                
                # Restore stdout
                sys.stdout = original_stdout
            
            print(f"✓ Detailed report saved to {output_file}")
            
        except Exception as e:
            print(f"✗ Error generating report: {str(e)}")


def main():
    """Main execution"""
    print("="*80)
    print("Protocol Performance Comparison Tool")
    print("="*80)
    
    # Determine paths
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    results_dir = os.path.join(project_root, 'results')
    
    # Create comparator
    comparator = ProtocolComparator(results_dir)
    
    # Check for available metrics files
    available_files = []
    for file in os.listdir(results_dir):
        if file.endswith('_performance_metrics.json'):
            available_files.append(file)
    
    if not available_files:
        print("\n✗ No performance metrics files found in results directory")
        print("Please run both gRPC and XML-RPC clients first to generate metrics.")
        return
    
    print(f"\nFound {len(available_files)} metrics files:")
    for file in available_files:
        print(f"  - {file}")
    
    # Try to find matching pairs
    grpc_files = [f for f in available_files if 'grpc' in f.lower()]
    xmlrpc_files = [f for f in available_files if 'xmlrpc' in f.lower()]
    
    if not grpc_files or not xmlrpc_files:
        print("\n✗ Missing metrics from one or both protocols")
        print(f"gRPC files: {len(grpc_files)}, XML-RPC files: {len(xmlrpc_files)}")
        return
    
    # Compare native implementations
    print("\n" + "="*80)
    print("Comparing Native Implementations (localhost)")
    print("="*80)
    
    grpc_native = next((f for f in grpc_files if 'docker' not in f.lower() and 'swarm' not in f.lower()), None)
    xmlrpc_native = next((f for f in xmlrpc_files if 'docker' not in f.lower() and 'swarm' not in f.lower()), None)
    
    if grpc_native and xmlrpc_native:
        if comparator.load_metrics(grpc_native, xmlrpc_native):
            comparator.print_summary_comparison()
            comparator.print_detailed_comparison()
            comparator.generate_comparison_chart('native_comparison.png')
            comparator.generate_report('native_comparison_report.txt')
    
    # Compare Docker implementations
    print("\n" + "="*80)
    print("Comparing Docker Implementations")
    print("="*80)
    
    grpc_docker = next((f for f in grpc_files if 'docker' in f.lower() and 'swarm' not in f.lower()), None)
    xmlrpc_docker = next((f for f in xmlrpc_files if 'docker' in f.lower() and 'swarm' not in f.lower()), None)
    
    if grpc_docker and xmlrpc_docker:
        if comparator.load_metrics(grpc_docker, xmlrpc_docker):
            comparator.print_summary_comparison()
            comparator.print_detailed_comparison()
            comparator.generate_comparison_chart('docker_comparison.png')
            comparator.generate_report('docker_comparison_report.txt')
    
    # Compare Swarm implementations
    print("\n" + "="*80)
    print("Comparing Docker Swarm Implementations")
    print("="*80)
    
    grpc_swarm = next((f for f in grpc_files if 'swarm' in f.lower()), None)
    xmlrpc_swarm = next((f for f in xmlrpc_files if 'swarm' in f.lower()), None)
    
    if grpc_swarm and xmlrpc_swarm:
        if comparator.load_metrics(grpc_swarm, xmlrpc_swarm):
            comparator.print_summary_comparison()
            comparator.print_detailed_comparison()
            comparator.generate_comparison_chart('swarm_comparison.png')
            comparator.generate_report('swarm_comparison_report.txt')
    
    print("\n" + "="*80)
    print("Comparison Complete!")
    print("="*80)


if __name__ == '__main__':
    main()
