#!/usr/bin/env python3
"""Quick test to see if MCP server can initialize"""

import sys
import asyncio
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

async def test_mcp():
    try:
        from mcp.server import Server
        from mcp.types import Tool
        
        print("✓ MCP imports successful")
        
        # Import our server
        from mcp_server import app, list_tools, call_tool
        
        print("✓ Server module imported")
        
        # Test list_tools
        tools = await list_tools()
        print(f"✓ Found {len(tools)} tools:")
        for tool in tools:
            print(f"  - {tool.name}: {tool.description[:50]}...")
        
        return True
        
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(test_mcp())
    sys.exit(0 if success else 1)
