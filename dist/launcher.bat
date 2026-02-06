@echo off
REM Media Organizer - Windows Launcher
REM Startet die Streamlit GUI direkt per Doppelklick

echo ================================================================================
echo Media Organizer - Photo Intelligence Suite
echo ================================================================================
echo.

REM Wechsle ins Projekt-Verzeichnis
cd /d "%~dp0.."

REM Prüfe Python
python --version >nul 2>&1
if errorlevel 1 (
    echo FEHLER: Python nicht gefunden!
    echo Bitte Python 3.12+ installieren: https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

REM Prüfe Streamlit
python -m streamlit --version >nul 2>&1
if errorlevel 1 (
    echo WARNUNG: Streamlit nicht installiert!
    echo Installiere Dependencies...
    echo.
    pip install -r requirements-gui.txt
    if errorlevel 1 (
        echo.
        echo FEHLER: Installation fehlgeschlagen!
        pause
        exit /b 1
    )
)

REM Starte Streamlit
echo Starte Media Organizer GUI...
echo Browser oeffnet automatisch auf http://localhost:8501
echo.
echo Druecke Ctrl+C zum Beenden
echo ================================================================================
echo.

python -m streamlit run app.py --server.headless=true --server.port=8501 --browser.gatherUsageStats=false

pause
