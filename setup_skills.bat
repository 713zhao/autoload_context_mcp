@echo off
setlocal enabledelayedexpansion

echo ================================================
echo Skills CLI Setup
echo ================================================
echo.

REM Step 1: Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found. Please install Python 3.x first.
    pause
    exit /b 1
)

echo [1/3] Installing Python dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo [ERROR] Failed to install dependencies.
    pause
    exit /b 1
)
echo      Done!
echo.

echo [2/3] Setting up VS Code keyboard shortcuts...

REM Define paths
set "KEYBINDINGS_SOURCE=.vscode\keybindings.json"
set "USER_KEYBINDINGS=%APPDATA%\Code\User\keybindings.json"

REM Check if source exists
if not exist "%KEYBINDINGS_SOURCE%" (
    echo [ERROR] Source keybindings not found: %KEYBINDINGS_SOURCE%
    pause
    exit /b 1
)

REM Create user keybindings if it doesn't exist
if not exist "%USER_KEYBINDINGS%" (
    echo []> "%USER_KEYBINDINGS%"
)

REM Backup existing keybindings
copy "%USER_KEYBINDINGS%" "%USER_KEYBINDINGS%.backup" >nul 2>&1

REM Read source keybindings (skip first [ and last ])
set "NEW_BINDINGS="
for /f "usebackq delims=" %%a in ("%KEYBINDINGS_SOURCE%") do (
    set "line=%%a"
    REM Skip empty lines and brackets
    if not "!line!"=="[" if not "!line!"=="]" if not "!line!"=="" (
        set "NEW_BINDINGS=!NEW_BINDINGS!%%a"
    )
)

REM Append to user keybindings (insert before closing bracket)
powershell -Command "$content = Get-Content '%USER_KEYBINDINGS%' -Raw; $content = $content.TrimEnd(); if ($content -match '^(\[\s*)(\]\s*)$') { $content = '[' } elseif ($content -match '(.*)\](\s*)$') { $content = $matches[1] + ',' } $newBindings = (Get-Content '%KEYBINDINGS_SOURCE%' | Select-Object -Skip 1 | Select-Object -SkipLast 1) -join \"`n\"; Set-Content '%USER_KEYBINDINGS%' \"$content`n$newBindings`n]\""

echo      Keyboard shortcuts added to: %USER_KEYBINDINGS%
echo      Backup saved to: %USER_KEYBINDINGS%.backup
echo.

echo [3/3] Setup complete!
echo.
echo ================================================
echo Next Steps (Please try these):
echo ================================================
echo.
echo   [Step 4] Verify tasks are available:
echo      1. Press Ctrl+Shift+P
echo      2. Type "Tasks: Run Task"
echo      3. You should see "Load Skill: Google Mock", etc.
echo.
echo   [Step 5] Test keyboard shortcuts:
echo      1. Press Ctrl+K Ctrl+M (loads Google Mock)
echo      2. File opens in editor for Copilot context
echo      3. Open Copilot chat (Ctrl+Alt+I)
echo      4. Ask: "How do I create a mock class?"
echo.
echo ================================================
echo Available Shortcuts:
echo   Ctrl+K Ctrl+M - Load Google Mock skill
echo   Ctrl+K Ctrl+E - Load GTest Execute skill
echo   Ctrl+K Ctrl+D - Load Design skill
echo   Ctrl+K Ctrl+L - List all skills
echo ================================================
echo.
echo If shortcuts don't work, restart VS Code.
echo.
pause
