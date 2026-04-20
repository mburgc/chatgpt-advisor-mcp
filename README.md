# ChatGPT Advisor MCP

MCP (Model Context Protocol) server that provides seamless access to ChatGPT via Freeloader. Auto-starts the Freeloader API and browser - no manual setup required.

## Features

- **Auto-start**: Automatically starts Freeloader API and browser if not running
- **Cross-platform**: Works on Windows, macOS, and Linux
- **Browser detection**: Automatically finds Brave, Chrome, Edge, or Chromium
- **Easy config**: Just add to your OpenCode MCP configuration
- **Status tool**: Check service health anytime

## Requirements

- Python 3.10+
- [Freeloader](https://github.com/linyuxuanlin/Freeloader-n)
- Brave or Chrome browser

## Setup

### 1. Clone Freeloader

```bash
git clone https://github.com/linyuxuanlin/Freeloader-n.git freeloader
```

### 2. Install dependencies

```bash
# Windows
setup.bat

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

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

Set the `FREELOADER_DIR` environment variable or ensure `freeloader/` folder is next to `mcp_server.py`.

### "No browser found"

Install Brave or Chrome, or manually open your browser with:
```
brave --remote-debugging-port=9222
```

### ChatGPT blocked (Cloudflare/CAPTCHA)

Open your browser manually, navigate to chat.openai.com, and log in. Then restart the MCP.

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
