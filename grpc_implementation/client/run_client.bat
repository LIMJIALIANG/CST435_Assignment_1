@echo off
REM Run microservices client

echo Running Microservices Client...
echo.

set SCRIPT_DIR=%~dp0
set PROJECT_ROOT=%SCRIPT_DIR%..\..

REM Activate virtual environment
if exist "%PROJECT_ROOT%\.venv\Scripts\activate.bat" (
    echo Activating virtual environment...
    call "%PROJECT_ROOT%\.venv\Scripts\activate.bat"
)

REM Run client
echo Initiating workflow: Client - A - B - C - D - E
echo.
python "%SCRIPT_DIR%\microservices_client.py"

pause
