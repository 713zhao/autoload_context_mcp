#!/usr/bin/env python3
"""
MCP Server for Context-Aware Documentation Loading
Automatically loads relevant markdown context files based on prompt keywords
"""

import json
import asyncio
from pathlib import Path
from typing import Any

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent, EmbeddedResource

# Root directory of the context files
ROOT = Path(__file__).resolve().parent

def read_text(rel_path: str) -> str:
    """Read text file relative to ROOT"""
    try:
        return (ROOT / rel_path).read_text(encoding="utf-8")
    except Exception as e:
        return f"Error reading {rel_path}: {str(e)}"

def load_manifest() -> dict:
    """Load the context manifest configuration"""
    try:
        manifest_path = ROOT / "context" / "manifest.json"
        with open(manifest_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        return {"docs": []}

def select_relevant_docs(prompt: str, max_docs: int = 3) -> list[dict]:
    """
    Intelligently select relevant documentation files based on prompt keywords
    Returns list of matching documents with their metadata
    """
    manifest = load_manifest()
    p = prompt.lower()
    
    scored = []
    for doc in manifest.get("docs", []):
        # Count keyword matches
        hits = sum(1 for keyword in doc.get("when", []) if keyword.lower() in p)
        if hits > 0:
            scored.append({
                "score": hits,
                "path": doc["path"],
                "keywords": doc.get("when", [])
            })
    
    # Sort by score (highest first) and return top matches
    scored.sort(key=lambda x: x["score"], reverse=True)
    return scored[:max_docs]

def build_context_response(prompt: str, include_base: bool = True) -> str:
    """Build complete context including base and relevant docs"""
    parts = []
    
    # Always include base context if requested
    if include_base:
        base_content = read_text("context/base.md")
        parts.append("=== Base Context ===\n" + base_content)
    
    # Add relevant documentation
    relevant = select_relevant_docs(prompt)
    
    if relevant:
        parts.append("\n=== Relevant Documentation ===")
        for doc in relevant:
            content = read_text(doc["path"])
            parts.append(f"\n--- {doc['path']} (matched keywords: {', '.join(doc['keywords'])}) ---\n{content}")
    else:
        parts.append("\n=== No specific documentation matched your query ===")
    
    return "\n\n".join(parts)

def list_all_contexts() -> str:
    """List all available context files"""
    manifest = load_manifest()
    
    result = ["Available Context Documents:\n"]
    for doc in manifest.get("docs", []):
        keywords = ", ".join(doc.get("when", []))
        result.append(f"- {doc['path']}")
        result.append(f"  Keywords: {keywords}\n")
    
    return "\n".join(result)

# Create MCP server instance
app = Server("context-loader")

@app.list_tools()
async def list_tools() -> list[Tool]:
    """List available MCP tools"""
    return [
        Tool(
            name="load_context",
            description="Automatically load relevant context/guideline markdown files based on your prompt. "
                       "The system intelligently matches keywords in your query to select the most relevant documentation. "
                       "Use this when you need design guidelines, testing instructions, or architectural context.",
            inputSchema={
                "type": "object",
                "properties": {
                    "prompt": {
                        "type": "string",
                        "description": "Your question or task description. Keywords will be matched against available documentation."
                    },
                    "include_base": {
                        "type": "boolean",
                        "description": "Whether to include base.md context (default: true)",
                        "default": True
                    }
                },
                "required": ["prompt"]
            }
        ),
        Tool(
            name="list_contexts",
            description="List all available context/guideline documents and their trigger keywords. "
                       "Use this to discover what documentation is available.",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        Tool(
            name="get_context_file",
            description="Directly retrieve a specific context file by its path. "
                       "Use this when you know exactly which document you need.",
            inputSchema={
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "Relative path to the context file (e.g., 'context/design/Design.md')"
                    }
                },
                "required": ["file_path"]
            }
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: Any) -> list[TextContent]:
    """Handle tool calls"""
    
    if name == "load_context":
        prompt = arguments.get("prompt", "")
        include_base = arguments.get("include_base", True)
        
        if not prompt:
            return [TextContent(
                type="text",
                text="Error: Please provide a prompt to match against context files."
            )]
        
        context = build_context_response(prompt, include_base)
        return [TextContent(type="text", text=context)]
    
    elif name == "list_contexts":
        contexts = list_all_contexts()
        return [TextContent(type="text", text=contexts)]
    
    elif name == "get_context_file":
        file_path = arguments.get("file_path", "")
        
        if not file_path:
            return [TextContent(
                type="text",
                text="Error: Please provide a file_path."
            )]
        
        content = read_text(file_path)
        return [TextContent(
            type="text",
            text=f"=== {file_path} ===\n\n{content}"
        )]
    
    else:
        return [TextContent(
            type="text",
            text=f"Error: Unknown tool '{name}'"
        )]

async def main():
    """Run the MCP server"""
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )

if __name__ == "__main__":
    asyncio.run(main())
