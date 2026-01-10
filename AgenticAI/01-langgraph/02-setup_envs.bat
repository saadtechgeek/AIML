@echo off
REM ===================================================
REM Setup .env files for LangGraph Academy modules
REM Works in both CMD and PowerShell
REM ===================================================

setlocal enabledelayedexpansion

echo Setting up .env files for modules 1 to 5...

REM Loop through modules 1 to 5
for /L %%i in (1,1,5) do (
    set "SRC=module-%%i\studio\.env.example"
    set "DEST=module-%%i\studio\.env"

    if exist "!SRC!" (
        copy /Y "!SRC!" "!DEST!" >nul
        echo OPENAI_API_KEY=%OPENAI_API_KEY%>>"!DEST!"
        echo Created !DEST! with OPENAI_API_KEY
    ) else (
        echo Skipped module %%i - .env.example not found
    )
)

REM Add TAVILY_API_KEY to module-4 if it exists
if exist "module-4\studio\.env" (
    echo TAVILY_API_KEY=%TAVILY_API_KEY%>>"module-4\studio\.env"
    echo Added TAVILY_API_KEY to module-4\studio\.env
)

echo.
echo ✅ Environment setup complete!
pause
