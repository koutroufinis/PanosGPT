@echo off
:: setup.bat — creates a virtual environment and installs all dependencies

set VENV_DIR=.venv

echo Creating virtual environment in '%VENV_DIR%'...
python -m venv %VENV_DIR%

echo Activating and installing dependencies...
call %VENV_DIR%\Scripts\activate.bat
python -m pip install --upgrade pip -q
pip install -r requirements.txt

echo.
echo Done! To start the chat:
echo   .venv\Scripts\activate
echo   python chat.py
pause