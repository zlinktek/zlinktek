@echo off
setlocal
cd /d "%~dp0"
python scripts\generate-products.py all
if errorlevel 1 goto failed
echo.
echo Generated website page and Taobao HTML successfully.
start "" "exports\index.html"
pause
exit /b 0
:failed
echo Generation failed. Check the error above. Python 3 is required.
pause
exit /b 1
