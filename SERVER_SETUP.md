# Central MCP Server Setup Guide

This guide explains how to set up the MCP server on a central server so multiple clients can connect without local installation.

## Architecture

```
┌─────────────────┐
│  Central Server │ ← Runs mcp_server_http.py
│   (Port 8000)   │
└────────┬────────┘
         │
    ┌────┴────┐
    │         │
┌───▼──┐  ┌──▼───┐
│ PC 1 │  │ PC 2 │ ← Configure Copilot to connect to server
└──────┘  └──────┘
```

## Server Setup

### 1. Install on Central Server

```bash
# Clone the repository
git clone https://github.com/713zhao/autoload_context_mcp.git
cd autoload_context_mcp

# Install dependencies
pip install -r requirements.txt
```

### 2. Run the HTTP Server

```bash
# Run on default port 8000, accessible from network
python mcp_server_http.py

# Or specify custom host and port
python mcp_server_http.py 192.168.1.100 8080
```

### 3. Test Server is Running

Open a browser and navigate to:
```
http://your-server-ip:8000/sse
```

You should see a connection attempt or MCP handshake.

### 4. Keep Server Running (Production)

#### Using systemd (Linux):

Create `/etc/systemd/system/mcp-context-loader.service`:

```ini
[Unit]
Description=MCP Context Loader Server
After=network.target

[Service]
Type=simple
User=your-user
WorkingDirectory=/path/to/autoload_context_mcp
ExecStart=/usr/bin/python3 mcp_server_http.py 0.0.0.0 8000
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable mcp-context-loader
sudo systemctl start mcp-context-loader
sudo systemctl status mcp-context-loader
```

#### Using PM2 (Cross-platform):

```bash
# Install PM2
npm install -g pm2

# Start server
pm2 start mcp_server_http.py --name mcp-context-loader --interpreter python3

# Save configuration
pm2 save

# Set to start on boot
pm2 startup
```

#### Using nohup (Simple method):

```bash
nohup python mcp_server_http.py > mcp_server.log 2>&1 &
```

### 5. Firewall Configuration

Ensure port 8000 (or your chosen port) is accessible:

**Windows:**
```powershell
netsh advfirewall firewall add rule name="MCP Server" dir=in action=allow protocol=TCP localport=8000
```

**Linux (ufw):**
```bash
sudo ufw allow 8000/tcp
```

**Linux (iptables):**
```bash
sudo iptables -A INPUT -p tcp --dport 8000 -j ACCEPT
```

## Client Configuration

### VS Code Configuration (All Client PCs)

No local installation needed! Just configure VS Code to connect to the server.

#### 1. Open VS Code Settings
- Press `Ctrl+Shift+P` (or `Cmd+Shift+P` on Mac)
- Type "Preferences: Open User Settings (JSON)"

#### 2. Add Remote MCP Server Configuration

```json
{
  "github.copilot.chat.mcpServers": {
    "context-loader": {
      "url": "http://your-server-ip:8000/sse"
    }
  }
}
```

**Example:**
```json
{
  "github.copilot.chat.mcpServers": {
    "context-loader": {
      "url": "http://192.168.1.100:8000/sse"
    }
  }
}
```

#### 3. Reload VS Code
- Press `Ctrl+Shift+P` → "Developer: Reload Window"

#### 4. Test Connection
Open Copilot Chat and ask: "How do I create a mock?"
The server should automatically load the relevant context.

### Claude Desktop Configuration

Edit `claude_desktop_config.json`:

**Location:**
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`
- Mac: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Linux: `~/.config/Claude/claude_desktop_config.json`

**Configuration:**
```json
{
  "mcpServers": {
    "context-loader": {
      "url": "http://your-server-ip:8000/sse"
    }
  }
}
```

Restart Claude Desktop.

## Benefits of Central Server

✅ **Single Installation**: Install and update once, all clients benefit
✅ **Consistent Context**: All team members use the same documentation
✅ **Easy Updates**: Update context files on server, no client changes needed
✅ **Centralized Management**: Control what documentation is available
✅ **No Local Dependencies**: Clients don't need Python or dependencies

## Troubleshooting

### Cannot Connect to Server

1. **Check server is running:**
   ```bash
   curl http://your-server-ip:8000/sse
   ```

2. **Verify firewall allows connections**

3. **Check network connectivity:**
   ```bash
   ping your-server-ip
   ```

4. **View server logs:**
   ```bash
   # If using systemd
   journalctl -u mcp-context-loader -f
   
   # If using PM2
   pm2 logs mcp-context-loader
   ```

### Server Crashes or Restarts

1. Check logs for errors
2. Ensure all dependencies are installed
3. Verify Python version (3.10+)
4. Check disk space for log files

### Context Not Loading

1. Verify manifest.json is properly formatted
2. Check context files exist in correct paths
3. Test locally first: `python test_mcp.py`

## Security Considerations

⚠️ **Important**: This setup exposes the MCP server to the network.

### Recommendations:

1. **Use Internal Network**: Don't expose to internet
2. **VPN Access**: Require VPN for remote access
3. **Reverse Proxy**: Use nginx/Apache with authentication
4. **HTTPS**: Add SSL/TLS encryption
5. **API Key**: Add authentication to the server

### Adding Basic Authentication (Example):

```python
# Add to mcp_server_http.py
from starlette.middleware import Middleware
from starlette.middleware.authentication import AuthenticationMiddleware

# Configure authentication as needed
```

## Updating Context Files

To update documentation for all users:

1. SSH to server or access via RDP
2. Edit files in `context/` directory
3. Update `context/manifest.json` if adding new files
4. No restart needed - changes are loaded dynamically

## Monitoring

### Check Server Status
```bash
# If using systemd
systemctl status mcp-context-loader

# If using PM2
pm2 status

# Check if port is listening
netstat -tlnp | grep 8000  # Linux
netstat -an | findstr 8000  # Windows
```

### View Active Connections
```bash
# Linux
ss -tunap | grep 8000

# Windows
netstat -ano | findstr 8000
```

## Advanced: Load Balancing

For high availability, run multiple server instances behind a load balancer:

```
       ┌────────────────┐
       │ Load Balancer  │
       │  (nginx/HAProxy)│
       └────────┬───────┘
           ┌────┴────┐
     ┌─────▼────┐ ┌──▼──────┐
     │ Server 1 │ │ Server 2│
     │ :8000    │ │ :8001   │
     └──────────┘ └─────────┘
```

Example nginx config:
```nginx
upstream mcp_servers {
    server 127.0.0.1:8000;
    server 127.0.0.1:8001;
}

server {
    listen 80;
    location /sse {
        proxy_pass http://mcp_servers;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```
