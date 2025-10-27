"""
Performance Testing Script - Automatic Server Detection
Compare gRPC vs XML-RPC vs MPI
Automatically detects number of running servers and adjusts tests accordingly
Generates visual comparison charts
"""
import argparse
import time
import os
import sys
import subprocess
from datetime import datetime
import matplotlib.pyplot as plt
import json

def detect_running_servers(protocol, max_servers=10):
    """Detect how many servers are running for a given protocol"""
    import socket
    
    if protocol == 'grpc':
        base_port = 50051
    elif protocol == 'xmlrpc':
        base_port = 8000
    else:
        return 0
    
    running_servers = []
    for i in range(max_servers):
        port = base_port + i
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5)
        result = sock.connect_ex(('localhost', port))
        sock.close()
        
        if result == 0:  # Port is open
            running_servers.append(port)
    
    return len(running_servers)

def test_grpc(data_file):
    '''Test gRPC - automatically detects and uses available servers'''
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'grpc_implementation'))
    
    import grpc
    import mapreduce_pb2
    import mapreduce_pb2_grpc
    from collections import Counter
    
    with open(data_file, 'r') as f:
        text = f.read()
    
    # Detect running servers
    num_servers = detect_running_servers('grpc')
    
    if num_servers == 0:
        print(f'\n❌ No gRPC servers detected. Please start at least one server.')
        return None
    
    print(f'\n📊 Testing gRPC with {data_file} ({num_servers} server{"s" if num_servers > 1 else ""}, all 3 services)')
    print(f'   Text: {len(text):,} chars, {len(text.split()):,} words')
    
    # Configure channel options to handle larger messages (100MB max)
    options = [
        ('grpc.max_send_message_length', 100 * 1024 * 1024),  # 100MB
        ('grpc.max_receive_message_length', 100 * 1024 * 1024),  # 100MB
    ]
    
    server_address = 'localhost:50051'
    channel = grpc.insecure_channel(server_address, options=options)
    stub = mapreduce_pb2_grpc.MapReduceServiceStub(channel)
    
    start = time.time()
    request = mapreduce_pb2.MapRequest(text_chunk=text, chunk_id=0)
    response = stub.Map(request)
    reduce_request = mapreduce_pb2.ReduceRequest(intermediate_counts=response.word_counts)
    reduce_response = stub.Reduce(reduce_request)
    time1 = time.time() - start
    
    start = time.time()
    request = mapreduce_pb2.SortWordsRequest(text_chunk=text, chunk_id=0)
    response = stub.SortWords(request)
    sorted_words = list(response.sorted_words)
    time2 = time.time() - start
    
    start = time.time()
    request = mapreduce_pb2.WordLengthRequest(text_chunk=text, chunk_id=0)
    response = stub.AnalyzeWordLengths(request)
    time3 = time.time() - start
    
    channel.close()
    
    total = time1 + time2 + time3
    
    print(f'\n   ⏱️  gRPC Results ({num_servers} server{"s" if num_servers > 1 else ""}):')
    print(f'      Service 1 (Word Count):    {time1:.4f}s')
    print(f'      Service 2 (Sorting):       {time2:.4f}s')
    print(f'      Service 3 (Word Lengths):  {time3:.4f}s')
    print(f'      Total:                     {total:.4f}s')
    
    return {
        'protocol': 'gRPC', 
        'service1': time1, 
        'service2': time2, 
        'service3': time3, 
        'total': total,
        'num_servers': num_servers
    }

