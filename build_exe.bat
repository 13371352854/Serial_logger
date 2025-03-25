@echo off

rd /s /q CSV_Files
rd /s /q dist
rd /s /q build
del /f *.spec

call %cd%/".venv/Scripts/activate"

if %errorlevel% neq 0 (
echo Failed to activate virtual environment.
exit /b %errorlevel%
)

pyinstaller -F main.py --name=Serial_logger

pause

deactivate

