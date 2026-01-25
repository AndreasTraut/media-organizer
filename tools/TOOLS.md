# Tools — Hilfsskripte für media-organizer

Dieses Verzeichnis enthält Utility-Skripte für die Installation von Abhängigkeiten, das Beschaffen von Testdaten und das Debugging der Anwendung.

## 📑 Inhaltsverzeichnis

1.  **Setup & Installation**
    * [📦 install_dlib_wheel.py](#-install_dlib_wheelpy) – Automatische dlib-Installation für Windows.
2.  **Datenbeschaffung (Demo)**
    * [📸 fetch_demo_pictures.py](#-fetch_demo_picturespy) – Lädt legale Testbilder (LFW-Datensatz) für Gesichtserkennung.
    * [🌄 fetch_scene_images.py](#-fetch_scene_imagespy) – Lädt Szenen-Bilder (Strand, Auto, etc.) für semantische Suche.
3.  **Analyse & Tests**
    * [🔍 inspect_index.py](#-inspect_indexpy) – Prüft den generierten JSON-Index auf Gesichter und Metadaten.
4.  **Low-Level Debugging**
    * [🌐 inspect_gohlke.py](#-inspect_gohlkepy) – Hilft beim manuellen Suchen von Wheel-Dateien.
5.  **Anleitungen**
    * [🚀 Typischer Workflow](#-typischer-workflow)
    * [📋 Abhängigkeiten](#-abhängigkeiten)

---

## 📦 `install_dlib_wheel.py`

**Zweck:**
Automatische Installation von `dlib` unter Windows durch Download der passenden Wheel-Datei von [Christoph Gohlkes Unofficial Binaries](https://www.lfd.uci.edu/~gohlke/pythonlibs/).

**Das Problem:**
Unter Windows schlägt `pip install dlib` oft fehl, da C++ Build Tools und CMake fehlen. Dieses Skript umgeht das Kompilieren durch fertige Binaries.

**Verwendung:**
```powershell
.\.venv\Scripts\Activate.ps1
python tools/install_dlib_wheel.py

```

---

## 📸 `fetch_demo_pictures.py`

**Zweck:**
Erstellung einer legalen, reproduzierbaren Demo-Umgebung unter Verwendung des wissenschaftlichen Datensatzes "Labeled Faces in the Wild" (LFW).

**Besonderheit:**
Das Skript simuliert einen realistischen Anwendungsfall, indem es Referenzbilder von unbekannten Bildern trennt und Dateinamen im Chaos-Ordner verschleiert.

**Verwendung:**

```powershell
python tools/fetch_demo_pictures.py

```

**Ergebnis (Ordnerstruktur):**

```text
demo_bilder/
├── known_faces/       # Referenz-Bilder (zum Lernen)
│   ├── George_W_Bush/
│   │   └── George_W_Bush_1.jpg  (Max 10 Stück)
│   └── ...
└── alle_bilder/       # Chaos-Ordner (zum Sortieren)
    ├── IMG_4f9a2b.jpg           (Enthält ALLE Bilder, aber anonymisiert)
    ├── IMG_1x2y3z.jpg
    └── ...

```

**Wann nutzen:**

* Um `photo_insights.py` (Gesichtserkennung) zu testen.
* Um zu beweisen, dass die KI Gesichter anhand des Bildinhalts erkennt (und nicht anhand des Dateinamens).

---

## 🌄 `fetch_scene_images.py`

**Zweck:**
Erweiterung des Demo-Datensatzes um allgemeine Szenen und Objekte (z.B. Strand, Berge, Autos, Hunde), um die **semantische Suche** (`photo_rag.py`) zu testen.

**Besonderheit:**
Das Skript nutzt LoremFlickr, um lizenzfreie Testbilder (Creative Commons) zu laden. Die Dateinamen werden ebenfalls anonymisiert (`IMG_xyz.jpg`), damit die KI den Bildinhalt visuell analysieren muss (CLIP-Embedding).

**Verwendung:**

```powershell
python tools/fetch_scene_images.py

```

**Was passiert:**

1. Lädt Bilder für Kategorien wie "beach", "car", "dog" herunter.
2. Speichert sie direkt in den gemeinsamen Chaos-Ordner `demo_bilder/alle_bilder` (mischt sie mit den Gesichtern).
3. Erstellt eine Log-Datei `demo_bilder/SCENES_LOG.txt` zur Kontrolle.

**Wann nutzen:**

* Wenn du die Text-zu-Bild Suche ("Zeige mir einen Strand") testen willst.
* Als Ergänzung zu `fetch_demo_pictures.py`, um einen gemischten Datensatz zu erhalten.

---

## 🔍 `inspect_index.py`

**Zweck:**
Analyse und Debugging des generierten `insights_index.json` mit Statistiken und Beispielen.

**Verwendung:**

```powershell
# Nach dem Index-Aufbau ausführen
python tools/inspect_index.py

```

**Was wird analysiert:**

* Gesamtanzahl indizierter Bilder.
* Anzahl Bilder mit erkannten Gesichtern & Emotionen.
* Stichprobenartige Suche nach Personennamen.
* Ausgabe von Beispiel-Metadaten (Embeddings, Face-Locations).

---

## 🌐 `inspect_gohlke.py`

**Zweck:**
Manuelle Inspektion der Gohlke-Website nach verfügbaren `dlib`-Wheels, falls das automatische Installations-Skript fehlschlägt.

**Verwendung:**

```powershell
python tools/inspect_gohlke.py

```

**Wann nutzen:**

* Wenn `install_dlib_wheel.py` kein passendes Wheel findet.
* Um zu prüfen, ob es Wheels für ganz neue Python-Versionen (z.B. 3.12/3.13) gibt.

---

## 🚀 Typischer Workflow

Dies ist die empfohlene Reihenfolge, um das Projekt frisch aufzusetzen und zu testen:

### 1. Installation (Nur Windows)

Zuerst die schwierige `dlib`-Abhängigkeit lösen:

```powershell
python tools/install_dlib_wheel.py

```

### 2. Demo-Daten holen

Wir laden neutrale Testdaten (Gesichter UND Szenen), statt private Bilder zu nutzen:

```powershell
python tools/fetch_demo_pictures.py  # Holt Gesichter
python tools/fetch_scene_images.py   # Holt Szenen (Strand, Auto...)

```

### 3. Index aufbauen (Chaos-Ordner scannen)

Wir indizieren den Ordner `alle_bilder` (wo alle Dateinamen anonymisiert sind):

```powershell
# Metadaten-Index
python phase2_photo_intelligence/photo_insights.py --build-index --source "./demo_bilder/alle_bilder"

# Vektor-Datenbank (für semantische Suche)
python phase2_photo_intelligence/photo_rag.py --build-vector-db --source "./demo_bilder/alle_bilder"

```

### 4. Suchen & Sortieren

Wir nutzen den Ordner `known_faces` als Vorlage oder suchen nach Begriffen:

```powershell
# Gesichtserkennung
python phase2_photo_intelligence/photo_insights.py --find-person "./demo_bilder/known_faces"

# Semantische Suche
python phase2_photo_intelligence/photo_rag.py --query "beach in summer" --top-k 5

```

---

## 📋 Abhängigkeiten

Die Skripte nutzen größtenteils Python-Standard-Bibliotheken (`urllib`, `json`, `subprocess`).

**Ausnahme:** Die `fetch_`-Skripte benötigen folgende Pakete:

```powershell
pip install scikit-learn numpy Pillow requests
```


