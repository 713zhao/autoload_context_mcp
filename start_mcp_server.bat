@echo off
REM MCP Context Loader HTTP Server Startup Script
REM This script creates a virtual environment and runs the MCP server

echo ========================================
echo MCP Context Loader Server Setup
echo ========================================
echo.

REM Check if Python 3.13 is available
python --version | findstr /C:"3.13" >nul
if %errorlevel% neq 0 (
    echo ERROR: Python 3.13 not found!
    echo Please install Python 3.13 or update the script.
    pause
    exit /b 1
)

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo Creating Python 3.13 virtual environment...
    py -3.13 -m venv venv
    if %errorlevel% neq 0 (
        echo ERROR: Failed to create virtual environment
        pause
        exit /b 1
    )
    echo Virtual environment created successfully!
    echo.
    
    echo Installing dependencies...
    call venv\Scripts\activate.bat
    python -m pip install --upgrade pip
    pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo ERROR: Failed to install dependencies
        pause
        exit /b 1
    )
    echo Dependencies installed successfully!
    echo.
) else (
    echo Virtual environment already exists, skipping setup...
    call venv\Scripts\activate.bat
)

REM Start the MCP server
echo.
echo ========================================
echo Starting MCP Context Loader Server
echo ========================================
echo.
echo Server will start on: http://0.0.0.0:8000
echo SSE Endpoint: http://0.0.0.0:8000/sse
echo.
echo Press Ctrl+C to stop the server
echo.

python mcp_server_http.py 0.0.0.0 8000

REM Deactivate virtual environment on exit
deactivate
