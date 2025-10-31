@echo off
REM Start all 3 microservices

echo Starting Microservices...
echo.

set SCRIPT_DIR=%~dp0
set PROJECT_ROOT=%SCRIPT_DIR%..\..

REM Activate virtual environment
if exist "%PROJECT_ROOT%\.venv\Scripts\activate.bat" (
    echo Activating virtual environment...
    call "%PROJECT_ROOT%\.venv\Scripts\activate.bat"
)

# Start each service
echo Starting MapReduce Service (Port 50051) - CGPA + Grade Classification...
start "MapReduce Service" cmd /k "cd /d %SCRIPT_DIR% && python mapreduce_cgpa.py"
timeout /t 2 /nobreak >nul

echo Starting MergeSort Service (Port 50053) - Sort CGPA + Grade...
start "MergeSort Service" cmd /k "cd /d %SCRIPT_DIR% && python mergesort_cgpa.py"
timeout /t 2 /nobreak >nul

echo Starting Statistics Service (Port 50055) - Statistical Analysis...
start "Statistics Service" cmd /k "cd /d %SCRIPT_DIR% && python statistics.py"
timeout /t 2 /nobreak >nul

echo.
echo All 3 services started!
echo Service Chain: MapReduce(50051) → MergeSort(50053) → Statistics(50055)
echo.
echo Now run the client: cd ..\client ^&^& run_client.bat
pause

