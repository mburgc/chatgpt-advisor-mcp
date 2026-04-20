# ChatGPT Advisor MCP

MCP (Model Context Protocol) server that provides seamless access to ChatGPT via Freeloader. Auto-starts Freeloader API and browser.

## Demo

[Watch demo video](./demo.mp4)

## Features

- **Auto-start**: Automatically starts Freeloader API and browser
- **Cross-platform**: Works on Windows, macOS, and Linux
- **Browser detection**: Automatically finds Brave, Chrome, Edge, or Chromium
- **Status tool**: Check service health anytime

## Requirements

- Python 3.10+
- Brave or Chrome browser
- Git

## Quick Install

```bash
# Download this repo, then:
# Windows
setup.bat

# Linux/Mac
chmod +x setup.sh && ./setup.sh
```

This will:
1. Clone Freeloader (your fork)
2. Create a virtual environment
3. Install dependencies (mcp, playwright, etc.)
4. Install Playwright browsers

## Usage

### Option 1: Add to OpenCode

Add to your OpenCode config (`~/.config/opencode/opencode.json` or `%APPDATA%\opencode\opencode.json`):

```json
{
  "mcp": {
    "ChatGPTAdvisor": {
      "type": "local",
      "command": ["PATH/TO/chatgpt-advisor-mcp/venv/Scripts/python.exe", "PATH/TO/chatgpt-advisor-mcp/mcp_server.py"],
      "enabled": true,
      "timeout": 60000
    }
  }
}
```

Replace `PATH/TO` with your actual installation path.

### Option 2: Run manually

```bash
# Activate venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Run server
python mcp_server.py
```

## Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `FREELOADER_API_URL` | `http://127.0.0.1:11435/v1/chat/completions` | Freeloader API endpoint |
| `CDP_ENDPOINT` | `http://127.0.0.1:9222` | Chrome DevTools Protocol endpoint |
| `FREELOADER_DIR` | (auto-detect) | Path to Freeloader installation |
| `STARTUP_TIMEOUT_API` | `60` | Seconds to wait for API startup |
| `STARTUP_TIMEOUT_BROWSER` | `30` | Seconds to wait for browser startup |
| `REQUEST_TIMEOUT` | `300` | Seconds to wait for ChatGPT response |

### Custom Browser Path

The server auto-detects:
- **Windows**: Brave, Chrome, Edge in Program Files or AppData
- **macOS**: Brave, Chrome in /Applications
- **Linux**: Brave, Chrome, Chromium in /usr/bin or ~/.local/bin

To use a custom browser, set the `--remote-debugging-port=9222` flag manually when opening.

## Tools

### `advisor_ask`

Ask ChatGPT any question.

```
advisor_ask("Explain quantum computing in simple terms")
```

### `advisor_status`

Check if services are running.

```
advisor_status()
```

## Troubleshooting

### "Freeloader not found"

Run `setup.bat` again - it will clone Freeloader automatically.

### "No browser found"

Install Brave or Chrome, or manually open your browser with:
```
brave --remote-debugging-port=9222
```

### ChatGPT blocked (Cloudflare/CAPTCHA)

When ChatGPT shows a CAPTCHA verification:
1. The MCP will automatically open a browser window
2. Complete the CAPTCHA in that window
3. Log in to your ChatGPT account
4. Once logged in, the MCP will work automatically

The browser stays open, so you only need to do this once per session.

### Port already in use

Change the CDP port:
```json
{
  "mcp": {
    "ChatGPTAdvisor": {
      "type": "local",
      "command": ["python", "mcp_server.py"],
      "environment": {
        "CDP_ENDPOINT": "http://127.0.0.1:9223"
      }
    }
  }
}
```

## Files

```
chatgpt-advisor-mcp/
├── mcp_server.py      # Main MCP server
├── requirements.txt   # Python dependencies
├── setup.bat         # Windows setup script
├── setup.sh          # Linux/Mac setup script
├── freeloader/       # Freeloader (clone or symlink)
└── README.md         # This file
```

## License

MIT - Use at your own risk. This tool interfaces with ChatGPT through Freeloader.
