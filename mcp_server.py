#!/usr/bin/env python3
"""
ChatGPT Advisor MCP - OpenCode MCP Server
Auto-starts Freeloader API and Browser for seamless ChatGPT access
"""
import sys
import os
import subprocess
import time
import threading
import urllib.request
import shutil
from pathlib import Path

# MCP Server
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("ChatGPTAdvisor")

# =============================================================================
# CONFIGURATION - Can be overridden via environment variables
# =============================================================================
PACKAGE_DIR = Path(__file__).resolve().parent
API_URL = os.environ.get("FREELOADER_API_URL", "http://127.0.0.1:11435/v1/chat/completions")
CDP_ENDPOINT = os.environ.get("CDP_ENDPOINT", "http://127.0.0.1:9222")

# Default freeloader path (relative to package)
DEFAULT_FREELOADER_DIR = PACKAGE_DIR / "freeloader"

# Timeout configuration
STARTUP_TIMEOUT_API = int(os.environ.get("STARTUP_TIMEOUT_API", "60"))
STARTUP_TIMEOUT_BROWSER = int(os.environ.get("STARTUP_TIMEOUT_BROWSER", "30"))
REQUEST_TIMEOUT = int(os.environ.get("REQUEST_TIMEOUT", "300"))

def log(msg):
    """Log to stderr"""
    print(f"[ChatGPTAdvisor] {msg}", flush=True, file=sys.stderr)

