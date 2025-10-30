@echo off
REM Start all 5 microservices

echo Starting Microservices...
echo.

set SCRIPT_DIR=%~dp0
set PROJECT_ROOT=%SCRIPT_DIR%..\..

REM Activate virtual environment
if exist "%PROJECT_ROOT%\.venv\Scripts\activate.bat" (
    echo Activating virtual environment...
    call "%PROJECT_ROOT%\.venv\Scripts\activate.bat"
)

REM Start each service
echo Starting Service A (Port 50051)...
start "Service A" cmd /k "cd /d %SCRIPT_DIR% && python service_a_mapreduce_cgpa.py"
timeout /t 2 /nobreak >nul

echo Starting Service B (Port 50052)...
start "Service B" cmd /k "cd /d %SCRIPT_DIR% && python service_b_mapreduce_grade.py"
timeout /t 2 /nobreak >nul

echo Starting Service C (Port 50053)...
start "Service C" cmd /k "cd /d %SCRIPT_DIR% && python service_c_mergesort_cgpa.py"
timeout /t 2 /nobreak >nul

echo Starting Service D (Port 50054)...
start "Service D" cmd /k "cd /d %SCRIPT_DIR% && python service_d_mergesort_grade.py"
timeout /t 2 /nobreak >nul

echo Starting Service E (Port 50055)...
start "Service E" cmd /k "cd /d %SCRIPT_DIR% && python service_e_statistics.py"
timeout /t 2 /nobreak >nul

echo.
echo All 5 services started!
echo Service Chain: A(50051) - B(50052) - C(50053) - D(50054) - E(50055)
echo.
echo Now run the client: cd ..\client ^&^& run_client.bat
pause
