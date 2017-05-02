@echo off
echo Delete and rebuild the virtual environment?
pause
rmdir /s /q venv
call ..\..\..\..\environments\python2.7\virtualenv.bat venv
call venv\Scripts\activate.bat
call pip install pylint
call pip install -e ..\..
call npm install
pause
