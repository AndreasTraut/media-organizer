"""
Media Organizer - Launcher Script

Einfacher Launcher für die Media Organizer GUI.
Startet die Streamlit-App mit korrekten Parametern.

Verwendung:
    python dist/launcher.py
    
    ODER doppelklick auf launcher.py (wenn Python-Assoziierung korrekt)
"""

import os
import sys
import subprocess
from pathlib import Path

# Repository-Root finden
REPO_ROOT = Path(__file__).parent.parent

def main():
    """Startet die Media Organizer Streamlit GUI"""
    
    print("=" * 80)
    print("Media Organizer - Photo Intelligence Suite")
    print("=" * 80)
    print()
    print("Starte Streamlit GUI...")
    print(f"Repository: {REPO_ROOT}")
    print(f"Python: {sys.executable}")
    print()
    
    # Wechsle ins Repository-Verzeichnis
    os.chdir(REPO_ROOT)
    
    # Prüfe ob .env existiert
    env_file = REPO_ROOT / ".env"
    if not env_file.exists():
        print("⚠️  WARNUNG: Keine .env-Datei gefunden!")
        print(f"   Erstelle eine .env-Datei basierend auf .env.example")
        print(f"   Pfad: {env_file}")
        print()
        
        # Frage ob fortfahren
        response = input("Ohne .env fortfahren? (j/n): ")
        if response.lower() not in ['j', 'y', 'ja', 'yes']:
            print("Abgebrochen.")
            sys.exit(1)
    
    # Streamlit-Befehl
    cmd = [
        sys.executable, "-m", "streamlit", "run",
        str(REPO_ROOT / "app.py"),
        "--server.headless=true",  # Für headless environments
        "--server.port=8501",
        "--browser.gatherUsageStats=false"
    ]
    
    try:
        # Starte Streamlit
        print("🚀 Starte Streamlit auf http://localhost:8501")
        print()
        print("Drücke Ctrl+C zum Beenden")
        print("=" * 80)
        print()
        
        subprocess.run(cmd, check=True)
        
    except KeyboardInterrupt:
        print()
        print("=" * 80)
        print("Streamlit beendet.")
        print("=" * 80)
        sys.exit(0)
        
    except subprocess.CalledProcessError as e:
        print()
        print("=" * 80)
        print("❌ Fehler beim Starten!")
        print("=" * 80)
        print(f"Exit Code: {e.returncode}")
        print()
        print("Mögliche Ursachen:")
        print("1. Streamlit nicht installiert: pip install streamlit")
        print("2. Dependencies fehlen: pip install -r requirements-gui.txt")
        print("3. Port 8501 bereits belegt")
        print()
        sys.exit(1)
    
    except FileNotFoundError:
        print()
        print("=" * 80)
        print("❌ Python oder Streamlit nicht gefunden!")
        print("=" * 80)
        print()
        print("Installiere Streamlit:")
        print("  pip install streamlit")
        print()
        sys.exit(1)

if __name__ == "__main__":
    main()
