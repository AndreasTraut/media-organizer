# Tools — Hilfsskripte für media-organizer

Dieses Verzeichnis enthält Utility-Skripte für Installation, Debugging und Analyse.

---

## 📦 `install_dlib_wheel.py`

**Zweck:** Automatische Installation von `dlib` unter Windows durch Download der passenden Wheel-Datei von [Christoph Gohlkes Unofficial Binaries](https://www.lfd.uci.edu/~gohlke/pythonlibs/).

**Problem:** Unter Windows schlägt die normale `pip install dlib` Installation oft fehl, da CMake und Visual Studio Build Tools erforderlich sind. Dieses Script umgeht das Problem durch vorgefertigte Wheel-Dateien.

**Verwendung:**
```powershell
# Aktiviere die venv
.\.venv\Scripts\Activate.ps1

# Führe das Script aus
python tools/install_dlib_wheel.py
```

**Was passiert:**
1. Erkennt Python-Version und Architektur (z.B. `cp39-win_amd64`)
2. Lädt die Gohlke-Seite herunter und sucht passendes Wheel
3. Lädt Wheel in temporären Ordner
4. Installiert via `pip install <wheel>`
5. Installiert anschließend `face_recognition`

**Ausgabe:**
- ✅ Erfolg: "Success: dlib and face_recognition should now be installed."
- ❌ Fehler: Exit-Codes 2-5 mit Fehlermeldung

**Wann nutzen:**
- Bei fehlendem CMake/Build-Tools unter Windows
- Wenn `pip install face_recognition` mit Build-Fehler abbricht
- Für schnelle dlib-Installation ohne Compiler-Setup

---

## 🔍 `inspect_index.py`

**Zweck:** Analyse und Debugging des generierten `insights_index.json` mit Statistiken und Beispielen.

**Verwendung:**
```powershell
# Nach dem Index-Aufbau ausführen
python tools/inspect_index.py
```

**Was wird analysiert:**
- Gesamtanzahl indizierter Bilder
- Anzahl Bilder mit erkannten Gesichtern
- Anzahl Bilder mit Emotions-Daten
- Treffer für "Person1" und "Person2" (Beispiel-Suche)
- Beispiel-Metadaten der ersten 5 Bilder mit Gesichtern

**Beispiel-Ausgabe:**
```
total: 156
with_faces: 45
with_emotions: 45
Person1 matches: 8
['C:\\Fotos\\Sortiert\\Portraits Person1 2025\\PXL_20230701_090051515.jpg',
 'C:\\Fotos\\Sortiert\\Portraits Person1 2025\\PXL_20250308_081856206.jpg',
 ...]
Person2 matches: 14
['C:\\Fotos\\Sortiert\\Portraits Person2 2025\\COLOR_POP.jpg',
 ...]

Examples (up to 5) with `faces` metadata:
----------------------------------------
C:\Fotos\Sortiert\...\bild.jpg
{'emotions': [{'angry': 0.01, 'happy': 0.95, ...}],
 'faces': [{'encodings': [...], 'locations': [...]}]}
```

**Wann nutzen:**
- Nach Index-Aufbau zur Qualitätskontrolle
- Debugging bei Problemen mit Gesichtserkennung
- Überprüfung, ob bekannte Personen erkannt wurden
- Analyse der Index-Struktur vor eigenen Erweiterungen

---

## 🌐 `inspect_gohlke.py`

**Zweck:** Manuelle Inspektion der Gohlke-Website nach verfügbaren `dlib`-Wheels.

**Verwendung:**
```powershell
python tools/inspect_gohlke.py
```

**Was passiert:**
1. Lädt HTML von https://www.lfd.uci.edu/~gohlke/pythonlibs/
2. Filtert alle Zeilen, die "dlib" enthalten
3. Zeigt die ersten 80 Treffer

**Beispiel-Ausgabe:**
```
found 12
1 <a href="/~gohlke/pythonlibs/dlib-19.24.0-cp39-cp39-win_amd64.whl">dlib-19.24.0-cp39-cp39-win_amd64.whl</a>
2 <a href="/~gohlke/pythonlibs/dlib-19.24.0-cp310-cp310-win_amd64.whl">dlib-19.24.0-cp310-cp310-win_amd64.whl</a>
...
```

**Wann nutzen:**
- Wenn `install_dlib_wheel.py` kein passendes Wheel findet
- Zur manuellen Überprüfung verfügbarer Versionen
- Debugging bei Download-Problemen
- Vor manuellem Download, um verfügbare Python-Versionen zu sehen

---

## 🚀 Typischer Workflow

### Neu-Installation unter Windows:

1. **dlib installieren:**
   ```powershell
   python tools/install_dlib_wheel.py
   ```

2. **Index aufbauen:**
   ```powershell
   python phase2_photo_intelligence/photo_insights.py --build-index --out insights_index.json
   ```

3. **Index inspizieren:**
   ```powershell
   python tools/inspect_index.py
   ```

### Debugging bei Installations-Problemen:

1. **Verfügbare Wheels prüfen:**
   ```powershell
   python tools/inspect_gohlke.py
   ```

2. **Manuell installieren:**
   - Passende Wheel-Datei von der Gohlke-Website herunterladen
   - `pip install <pfad-zur-wheel-datei>`

---

## 📋 Abhängigkeiten

Alle Tools benötigen nur Python-Standard-Libraries:
- `urllib.request` — Web-Downloads
- `json` — JSON-Parsing
- `subprocess` — pip-Aufrufe
- `ssl`, `tempfile`, `platform`, `re` — System-Utilities

Keine zusätzlichen pip-Pakete erforderlich ✅

---

## 💡 Hinweise

- **inspect_index.py** erwartet `insights_index.json` im Root des Repositories
- **install_dlib_wheel.py** funktioniert nur unter Windows (nutzt `win_amd64`/`win_arm64` Tags)
- Bei Problemen mit SSL-Zertifikaten siehe Python-Dokumentation zu `ssl.create_default_context()`
