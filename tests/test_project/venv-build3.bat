@echo off
echo Delete and rebuild the virtual environment?
pause
rmdir /s /q venv
call ..\..\..\..\environments\python3.7\virtualenv.bat venv
call venv\Scripts\activate.bat
call python -m pip install --upgrade pip
call pip install --upgrade setuptools
call pip install twine
call pip install pylint
call pip install -e ..\..
call npm install
pause
