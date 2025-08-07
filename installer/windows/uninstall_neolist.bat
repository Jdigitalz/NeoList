@echo off
setlocal enabledelayedexpansion

:: Set the target install directory
set "TARGET_DIR=%USERPROFILE%\Scripts"
set "SCRIPT_NAME=neolist.bat"
set "FULL_PATH=%TARGET_DIR%\%SCRIPT_NAME%"

:: Delete the neolist.bat file
if exist "%FULL_PATH%" (
    del "%FULL_PATH%"
    echo Removed %SCRIPT_NAME% from %TARGET_DIR%
) else (
    echo %SCRIPT_NAME% was not found in %TARGET_DIR%
)

:: Ask user if they want to remove the folder from PATH
echo.
set /p REMOVE_PATH=Do you want to remove %TARGET_DIR% from your PATH? (y/N): 
if /I "%REMOVE_PATH%"=="Y" (
    echo Updating PATH...
    for /f "tokens=1,* delims==" %%a in ('set PATH') do (
        set "NEW_PATH=%%b"
        set "NEW_PATH=!NEW_PATH:%TARGET_DIR%;=!"
        set "NEW_PATH=!NEW_PATH:;%TARGET_DIR%=!"
        set "NEW_PATH=!NEW_PATH:%TARGET_DIR%=!"
        setx PATH "!NEW_PATH!" >nul
    )
    echo Removed %TARGET_DIR% from your PATH.
) else (
    echo Skipped PATH cleanup.
)

echo.
echo Uninstall complete.
pause

