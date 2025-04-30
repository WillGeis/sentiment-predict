@echo off

echo Starting up the app...

python -m compileall -q .

python main.py

pause
