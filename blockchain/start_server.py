#!/usr/bin/env python3
"""
Simple server startup script for Render.com deployment
"""
import os
import sys
import argparse

# Add blockchain directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import after path setup
from run_node import main

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='POS Blockchain Node')
    parser.add_argument('--ip', default='0.0.0.0', help='IP address to bind to')
    parser.add_argument('--node_port', type=int, default=8050, help='Node port')
    parser.add_argument('--api_port', type=int, default=8050, help='API port')
    parser.add_argument('--key_file', default='./keys/genesis_private_key.pem', help='Private key file')
    
    args = parser.parse_args()
    
    # Change to blockchain directory for correct relative paths
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # Run the node
    main(args)