def test_xmlrpc(data_file):
    '''Test XML-RPC - automatically detects and uses available servers'''
    import xmlrpc.client
    
    with open(data_file, 'r') as f:
        text = f.read()
    
    # Detect running servers
    num_servers = detect_running_servers('xmlrpc')
    
    if num_servers == 0:
        print(f'\n❌ No XML-RPC servers detected. Please start at least one server.')
        return None
    
    print(f'\n📊 Testing XML-RPC with {data_file} ({num_servers} server{"s" if num_servers > 1 else ""}, all 3 services)')
    print(f'   Text: {len(text):,} chars, {len(text.split()):,} words')
    
    server_address = 'http://localhost:8000'
    proxy = xmlrpc.client.ServerProxy(server_address)
    
    start = time.time()
    map_result = proxy.map_operation(text, 0)
    reduce_result = proxy.reduce_operation(map_result['word_counts'])
    time1 = time.time() - start
    
    start = time.time()
    sort_result = proxy.sort_words(text, 0)
    time2 = time.time() - start
    
    start = time.time()
    length_result = proxy.analyze_word_lengths(text, 0)
    time3 = time.time() - start
    
    total = time1 + time2 + time3
    
    print(f'\n   ⏱️  XML-RPC Results ({num_servers} server{"s" if num_servers > 1 else ""}):')
    print(f'      Service 1 (Word Count):    {time1:.4f}s')
    print(f'      Service 2 (Sorting):       {time2:.4f}s')
    print(f'      Service 3 (Word Lengths):  {time3:.4f}s')
    print(f'      Total:                     {total:.4f}s')
    
    return {
        'protocol': 'XML-RPC', 
        'service1': time1, 
        'service2': time2, 
        'service3': time3, 
        'total': total,
        'num_servers': num_servers
    }

def test_mpi(data_file):
    '''Test MPI - runs as single job with 3 internal processes'''
    
    with open(data_file, 'r') as f:
        text = f.read()
    
    print(f'\n📊 Testing MPI with {data_file} (1 container, 3 internal processes)')
    print(f'   Text: {len(text):,} chars, {len(text.split()):,} words')
    
    workspace_root = os.path.dirname(os.path.abspath(__file__))
    rel_data_file = os.path.relpath(data_file, workspace_root)
    docker_data_file = f'/app/{rel_data_file.replace(os.sep, "/")}'
    
    test_script_content = """
import sys
import os
sys.path.insert(0, '/app/mpi_implementation')

from mpi4py import MPI
import time
import re
from collections import Counter
import heapq

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

with open('""" + docker_data_file + """', 'r') as f:
    text = f.read()

def split_text(text, num_chunks):
    lines = text.strip().split('\\n')
    chunk_size = max(1, len(lines) // num_chunks)
    chunks = []
    for i in range(num_chunks):
        start = i * chunk_size
        end = start + chunk_size if i < num_chunks - 1 else len(lines)
        chunk = '\\n'.join(lines[start:end])
        chunks.append(chunk)
    return chunks

comm.Barrier()
start_time = time.time()

if rank == 0:
    chunks = split_text(text, size)
else:
    chunks = None

chunk = comm.scatter(chunks, root=0)
words = re.findall(r'\\b\\w+\\b', chunk.lower())
local_counts = dict(Counter(words))
all_counts = comm.gather(local_counts, root=0)

if rank == 0:
    final_counts = Counter()
    for counts in all_counts:
        if counts:
            final_counts.update(counts)
    time1 = time.time() - start_time
else:
    time1 = 0

comm.Barrier()
if rank == 0:
    start = time.time()

if rank == 0:
    chunks = split_text(text, size)
else:
    chunks = None

chunk = comm.scatter(chunks, root=0)
words = list(set(re.findall(r'\\b\\w+\\b', chunk.lower())))
local_sorted = sorted(words)
all_sorted = comm.gather(local_sorted, root=0)

if rank == 0:
    final_sorted = list(heapq.merge(*all_sorted))
    time2 = time.time() - start
else:
    time2 = 0

comm.Barrier()
if rank == 0:
    start = time.time()

if rank == 0:
    chunks = split_text(text, size)
else:
    chunks = None

chunk = comm.scatter(chunks, root=0)
words = re.findall(r'\\b\\w+\\b', chunk.lower())
length_dist = Counter()
for word in words:
    length_dist[len(word)] += 1

local_result = {'length_distribution': dict(length_dist)}
all_results = comm.gather(local_result, root=0)

if rank == 0:
    all_distributions = Counter()
    for result in all_results:
        if result:
            all_distributions.update(result['length_distribution'])
    time3 = time.time() - start
    
    total = time1 + time2 + time3
    print(f"{time1:.4f},{time2:.4f},{time3:.4f},{total:.4f}")
"""
    
    temp_script = os.path.join(workspace_root, f'_temp_mpi_test_{os.getpid()}.py')
    
    with open(temp_script, 'w') as f:
        f.write(test_script_content)
    
    try:
        rel_script = os.path.relpath(temp_script, workspace_root)
        docker_script = f'/app/{rel_script.replace(os.sep, "/")}'
        
        result = subprocess.run(
            ['docker', 'run', '--rm', '-v', f'{workspace_root}:/app',
             'docker-mpi-runner', 'mpiexec', '-n', '3', '--allow-run-as-root',
             'python', docker_script],
            capture_output=True, text=True, timeout=300
        )
        
        if result.returncode != 0:
            print(f'\n❌ MPI Docker execution failed (exit code {result.returncode})')
            print(f'STDOUT: {result.stdout}')
            print(f'STDERR: {result.stderr}')
            return None
        
        stdout_lines = result.stdout.strip().split('\n')
        timing_line = None
        for line in reversed(stdout_lines):
            if line and ',' in line and not line.startswith(' '):
                try:
                    parts = line.split(',')
                    if len(parts) == 4:
                        time1, time2, time3, total = map(float, parts)
                        timing_line = line
                        break
                except ValueError:
                    continue
        
        if not timing_line:
            print(f'\n❌ Could not find timing data in MPI output:')
            print(f'STDOUT:\n{result.stdout}')
            return None
        
        print(f'\n   ⏱️  MPI Results (1 container, 3 processes):')
        print(f'      Service 1 (Word Count):    {time1:.4f}s')
        print(f'      Service 2 (Sorting):       {time2:.4f}s')
        print(f'      Service 3 (Word Lengths):  {time3:.4f}s')
        print(f'      Total:                     {total:.4f}s')
        
        return {
            'protocol': 'MPI', 
            'service1': time1, 
            'service2': time2, 
            'service3': time3, 
            'total': total,
            'num_servers': 1  # MPI always runs in 1 container
        }
        
    except subprocess.TimeoutExpired:
        print(f'\n❌ MPI test timed out (>5 minutes)')
        return None
    except Exception as e:
        print(f'\n❌ MPI test failed: {e}')
        print(f'   Make sure Docker is running and MPI image is built:')
        print(f'   cd docker && docker-compose build mpi-runner')
        return None
    finally:
        try:
            os.unlink(temp_script)
        except:
            pass

