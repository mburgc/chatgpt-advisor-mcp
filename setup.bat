@echo off
REM ChatGPT Advisor MCP - Setup Script
REM Creates virtual environment and installs dependencies

echo [ChatGPTAdvisor] Setting up...

REM Clone Freeloader if not present
if not exist "freeloader" (
    echo [ChatGPTAdvisor] Cloning Freeloader...
    git clone https://github.com/mburgc/freeloader.git freeloader
)

REM Create venv
python -m venv venv

REM Activate and install
call venv\Scripts\activate.bat
pip install --upgrade pip
pip install -r requirements.txt
pip install playwright
python -m playwright install chromium

echo.
echo [ChatGPTAdvisor] Setup complete!
echo.
echo To run the MCP:
echo   venv\Scripts\python mcp_server.py
echo.
echo Or add to OpenCode config (see README.md)
pause