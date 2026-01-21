# Context-Aware MCP Server

An MCP (Model Context Protocol) server that automatically loads relevant markdown context files as guidelines for GitHub Copilot.

## Features

- 🎯 **Intelligent Context Matching**: Automatically selects relevant documentation based on keywords in your prompt
- 📚 **Multiple Tools**: Load context automatically, list available docs, or fetch specific files
- ⚙️ **Configurable**: Easy-to-manage manifest.json for adding new context files
- 🔄 **Base Context**: Always includes foundational guidelines from base.md
- 🖥️ **Central Server Mode**: Run on a server, connect from multiple clients (see [SERVER_SETUP.md](SERVER_SETUP.md))

## Setup Options

### Option A: Local Setup (Each PC)
Run MCP server locally on each machine. Best for individual use.

### Option B: Central Server Setup (Recommended for Teams)
Run MCP server on one central server, all PCs connect remotely. **No installation needed on client PCs!**

👉 **[See SERVER_SETUP.md for central server instructions](SERVER_SETUP.md)**

## Setup

### 1. Clone the Repository

```bash
git clone https://github.com/713zhao/autoload_context_mcp.git
cd autoload_context_mcp
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure GitHub Copilot to Use This MCP

#### For VS Code:

1. **Open VS Code Settings (JSON)**
   - Press `Ctrl+Shift+P` (or `Cmd+Shift+P` on Mac)
   - Type "Preferences: Open User Settings (JSON)"
   - Select it to open your `settings.json` file

2. **Add the MCP Server Configuration**
   
   Add the following configuration to your settings.json (update the path to match where you cloned the repository):

   ```json
   {
     "github.copilot.chat.mcpServers": {
       "context-loader": {
         "command": "python",
         "args": ["/absolute/path/to/autoload_context_mcp/mcp_server.py"]
       }
     }
   }
   ```

   **Windows Example:**
   ```json
   {
     "github.copilot.chat.mcpServers": {
       "context-loader": {
         "command": "python",
         "args": ["c:\\Users\\YourName\\autoload_context_mcp\\mcp_server.py"]
       }
     }
   }
   ```

   **Mac/Linux Example:**
   ```json
   {
     "github.copilot.chat.mcpServers": {
       "context-loader": {
         "command": "python3",
         "args": ["/home/username/autoload_context_mcp/mcp_server.py"]
       }
     }
   }
   ```

3. **Save the settings.json file**

4. **Reload VS Code**
   - Press `Ctrl+Shift+P` (or `Cmd+Shift+P` on Mac)
   - Type "Developer: Reload Window"
   - Press Enter

5. **Verify MCP is Active**
   - Open Copilot Chat in VS Code
   - The MCP server should now be available as a tool
   - Try asking: "How do I write a mock?" to see it automatically load context

#### For Claude Desktop:

Add to your `claude_desktop_config.json`:

**Location:**
- **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`
- **Mac:** `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Linux:** `~/.config/Claude/claude_desktop_config.json`

**Configuration:**
```json
{
  "mcpServers": {
    "context-loader": {
      "command": "python",
      "args": ["/absolute/path/to/autoload_context_mcp/mcp_server.py"]
    }
  }
}
```

Restart Claude Desktop after saving.

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
