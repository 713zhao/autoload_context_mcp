# Context-Aware MCP Server & Agent Skills

An MCP (Model Context Protocol) server that automatically loads relevant markdown context files as guidelines for GitHub Copilot, with support for GitHub Copilot Agent Skills.

## Features

- 🎯 **Intelligent Context Matching**: Automatically selects relevant documentation based on keywords in your prompt
- 📚 **Multiple Tools**: Load context automatically, list available docs, or fetch specific files
- ⚙️ **Configurable**: Easy-to-manage manifest.json for adding new context files
- 🔄 **Base Context**: Always includes foundational guidelines from base.md
- 🖥️ **Central Server Mode**: Run on a server, connect from multiple clients (see [SERVER_SETUP.md](SERVER_SETUP.md))
- ✨ **Agent Skills Support**: VS Code automatically loads skills from `.github/skills` (no setup required!)

## Setup Options

### Option A: Agent Skills (Recommended - Zero Setup!)
VS Code automatically discovers and loads skills from `.github/skills/`. **No configuration needed!**

Just commit the `.github/skills` folder to your repository and Copilot will automatically use them.

👉 **[See Agent Skills Documentation](#agent-skills-automatic-loading)** below for details.

### Option B: MCP Server - Local Setup (Each PC)
Run MCP server locally on each machine. Best for individual use or Claude Desktop.

### Option C: MCP Server - Central Server Setup (Teams)
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

### Using Agent Skills (Automatic)

When Agent Skills are committed to your repository in `.github/skills/`, Copilot automatically loads them when relevant:

```
Ask Copilot: "How do I create a mock class?"
→ Copilot automatically loads gtest-mock skill

Ask Copilot: "How do I run tests with filters?"
→ Copilot automatically loads gtest-execute skill

Ask Copilot: "What design patterns should I use?"
→ Copilot automatically loads design-guidelines skill
```

**No special commands needed!** Just ask your question and Copilot intelligently loads the right skill based on your prompt.

### Using MCP Server (Manual)

Once configured, you can use these tools in Copilot Chat:

#### Load Context Automatically
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

## Agent Skills (Automatic Loading)

### What are Agent Skills?

Agent Skills are an [open standard](https://github.com/agentskills/agentskills) used by GitHub Copilot, Claude, and other AI agents. Skills are automatically discovered and loaded when relevant to your prompt.

### Available Skills in This Project

Located in `.github/skills/`:

1. **gtest-mock** - Google Mock (gmock) guide
   - Creating mock classes with MOCK_METHOD
   - Setting up EXPECT_CALL expectations
   - Matchers and cardinality
   - Best practices for mocking

2. **gtest-execute** - Google Test execution and coverage
   - Running tests with filters
   - Achieving 100% CTC coverage
   - Test documentation standards
   - Boundary and input testing strategies

3. **design-guidelines** - Software design principles
   - Architecture patterns
   - Module structure
   - Dependency injection
   - Best practices and design review checklist

### How Agent Skills Work

1. **Automatic Discovery**: VS Code scans `.github/skills/` folders in your repository
2. **Intelligent Loading**: When you ask a question, Copilot matches keywords in your prompt to skill descriptions
3. **Context Injection**: Relevant skills are automatically loaded into Copilot's context
4. **No Configuration**: Works automatically - no settings.json changes needed!

### Adding New Agent Skills

1. Create a new subdirectory in `.github/skills/`
   ```bash
   mkdir .github/skills/your-skill-name
   ```

2. Create `SKILL.md` with YAML frontmatter:
   ```markdown
   ---
   name: your-skill-name
   description: What this skill does and when to use it. Include trigger keywords.
   ---

   # Your Skill Content

   Documentation, examples, and guidelines here...
   ```

3. Commit to your repository - Copilot will automatically discover it!

### Agent Skills vs MCP Server

| Feature | Agent Skills | MCP Server |
|---------|-------------|------------|
| **Setup Required** | None | Settings.json config |
| **Works In** | VS Code, GitHub Copilot | VS Code, Claude Desktop |
| **Discovery** | Automatic | Manual tool invocation |
| **Storage** | `.github/skills/` in repo | `context/` folder |
| **Best For** | Teams, shared repos | Personal, legacy support |

**Recommendation**: Use Agent Skills for new projects - they require zero setup and work automatically!

## MCP Server Setup (Alternative Method)