def compare_results(grpc_result, xmlrpc_result, mpi_result=None):
    '''Compare and display results'''
    
    # Collect server counts
    server_counts = {}
    if mpi_result:
        server_counts['MPI'] = 1  # MPI always 1 container
    if grpc_result:
        server_counts['gRPC'] = grpc_result.get('num_servers', 1)
    if xmlrpc_result:
        server_counts['XML-RPC'] = xmlrpc_result.get('num_servers', 1)
    
    # Determine title based on server counts
    if len(set(server_counts.values())) == 1:
        # All protocols using same number of servers
        num = list(server_counts.values())[0]
        title_suffix = f'({num} Container{"s" if num > 1 else ""} Each)'
    else:
        # Different number of servers
        server_info = ', '.join([f'{name}: {count}' for name, count in server_counts.items()])
        title_suffix = f'(Containers: {server_info})'
    
    print('\n' + '='*70)
    print(f'📊 PERFORMANCE COMPARISON {title_suffix}')
    print('='*70)
    
    protocols = []
    if mpi_result:
        protocols.append(('MPI', mpi_result))
    if grpc_result:
        protocols.append(('gRPC', grpc_result))
    if xmlrpc_result:
        protocols.append(('XML-RPC', xmlrpc_result))
    
    if len(protocols) < 2:
        print('Not enough protocols tested for comparison')
        return None
    
    header = f"{'Service':<30}"
    for name, _ in protocols:
        header += f' {name:<15}'
    print(header)
    print('-' * 70)
    
    services = [
        ('Service 1 (Word Count)', 'service1'),
        ('Service 2 (Sorting)', 'service2'),
        ('Service 3 (Word Lengths)', 'service3'),
        ('TOTAL', 'total')
    ]
    
    for service_name, key in services:
        line = f'{service_name:<30}'
        times = []
        for name, result in protocols:
            time_val = result[key]
            times.append((name, time_val))
            line += f' {time_val:>7.4f}s      '
        
        fastest = min(times, key=lambda x: x[1])
        line += f' ✅ {fastest[0]}'
        print(line)
    
    print('\n' + '='*70)
    
    total_times = [(name, result['total']) for name, result in protocols]
    fastest = min(total_times, key=lambda x: x[1])
    
    print(f'🏆 OVERALL WINNER: {fastest[0]} ({fastest[1]:.4f}s)\n')
    
    print('Speedup Comparisons:')
    for name1, time1 in total_times:
        for name2, time2 in total_times:
            if name1 != name2 and time1 < time2:
                speedup = time2 / time1
                print(f'  {name1} is {speedup:.2f}x faster than {name2}')
    
    print('='*70)
    
    return protocols, server_counts

