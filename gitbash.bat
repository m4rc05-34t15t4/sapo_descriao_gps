@echo off
setlocal
set "GIT_BASH_PATH=C:\Program Files\Git\bin\bash.exe"
if not exist "%GIT_BASH_PATH%" (
    echo Git Bash não encontrado. Verifique o caminho para bash.exe.
    exit /b 1
)
"%GIT_BASH_PATH%" --cd=%cd%