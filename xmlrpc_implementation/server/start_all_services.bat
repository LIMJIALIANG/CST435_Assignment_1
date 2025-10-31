@echo off
REM Start all XML-RPC microservices
echo Starting XML-RPC Microservices...
echo.
echo Note: This will start 5 services in separate windows
echo Press Ctrl+C to cancel, or any other key to continue...
pause > nul

cd /d "%~dp0"

REM Start Service E first (terminal service)
echo Starting Service E (Statistics) on port 8005...
start "Service E" cmd /k "call ..\..\..\.venv\Scripts\activate.bat && python service_e.py"
timeout /t 2 /nobreak > nul

REM Start Service D
echo Starting Service D (Sort Grade) on port 8004...
start "Service D" cmd /k "call ..\..\..\.venv\Scripts\activate.bat && python service_d.py"
timeout /t 2 /nobreak > nul

REM Start Service C
echo Starting Service C (Sort CGPA) on port 8003...
start "Service C" cmd /k "call ..\..\..\.venv\Scripts\activate.bat && python service_c.py"
timeout /t 2 /nobreak > nul

REM Start Service B
echo Starting Service B (Grade Count) on port 8002...
start "Service B" cmd /k "call ..\..\..\.venv\Scripts\activate.bat && python service_b.py"
timeout /t 2 /nobreak > nul

REM Start Service A (entry point)
echo Starting Service A (CGPA Count) on port 8001...
start "Service A" cmd /k "call ..\..\..\.venv\Scripts\activate.bat && python service_a.py"

echo.
echo ======================================================================
echo All services started!
echo ======================================================================
echo Service Chain:
echo   Client → Service A (8001) → Service B (8002) → Service C (8003) → Service D (8004) → Service E (8005) → Client
echo.
echo To run the client:
echo   cd client
echo   run_client.bat
echo.
echo To stop all services, close the command windows
echo ======================================================================
pause