def create_visualization(protocols, data_file, server_counts):
    '''Create bar charts comparing protocols'''
    if not protocols or len(protocols) < 2:
        return
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_dir = 'performance_results'
    os.makedirs(output_dir, exist_ok=True)
    
    # Determine title based on server counts
    if len(set(server_counts.values())) == 1:
        # All protocols using same number of servers
        num = list(server_counts.values())[0]
        title_suffix = f'{num} Container{"s" if num > 1 else ""} Each'
    else:
        # Different number of servers - show details
        server_info = ', '.join([f'{name}: {count}' for name, count in server_counts.items()])
        title_suffix = f'Containers: {server_info}'
    
    # Prepare data
    protocol_names = [name for name, _ in protocols]
    service1_times = [result['service1'] for _, result in protocols]
    service2_times = [result['service2'] for _, result in protocols]
    service3_times = [result['service3'] for _, result in protocols]
    total_times = [result['total'] for _, result in protocols]
    
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    fig.suptitle(f'Performance Comparison ({title_suffix})\\n{os.path.basename(data_file)}', 
                 fontsize=16, fontweight='bold')
    
    colors = {'MPI': '#2ca02c', 'gRPC': '#1f77b4', 'XML-RPC': '#ff7f0e'}
    bar_colors = [colors.get(name, '#d62728') for name in protocol_names]
    
    axes[0, 0].bar(protocol_names, service1_times, color=bar_colors, alpha=0.8)
    axes[0, 0].set_ylabel('Execution Time (seconds)', fontsize=11)
    axes[0, 0].set_title('Service 1: Word Count (MapReduce)', fontsize=12, fontweight='bold')
    axes[0, 0].grid(axis='y', alpha=0.3)
    for i, (name, time_val) in enumerate(zip(protocol_names, service1_times)):
        axes[0, 0].text(i, time_val, f'{time_val:.4f}s', ha='center', va='bottom', fontsize=9)
    
    axes[0, 1].bar(protocol_names, service2_times, color=bar_colors, alpha=0.8)
    axes[0, 1].set_ylabel('Execution Time (seconds)', fontsize=11)
    axes[0, 1].set_title('Service 2: Alphabetical Sorting', fontsize=12, fontweight='bold')
    axes[0, 1].grid(axis='y', alpha=0.3)
    for i, (name, time_val) in enumerate(zip(protocol_names, service2_times)):
        axes[0, 1].text(i, time_val, f'{time_val:.4f}s', ha='center', va='bottom', fontsize=9)
    
    axes[1, 0].bar(protocol_names, service3_times, color=bar_colors, alpha=0.8)
    axes[1, 0].set_ylabel('Execution Time (seconds)', fontsize=11)
    axes[1, 0].set_title('Service 3: Word Length Analysis', fontsize=12, fontweight='bold')
    axes[1, 0].grid(axis='y', alpha=0.3)
    for i, (name, time_val) in enumerate(zip(protocol_names, service3_times)):
        axes[1, 0].text(i, time_val, f'{time_val:.4f}s', ha='center', va='bottom', fontsize=9)
    
    axes[1, 1].bar(protocol_names, total_times, color=bar_colors, alpha=0.8, edgecolor='black', linewidth=2)
    axes[1, 1].set_ylabel('Execution Time (seconds)', fontsize=11)
    axes[1, 1].set_title('TOTAL EXECUTION TIME', fontsize=12, fontweight='bold')
    axes[1, 1].grid(axis='y', alpha=0.3)
    for i, (name, time_val) in enumerate(zip(protocol_names, total_times)):
        axes[1, 1].text(i, time_val, f'{time_val:.4f}s', ha='center', va='bottom', fontsize=10, fontweight='bold')
    
    min_total = min(total_times)
    winner_idx = total_times.index(min_total)
    axes[1, 1].patches[winner_idx].set_edgecolor('gold')
    axes[1, 1].patches[winner_idx].set_linewidth(3)
    
    plt.tight_layout()
    
    plot_file = os.path.join(output_dir, f'performance_comparison_{timestamp}.png')
    plt.savefig(plot_file, dpi=300, bbox_inches='tight')
    print(f'\n📊 Visualization saved to: {plot_file}')
    
    results_data = {
        'timestamp': timestamp,
        'protocols': {}
    }
    
    for name, result in protocols:
        results_data['protocols'][name] = {
            'service1': result['service1'],
            'service2': result['service2'],
            'service3': result['service3'],
            'total': result['total'],
            'num_servers': result.get('num_servers', 1)
        }
    
    json_file = os.path.join(output_dir, f'performance_results_{timestamp}.json')
    with open(json_file, 'w') as f:
        json.dump(results_data, f, indent=2)
    print(f'📄 Results saved to: {json_file}')
    with open(json_file, 'w') as f:
        json.dump(results_data, f, indent=2)
    print(f'📄 Results saved to: {json_file}')
    
    plt.show()

