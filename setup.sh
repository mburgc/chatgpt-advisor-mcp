#!/bin/bash
# ChatGPT Advisor MCP - Setup Script (Linux/Mac)

echo "[ChatGPTAdvisor] Setting up..."

# Check if freeloader exists
if [ ! -d "freeloader" ]; then
    echo "[ChatGPTAdvisor] Cloning Freeloader..."
    git clone https://github.com/mburgc/freeloader.git freeloader
fi

# Create venv
python3 -m venv venv

# Activate and install
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
pip install playwright
python -m playwright install chromium

echo ""
echo "[ChatGPTAdvisor] Setup complete!"
echo ""
echo "To run: source venv/bin/activate && python mcp_server.py"
echo "Or add to OpenCode (see README.md)"