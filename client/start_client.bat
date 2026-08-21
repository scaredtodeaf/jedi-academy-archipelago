@echo off
setlocal

echo Jedi Academy SP - Archipelago Client
echo.

set /p AP_HOST=Server IP/address (e.g. localhost or archipelago.gg):
if "%AP_HOST%"=="" set AP_HOST=localhost

set /p AP_PORT=Port:
if "%AP_PORT%"=="" (
    echo Port is required.
    pause
    exit /b 1
)

set /p AP_NAME=Slot name:
set /p AP_PASSWORD=Password (leave blank if none):

set AP_ARGS=--connect %AP_HOST%:%AP_PORT%
if not "%AP_NAME%"=="" set AP_ARGS=%AP_ARGS% --name "%AP_NAME%"
if not "%AP_PASSWORD%"=="" set AP_ARGS=%AP_ARGS% --password "%AP_PASSWORD%"

echo.
echo Connecting to %AP_HOST%:%AP_PORT% ...
python "%~dp0JediAcademySPClient.py" %AP_ARGS%

pause
