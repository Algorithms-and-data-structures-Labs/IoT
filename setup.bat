@echo off
IF EXIST .venv (
    rmdir .venv /s /q
)

python -m venv .venv
CALL .venv\Scripts\activate.bat

pip install -r requirements.txt