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

> 📦 **Implementierung:** Siehe [install_dlib_wheel.py](install_dlib_wheel.py)

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

> 📦 **Implementierung:** Siehe [fetch_demo_pictures.py](fetch_demo_pictures.py)

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

> 📦 **Implementierung:** Siehe [fetch_scene_images.py](fetch_scene_images.py)

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

> 📦 **Implementierung:** Siehe [inspect_index.py](inspect_index.py)

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

> 📦 **Implementierung:** Siehe [inspect_gohlke.py](inspect_gohlke.py)

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

### 5. Entwicklungsumgebung mit DevContainer (Optional, aber empfohlen)

#### Was ist ein DevContainer?

Ein **DevContainer** ist eine standardisierte Entwicklungsumgebung basierend auf Docker, die direkt in VS Code und GitHub Codespaces funktioniert. Er definiert das komplette Setup (Python-Version, Dependencies, Tools) in einer Konfigurationsdatei.

#### Warum DevContainer nutzen?

Warum DevContainer für dieses Projekt ein Game-Changer sind
Für den Media Organizer bietet der Einsatz von DevContainers entscheidende Vorteile, die weit über reine Bequemlichkeit hinausgehen. Die größte Herausforderung bei diesem Projekt liegt in den komplexen Abhängigkeiten der "Phase 2" (KI-Analyse). Bibliotheken wie DeepFace, FAISS und insbesondere dlib benötigen unter Windows oft eine aufwändige manuelle Einrichtung von C++ Build Tools und CMake. Ohne diese Vorarbeit scheitert die Installation häufig.

Der DevContainer löst dieses Problem radikal, indem er eine standardisierte Linux-Umgebung bereitstellt, in der diese Pakete nahtlos funktionieren. Das eliminiert die technische Einstiegshürde komplett: Es ist keine lokale Konfiguration von Compilern oder Python-Pfaden nötig.

Zudem öffnet dies das Projekt für eine breitere Community (z.B. Tester von LinkedIn). Durch die Integration mit GitHub Codespaces lässt sich die gesamte Anwendung mit einem einzigen Klick direkt im Browser starten. Anstatt 30 Minuten oder mehr mit der Fehlersuche bei der Installation zu verbringen, ist das System innerhalb von etwa zwei Minuten voll einsatzbereit. Dies garantiert absolute Reproduzierbarkeit: Egal ob auf einem lokalen Windows-PC, einem Mac oder in der Cloud – jeder Nutzer hat exakt dieselbe, funktionierende Umgebung.

#### Wie nutzen?

**Variante A: In GitHub Codespaces (Cloud-basiert)**

**1. Repository aufrufen**
Das Projekt-Repository auf der GitHub-Webseite öffnen.

**2. Codespace erstellen**
Die grüne Schaltfläche **Code** betätigen, zum Reiter **Codespaces** wechseln und die Option **Create codespace on main** auswählen.

**3. Initialisierung abwarten**
Der Cloud-Container wird automatisch bereitgestellt und konfiguriert. Dieser Vorgang nimmt ca. 2-3 Minuten in Anspruch.

**4. Anwendung nutzen**
Nach Abschluss der Installation startet die Streamlit-App automatisch und öffnet sich in einem neuen Browser-Tab oder im Vorschaufenster.

```powershell
# Keine Installation nötig! Alles automatisch.
# Nach Container-Start ist die App unter Port 8501 erreichbar
```

**Variante B: Lokal mit VS Code Dev Containers Extension**

Diese Methode empfiehlt sich für eine persistente lokale Entwicklungsumgebung, um Versionskonflikte zu vermeiden und die manuelle Konfiguration von Abhängigkeiten überflüssig zu machen.

**1. Installation von Docker Desktop**
Docker fungiert als Laufzeitumgebung für den Container.

