# Media Organizer - Ausführbare Dateien

Dieses Verzeichnis enthält Skripte und Konfigurationen zum Erstellen und Ausführen von Media Organizer als ausführbare Anwendung.

## 🎯 Quick Start - Einfachste Methode

### Windows

**Doppelklick auf:** `launcher.bat`

Die Batch-Datei:
- ✅ Prüft Python-Installation
- ✅ Installiert fehlende Dependencies
- ✅ Startet Streamlit GUI automatisch
- ✅ Öffnet Browser auf http://localhost:8501

### Linux/Mac

```bash
python dist/launcher.py
```

## 📦 Dateien in diesem Ordner

| Datei | Beschreibung |
|-------|--------------|
| `launcher.bat` | **Windows Launcher** - Einfachster Start per Doppelklick |
| `launcher.py` | **Python Launcher** - Cross-platform Start-Skript |
| `build_exe.py` | **EXE Builder** - Erstellt standalone .exe mit PyInstaller |
| `README_DISTRIBUTION.md` | **Detaillierte Anleitung** für .exe-Erstellung |
| `README.md` | **Diese Datei** - Übersicht |

## 🛠️ Methode 1: Launcher (Empfohlen für Entwicklung)

**Vorteile:**
- ✅ Schneller Start
- ✅ Einfache Fehlerbehebung
- ✅ Keine Build-Zeit
- ✅ Einfache Updates

**Nachteile:**
- ❌ Benötigt Python-Installation
- ❌ Benötigt installierte Dependencies

### Verwendung

**Windows:**
```bash
launcher.bat
```

**Linux/Mac/Windows:**
```bash
python launcher.py
```

## 🎁 Methode 2: Standalone EXE (Für Distribution)

**Vorteile:**
- ✅ Einzelne ausführbare Datei
- ✅ Kein sichtbares Terminal-Fenster
- ✅ Einfacher für Endnutzer

**Nachteile:**
- ❌ Lange Build-Zeit (5-15 Minuten)
- ❌ Große Datei (500 MB - 1.5 GB)
- ❌ Benötigt weiterhin Python-Runtime
- ❌ Kann von Antivirus blockiert werden

### EXE erstellen

```bash
# Installiere PyInstaller
pip install pyinstaller

# Erstelle EXE
python dist/build_exe.py

# Fertige EXE liegt in:
dist/output/MediaOrganizer.exe
```

**⚠️ WICHTIG:** Siehe `README_DISTRIBUTION.md` für Details und Troubleshooting!

## 🚀 Welche Methode soll ich verwenden?

### Für Entwickler / Eigene Nutzung
➡️ **Verwende Launcher** (`launcher.bat` oder `launcher.py`)
- Schneller
- Einfacher zu debuggen
- Kein Build-Overhead

### Für Distribution an Endnutzer
➡️ **Erstelle EXE** (`build_exe.py`)
- Professioneller
- Versteckt technische Details
- Einzelne Datei zum Verteilen

### Für Server-Deployment
➡️ **Verwende direkt Streamlit**
```bash
streamlit run app.py
```

## 📋 Voraussetzungen

### Für Launcher

- Python 3.12+
- Dependencies installiert:
  ```bash
  pip install -r requirements-gui.txt
  ```

### Für EXE-Build

Zusätzlich:
- PyInstaller:
  ```bash
  pip install pyinstaller
  ```
- 5-15 Minuten Build-Zeit
- 2-3 GB freier Speicher für Build

## 🐛 Troubleshooting

### Problem: "Python nicht gefunden"

**Lösung:**
- Installiere Python 3.12+: https://www.python.org/downloads/
- Bei Installation "Add to PATH" aktivieren
- Neu starten

### Problem: "Streamlit nicht gefunden"

**Lösung:**
```bash
pip install streamlit
# ODER installiere alle Dependencies:
pip install -r requirements-gui.txt
```

### Problem: Port 8501 bereits belegt

**Lösung:**
```bash
# Finde Prozess auf Port 8501
netstat -ano | findstr :8501

# Beende Prozess (Windows)
taskkill /PID <PID> /F

# Oder verwende anderen Port
streamlit run app.py --server.port=8502
```

### Problem: EXE wird von Antivirus blockiert

**Lösung:**
- Dies ist normal für self-compiled executables
- Füge .exe zu Antivirus-Ausnahmen hinzu
- Oder signiere die .exe mit Code-Signing-Zertifikat
- Oder verwende Launcher stattdessen

## 📚 Weitere Dokumentation

- **EXE Build-Details:** [README_DISTRIBUTION.md](README_DISTRIBUTION.md)
- **Projekt-Hauptdokumentation:** [../README.md](../README.md)
- **Phase 1:** [../docs/PHASE1_PHOTO_SORT.md](../docs/PHASE1_PHOTO_SORT.md)
- **Phase 2:** [../docs/PHASE2_PHOTO_INTELLIGENCE.md](../docs/PHASE2_PHOTO_INTELLIGENCE.md)

## 🔗 Links

- **Repository:** https://github.com/AndreasTraut/media-organizer
- **PyInstaller Docs:** https://pyinstaller.org/
- **Streamlit Docs:** https://docs.streamlit.io/

---

**Entwickelt von:** Andreas Traut  
💼 [LinkedIn](https://www.linkedin.com/in/andreas-traut-89340/)  
💾 [GitHub Repository](https://github.com/AndreasTraut/media-organizer)
