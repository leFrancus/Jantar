@echo off
echo Jantar Uninstaller

echo WARNING! This program will delete ALL OF YOUR FILES, SETTINGS AND PROFILES inside the program directory and appdata.
set /p Confirm=Are you sure you want to delete Jantar? Y/n:

if /i "%Confirm%"=="Y" goto :Delete
if /i "%Confirm%"=="y" goto :Delete

echo Uninstallation has been canceled.
goto :End

:Delete
echo Need to delete libraries that used in program? WARNING: may break other programs! Y/n
if /i "%Confirm%"=="y" goto :UninstLibs
if /i "%Confirm%"=="Y" goto :UninstLibs

:UninstLibs
pip uninstall -r requirements.txt

rmdir /s /q %appdata%\Jantar
rmdir /s /q ..

:End
pause