# =============================================================================
# BROWSER DETECTION
# =============================================================================
def find_browser():
    """Find installed browser (Brave or Chrome)"""
    candidates = []
    
    # Windows paths
    if sys.platform == "win32":
        candidates = [
            Path("C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe"),
            Path("C:/Program Files/Google/Chrome/Application/chrome.exe"),
            Path("C:/Program Files (x86)/BraveSoftware/Brave-Browser/Application/brave.exe"),
            Path("C:/Program Files (x86)/Google/Chrome/Application/chrome.exe"),
            Path.home() / "AppData/Local/BraveSoftware/Brave-Browser/Application/brave.exe",
            Path.home() / "AppData/Local/Google/Chrome/Application/chrome.exe",
            Path.home() / "AppData/Local/Microsoft/Edge/Application/msedge.exe",
        ]
    # macOS paths
    elif sys.platform == "darwin":
        candidates = [
            Path("/Applications/Brave Browser.app/Contents/MacOS/Brave Browser"),
            Path("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"),
            Path.home() / "Applications/Brave Browser.app/Contents/MacOS/Brave Browser",
            Path.home() / "Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        ]
    # Linux paths
    else:
        candidates = [
            Path("/usr/bin/brave"),
            Path("/usr/bin/google-chrome"),
            Path("/usr/bin/chromium"),
            Path("/usr/bin/chromium-browser"),
            Path.home() / ".local/bin/brave-browser",
            Path.home() / ".local/bin/google-chrome",
        ]
    
    # Also check PATH
    for name in ["brave", "brave-browser", "google-chrome", "chrome", "chromium", "chromium-browser"]:
        path = shutil.which(name)
        if path:
            candidates.append(Path(path))
    
    for c in candidates:
        if c.exists():
            return c
    
    return None

# =============================================================================
# SERVICE HEALTH CHECKS
# =============================================================================
def is_freeloader_running():
    """Check if Freeloader API is running"""
    try:
        health_url = API_URL.replace('/v1/chat/completions', '/health')
        req = urllib.request.Request(health_url)
        with urllib.request.urlopen(req, timeout=2):
            return True
    except:
        return False

def is_browser_running_with_cdp():
    """Check if browser is running with CDP"""
    try:
        req = urllib.request.Request(f"{CDP_ENDPOINT}/json/version")
        with urllib.request.urlopen(req, timeout=2):
            return True
    except:
        return False

# =============================================================================
# SERVICE STARTUP
# =============================================================================
def find_freeloader():
    """Find freeloader installation"""
    # 1. Check environment variable
    fl_dir = os.environ.get("FREELOADER_DIR")
    if fl_dir:
        p = Path(fl_dir)
        if (p / "freeloader.py").exists():
            return p
    
    # 2. Check default path (relative to package)
    if (DEFAULT_FREELOADER_DIR / "freeloader.py").exists():
        return DEFAULT_FREELOADER_DIR
    
    # 3. Check parent directory
    parent_fl = PACKAGE_DIR.parent / "freeloader"
    if (parent_fl / "freeloader.py").exists():
        return parent_fl
    
    return None

def start_services():
    """Auto-start freeloader API and browser if not running"""
    
    # Check/start Freeloader API
    if not is_freeloader_running():
        fl_dir = find_freeloader()
        if fl_dir:
            log(f"Starting Freeloader API from {fl_dir}...")
            try:
                subprocess.Popen(
                    [sys.executable, str(fl_dir / "freeloader.py"), "serve"],
                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                    start_new_session=True,
                    creationflags=subprocess.CREATE_NEW_CONSOLE if sys.platform == "win32" else 0
                )
                for _ in range(STARTUP_TIMEOUT_API):
                    time.sleep(1)
                    if is_freeloader_running():
                        log("Freeloader API ready")
                        break
                else:
                    log("Freeloader API startup timeout")
            except Exception as e:
                log(f"Failed to start Freeloader: {e}")
        else:
            log("Freeloader not found. Set FREELOADER_DIR env var or place freeloader/ folder here.")
    
    # Check/start Browser
    if not is_browser_running_with_cdp():
        browser = find_browser()
        if browser:
            log(f"Starting {browser.name}...")
            try:
                subprocess.Popen(
                    [str(browser), "--remote-debugging-port=9222", "--no-first-run", "--no-default-browser-check"],
                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                    start_new_session=True
                )
                for _ in range(STARTUP_TIMEOUT_BROWSER):
                    time.sleep(1)
                    if is_browser_running_with_cdp():
                        log("Browser ready")
                        break
                else:
                    log("Browser startup timeout")
            except Exception as e:
                log(f"Failed to start browser: {e}")
        else:
            log("No browser found. Install Brave or Chrome.")
    
    log("Services initialized")

# =============================================================================
# FREELOADER API CALL
# =============================================================================
def call_freeloader(prompt: str) -> str:
    """Call Freeloader API"""
    import json
    import urllib.error
    
    payload = {
        "model": "freeloader",
        "messages": [{"role": "user", "content": prompt}]
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(API_URL, data=data, headers={"Content-Type": "application/json"})
    
    try:
        with urllib.request.urlopen(req, timeout=REQUEST_TIMEOUT) as response:
            result = json.loads(response.read().decode("utf-8"))
            return result.get("choices", [{}])[0].get("message", {}).get("content", "Sin respuesta")
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        if "Cloudflare" in body or "CAPTCHA" in body:
            return "ChatGPT bloqueado (Cloudflare/CAPTCHA). Abre el navegador manualmente e inicia sesión."
        return f"Error HTTP {e.code}: {body[:200]}"
    except urllib.error.URLError as e:
        return f"Freeloader no disponible. Inicia manualmente: python freeloader.py serve"
    except Exception as e:
        return f"Error: {str(e)[:100]}"

# =============================================================================
# MCP TOOLS
# =============================================================================
@mcp.tool()
def advisor_ask(prompt: str) -> str:
    """
    Ask ChatGPT any question.
    
    Usage: Ask questions, get explanations, write code, analyze problems, etc.
    """
    return call_freeloader(prompt)

@mcp.tool()
def advisor_status() -> str:
    """
    Check if Freeloader services are running.
    """
    api_status = "✓ running" if is_freeloader_running() else "✗ not running"
    browser_status = "✓ running" if is_browser_running_with_cdp() else "✗ not running"
    browser_path = find_browser()
    
    return f"""ChatGPTAdvisor Status:
- Freeloader API: {api_status}
- Browser (CDP): {browser_status}
- Browser: {browser_path.name if browser_path else 'none'}

Endpoints:
- API: {API_URL}
- CDP: {CDP_ENDPOINT}
"""

# =============================================================================
# MAIN
# =============================================================================
if __name__ == "__main__":
    log("Starting MCP server...")
    log(f"Package directory: {PACKAGE_DIR}")
    
    # Start services in background
    threading.Thread(target=start_services, daemon=True).start()
    
    # Run MCP server
    mcp.run()