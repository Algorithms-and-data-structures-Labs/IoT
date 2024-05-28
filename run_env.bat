@echo off

IF NOT EXIST .venv\Scripts\activate.bat (
    CALL setup.bat
)

CALL .venv\Scripts\activate.bat