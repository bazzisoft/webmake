@echo off
echo Delete and rebuild the virtual environment?
pause
rmdir /s /q venv
call \PROGRAMS\Python\virtualenv3.bat venv
call venv\Scripts\activate.bat
call python -m pip install --upgrade pip
call pip install --upgrade setuptools wheel
call pip install twine ruff
call pip install -e ..\..
call npm install
pause