* **Docker Desktop für Windows** von der [offiziellen Website](https://www.docker.com/products/docker-desktop/) herunterladen und installieren.
* **Wichtig:** Während der Installation sicherstellen, dass die Option zur Verwendung des **WSL 2** (Windows Subsystem for Linux) Backends aktiviert ist. Dies ist entscheidend für Performance und Kompatibilität.
* Docker Desktop nach der Installation starten, um die Aktivität des Dienstes zu prüfen.

**2. Installation der "Dev Containers" Erweiterung**
Diese Erweiterung ermöglicht VS Code die Interaktion mit der Docker-Umgebung.

* VS Code öffnen.
* Zur **Erweiterungs-Leiste** (Symbol mit vier Quadraten in der linken Leiste) navigieren oder den Shortcut `Strg+Shift+X` nutzen.
* Nach `Dev Containers` suchen.
* Die offizielle Erweiterung von **Microsoft** (ID: `ms-vscode-remote.remote-containers`) installieren.

**3. Projekt laden**

* In VS Code `Datei` → `Ordner öffnen...` wählen.
* Zum geklonten Projektverzeichnis `media-organizer` navigieren und dieses öffnen.

**4. Umgebung initialisieren (Reopen in Container)**
Dieser Schritt weist VS Code an, die definierte Container-Umgebung anstelle des lokalen Windows-Systems zu verwenden.

* Die Befehlspalette mit `F1` (oder `Strg+Shift+P`) öffnen.
* Den Befehl `Dev Containers: Reopen in Container` eingeben und mit Enter bestätigen.
* *(Hinweis: VS Code erkennt die Konfigurationsdateien oft automatisch und bietet unten rechts ein Pop-up mit der Option "Reopen in Container" an).*

**5. Initialer Build-Prozess**
Beim ersten Start wird das Docker-Image erstellt und die Umgebung konfiguriert.

* **Dauer:** Dieser Vorgang beinhaltet den Download und die Installation aller Systembibliotheken sowie Python-Pakete (DeepFace, PyTorch etc.) und kann initial 5 bis 10 Minuten in Anspruch nehmen.
* **Status:** Der Fortschritt lässt sich über den Link "Show Log" im Benachrichtigungsfenster verfolgen.
* Sobald das integrierte Terminal in VS Code eingabebereit ist, ist die Installation abgeschlossen und die Umgebung einsatzbereit.

```powershell
# Container baut sich automatisch mit allen Dependencies
# .devcontainer/devcontainer.json definiert das Setup
```

#### Was passiert im DevContainer?

Der Container führt automatisch folgende Schritte aus:

```json
// Aus .devcontainer/devcontainer.json

// 1. Python 3.11 Base Image laden
"image": "mcr.microsoft.com/devcontainers/python:1-3.11-bookworm"

// 2. Alle Dependencies installieren (Phase 1 + 2 + GUI)
"updateContentCommand": "pip3 install --user -r requirements-gui.txt"

// 3. Streamlit App automatisch starten
"postAttachCommand": "streamlit run app.py --server.headless true"

// 4. Port 8501 automatisch weiterleiten
"forwardPorts": [8501]
```

**Resultat:**
- ✅ Python 3.11 installiert
- ✅ Alle Dependencies aus `requirements-gui.txt` installiert (inkl. DeepFace, FAISS, CLIP)
- ✅ Streamlit-App läuft auf Port 8501
- ✅ VS Code Extensions (Python, Pylance, Jupyter) aktiviert
- ✅ Git konfiguriert für Commits

#### Wann solltest du DevContainer nutzen?

**Nutze DevContainer, wenn:**
- ✅ Du unter **Windows** entwickelst (vermeidet dlib-Kompilierung)
- ✅ Du das Projekt **jemandem zeigen** willst (Codespaces = 1-Klick-Demo)
- ✅ Du **schnell starten** willst ohne Dependencies manuell zu installieren
- ✅ Du **mehrere Projekte** hast und Versions-Konflikte vermeiden willst

**Nutze lokale Installation, wenn:**
- ⚠️ Du kein Docker installieren kannst/willst
- ⚠️ Du sehr limitierte Internet-Bandbreite hast (Container-Download ~2GB)
- ⚠️ Du bereits ein funktionierendes lokales Setup hast

#### Typischer DevContainer-Workflow

```powershell
# 1. Repository klonen
git clone https://github.com/AndreasTraut/media-organizer.git
cd media-organizer

# 2. In VS Code öffnen
code .

# 3. DevContainer starten (F1 → "Reopen in Container")
# ... Container baut sich ...
# ... Dependencies werden installiert ...
# ... Streamlit startet automatisch ...

# 4. Browser öffnet sich mit Streamlit-GUI auf http://localhost:8501
# ✅ Fertig! Keine manuelle Installation nötig.
```

**Debugging im DevContainer:**

```powershell
# Terminal im Container öffnen (automatisch in VS Code verfügbar)
# Hier kannst du normale Python-Befehle ausführen:

python phase2_photo_intelligence/photo_insights.py --build-index
python tools/fetch_demo_pictures.py
```

---

## 📋 Abhängigkeiten

Die Skripte nutzen größtenteils Python-Standard-Bibliotheken (`urllib`, `json`, `subprocess`).

**Ausnahme:** Die `fetch_`-Skripte benötigen folgende Pakete:

```powershell
pip install scikit-learn numpy Pillow requests
```


