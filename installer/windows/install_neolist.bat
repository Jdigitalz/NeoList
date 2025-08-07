@echo off
setlocal enabledelayedexpansion

:: Set the target install directory
set "TARGET_DIR=%USERPROFILE%\Scripts"

:: Create directory if it doesn't exist
if not exist "%TARGET_DIR%" (
    mkdir "%TARGET_DIR%"
    echo Created directory: %TARGET_DIR%
)

:: Copy neolist.bat to the target directory
copy /Y "neolist.bat" "%TARGET_DIR%\neolist.bat"
echo Installed neolist.bat to %TARGET_DIR%

:: Check if TARGET_DIR is in user PATH
echo Checking if %TARGET_DIR% is in PATH...
echo %PATH% | find /I "%TARGET_DIR%" >nul
if errorlevel 1 (
    echo Adding %TARGET_DIR% to your user PATH...
    setx PATH "%PATH%;%TARGET_DIR%" >nul
    echo You may need to restart your terminal for changes to take effect.
) else (
    echo %TARGET_DIR% is already in your PATH.
)

echo Done. You can now run 'neolist' from any terminal.
pause

