# Skills CLI - Quick Context Loading

A lightweight alternative to MCP that uses VS Code tasks and keyboard shortcuts to load context documentation directly into your workflow.

## Setup on New PC

### Automated Setup (Windows)

1. Clone and run setup script
   ```bash
   clone the code from git.
   cd autoload_context_mcp
   setup_skills.bat
   ```

2. Follow on-screen instructions to verify:
   - Tasks are available: `Ctrl+Shift+P` → "Tasks: Run Task"
   - Test shortcut: `Ctrl+K Ctrl+M` (loads Google Mock)

## Quick Start

### 1. Use Keyboard Shortcuts

| Shortcut | Skill | Description |
|----------|-------|-------------|
| `Ctrl+K Ctrl+M` | Google Mock | Load GMock documentation to clipboard |
| `Ctrl+K Ctrl+E` | GTest Execute | Load test execution guide to clipboard |
| `Ctrl+K Ctrl+D` | Design | Load design guidelines to clipboard |
| `Ctrl+K Ctrl+L` | List Skills | Show all available skills |

### 2. Workflow

**NEW: Automatic Copilot Integration**

1. Press the shortcut key (e.g., `Ctrl+K Ctrl+M` for Google Mock)
2. The skill is saved to `.copilot_context.md` and opened in editor
3. Open Copilot chat (`Ctrl+Alt+I` or click chat icon)
4. Copilot automatically has access to the open file as context
5. Ask your question - Copilot will use the skill content

**Alternative: Manual Paste**

Use `--output clipboard` flag to copy to clipboard instead, then paste into chat.

## CLI Usage

You can also use the skills CLI directly:

```bash
# List all available skills
python skills.py list

# Load a skill for Copilot (opens in editor)
python skills.py load GTest_Mock

# Load to clipboard instead
python skills.py load GTest_Mock --output clipboard

# Display skill content
python skills.py show GTest_Execute
```

## Available Skills

- **GTest_Mock** - Comprehensive Google Mock guide (3500+ chars)
  - Creating mock classes
  - EXPECT_CALL patterns
  - Matchers and cardinality
  - Best practices

- **GTest_Execute** - Test execution guide
  - Running tests with filters
  - CTest integration
  - Test output interpretation

- **Design** - Design guidelines
  - Architecture patterns
  - Module structure
  - Best practices

## Adding New Skills

1. Create your markdown documentation in `context/` folder
2. Add entry to `context/manifest.json`:

```json
{
  "path": "context/your/new-skill.md",
  "when": ["keyword1", "keyword2"]
}
```

3. Add a task in `.vscode/tasks.json`:

```json
{
  "label": "Load Skill: Your New Skill",
  "type": "shell",
  "command": "python",
  "args": ["skills.py", "load", "new-skill"]
}
```

4. Add keybinding in `.vscode/keybindings.json`:

```json
{
  "key": "ctrl+k ctrl+n",
  "command": "workbench.action.tasks.runTask",
  "args": "Load Skill: Your New Skill"
}
```

## Why Skills CLI vs MCP?
Copilot automatically sees open files as context
- ✅ Easy keyboard shortcuts
- ✅ No configuration complexity
- ✅ Fast and lightweight
- ✅ Works with @workspace references

**MCP Advantages:**
- ✅ Automatic context injection via API
- ✅ No file opening
**MCP Advantages:**
- ✅ Automatic context injection
- ✅ No manual paste needed
- ✅ Better for remote/multi-client setups

## Troubleshooting

### Keyboard shortcuts not working

1. Check if keybindings.json is in `.vscode/` folder (workspace-specific)
2. For global keybindings, add to VS Code's user keybindings:
   - `Ctrl+K Ctrl+S` → Search for "keybindings.json"
   - Copy entries from `.vscode/keybindings.json`

### Task not found

1. Run `Tasks: Run Task` command (`Ctrl+Shift+P`)
2. Verify task appears in the list
3. Check `.vscode/tasks.json` syntax

### Clipboard not working

1. Ensure `pyperclip` is installed: `pip install pyperclip`
2. On Linux, may need `xclip` or `xsel`: `sudo apt-get install xclip`
3. Use `--output stdout` flag to display content instead

## Architecture

```
skills.py                    # CLI tool
├── list                     # List all skills
├── load <skill>             # Load to clipboard
└── show <skill>             # Display content

.vscode/tasks.json           # VS Code task definitions
.vscode/keybindings.json     # Keyboard shortcuts

context/manifest.json        # Skill definitions
context/                     # Markdown documentation
├── testing/
│   ├── GTest_Mock.md
│   └── GTest_Execute.md
└── design/
    └── Design.md
```

## Tips

- **Combine Skills**: Load multiple skills before asking complex questions
- **Edit Before Paste**: Review/trim content in clipboard before pasting
- **Custom Commands**: Run `python skills.py load <skill> --output file` to save to temp file
- **Quick Reference**: Use `Ctrl+K Ctrl+L` to remind yourself of available skills
