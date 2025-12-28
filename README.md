# Media-Organizer: Von Big Data zu Smart Storage 📸

Dieses Projekt automatisiert die Sortierung von großen Bild- und Videomengen (z.B. Google Photos Takeout) in eine strukturierte Ordnerhierarchie auf einem **Synology NAS**.

![20251223_152623-COLLAGE](https://github.com/user-attachments/assets/131b96d2-a430-4163-baa1-adf2a62677c5)

## Über den Autor
**Andreas Traut** ist ein Senior BI-Entwickler, der sich auf Data Warehousing, SQL Server und Microsoft BI Stack spezialisiert hat. Dieses Projekt ist ein privates Beispiel dafür, wie KI-gesteuerte Entwicklung und Python reale Herausforderungen bei der Datenorganisation lösen können.

🔗 [Vernetze dich auf LinkedIn](https://www.linkedin.com/in/andreas-traut-89340/)

🔗 [Schaue dir weitere, interessante BI Umsetzungen an](https://github.com/AndreasTraut)

## 🛠 Tech Stack & Hintergrund
Als **Senior BI Developer** habe ich dieses Tool entwickelt, um eine robuste "Single Source of Truth" für mein privates Fotoarchiv zu schaffen. 

- **Sprache:** Python 3.x
- **Core Library:** [Pillow](https://pypi.org/project/pillow/) für EXIF-Metadaten-Parsing.
- **Infrastruktur:** Optimiert für Windows-Netzwerkpfade zu NAS-Systemen.

## 🚀 Key Features
- **EXIF-First Logik:** Nutzt den `DateTimeOriginal` Header für präzise Datierung.
- **Fallback-Mechanismus:** Erkennt heterogene Datenquellen (Videos, Collagen) via Dateisystem-Statistiken, falls keine EXIF-Daten vorliegen.
- **Redundanz-Fokus:** Ideal für die Vorbereitung von Backups auf redundanten Systemen (RAID).

## ⚙️ Installation
1. Repository klonen.
2. Abhängigkeiten installieren: `pip install -r requirements.txt`
3. `.env.example` kopieren nach `.env` und Pfade anpassen.
4. Skript ausführen: `python photo_sort.py`

Weitere Details zur Funktionsweise des Skriptes und eine Zeile-für-Zeile-Erklärung findest du in der separaten Dokumentation: [photo_sort.py — Detaillierte Erklärung](docs/PHOTO_SORT.md).

## 🤖 KI-gestützter Entwicklungsworkflow

Dieses Projekt enthält keine "KI‑Logik" im Laufzeitcode — das Skript ist bewusst leichtgewichtig und nutzt Standardbibliotheken. Der KI‑Aspekt bezieht sich auf den Entwicklungsprozess: Teile des Projektgerüsts, Modernisierungen (z. B. `pathlib` statt veralteter `os`‑Aufrufe), aktuelle Best‑Practices im Error‑Handling und Hilfs‑Boilerplate wurden mithilfe einer KI-Assistenz generiert. Vorteile:

- **Schneller Start:** Boilerplate und Vorschläge in Sekunden statt langem Suchen auf Foren.
- **Modernere Patterns:** Weniger Risiko, veraltete (z. B. Python‑2) Beispiele zu übernehmen.
- **Konzentration auf Review:** Der Entwickler prüft und verbessert den generierten Code statt alles von Grund auf zu schreiben.
- **Transferleistung & Training:** Dieses Projekt dient als Übungsumgebung ("Sandbox"), um KI-Workflows risikofrei zu testen. Ich wende hier professionelle Prinzipien (wie ETL-Prozesse und Datenbereinigung) auf ein privates Szenario an. Das Ziel: Routinen für den beruflichen Alltag schärfen und KI-Prompting-Strategien verfeinern.

Hinweis: KI ist Werkzeug, nicht Ersatz — Review, Tests und Sicherheitsprüfungen bleiben wichtig.

