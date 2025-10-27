"""
Generate gRPC code from proto files
Run this script to generate the necessary Python files from the .proto definition
"""

import os
import subprocess
import sys


def generate_grpc_code():
    """Generate gRPC Python code from proto files"""
    
    # Paths
    proto_dir = "proto"
    proto_file = "student_service.proto"
    server_output = "server/generated"
    client_output = "client/generated"
    
    # Create output directories
    os.makedirs(server_output, exist_ok=True)
    os.makedirs(client_output, exist_ok=True)
    
    # Create __init__.py files
    open(os.path.join(server_output, "__init__.py"), 'a').close()
    open(os.path.join(client_output, "__init__.py"), 'a').close()
    
    print("Generating gRPC code for server...")
    subprocess.run([
        sys.executable, "-m", "grpc_tools.protoc",
        f"-I{proto_dir}",
        f"--python_out={server_output}",
        f"--grpc_python_out={server_output}",
        os.path.join(proto_dir, proto_file)
    ])
    
    print("Generating gRPC code for client...")
    subprocess.run([
        sys.executable, "-m", "grpc_tools.protoc",
        f"-I{proto_dir}",
        f"--python_out={client_output}",
        f"--grpc_python_out={client_output}",
        os.path.join(proto_dir, proto_file)
    ])
    
    print("\nCode generation completed!")
    print(f"Server files: {server_output}/")
    print(f"Client files: {client_output}/")
    print("\nYou can now run:")
    print("  python server/server.py  (in one terminal)")
    print("  python client/client.py  (in another terminal)")


if __name__ == "__main__":
    generate_grpc_code()
