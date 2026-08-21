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

rem A frozen/installed Archipelago (the kind with Archipelago*.exe files and
rem no loose Utils.py/CommonClient.py) can't run this client directly - those
rem modules only exist bundled inside its compiled exes, not as importable
rem source. This needs a real source checkout of Archipelago with this
rem client (and the jedi_academy_sp world) dropped into it. Edit this path
rem to wherever that is on your machine if it's not here.
set AP_SOURCE_CHECKOUT=D:\Claude Stuff\Archiplego modded one\ja-ap-dev

if not exist "%AP_SOURCE_CHECKOUT%\JediAcademySPClient.py" (
    echo.
    echo Couldn't find JediAcademySPClient.py in:
    echo   %AP_SOURCE_CHECKOUT%
    echo Edit AP_SOURCE_CHECKOUT at the top of this section in start_client.bat
    echo to point at your own Archipelago source checkout.
    pause
    exit /b 1
)

pushd "%AP_SOURCE_CHECKOUT%"
python JediAcademySPClient.py %AP_ARGS%
popd

pause
