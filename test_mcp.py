#!/usr/bin/env python3
"""
Test script for the MCP server - validates functionality without running full MCP protocol
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from mcp_server import select_relevant_docs, build_context_response, list_all_contexts, load_manifest

def test_manifest_loading():
    """Test manifest loads correctly"""
    print("=" * 60)
    print("TEST 1: Loading Manifest")
    print("=" * 60)
    manifest = load_manifest()
    print(f"✓ Loaded {len(manifest.get('docs', []))} documents from manifest")
    for doc in manifest.get('docs', []):
        print(f"  - {doc['path']}: {doc['when']}")
    print()

def test_keyword_matching():
    """Test keyword matching algorithm"""
    print("=" * 60)
    print("TEST 2: Keyword Matching")
    print("=" * 60)
    
    test_cases = [
        ("How do I write a mock for my function?", ["mock", "gmock"]),
        ("I need to run specific tests with ctest", ["run", "execute", "ctest"]),
        ("What's the module design architecture?", ["design", "architecture", "module"]),
        ("Some random query with no matches", [])
    ]
    
    for prompt, expected_keywords in test_cases:
        print(f"\nPrompt: '{prompt}'")
        docs = select_relevant_docs(prompt)
        if docs:
            print(f"✓ Found {len(docs)} matching document(s):")
            for doc in docs:
                print(f"  - {doc['path']} (score: {doc['score']}, keywords: {doc['keywords']})")
        else:
            print("✗ No matching documents")
    print()

def test_context_building():
    """Test full context building"""
    print("=" * 60)
    print("TEST 3: Context Building")
    print("=" * 60)
    
    prompt = "How do I use EXPECT_CALL for mocking?"
    print(f"Prompt: '{prompt}'\n")
    
    context = build_context_response(prompt, include_base=True)
    print(f"✓ Built context response ({len(context)} characters)")
    print("\nFirst 500 characters of response:")
    print("-" * 60)
    print(context[:500])
    print("...")
    print()

def test_list_contexts():
    """Test listing all contexts"""
    print("=" * 60)
    print("TEST 4: List All Contexts")
    print("=" * 60)
    
    contexts = list_all_contexts()
    print(contexts)
    print()

def main():
    """Run all tests"""
    print("\n" + "=" * 60)
    print("MCP SERVER FUNCTIONALITY TESTS")
    print("=" * 60 + "\n")
    
    try:
        test_manifest_loading()
        test_keyword_matching()
        test_context_building()
        test_list_contexts()
        
        print("=" * 60)
        print("✓ ALL TESTS COMPLETED SUCCESSFULLY")
        print("=" * 60)
        print("\nYour MCP server is ready to use!")
        print("\nNext steps:")
        print("1. Add to VS Code settings.json:")
        print('   "github.copilot.chat.mcpServers": {')
        print('     "context-loader": {')
        print('       "command": "python",')
        print('       "args": ["c:\\\\ZJB\\\\autoload\\\\mcp_server.py"]')
        print('     }')
        print('   }')
        print("2. Reload VS Code")
        print("3. Ask Copilot questions with keywords like 'mock', 'test', 'design'\n")
        
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