def main():
    parser = argparse.ArgumentParser(description='Performance test with automatic server detection')
    parser.add_argument('--data', type=str, required=True, help='Path to data file')
    parser.add_argument('--protocol', type=str, choices=['grpc', 'xmlrpc', 'mpi', 'all'], default='all',
                       help='Protocol to test (grpc, xmlrpc, mpi, or all)')
    
    args = parser.parse_args()
    
    print('='*70)
    print('🚀 PERFORMANCE TEST (Automatic Server Detection)')
    print('='*70)
    print(f'Data File: {args.data}')
    print(f'Protocol: {args.protocol}')
    print('\nDetecting running servers...')
    
    if not os.path.exists(args.data):
        print(f'\n❌ Error: File not found: {args.data}')
        print('💡 Run generate_large_data.py to create test datasets')
        return
    
    grpc_result = None
    xmlrpc_result = None
    mpi_result = None
    
    if args.protocol in ['mpi', 'all']:
        try:
            mpi_result = test_mpi(args.data)
        except Exception as e:
            print(f'\n❌ MPI test failed: {e}')
            print('💡 Make sure Docker is running and MPI image is built')
    
    if args.protocol in ['grpc', 'all']:
        try:
            grpc_result = test_grpc(args.data)
        except Exception as e:
            print(f'\n❌ gRPC test failed: {e}')
            print('💡 Make sure gRPC server is running:')
            print('   docker-compose up -d grpc-server-1')
    
    if args.protocol in ['xmlrpc', 'all']:
        try:
            xmlrpc_result = test_xmlrpc(args.data)
        except Exception as e:
            print(f'\n❌ XML-RPC test failed: {e}')
            print('💡 Make sure XML-RPC server is running:')
            print('   docker-compose up -d xmlrpc-server-1')
    
    results = [r for r in [grpc_result, xmlrpc_result, mpi_result] if r is not None]
    if len(results) >= 2:
        protocols, server_counts = compare_results(grpc_result, xmlrpc_result, mpi_result)
        if protocols:
            create_visualization(protocols, args.data, server_counts)
    elif len(results) == 1:
        print(f'\n✅ {results[0]["protocol"]} test completed: {results[0]["total"]:.4f}s')
        print(f'   Servers detected: {results[0].get("num_servers", 1)}')
        print('💡 Run with --protocol all to compare multiple protocols and generate visualizations')
    
    print('\n✅ Test complete!')

if __name__ == '__main__':
    main()
