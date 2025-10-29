@echo off
REM Run XML-RPC Server
echo Starting XML-RPC Server...
cd /d "%~dp0"
call ..\.venv\Scripts\activate.bat
python server\server.py
pause
