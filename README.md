# Media-Organizer: Von Big Data zu Smart Storage 📸

**Data Engineering im Privaten:** Die Evolution vom einfachen Sortier-Skript zur intelligenten Photo Intelligence Suite – angetrieben durch Community-Feedback.

Dieses Projekt automatisiert die Sortierung von großen Bild- und Videomengen (z.B. Google Photos Takeout) in eine strukturierte Ordnerhierarchie auf einem **Synology NAS** und bietet erweiterte KI-basierte Analyse-Tools für semantische Suche, Gesichtserkennung und natürlichsprachliche Interaktion.

![20251223_152623-COLLAGE](https://github.com/user-attachments/assets/131b96d2-a430-4163-baa1-adf2a62677c5)


## 👨‍💻 Über den Autor

**Andreas Traut** ist ein Senior BI-Entwickler, der sich auf Data Warehousing, SQL Server und Microsoft BI Stack spezialisiert hat. Dieses Projekt ist ein privates Beispiel dafür, wie KI-gesteuerte Entwicklung und Python reale Herausforderungen bei der Datenorganisation lösen können.

🔗 [Vernetze dich auf LinkedIn](https://www.linkedin.com/in/andreas-traut-89340/)

🔗 [Schaue dir weitere, interessante BI Umsetzungen an](https://github.com/AndreasTraut)

---

## 📋 Inhaltsverzeichnis

1. [KI-gestützter Entwicklungsworkflow](#-ki-gestützter-entwicklungsworkflow)
   - [Zwei Ebenen der KI-Integration](#zwei-ebenen-der-ki-integration)
   - [Phase 1: Development-Time — KI als Entwicklungs-Werkzeug](#phase-1-development-time--ki-als-entwicklungs-werkzeug)
   - [Phase 2: Runtime — KI für intelligente Datenanalyse](#phase-2-runtime--ki-für-intelligente-datenanalyse)
   - [Die Philosophie](#die-philosophie)
2. [Projekt-Evolution: Feedback ist ein Geschenk](#-projekt-evolution-feedback-ist-ein-geschenk)
   - [Phase 1: Data Cleaning & Organisation (Dezember 2025)](#phase-1-data-cleaning--organisation-dezember-2025)
   - [Das Game-Changing Feedback](#-das-game-changing-feedback)
   - [Phase 2: Photo Intelligence Suite (Dezember 2025 - Januar 2026)](#phase-2-photo-intelligence-suite-dezember-2025---januar-2026)
3. [Tech Stack](#-tech-stack)
   - [Phase 1: Basis-Module (Photo Sort)](#phase-1-basis-module-photo-sort)
   - [Phase 2: Intelligence-Module (Photo Intelligence)](#phase-2-intelligence-module-photo-intelligence)
4. [🖥️ Streamlit GUI](#%EF%B8%8F-streamlit-gui---grafische-oberfl%C3%A4che)
5. [Tools & Hilfsskripte](TOOLS.md)
---

## 🤖 KI-gestützter Entwicklungsworkflow

### Zwei Ebenen der KI-Integration

Dieses Projekt demonstriert eindrucksvoll die Evolution der KI-Nutzung im modernen Software-Engineering – von der Entwicklungsunterstützung (Phase 1) bis zur intelligenten Laufzeit-Analyse (Phase 2). Während KI-Assistenten wie GitHub Copilot heute in der Softwareentwicklung, beim Prototyping von Datenbank-Abfragen und bei der Optimierung komplexer BI-Modelle zum Standard gehören, geht dieses Projekt einen Schritt weiter: Es nutzt KI nicht nur als Entwicklungswerkzeug, sondern integriert maschinelles Lernen direkt in die Anwendungslogik.

In meiner täglichen Arbeit als BI-Entwickler beschleunigt KI das Prototyping von SQL-Abfragen und ETL-Strecken erheblich, hilft bei der Optimierung von Tabular Models und automatisiert Routine-Tasks im Reporting – sodass mehr Zeit für strategische Datenfragen bleibt. Dieses private Projekt überträgt diese Erfahrungen auf eine neue Dimension: Hier wird KI zur Laufzeit eingesetzt, um unstrukturierte Bilddaten zu analysieren, semantische Zusammenhänge zu erkennen und natürlichsprachliche Interaktion zu ermöglichen.

### Phase 1: Development-Time — KI als Entwicklungs-Werkzeug

In **Phase 1** (`phase1_photo_sort/photo_sort.py`) wurde GitHub Copilot eingesetzt, um den Entwicklungsprozess zu beschleunigen: Modernisierte Code-Patterns, Best-Practices im Error-Handling und Boilerplate-Code entstanden in Sekunden statt Stunden. Das Skript selbst bleibt bewusst leichtgewichtig und nutzt nur Standardbibliotheken – KI wirkt hier ausschließlich als Entwicklungsassistent, nicht zur Laufzeit.

> ➡️ **Details siehe:** [Phase 1 in Projekt-Evolution](#phase-1-data-cleaning--organisation-dezember-2025)  
> 💼 **[LinkedIn Post 1: Data Engineering im Privaten](https://www.linkedin.com/posts/activity-7409246436468576257-6LvU)**  
> 💾 **Modul:** `phase1_photo_sort/photo_sort.py`  

### Phase 2: Runtime — KI für intelligente Datenanalyse

**Phase 2** (`phase2_photo_intelligence/`) markiert den Paradigmenwechsel: Hier wird KI **zur Laufzeit** eingesetzt. CLIP-Embeddings ermöglichen semantische Bildsuche, DeepFace und FER analysieren Gesichter und Emotionen, GPT-4o versteht natürlichsprachliche Queries, und FAISS orchestriert die Vector-Suche über 12.000+ Fotos. Die Evolution ist komplett: Von "KI hilft beim Programmieren" zu "KI analysiert meine Daten zur Laufzeit".

> ➡️ **Details siehe:** [Phase 2 in Projekt-Evolution](#phase-2-photo-intelligence-suite-dezember-2025---januar-2026)  
> 🚀 **LinkedIn Post 2: Die Evolution zur Intelligence Suite** (coming soon)  
> 💾 **Module:** `phase2_photo_intelligence/photo_insights.py` + `phase2_photo_intelligence/photo_rag.py`  


### Die Philosophie

> **"KI macht uns nicht arbeitslos, sie macht uns fähiger."**

Wer lernt, KI-Tools präzise zu steuern und mit einer soliden Infrastruktur zu kombinieren, steigert seinen Impact massiv – vom privaten Fotoalbum bis zum Enterprise Data Warehouse.




---



## 🌟 Projekt-Evolution: Feedback ist ein Geschenk

### Phase 1: Data Cleaning & Organisation (Dezember 2025)

> 💼 **[LinkedIn Post 1: Data Engineering im Privaten](https://www.linkedin.com/posts/activity-7409246436468576257-6LvU)**  
> 💾 **Modul:** `phase1_photo_sort/photo_sort.py`  
> 📖 **[Detaillierte Dokumentation: Phase 1 - Photo Sort](docs/PHASE1_PHOTO_SORT.md)**

**Das Problem:** 12.000 unsortierte Fotos aus Google Photos Takeout  
**Die Lösung:** `phase1_photo_sort/photo_sort.py` — Automatische Organisation nach Aufnahmedatum

#### 🤖 KI als Entwicklungs-Werkzeug

Das ursprüngliche Skript enthält **keine KI-Logik zur Laufzeit** – es ist bewusst leichtgewichtig und nutzt Standardbibliotheken (Pillow, pathlib). Der KI-Aspekt bezieht sich auf den **Entwicklungsprozess**:

Teile des Projektgerüsts, Modernisierungen (z.B. `pathlib` statt veralteter `os`-Aufrufe), aktuelle Best-Practices im Error-Handling und Hilfs-Boilerplate wurden mithilfe von **GitHub Copilot** generiert.

**Vorteile:**
- ✅ **Schneller Start:** Boilerplate und Vorschläge in Sekunden statt langem Suchen auf Foren
- ✅ **Modernere Patterns:** Weniger Risiko, veraltete (z.B. Python-2) Beispiele zu übernehmen
- ✅ **Konzentration auf Review:** Der Entwickler prüft und verbessert den generierten Code statt alles von Grund auf zu schreiben

> ⚠️ **Wichtig:** KI ist Werkzeug, nicht Ersatz — Review, Tests und Sicherheitsprüfungen bleiben essentiell.

#### 🚀 Key Features

- **EXIF-First Logik:** Nutzt den `DateTimeOriginal` Header für präzise Datierung
- **Fallback-Mechanismus:** Erkennt heterogene Datenquellen (Videos, Collagen) via Dateisystem-Statistiken
- **Redundanz-Fokus:** Ideal für die Vorbereitung von Backups auf redundanten Systemen (RAID)
- **Robuste Fehlerbehandlung:** Protokolliert Probleme, ohne den gesamten Prozess zu stoppen

#### ⚙️ Quick Start

```bash
# Abhängigkeiten installieren
pip install -r requirements-phase1.txt

# .env konfigurieren
cp .env.example .env
# Bearbeite .env: PHOTO_SOURCE und PHOTO_TARGET setzen

# Sortierung starten
python phase1_photo_sort/photo_sort.py
```

**Status:** ✅ Produktiv im Einsatz

---

### 💡 Das Game-Changing Feedback

Nach der Veröffentlichung erhielt ich [folgenden wertvollen Kommentar aus der Community](https://www.linkedin.com/feed/update/urn:li:activity:7409246436468576257?commentUrn=urn%3Ali%3Acomment%3A%28activity%3A7409246436468576257%2C7411139961678131200%29&dashCommentUrn=urn%3Ali%3Afsd_comment%3A%287411139961678131200%2Curn%3Ali%3Aactivity%3A7409246436468576257%29):

> *"Das nächste Level, und vor allem auch im BI Bereich die nächste '**Goldene Schaufel**', ist die **Unstrukturierte Datenanalyse**.*  
> 
> *Aus den 12k Bildern **Entitäten extrahieren** (was kann man im Hintergrund erkennen, **Gesichtsanalyse**, **Emotionale Zustände**, verschiedene Anlässe, etc.), um dann eine Analyse und Gruppierung zu ermöglichen.*  
>
> *Fragen wie: '**In welchen Bildern ist Person A vorhanden? Wie veränderte sich der emotionale Zustand der Person über das Jahr verteilt? Welche High- und Lowlights gab es?**' werden dann möglich.*  
>
> *Du kannst **Bilder auch in Embeddings umwandeln**, um eine direkte Verbindung mit LLMs zu ermöglichen. **Ein RAG auf Bilderbasis** wäre auch cool.*  
>
> *Du hast jetzt mit der Repo einmal die Basis von Data Cleaning. Die KI unterstützt dich im Workflow. Du hast alles, was du dafür brauchst! Viel Spaß!"*

<img width="535" height="564" alt="Kommentar aus der Community" src="https://github.com/user-attachments/assets/e52b0f4d-7ece-4765-b6a3-52eecf2c0a83" />     

**Challenge accepted! 🚀**

---

### Phase 2: Photo Intelligence Suite (Dezember 2025 - Januar 2026)

> 🚀 **LinkedIn Post 2: Die Evolution zur Intelligence Suite** (coming soon)  
> 💾 **Module:** `phase2_photo_intelligence/photo_insights.py` + `phase2_photo_intelligence/photo_rag.py`  
> 🧠 **[Detaillierte Dokumentation: Phase 2 - Photo Intelligence](docs/PHASE2_PHOTO_INTELLIGENCE.md)**

**Die Weiterentwicklung:** Aus einem einfachen Organizer wurde eine **modulare Photo Intelligence Engine** für unstrukturierte Datenanalyse – direkt inspiriert durch Community-Feedback.

#### 🤖 KI für intelligente Datenanalyse zur Laufzeit

Die Intelligence-Module nutzen KI **zur Laufzeit** für unstrukturierte Datenanalyse:

- **CLIP-Embeddings** für semantisches Bild-Verständnis
- **DeepFace + FER** für Gesichts- und Emotionserkennung
- **GPT-4o** für natürlichsprachliche Interaktion
- **FAISS** für effiziente Vector-Suche

**Die Evolution:** Von "KI hilft mir beim Programmieren" → "KI analysiert meine Daten zur Laufzeit"

#### Vom Feedback zur Feature-Liste

| Feedback-Anforderung | ✅ Implementierung | Modul |
|---------------------|-------------------|-------|
| Entitäten extrahieren | Face Recognition + Object Detection | `phase2_photo_intelligence/photo_insights.py` |
| Gesichtsanalyse | DeepFace Integration | `phase2_photo_intelligence/photo_insights.py` |
| **In welchen Bildern ist Person A?** | **Personensuche mit `--find-person` + `--copy-to`** | `phase2_photo_intelligence/photo_insights.py` |
| Emotionale Zustände | FER (Facial Expression Recognition) + Emotions-Filter (`--emotion`) | `phase2_photo_intelligence/photo_insights.py` |
| Bilder in Embeddings umwandeln | CLIP-Embeddings + FAISS Vector-DB | `phase2_photo_intelligence/photo_rag.py` |
| RAG auf Bilderbasis | Semantische Suche + Kontext-Engine | `phase2_photo_intelligence/photo_rag.py` |
| LLM-Integration | GPT-4o Chat-Interface | `phase2_photo_intelligence/photo_rag.py` |

#### 🧠 Was ist neu?

**🔍 Semantische Suche (RAG-basiert) — `phase2_photo_intelligence/photo_rag.py`**

- **CLIP-Embeddings** ermöglichen Suche nach Inhalten statt nur Metadaten
- **FAISS Vector-DB** für schnelle Ähnlichkeitssuche in großen Sammlungen
- **Beispiel-Query:** *"beach in summer"* → System findet passende Bilder ohne explizite Tags
- **LLM-Integration:** Interaktiver GPT-4o Chatbot
  - *"Zeige mir Fotos mit Familie aus 2024"*
  - Kontextuelles Verständnis der gesamten Bildersammlung

**🧑‍🔬 Deep Insights & Entity-Extraktion — `phase2_photo_intelligence/photo_insights.py`**

- **Gesichtserkennung (DeepFace):** Automatische Erkennung von Personen
- **Personensuche:** Finde alle Bilder mit bestimmten Personen (`--find-person`)
- **Bilder kopieren:** Gefundene Bilder automatisch in Personen-Ordner sortieren (`--copy-to`)
- **Emotionsanalyse (FER):** Erkennung von Gesichtsausdrücken (glücklich, traurig, neutral, etc.)
- **Timeline-Analysen:** Emotionaler Zustand von Personen über Zeit
- **Event-Detection:** High- und Lowlights automatisch identifizieren
- **Metadaten-Extraktion:** Erweiterte EXIF-Analyse und Geo-Location

**🛡️ Robustheit**

- Multi-Level Fallback-Logiken (EXIF → File-Stat → Heuristik)
- Unterstützung für heterogene Datenquellen (JPG, PNG, MP4, MOV)

#### ⚙️ Quick Start

```bash
# Erweiterte Abhängigkeiten installieren
pip install -r requirements-phase2.txt

# Index mit Metadaten, Gesichtern, Emotionen erstellen
python phase2_photo_intelligence/photo_insights.py --build-index --out insights_index.json

# Personensuche: Finde alle Bilder mit bestimmten Personen (nur JSON-Ausgabe)
python phase2_photo_intelligence/photo_insights.py --find-person --index-path insights_index.json

# Personensuche MIT Kopieren: Verwendet PHOTO_TARGET aus .env (empfohlen)
python phase2_photo_intelligence/photo_insights.py --find-person --use-target-from-env --threshold 0.85

# Personensuche MIT Kopieren: Expliziter Pfad
python phase2_photo_intelligence/photo_insights.py --find-person --copy-to "C:\Gefundene\Personen" --threshold 0.85

# Personensuche mit Emotions-Filter: Nur glückliche Momente
python phase2_photo_intelligence/photo_insights.py --find-person demo_bilder/known_faces --emotion happy --copy-to ausgabe

# Semantische Suche
python phase2_photo_intelligence/photo_rag.py --query "beach in summer"

# Interaktiver Chat-Modus
python phase2_photo_intelligence/photo_rag.py --chat
```



#### 🌟 Was jetzt möglich ist

Mit Phase 2 hat sich der media-organizer von einem reinen Sortier-Tool zu einer echten **Photo Intelligence Suite** entwickelt. Was früher mühsame manuelle Arbeit war — das Durchsuchen tausender Familienfotos nach bestimmten Personen oder Momenten — erledigt jetzt die KI in Sekunden.

**Personen wiederfinden:** Du fragst dich, auf welchen Bildern Oma zu sehen ist? DeepFace vergleicht Gesichter und liefert dir alle Treffer. Keine Tags nötig, keine Vorbereitung — einfach ein Referenzbild und los.

**Momente beschreiben:** Statt Dateinamen zu durchforsten, beschreibst du einfach, was du suchst: *"beach in summer"*, *"Geburtstagskuchen"*, *"Wanderung in den Bergen"*. CLIP versteht den Inhalt deiner Bilder und findet passende Treffer.

**Natürlich kommunizieren:** Im Chat-Modus unterhältst du dich mit deiner Bildersammlung. GPT-4o kombiniert deine Fragen mit den RAG-Ergebnissen und antwortet kontextuell: *"Die meisten Familienfotos aus 2024 wurden im August aufgenommen..."*


➡️ **[🧠 Detaillierte Dokumentation: Phase 2 - Photo Intelligence](docs/PHASE2_PHOTO_INTELLIGENCE.md)**


---

## �️ Streamlit GUI — Grafische Oberfläche

> 🎮 **[Detaillierte Dokumentation: Streamlit App](docs/APP.md)**  
> 💾 **Modul:** `app.py`  
> 🚀 **Quick Start:** `streamlit run app.py`

**Für alle, die ohne Code-Kenntnisse arbeiten möchten:** Eine browserbasierte GUI, die alle Phasen des media-organizer vereint.

### 🎯 Was kann die GUI?

**💻 Einfache Bedienung — wie eine normale Windows-Anwendung**

Statt Befehle in eine schwarze Kommandozeile zu tippen, öffnest du einfach deinen Browser (wie Chrome oder Firefox). Die App sieht aus wie eine moderne Webseite mit Buttons, Schiebereglern und Eingabefeldern — alles selbsterklärend.

**🏛️ Vier übersichtliche Bereiche (Tabs) für verschiedene Aufgaben:**

1. **📁 Fotos sortieren** — Du gibst zwei Ordner an: wo deine unsortierten Bilder liegen und wo sie hin sollen. Ein Klick auf "Sortierung starten" und fertig — das Tool organisiert alles nach Aufnahmedatum (z.B. 2024-12-25, 2025-01-15, etc.).

2. **🧠 Index aufbauen** — Hier analysiert die KI deine Bilder: Wer ist auf den Fotos? Welche Emotionen zeigen die Gesichter? Diese Informationen werden in einer Datei gespeichert, damit du später schnell suchen kannst.

3. **🔍 Personensuche** — Zeige der App ein paar Fotos von einer Person (z.B. Oma) und sie findet automatisch ALLE Bilder aus deiner Sammlung, auf denen diese Person zu sehen ist. Du kannst sogar nach Emotionen filtern: "Zeig mir nur die Bilder, wo Oma lacht."

4. **💬 Bilder beschreiben statt suchen** — Schreibe einfach, was du suchst: "Strand im Sommer" oder "rotes Auto" — und die KI findet passende Bilder, ohne dass du vorher mühsam Tags setzen musstest.

**⚙️ Einstellungen, die du selbst anpassen kannst:**

- **Genauigkeit einstellen:** Mit einem Schieberegler wählst du, wie genau eine Übereinstimmung sein soll (z.B. bei Gesichtserkennung: streng = weniger Fehler, locker = mehr Treffer)
- **Nach Stimmung filtern:** Wähle aus einer Liste: glücklich, traurig, wütend, neutral, etc.
- **Anzahl der Ergebnisse:** Bestimme, wie viele Bilder dir angezeigt werden sollen (z.B. nur die 10 besten Treffer)
- **Ordner auswählen:** Über normale Textfelder gibst du an, wo deine Bilder liegen

**📈 Du siehst sofort, was passiert:**

- **Fortschrittsbalken** zeigen dir, wie weit die Verarbeitung ist (wie beim Kopieren von Dateien in Windows)
- **Statistiken** nach Abschluss: "Gefunden: 23 Bilder von 3 Personen"
- **Fehlerprotokolle** falls etwas nicht klappt — in verständlicher Sprache, nicht in kryptischen Code-Meldungen

### 🚀 Quick Start

```bash
# 1. Streamlit installieren (falls noch nicht vorhanden)
pip install streamlit

# Oder alle GUI-Requirements:
pip install -r requirements-gui.txt

# 2. App starten
streamlit run app.py
```

Die App öffnet sich automatisch im Browser auf `http://localhost:8501`

### 🎯 Warum Streamlit?

- **Keine Web-Entwicklung nötig:** Reine Python-Datei, die sich in interaktive Webseiten verwandelt
- **Schnelles Prototyping:** Von Kommandozeile zu GUI in Minuten statt Tagen
- **Ideal für Data Science:** Perfekt für BI-Entwickler, die Dashboards statt CLI bevorzugen
- **Teilen ohne Installation:** Kann später auf Streamlit Cloud oder Server deployed werden

➡️ **[📚 Ausführliche Dokumentation mit Screenshots](docs/APP.md)**

---

## �🛠 Tech Stack

### Phase 1: Basis-Module (Photo Sort)

**Core Technologies:**
- **Sprache:** Python 3.8+
- **Bildverarbeitung:** [Pillow (PIL)](https://pypi.org/project/pillow/) — EXIF-Metadaten-Extraktion aus Bilddateien
  - Liest `DateTimeOriginal` EXIF-Tag für präzise Zeitstempel
  - Fallback auf Dateisystem-Metadaten (`st_mtime`) für Videos und Collagen
- **Pfadverwaltung:** `pathlib.Path` — Moderne, plattformübergreifende Pfad-Operationen
- **Konfiguration:** `python-dotenv` — Sichere Umgebungsvariablen-Verwaltung über `.env`-Dateien
- **Datei-Operationen:** `shutil` — Robuste Move/Copy-Operationen mit Fehlerbehandlung

**Infrastruktur:**
- Optimiert für Windows-Netzwerkpfade (UNC) zu NAS-Systemen (Synology)
- EXIF-First-Strategie mit intelligentem Fallback-Mechanismus
- Unterstützte Formate: `.jpg`, `.jpeg`, `.png`, `.tiff`, `.mp4`, `.mov`

**Dependencies:** Siehe [requirements-phase1.txt](requirements-phase1.txt)

---

### Phase 2: Intelligence-Module (Photo Intelligence)

**Deep Learning & Computer Vision:**
- **[CLIP](https://openai.com/research/clip) (openai/clip-vit-base-patch32)** — Contrastive Language-Image Pre-training
  - Text-zu-Bild-Embeddings im gemeinsamen 512-dimensionalen Vektorraum
  - Ermöglicht semantische Suche ohne manuelle Tags
  - Integration via [HuggingFace Transformers](https://huggingface.co/docs/transformers/)
- **[DeepFace](https://github.com/serengil/deepface)** — State-of-the-Art Face Recognition Framework
  - Unterstützt mehrere Modelle: VGG-Face, Facenet, ArcFace
  - Face-Embeddings für Personen-Matching mit konfigurierbarem Threshold
  - Automatische Gesichts-Detection und -Alignment
- **[FER](https://github.com/justinshenk/fer)** — Facial Expression Recognition
  - Emotionsklassifikation: `happy`, `sad`, `angry`, `neutral`, `surprise`, `fear`, `disgust`
  - Konfidenz-Scores pro erkannter Emotion

**Vector Database & Search:**
- **[FAISS](https://github.com/facebookresearch/faiss)** (Facebook AI Similarity Search)
  - Hochperformante Nearest-Neighbor-Suche in Millionen von Embeddings
  - `IndexFlatIP` für Cosine-Similarity (Inner Product nach L2-Normalisierung)
  - Effiziente Speicherung via `faiss.write_index()` / `faiss.read_index()`

**LLM & Natural Language:**
- **[OpenAI GPT-4o](https://platform.openai.com/docs/)** — Interaktiver Chat-Modus
  - RAG-basierte Kontext-Anreicherung (Retrieval-Augmented Generation)
  - Natürlichsprachliche Queries: *"Zeige mir Fotos mit Familie aus 2024"*
  - System-Prompt für domänenspezifisches Verständnis der Bildersammlung

**Backend & Processing:**
- **[PyTorch](https://pytorch.org/)** — Deep Learning Framework als Backend für CLIP
- **NumPy** — Numerische Berechnungen und Vektor-Operationen
- **[Pillow](https://pillow.readthedocs.io/)** — Bild-Loading und EXIF-Metadaten-Extraktion

**Data Persistence:**
- **JSON** — Index-Speicherung für Metadaten, Gesichter, Emotionen (`insights_index.json`)
- **FAISS Binary** — Optimierte Vector-DB (`photo_vectors.faiss`)
- **Mapping-JSON** — Rückübersetzung Vektor-Indizes zu Dateipfaden (`photo_vectors_mapping.json`)

**Dependencies:** Siehe [requirements-phase2.txt](requirements-phase2.txt)

**Performance:**
- Index-Aufbau: ~1-2 Min pro 1.000 Bilder
- Empfohlener RAM: 8GB+ (abhängig von Sammlungsgröße)
- GPU-Unterstützung optional (CPU-Modus funktioniert für kleinere Sammlungen)




