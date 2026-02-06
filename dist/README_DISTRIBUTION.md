# Media Organizer - Executable Distribution

Diese Dokumentation beschreibt, wie die ausführbare .exe-Datei für Media Organizer erstellt und verwendet wird.

## 📦 Inhalt des Ordners

```
dist/
├── build_exe.py              # Build-Skript für PyInstaller
├── README_DISTRIBUTION.md    # Diese Datei
├── output/                   # Generierte .exe-Dateien (nach Build)
│   └── MediaOrganizer.exe
├── build/                    # Temporäre Build-Dateien (ignoriert)
└── MediaOrganizer.spec       # PyInstaller Konfiguration (generiert)
```

## 🛠️ EXE erstellen

### Voraussetzungen

1. **Python 3.12+** installiert
2. **Alle Dependencies** installiert:
   ```bash
   pip install -r requirements-gui.txt
   pip install pyinstaller
   ```

### Build-Prozess

```bash
# Im Repository-Root ausführen:
python dist/build_exe.py
```

Der Build-Prozess:
- ✅ Erstellt eine einzelne .exe-Datei (`--onefile`)
- ✅ Ohne Konsolen-Fenster (`--windowed`)
- ✅ Inkludiert alle Python-Module und Dependencies
- ✅ Bindet notwendige Daten-Dateien ein (.env.example, README.md)
- ✅ Ausgabe: `dist/output/MediaOrganizer.exe`

**Build-Dauer:** Ca. 5-15 Minuten (je nach Hardware)

## 🚀 EXE verwenden

### Starten der Anwendung

```bash
# Doppelklick auf die .exe ODER:
.\dist\output\MediaOrganizer.exe
```

Die Streamlit-GUI startet automatisch im Standard-Browser.

### ⚠️ Wichtige Hinweise

1. **Erste Ausführung kann langsam sein**
   - Die .exe entpackt beim ersten Start alle Module in einen temporären Ordner
   - Nachfolgende Starts sind schneller

2. **.env-Datei benötigt**
   - Erstelle eine `.env`-Datei im selben Ordner wie die .exe
   - Verwende `.env.example` als Vorlage
   - Setze Pfade zu deinen Foto-Ordnern

3. **Firewall/Antivirus**
   - Erste Ausführung kann Firewall-Warnung auslösen
   - Dies ist normal für selbst-erstellte .exe-Dateien
   - Erlaube den Zugriff für Streamlit (Port 8501)

4. **Python-Runtime erforderlich**
   - Die .exe ist **NICHT vollständig standalone**
   - Python 3.12+ muss auf dem Ziel-System installiert sein
   - Alternative: Verwende `--onefile` mit embedded Python (komplexer)

## 📋 Datei-Größe

Die .exe ist relativ groß (ca. 500 MB - 1.5 GB), weil sie enthält:
- Streamlit Framework
- PyTorch + CLIP
- DeepFace + Computer Vision Libraries
- TensorFlow/Keras
- FAISS Vector-DB

**Tipp:** Für kleinere .exe nur benötigte Module importieren.

## 🐛 Troubleshooting

### Problem: "Failed to execute script"

**Lösung:**
- Führe .exe im Terminal aus, um Fehler zu sehen:
  ```bash
  .\MediaOrganizer.exe
  ```
- Prüfe Logs in: `%TEMP%\_MEI*\`

### Problem: "Module not found"

**Lösung:**
- Prüfe `--hidden-import` in `build_exe.py`
- Füge fehlendes Modul hinzu und rebuild

### Problem: Streamlit startet nicht

**Lösung:**
- Prüfe ob Port 8501 frei ist
- Firewall/Antivirus deaktivieren (temporär)
- .env-Datei korrekt?

### Problem: .exe zu groß

**Lösung:**
- Nutze `--onedir` statt `--onefile` (mehrere Dateien, schneller)
- Entferne nicht benötigte Dependencies (z.B. nur Phase 1)
- Nutze virtuelle Umgebung mit minimalen Packages

## 🔒 Sicherheit

**WICHTIG für Distribution:**

1. **Keine Secrets in .exe einbetten**
   - ❌ NICHT `.env` mit Passwörtern einbinden
   - ✅ Nutzer müssen eigene `.env` erstellen
   
2. **Code Signing** (optional, aber empfohlen)
   - Windows Defender könnte unsigned .exe blockieren
   - Signiere die .exe mit Zertifikat für Vertrauen

3. **Virus-Scanner können False Positives melden**
   - PyInstaller .exe werden oft als "suspicious" markiert
   - Submit to VirusTotal vor Verteilung

## 🎯 Alternative: Portable Version

Für einfachere Distribution kann man auch verwenden:

```bash
# Erstelle portable Ordner-Struktur (kein --onefile)
pyinstaller --name=MediaOrganizer \
            --onedir \
            --windowed \
            app.py
```

Vorteile:
- Schnellere Starts (kein Entpacken)
- Kleinerer Download (komprimierbar)
- Einfacheres Debugging

## 📚 Weiterführende Links

- [PyInstaller Dokumentation](https://pyinstaller.org/)
- [Streamlit Deployment Guide](https://docs.streamlit.io/deploy)
- [Windows Code Signing](https://learn.microsoft.com/en-us/windows/win32/seccrypto/cryptography-tools)

---

**Entwickelt von:** Andreas Traut  
💼 [LinkedIn](https://www.linkedin.com/in/andreas-traut-89340/)  
💾 [GitHub Repository](https://github.com/AndreasTraut/media-organizer)
