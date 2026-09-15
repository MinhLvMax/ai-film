@echo off
cd /d %~dp0

REM Chạy Streamlit bằng Python nhúng
downloads\embed\python_embed\python.exe -m streamlit run main.py

REM Chạy Streamlit từ venv
REM venv\Scripts\streamlit.exe run main.py --server.runOnSave false

pause