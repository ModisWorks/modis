for /d /r . %%d in (__pycache__) do @if exist "%%d" echo "%%d" && rd /s/q "%%d"
pause