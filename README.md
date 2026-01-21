# Context-Aware MCP Server

An MCP (Model Context Protocol) server that automatically loads relevant markdown context files as guidelines for GitHub Copilot.

## Features

- 🎯 **Intelligent Context Matching**: Automatically selects relevant documentation based on keywords in your prompt
- 📚 **Multiple Tools**: Load context automatically, list available docs, or fetch specific files
- ⚙️ **Configurable**: Easy-to-manage manifest.json for adding new context files
- 🔄 **Base Context**: Always includes foundational guidelines from base.md

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Copilot to Use This MCP

Add to your Copilot settings (in VS Code `settings.json`):

```json
{
  "github.copilot.chat.mcpServers": {
    "context-loader": {
      "command": "python",
      "args": ["c:\\ZJB\\autoload\\mcp_server.py"]
    }
  }
}
```

Or if using Claude Desktop, add to `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "context-loader": {
      "command": "python",
      "args": ["c:\\ZJB\\autoload\\mcp_server.py"]
    }
  }
}
```

### 3. Restart Copilot/Claude

Reload VS Code or restart Claude Desktop to activate the MCP server.

## Usage

Once configured, you can use these tools in Copilot Chat:

### Load Context Automatically
```
@workspace How do I write a mock for my function?
```
The MCP will automatically detect "mock" keyword and load relevant testing documentation.

### List Available Contexts
```
@workspace Use load_contexts tool to show what documentation is available
```

### Get Specific File
```
@workspace Load the Design.md context file
```

## Adding New Context Files

Edit `context/manifest.json` to add new documentation:

```json
{
  "docs": [
    {
      "path": "context/your-new-doc.md",
      "when": ["keyword1", "keyword2", "trigger-word"]
    }
  ]
}
```

The `when` array contains keywords that will trigger this document to be loaded.

## File Structure

```
autoload/
├── mcp_server.py          # Main MCP server
├── context/
│   ├── base.md            # Always-included base context
│   ├── manifest.json      # Configuration for context routing
│   ├── design/
│   │   └── Design.md
│   └── testing/
│       ├── GTest_Mock.md
│       └── GTest_Execute.md
└── agent/                 # Legacy API server (optional)
```

## How It Works

1. When you ask Copilot a question, the MCP server receives your prompt
2. It analyzes keywords in your prompt against the `manifest.json` configuration
3. It scores each document based on keyword matches
4. It loads the top 3 most relevant documents plus base.md
5. All context is returned to Copilot as guidelines for generating responses

## Example

**Your prompt:** "How do I run specific tests with filters?"

**MCP automatically loads:**
- base.md (always included)
- GTest_Execute.md (matched "run", "execute", "filter")

The loaded context guides Copilot's response with your specific guidelines and best practices.
