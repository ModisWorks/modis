echo off
cls
echo Creating Python virtual environment...
set VENVPATH=.\modis-venv
echo(
echo Activating virtual environment...
python -m venv "%VENVPATH%"
call "%VENVPATH%"\Scripts\activate.bat
echo ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
echo(
echo Updating pip...
python -m pip install --upgrade pip
echo(
echo Installing Modis Python package requirements...
pip install tkinter
pip install -U discord.py[voice]
pip install PyGithub
pip install youtube-dl
pip install soundcloud
pip install pynacl
pip install google-api-python-client
pip install requests
pip install lxml
pip install praw
pip install spotipy
echo ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
echo(
echo Copying ffmpeg binary...
xcopy .\venv-resources\ffmpeg.exe "%VENVPATH%"\Scripts
echo(
echo Copying modis files...
xcopy .\modis "%VENVPATH%"\modis /s /e /i
xcopy .\LauncherCMD.py "%VENVPATH%"
xcopy .\LauncherGUI.pyw "%VENVPATH%"
xcopy ".\venv-resources\#START MODIS.bat" "%VENVPATH%"
echo(
echo Replacing scripts with version with relative paths
xcopy .\venv-resources\activate "%VENVPATH%"\Scripts /y
xcopy .\venv-resources\activate.bat "%VENVPATH%"\Scripts /y
xcopy .\venv-resources\Activate.ps1 "%VENVPATH%"\Scripts /y
echo(
echo deleting __pycache__ folders and .pyc files
for /d /r "%VENVPATH%" %%d in (__pycache__) do @if exist "%%d" echo "%%d" && rd /s/q "%%d"
echo ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
echo(
echo Portable Modis creation complete.
pause