@echo off 

CALL run_env.bat
FOR /F "tokens=1,2,3,4" %%i in (test_bot_tokens.txt) do (
    start python bots\main.py %%i %%j %%k %%l
)

