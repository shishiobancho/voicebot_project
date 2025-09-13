@echo off
REM ===== VOICEBOT RUN SCRIPT =====
setlocal

REM プロジェクトのルートへ移動
set PYTHONPATH=D:\voicebot_project\src
cd /d D:\voicebot_project

REM 日時付きログファイル名
set LOGDIR=logs
if not exist %LOGDIR% mkdir %LOGDIR%
set LOGFILE=%LOGDIR%\run_%DATE:~0,4%%DATE:~5,2%%DATE:~8,2%_%TIME:~0,2%%TIME:~3,2%%TIME:~6,2%.log

echo [INFO] Starting VOICEBOT...
python -m src.main

echo [INFO] Process finished.
pause
