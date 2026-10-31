@echo off
rem Lanza herramientas\iabl.py con el Python de herramientas\.venv (lo crea instalar.py). Para PowerShell y CMD.
setlocal
set "AQUI=%~dp0"
set "PYTHONUTF8=1"
if not exist "%AQUI%.venv\Scripts\python.exe" (
  echo Primero: python herramientas\instalar.py
  exit /b 1
)
"%AQUI%.venv\Scripts\python.exe" "%AQUI%iabl.py" %*
exit /b %ERRORLEVEL%
