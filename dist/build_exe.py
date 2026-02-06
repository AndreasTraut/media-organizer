"""
Build-Skript für Media Organizer Executable

Dieses Skript erstellt eine ausführbare .exe-Datei für die Media Organizer GUI (app.py).
Verwendet PyInstaller mit Streamlit-spezifischen Anpassungen.

Verwendung:
    python dist/build_exe.py
"""

import os
import sys
import subprocess
from pathlib import Path

# Repository-Root finden
REPO_ROOT = Path(__file__).parent.parent
os.chdir(REPO_ROOT)

print("=" * 80)
print("Media Organizer - EXE Build Script")
print("=" * 80)
print(f"Repository Root: {REPO_ROOT}")
print(f"Python Version: {sys.version}")
print()

# PyInstaller Befehl zusammenbauen
cmd = [
    sys.executable, "-m", "PyInstaller",
    "--name=MediaOrganizer",
    "--onefile",
    "--windowed",  # Kein Konsolen-Fenster bei Start
    "--noconfirm",  # Überschreibe vorherige Builds
    "--clean",  # Cleanup vor Build
    
    # Icon (optional - kann später hinzugefügt werden)
    # "--icon=icon.ico",
    
    # Versteckte Imports für Streamlit
    "--hidden-import=streamlit",
    "--hidden-import=streamlit.web.cli",
    "--hidden-import=streamlit.runtime.scriptrunner.magic_funcs",
    
    # Phase 1 Module
    "--hidden-import=phase1_photo_sort.photo_sort",
    
    # Phase 2 Module
    "--hidden-import=phase2_photo_intelligence.photo_insights",
    "--hidden-import=phase2_photo_intelligence.photo_rag",
    
    # ML/AI Libraries
    "--hidden-import=PIL",
    "--hidden-import=PIL._imaging",
    "--hidden-import=numpy",
    "--hidden-import=torch",
    "--hidden-import=torchvision",
    "--hidden-import=transformers",
    "--hidden-import=deepface",
    "--hidden-import=fer",
    "--hidden-import=cv2",
    "--hidden-import=faiss",
    "--hidden-import=openai",
    
    # Daten-Dateien einbinden
    "--add-data=.env.example:.",
    "--add-data=README.md:.",
    
    # Ausgabe-Ordner
    "--distpath=dist/output",
    "--workpath=dist/build",
    "--specpath=dist",
    
    # Haupt-Datei
    "app.py"
]

print("Führe PyInstaller aus...")
print(f"Befehl: {' '.join(cmd)}")
print()

try:
    result = subprocess.run(cmd, check=True)
    print()
    print("=" * 80)
    print("✅ Build erfolgreich!")
    print("=" * 80)
    print(f"Executable: {REPO_ROOT}/dist/output/MediaOrganizer.exe")
    print()
    print("⚠️ WICHTIG:")
    print("1. Die .exe benötigt weiterhin Python-Runtime Umgebung")
    print("2. Für Distribution siehe: dist/README_DISTRIBUTION.md")
    print("3. Teste die .exe gründlich vor Verteilung")
    
except subprocess.CalledProcessError as e:
    print()
    print("=" * 80)
    print("❌ Build fehlgeschlagen!")
    print("=" * 80)
    print(f"Exit Code: {e.returncode}")
    sys.exit(1)
