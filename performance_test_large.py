"""
Performance Testing Script for Large Datasets
Compare gRPC vs XML-RPC with different data sizes
"""
import argparse
import time
import os
import sys

def test_grpc(data_file, num_servers=3):
    """Test gRPC with specified data file"""
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'grpc_implementation'))
    
    import grpc
    import mapreduce_pb2
    import mapreduce_pb2_grpc
    from collections import Counter
    
    # Load data
    with open(data_file, 'r') as f:
        text = f.read()
    
    print(f"\n📊 Testing gRPC with {data_file}")
    print(f"   Text: {len(text):,} chars, {len(text.split()):,} words")
    
    # Setup servers
    servers = [f'localhost:{50051+i}' for i in range(num_servers)]
    channels = []
    stubs = []
    
    for address in servers:
        channel = grpc.insecure_channel(address)
        stub = mapreduce_pb2_grpc.MapReduceServiceStub(channel)
        channels.append(channel)
        stubs.append(stub)
    
    # Split text
    lines = text.strip().split('\n')
    chunk_size = max(1, len(lines) // num_servers)
    chunks = []
    for i in range(num_servers):
        start = i * chunk_size
        end = start + chunk_size if i < num_servers - 1 else len(lines)
        chunk = '\n'.join(lines[start:end])
        chunks.append(chunk)
    
    # Test Service 1: Word Count
    start = time.time()
    map_results = []
    for i, (chunk, stub) in enumerate(zip(chunks, stubs)):
        request = mapreduce_pb2.MapRequest(text_chunk=chunk, chunk_id=i)
        response = stub.Map(request)
        map_results.append(response.word_counts)
    
    combined_counts = Counter()
    for counts in map_results:
        combined_counts.update(counts)
    
    reduce_request = mapreduce_pb2.ReduceRequest(
        intermediate_counts=dict(combined_counts)
    )
    reduce_response = stubs[0].Reduce(reduce_request)
    time1 = time.time() - start
    
    # Test Service 2: Sorting
    start = time.time()
    sorted_chunks = []
    for i, (chunk, stub) in enumerate(zip(chunks, stubs)):
        request = mapreduce_pb2.SortWordsRequest(text_chunk=chunk, chunk_id=i)
        response = stub.SortWords(request)
        sorted_chunks.append(list(response.sorted_words))
    
    import heapq
    final_sorted = list(heapq.merge(*sorted_chunks))
    time2 = time.time() - start
    
    # Test Service 3: Word Lengths
    start = time.time()
    all_distributions = Counter()
    for i, (chunk, stub) in enumerate(zip(chunks, stubs)):
        request = mapreduce_pb2.WordLengthRequest(text_chunk=chunk, chunk_id=i)
        response = stub.AnalyzeWordLengths(request)
        all_distributions.update(response.length_distribution)
    time3 = time.time() - start
    
    # Close channels
    for channel in channels:
        channel.close()
    
    total = time1 + time2 + time3
    
    print(f"\n   ⏱️  gRPC Results:")
    print(f"      Service 1 (Word Count):    {time1:.4f}s")
    print(f"      Service 2 (Sorting):       {time2:.4f}s")
    print(f"      Service 3 (Word Lengths):  {time3:.4f}s")
    print(f"      Total:                     {total:.4f}s")
    
    return {
        'protocol': 'gRPC',
        'service1': time1,
        'service2': time2,
        'service3': time3,
        'total': total,
        'words': len(reduce_response.final_counts),
        'unique_words': len(final_sorted)
    }

def test_xmlrpc(data_file, num_servers=3):
    """Test XML-RPC with specified data file"""
    import xmlrpc.client
    from collections import Counter
    
    # Load data
    with open(data_file, 'r') as f:
        text = f.read()
    
    print(f"\n📊 Testing XML-RPC with {data_file}")
    print(f"   Text: {len(text):,} chars, {len(text.split()):,} words")
    
    # Setup servers
    servers = [f'http://localhost:{8000+i}' for i in range(num_servers)]
    proxies = [xmlrpc.client.ServerProxy(server) for server in servers]
    
    # Split text
    lines = text.strip().split('\n')
    chunk_size = max(1, len(lines) // num_servers)
    chunks = []
    for i in range(num_servers):
        start = i * chunk_size
        end = start + chunk_size if i < num_servers - 1 else len(lines)
        chunk = '\n'.join(lines[start:end])
        chunks.append(chunk)
    
    # Test Service 1: Word Count
    start = time.time()
    map_results = []
    for i, (chunk, proxy) in enumerate(zip(chunks, proxies)):
        result = proxy.map_operation(chunk, i)
        map_results.append(result['word_counts'])
    
    combined_counts = Counter()
    for counts in map_results:
        combined_counts.update(counts)
    
    reduce_result = proxies[0].reduce_operation(dict(combined_counts))
    time1 = time.time() - start
    
    # Test Service 2: Sorting
    start = time.time()
    sorted_chunks = []
    for i, (chunk, proxy) in enumerate(zip(chunks, proxies)):
        result = proxy.sort_words(chunk, i)
        sorted_chunks.append(result['sorted_words'])
    
    import heapq
    final_sorted = list(heapq.merge(*sorted_chunks))
    time2 = time.time() - start
    
    # Test Service 3: Word Lengths
    start = time.time()
    all_distributions = Counter()
    for i, (chunk, proxy) in enumerate(zip(chunks, proxies)):
        result = proxy.analyze_word_lengths(chunk, i)
        for length, count in result['length_distribution']:
            all_distributions[length] += count
    time3 = time.time() - start
    
    total = time1 + time2 + time3
    
    print(f"\n   ⏱️  XML-RPC Results:")
    print(f"      Service 1 (Word Count):    {time1:.4f}s")
    print(f"      Service 2 (Sorting):       {time2:.4f}s")
    print(f"      Service 3 (Word Lengths):  {time3:.4f}s")
    print(f"      Total:                     {total:.4f}s")
    
    return {
        'protocol': 'XML-RPC',
        'service1': time1,
        'service2': time2,
        'service3': time3,
        'total': total,
        'words': len(reduce_result['final_counts']),
        'unique_words': len(final_sorted)
    }

def compare_results(grpc_result, xmlrpc_result):
    """Compare and display results"""
    print("\n" + "="*70)
    print("📊 PERFORMANCE COMPARISON")
    print("="*70)
    
    print(f"\n{'Service':<30} {'gRPC':<15} {'XML-RPC':<15} {'Speedup':<10}")
    print("-" * 70)
    
    services = [
        ('Service 1 (Word Count)', 'service1'),
        ('Service 2 (Sorting)', 'service2'),
        ('Service 3 (Word Lengths)', 'service3'),
        ('TOTAL', 'total')
    ]
    
    for name, key in services:
        grpc_time = grpc_result[key]
        xmlrpc_time = xmlrpc_result[key]
        speedup = xmlrpc_time / grpc_time if grpc_time > 0 else 0
        
        if speedup > 1:
            winner = "✅ gRPC faster"
        elif speedup < 1:
            winner = "❌ XML-RPC faster"
        else:
            winner = "Same"
        
        print(f"{name:<30} {grpc_time:>7.4f}s      {xmlrpc_time:>7.4f}s      {speedup:>4.2f}x  {winner}")
    
    print("\n" + "="*70)
    
    # Overall winner
    if grpc_result['total'] < xmlrpc_result['total']:
        speedup = xmlrpc_result['total'] / grpc_result['total']
        print(f"🏆 WINNER: gRPC is {speedup:.2f}x faster overall!")
    else:
        speedup = grpc_result['total'] / xmlrpc_result['total']
        print(f"🏆 WINNER: XML-RPC is {speedup:.2f}x faster overall!")
    
    print("="*70)

def main():
    parser = argparse.ArgumentParser(description='Test protocol performance with large datasets')
    parser.add_argument('--data', type=str, required=True, help='Path to data file')
    parser.add_argument('--protocol', type=str, choices=['grpc', 'xmlrpc', 'both'], default='both',
                       help='Protocol to test (grpc, xmlrpc, or both)')
    parser.add_argument('--servers', type=int, default=3, help='Number of servers to use')
    
    args = parser.parse_args()
    
    print("="*70)
    print("🚀 LARGE DATASET PERFORMANCE TEST")
    print("="*70)
    print(f"Data File: {args.data}")
    print(f"Protocol: {args.protocol}")
    print(f"Servers: {args.servers}")
    
    # Check if file exists
    if not os.path.exists(args.data):
        print(f"\n❌ Error: File not found: {args.data}")
        print("💡 Run 'python generate_large_data.py' to create test datasets")
        return
    
    # Test protocols
    grpc_result = None
    xmlrpc_result = None
    
    if args.protocol in ['grpc', 'both']:
        try:
            grpc_result = test_grpc(args.data, args.servers)
        except Exception as e:
            print(f"\n❌ gRPC test failed: {e}")
            print("💡 Make sure gRPC servers are running:")
            print("   docker-compose up -d grpc-server-1 grpc-server-2 grpc-server-3")
    
    if args.protocol in ['xmlrpc', 'both']:
        try:
            xmlrpc_result = test_xmlrpc(args.data, args.servers)
        except Exception as e:
            print(f"\n❌ XML-RPC test failed: {e}")
            print("💡 Make sure XML-RPC servers are running:")
            print("   docker-compose up -d xmlrpc-server-1 xmlrpc-server-2 xmlrpc-server-3")
    
    # Compare if both were tested
    if grpc_result and xmlrpc_result:
        compare_results(grpc_result, xmlrpc_result)
    
    print("\n✅ Test complete!")

if __name__ == '__main__':
    main()
