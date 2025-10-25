"""
Generate Large Test Datasets
Creates multiple text files of different sizes to test protocol performance
"""
import random
import os

# Word pool for generating realistic text
WORD_POOL = [
    "the", "quick", "brown", "fox", "jumps", "over", "lazy", "dog", "computer", "science",
    "distributed", "systems", "network", "protocol", "performance", "testing", "analysis",
    "algorithm", "data", "structure", "processing", "parallel", "computing", "efficiency",
    "scalability", "throughput", "latency", "bandwidth", "optimization", "benchmark",
    "server", "client", "request", "response", "communication", "serialization", "binary",
    "text", "encoding", "decoding", "compression", "transmission", "connection", "channel",
    "message", "payload", "overhead", "infrastructure", "deployment", "containerization",
    "docker", "kubernetes", "microservices", "architecture", "design", "pattern", "implementation",
    "integration", "evaluation", "comparison", "measurement", "metric", "statistics", "results",
    "experiment", "methodology", "framework", "library", "toolkit", "utility", "function",
    "module", "package", "dependency", "configuration", "parameter", "argument", "variable",
    "constant", "operation", "execution", "runtime", "memory", "storage", "database", "query",
    "index", "search", "sort", "filter", "aggregate", "transform", "pipeline", "workflow"
]

def generate_text(num_words):
    """Generate random text with specified number of words"""
    words = []
    for _ in range(num_words):
        word = random.choice(WORD_POOL)
        words.append(word)
    
    # Format into lines of ~10 words each
    lines = []
    line = []
    for i, word in enumerate(words):
        line.append(word)
        if len(line) >= 10 or i == len(words) - 1:
            lines.append(' '.join(line))
            line = []
    
    return '\n'.join(lines)

def create_dataset(filename, num_words):
    """Create a dataset file with specified number of words"""
    text = generate_text(num_words)
    
    filepath = os.path.join('data', filename)
    with open(filepath, 'w') as f:
        f.write(text)
    
    # Get file size
    size_bytes = os.path.getsize(filepath)
    size_kb = size_bytes / 1024
    size_mb = size_kb / 1024
    
    actual_words = len(text.split())
    
    print(f"✓ Created {filename}")
    print(f"  Words: {actual_words:,}")
    print(f"  Size: {size_bytes:,} bytes ({size_kb:.2f} KB / {size_mb:.2f} MB)")
    print(f"  Lines: {len(text.splitlines())}")
    print()

def main():
    """Generate multiple test datasets of varying sizes"""
    print("="*60)
    print("GENERATING LARGE TEST DATASETS")
    print("="*60)
    print()
    
    # Ensure data directory exists
    os.makedirs('data', exist_ok=True)
    
    # Generate datasets of increasing sizes
    datasets = [
        ('small_1k.txt', 1_000),           # ~7 KB
        ('medium_10k.txt', 10_000),        # ~70 KB
        ('large_50k.txt', 50_000),         # ~350 KB
        ('xlarge_100k.txt', 100_000),      # ~700 KB
        ('xxlarge_500k.txt', 500_000),     # ~3.5 MB
        ('huge_1m.txt', 1_000_000),        # ~7 MB
    ]
    
    for filename, num_words in datasets:
        create_dataset(filename, num_words)
    
    print("="*60)
    print("DATASET GENERATION COMPLETE!")
    print("="*60)
    print("\nGenerated files in 'data/' directory:")
    for filename, num_words in datasets:
        filepath = os.path.join('data', filename)
        size_mb = os.path.getsize(filepath) / (1024 * 1024)
        print(f"  {filename:20s} - {num_words:>8,} words ({size_mb:>5.2f} MB)")
    
    print("\n📊 Use these files with performance_test.py to compare protocols!")
    print("\nExample:")
    print("  python performance_test.py --data data/large_50k.txt --protocol grpc")
    print("  python performance_test.py --data data/large_50k.txt --protocol xmlrpc")

if __name__ == '__main__':
    main()
