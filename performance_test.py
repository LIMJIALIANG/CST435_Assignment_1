"""
Performance Comparison Script
Tests all implementations and generates comparison report
"""
import time
import subprocess
import json
import os
from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd


class PerformanceTester:
    """Performance testing for all MapReduce implementations"""
    
    def __init__(self):
        self.results = {
            'grpc': [],
            'xmlrpc': [],
            'reqrep': [],
            'mpi': []
        }
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    def test_grpc(self, num_runs=5):
        """Test gRPC implementation"""
        print("\n" + "="*60)
        print("Testing gRPC Implementation")
        print("="*60)
        
        for run in range(num_runs):
            print(f"\nRun {run + 1}/{num_runs}")
            
            # Start servers
            print("Starting gRPC servers...")
            subprocess.run([
                "docker-compose", "-f", "docker/docker-compose.yml",
                "up", "-d", "grpc-server-1", "grpc-server-2", "grpc-server-3"
            ])
            
            # Wait for servers to be ready
            time.sleep(5)
            
            # Run client and capture output
            start_time = time.time()
            result = subprocess.run([
                "docker-compose", "-f", "docker/docker-compose.yml",
                "run", "--rm", "grpc-client"
            ], capture_output=True, text=True)
            
            duration = time.time() - start_time
            
            self.results['grpc'].append({
                'run': run + 1,
                'duration': duration,
                'output': result.stdout
            })
            
            print(f"Duration: {duration:.4f}s")
            
            # Stop servers
            subprocess.run([
                "docker-compose", "-f", "docker/docker-compose.yml",
                "down"
            ])
            
            time.sleep(2)
        
        return self.results['grpc']
    
    def test_xmlrpc(self, num_runs=5):
        """Test XML-RPC implementation"""
        print("\n" + "="*60)
        print("Testing XML-RPC Implementation")
        print("="*60)
        
        for run in range(num_runs):
            print(f"\nRun {run + 1}/{num_runs}")
            
            # Start servers
            print("Starting XML-RPC servers...")
            subprocess.run([
                "docker-compose", "-f", "docker/docker-compose.yml",
                "up", "-d", "xmlrpc-server-1", "xmlrpc-server-2", "xmlrpc-server-3"
            ])
            
            # Wait for servers to be ready
            time.sleep(5)
            
            # Run client and capture output
            start_time = time.time()
            result = subprocess.run([
                "docker-compose", "-f", "docker/docker-compose.yml",
                "run", "--rm", "xmlrpc-client"
            ], capture_output=True, text=True)
            
            duration = time.time() - start_time
            
            self.results['xmlrpc'].append({
                'run': run + 1,
                'duration': duration,
                'output': result.stdout
            })
            
            print(f"Duration: {duration:.4f}s")
            
            # Stop servers
            subprocess.run([
                "docker-compose", "-f", "docker/docker-compose.yml",
                "down"
            ])
            
            time.sleep(2)
        
        return self.results['xmlrpc']
    
    def test_mpi(self, num_runs=5):
        """Test MPI implementation"""
        print("\n" + "="*60)
        print("Testing MPI Implementation")
        print("="*60)
        
        for run in range(num_runs):
            print(f"\nRun {run + 1}/{num_runs}")
            
            # Run MPI container
            start_time = time.time()
            result = subprocess.run([
                "docker-compose", "-f", "docker/docker-compose.yml",
                "run", "--rm", "mpi-runner"
            ], capture_output=True, text=True)
            
            duration = time.time() - start_time
            
            self.results['mpi'].append({
                'run': run + 1,
                'duration': duration,
                'output': result.stdout
            })
            
            print(f"Duration: {duration:.4f}s")
            
            time.sleep(2)
        
        return self.results['mpi']
    
    def test_reqrep(self, num_runs=5):
        """Test Request-Reply implementation"""
        print("\n" + "="*60)
        print("Testing Request-Reply Implementation")
        print("="*60)
        
        for run in range(num_runs):
            print(f"\nRun {run + 1}/{num_runs}")
            
            # Start servers
            print("Starting Request-Reply servers...")
            subprocess.run([
                "docker-compose", "-f", "docker/docker-compose.yml",
                "up", "-d", "reqrep-server-1", "reqrep-server-2", "reqrep-server-3"
            ])
            
            # Wait for servers to be ready
            time.sleep(5)
            
            # Run client and capture output
            start_time = time.time()
            result = subprocess.run([
                "docker-compose", "-f", "docker/docker-compose.yml",
                "run", "--rm", "reqrep-client"
            ], capture_output=True, text=True)
            
            duration = time.time() - start_time
            
            self.results['reqrep'].append({
                'run': run + 1,
                'duration': duration,
                'output': result.stdout
            })
            
            print(f"Duration: {duration:.4f}s")
            
            # Stop servers
            subprocess.run([
                "docker-compose", "-f", "docker/docker-compose.yml",
                "down"
            ])
            
            time.sleep(2)
        
        return self.results['reqrep']
    
    def generate_report(self):
        """Generate performance comparison report"""
        print("\n" + "="*60)
        print("PERFORMANCE COMPARISON REPORT")
        print("="*60)
        
        # Calculate statistics
        stats = {}
        for impl, runs in self.results.items():
            if runs:
                durations = [r['duration'] for r in runs]
                stats[impl] = {
                    'mean': sum(durations) / len(durations),
                    'min': min(durations),
                    'max': max(durations),
                    'runs': len(durations)
                }
        
        # Print statistics
        print("\nExecution Times (seconds):")
        print(f"{'Implementation':<20} {'Mean':<10} {'Min':<10} {'Max':<10} {'Runs':<10}")
        print("-" * 60)
        
        for impl, data in stats.items():
            print(f"{impl:<20} {data['mean']:<10.4f} {data['min']:<10.4f} {data['max']:<10.4f} {data['runs']:<10}")
        
        # Create comparison chart
        self._create_charts(stats)
        
        # Save results to JSON
        self._save_results(stats)
        
        return stats
    
    def _create_charts(self, stats):
        """Create comparison charts"""
        if not stats:
            print("No data to plot")
            return
        
        # Create figure with subplots
        fig, axes = plt.subplots(1, 2, figsize=(15, 6))
        
        # Bar chart - Mean execution time
        implementations = list(stats.keys())
        means = [stats[impl]['mean'] for impl in implementations]
        
        axes[0].bar(implementations, means, color=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728'])
        axes[0].set_xlabel('Implementation')
        axes[0].set_ylabel('Mean Execution Time (seconds)')
        axes[0].set_title('Performance Comparison - Mean Execution Time')
        axes[0].grid(axis='y', alpha=0.3)
        
        # Box plot - Distribution
        all_durations = []
        labels = []
        for impl in implementations:
            durations = [r['duration'] for r in self.results[impl]]
            all_durations.append(durations)
            labels.append(impl)
        
        axes[1].boxplot(all_durations, labels=labels)
        axes[1].set_xlabel('Implementation')
        axes[1].set_ylabel('Execution Time (seconds)')
        axes[1].set_title('Performance Distribution')
        axes[1].grid(axis='y', alpha=0.3)
        
        plt.tight_layout()
        
        # Save plot
        output_dir = 'performance_results'
        os.makedirs(output_dir, exist_ok=True)
        plot_file = os.path.join(output_dir, f'performance_comparison_{self.timestamp}.png')
        plt.savefig(plot_file, dpi=300, bbox_inches='tight')
        print(f"\nChart saved to: {plot_file}")
        
        plt.show()
    
    def _save_results(self, stats):
        """Save results to JSON file"""
        output_dir = 'performance_results'
        os.makedirs(output_dir, exist_ok=True)
        
        # Prepare data
        output = {
            'timestamp': self.timestamp,
            'statistics': stats,
            'raw_results': self.results
        }
        
        # Save to JSON
        json_file = os.path.join(output_dir, f'results_{self.timestamp}.json')
        with open(json_file, 'w') as f:
            json.dump(output, f, indent=2)
        
        print(f"Results saved to: {json_file}")
        
        # Save to CSV
        csv_data = []
        for impl, runs in self.results.items():
            for run in runs:
                csv_data.append({
                    'Implementation': impl,
                    'Run': run['run'],
                    'Duration': run['duration']
                })
        
        df = pd.DataFrame(csv_data)
        csv_file = os.path.join(output_dir, f'results_{self.timestamp}.csv')
        df.to_csv(csv_file, index=False)
        print(f"CSV saved to: {csv_file}")


def main():
    """Run performance tests"""
    print("MapReduce Performance Testing")
    print("This will test all implementations and generate comparison report")
    
    tester = PerformanceTester()
    
    # Number of runs per implementation
    num_runs = 3
    
    # Test each implementation
    try:
        # Test gRPC
        tester.test_grpc(num_runs)
        
        # Test XML-RPC
        tester.test_xmlrpc(num_runs)
        
        # Test Request-Reply
        tester.test_reqrep(num_runs)
        
        # Test MPI
        tester.test_mpi(num_runs)
        
    except KeyboardInterrupt:
        print("\n\nTesting interrupted by user")
    except Exception as e:
        print(f"\n\nError during testing: {e}")
    finally:
        # Clean up
        subprocess.run([
            "docker-compose", "-f", "docker/docker-compose.yml", "down"
        ])
    
    # Generate report
    stats = tester.generate_report()
    
    print("\n" + "="*60)
    print("Testing completed!")
    print("="*60)


if __name__ == '__main__':
    main()
