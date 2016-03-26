::Quick 'n dirty pyside-uic script for Windows, because it doesn't play nicely with bash...
@echo off
SET basepath=%~dp0..\app\view\gen\

for /f %%i in ('dir /b %basepath%\qt\*.ui') do (
	pyside-uic -o %basepath%%%~ni.py %basepath%qt\%%i
	echo Converting %%i to %%~ni.py...
)

echo.
for /f %%i in ('dir /b %basepath%\qt\*.qrc') do (
	pyside-rcc -o %basepath%%%~ni_rc.py %basepath%qt\%%i -py3
	echo Converting %%i to %%~ni_rc.py...
)

echo.
echo Done!