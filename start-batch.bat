@echo off
set "PROJECT_DIR=D:\tutorial\nodejs&reactjs"

echo Starting Backend
cd /d "%PROJECT_DIR%\backend"
start cmd /k npm start

echo Starting Frontend
cd /d "%PROJECT_DIR%\frontend"
start cmd /k npm start
