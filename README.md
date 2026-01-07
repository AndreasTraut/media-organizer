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

1. [KI-gestützter Entwicklungsworkflow](#-ki-gestuetzter-entwicklungsworkflow)
2. [Projekt-Evolution: Feedback ist ein Geschenk](#-projekt-evolution-feedback-ist-ein-geschenk)
3. [Tech Stack](#-tech-stack)

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

Nach der Veröffentlichung erhielt ich folgenden wertvollen Kommentar aus der Community:

> *"Das nächste Level, und vor allem auch im BI Bereich die nächste '**Goldene Schaufel**', ist die **Unstrukturierte Datenanalyse**.*  
> 
> *Aus den 12k Bildern **Entitäten extrahieren** (was kann man im Hintergrund erkennen, **Gesichtsanalyse**, **Emotionale Zustände**, verschiedene Anlässe, etc.), um dann eine Analyse und Gruppierung zu ermöglichen.*  
>
> *Fragen wie: '**In welchen Bildern ist Person A vorhanden? Wie veränderte sich der emotionale Zustand der Person über das Jahr verteilt? Welche High- und Lowlights gab es?**' werden dann möglich.*  
>
> *Du kannst **Bilder auch in Embeddings umwandeln**, um eine direkte Verbindung mit LLMs zu ermöglichen. **Ein RAG auf Bilderbasis** wäre auch cool.*  
>
> *Du hast jetzt mit der Repo einmal die Basis von Data Cleaning. Die KI unterstützt dich im Workflow. Du hast alles, was du dafür brauchst! Viel Spaß!"*

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
| Emotionale Zustände | FER (Facial Expression Recognition) | `phase2_photo_intelligence/photo_insights.py` |
| Bilder in Embeddings umwandeln | CLIP-Embeddings + FAISS Vector-DB | `phase2_photo_intelligence/photo_rag.py` |
| RAG auf Bilderbasis | Semantische Suche + Kontext-Engine | `phase2_photo_intelligence/photo_rag.py` |
| LLM-Integration | GPT-4o Chat-Interface | `phase2_photo_intelligence/photo_rag.py` |

#### 🧠 Was ist neu?

**🔍 Semantische Suche (RAG-basiert) — `phase2_photo_intelligence/photo_rag.py`**

- **CLIP-Embeddings** ermöglichen Suche nach Inhalten statt nur Metadaten
- **FAISS Vector-DB** für schnelle Ähnlichkeitssuche in großen Sammlungen
- **Beispiel-Query:** *"Strand im Sommer"* → System findet passende Bilder ohne explizite Tags
- *# 🧠 Was ist neu?

**🔍 Semantische Suche (RAG-basiert) — `phase2_photo_intelligence/photo_rag.py`**

- **CLIP-Embeddings** ermöglichen Suche nach Inhalten statt nur Metadaten
- **FAISS Vector-DB** für schnelle Ähnlichkeitssuche in großen Sammlungen
- **Beispiel-Query:** *"Strand im Sommer"* → System findet passende Bilder ohne explizite Tags
- **LLM-Integration:** Interaktiver GPT-4o Chatbot
  - *"Zeige mir Fotos mit Familie aus 2024"*
  - Kontextuelles Verständnis der gesamten Bildersammlung

**🧑‍🔬 Deep Insights & Entity-Extraktion — `phase2_photo_intelligence/photo_insights.py`**

- **Gesichtserkennung (DeepFace):** Automatische Erkennung von Personen
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
python phase2_photo_intelligence/photo_insights.py --build-index

# Semantische Suche
python phase2_photo_intelligence/photo_rag.py --query "Strand im Sommer"

# Interaktiver Chat-Modus
python phase2_photo_intelligence/photo_rag.py --chat
```

➡️ **[🧠 Detaillierte Dokumentation: Phase 2 - Photo Intelligence](docs/PHASE2_PHOTO_INTELLIGENCE.md)**

---

## 🛠 Tech Stack

### Basis-Module (Photo Sort)

- **Sprache:** Python 3.x
- **Core Library:** [Pillow](https://pypi.org/project/pillow/) für EXIF-Metadaten-Parsing
- **Konfiguration:** python-dotenv für sichere Pfadverwaltung
- **Infrastruktur:** Optimiert für Windows-Netzwerkpfade zu NAS-Systemen (Synology)

### Intelligence-Module (Photo Intelligence)

- **CLIP-Embeddings:** OpenAI CLIP für semantische Bild-Text-Zuordnung
- **Vector Database:** FAISS für effiziente Ähnlichkeitssuche
- **Face Recognition:** DeepFace für Gesichtserkennung
- **LLM-Integration:** OpenAI GPT-4o für natürlichsprachliche Interaktion
- **Emotion Analysis:** FER (Facial Expression Recognition)




