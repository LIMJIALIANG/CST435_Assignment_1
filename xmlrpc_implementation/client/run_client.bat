@echo off
REM Run XML-RPC Client
echo Starting XML-RPC Client...
cd /d "%~dp0"
call ..\..\..\.venv\Scripts\activate.bat
python client.py
pause
