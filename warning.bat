@echo off
set MESSAGE=Task Failed Successfully
set TITLE=Error
set DELAY=3

:loop
mshta "javascript:alert('%MESSAGE%');close();"
timeout /t %DELAY% /nobreak >nul
goto loop
