@echo off
cd /d %~dp0

@REM downloads\embed\python_embed\Scripts\streamlit.exe run main.py

REM Chạy Streamlit từ venv
venv\Scripts\streamlit.exe run main.py --server.runOnSave false

pause