@echo off
cd /d "C:\Users\jhane\Desktop\JJ ELEVATE Final Project"

:: Check if required commands exist
where pyuic5 >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: pyuic5 not found. Make sure PyQt5 is installed.
    pause
    exit /b 1
)

where pyrcc5 >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: pyrcc5 not found. Make sure PyQt5 is installed.
    pause
    exit /b 1
)

:: Clear old generated files
del /q ui\generated_files\*.py >nul 2>&1
del /q ui\resources\jj_resources_rc.py >nul 2>&1

:: Compile resources FIRST
echo Compiling resources...
pushd ui\resources
pyrcc5 jj_resources.qrc -o jj_resources_rc.py
if %errorlevel% neq 0 (
    echo Error compiling resources!
    popd
    pause
    exit /b 1
)
popd

:: Convert UI files
echo Generating UI files...

:: Authentication pages
call :convert_ui UI_Landing
call :convert_ui UI_LogIn
call :convert_ui UI_ForgotPass

:: Owner interface
call :convert_ui UI_ODashboard
call :convert_ui UI_OInventory
call :convert_ui UI_OOrders
call :convert_ui UI_OSales
call :convert_ui UI_OStockHistory
call :convert_ui UI_OAccount

:: Cashier interface
call :convert_ui UI_CDashboard
call :convert_ui UI_CInventory
call :convert_ui UI_COrders
call :convert_ui UI_CSales
call :convert_ui UI_CStockHistory
call :convert_ui UI_CAccount

:: Fix imports in all generated files
echo Fixing imports...
powershell -Command "(Get-ChildItem ui/generated_files/*.py) | ForEach-Object { (Get-Content $_) -replace 'import jj_resources_rc', 'from ui.resources import jj_resources_rc' | Set-Content $_ }"

:: Verify generation - more accurate check
set "error=0"
for /f %%i in ('dir /b ui\generated_files ^| find /c /v ""') do set "filecount=%%i"
if %filecount% lss 15 (
    set "error=1"
    echo Warning: Expected 15 files but only found %filecount%!
)

if %error% equ 0 (
    echo Success: All UI files and resources generated correctly!
    echo Total files generated: %filecount%
) else (
    echo Warning: Some UI files might be missing!
)

pause
exit /b 0

:convert_ui
pyuic5 ui/raw_files/%1.ui -o ui/generated_files/%1.py
if not exist "ui/generated_files/%1.py" (
    echo Error generating %1.py
    set "error=1"
)
exit /b