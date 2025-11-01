@echo off
REM Start all XML-RPC microservices
echo Starting XML-RPC Microservices...
echo.
echo Note: This will start 3 services in separate windows
echo Press Ctrl+C to cancel, or any other key to continue...
pause > nul

cd /d "%~dp0"

REM Start Statistics Service first (terminal service)
echo Starting Statistics Service on port 8005...
start "Statistics Service" cmd /k "python statistics.py"
timeout /t 2 /nobreak > nul

REM Start MergeSort Service
echo Starting MergeSort Service (Sort CGPA + Grade) on port 8003...
start "MergeSort Service" cmd /k "python mergesort.py"
timeout /t 2 /nobreak > nul

REM Start MapReduce Service (entry point)
echo Starting MapReduce Service (CGPA + Grade Count) on port 8001...
start "MapReduce Service" cmd /k "python mapreduce.py"

echo.
echo ======================================================================
echo All services started!
echo ======================================================================
echo Service Chain:
echo   Client → MapReduce (8001) → MergeSort (8003) → Statistics (8005) → Client
echo.
echo To run the client:
echo   cd client
echo   run_client.bat
echo.
echo To stop all services, close the command windows
echo ======================================================================
pause

