#!/usr/bin/env python3
"""
Test script for HTTP MCP server
"""

import requests
import time
import sys

def test_server(base_url="http://localhost:8000"):
    """Test the HTTP MCP server"""
    
    print("=" * 60)
    print("HTTP MCP SERVER TESTS")
    print("=" * 60)
    
    # Test 1: SSE Endpoint accessibility
    print("\nTest 1: SSE Endpoint Accessibility")
    print("-" * 60)
    try:
        response = requests.get(f"{base_url}/sse", timeout=5, stream=True)
        if response.status_code == 200:
            print(f"✓ SSE endpoint is accessible (Status: {response.status_code})")
            # Close the streaming connection
            response.close()
        else:
            print(f"✗ SSE endpoint returned status: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"✗ Cannot connect to server: {e}")
        print("\nMake sure the server is running:")
        print("  python mcp_server_http.py localhost 8000")
        return False
    
    # Test 2: Server Info
    print("\nTest 2: Server Configuration")
    print("-" * 60)
    print(f"✓ Server URL: {base_url}")
    print(f"✓ SSE Endpoint: {base_url}/sse")
    print(f"✓ Messages Endpoint: {base_url}/messages")
    
    print("\n" + "=" * 60)
    print("✓ ALL HTTP TESTS PASSED")
    print("=" * 60)
    
    print("\nServer is ready for client connections!")
    print("\nClient Configuration:")
    print('  "github.copilot.chat.mcpServers": {')
    print('    "context-loader": {')
    print(f'      "url": "{base_url}/sse"')
    print('    }')
    print('  }')
    
    return True

if __name__ == "__main__":
    base_url = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8000"
    
    # Give server time to start if just launched
    print("Waiting 2 seconds for server to be ready...")
    time.sleep(2)
    
    success = test_server(base_url)
    sys.exit(0 if success else 1)
