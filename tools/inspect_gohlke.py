"""
inspect_gohlke.py

Zweck: Manuelles Debugging-Tool.
Es lädt den HTML-Quelltext der Webseite von Christoph Gohlke herunter und
filtert ihn nach Zeilen, die "dlib" enthalten.

Das ist hilfreich, wenn 'install_dlib_wheel.py' fehlschlägt, um zu prüfen:
1. Ist die Webseite erreichbar?
2. Hat sich die Struktur der Webseite geändert?
3. Welche dlib-Versionen (Wheel-Dateien) sind aktuell gelistet?
"""

import urllib.request

# Die URL zu den inoffiziellen Python-Binaries für Windows
URL = 'https://www.lfd.uci.edu/~gohlke/pythonlibs/'

print(f"Verbinde zu {URL} ...")

try:
    # 1. Webseite öffnen und Inhalt herunterladen
    # Wir nutzen urllib (Standard-Bibliothek), um keinen externen 'requests'-Zwang zu haben.
    response = urllib.request.urlopen(URL)
    
    # 2. Inhalt lesen und decodieren
    # .read() holt die Bytes.
    # .decode('utf-8', 'ignore') wandelt Bytes in String um und ignoriert unbekannte Zeichen,
    # damit das Skript nicht wegen eines unwichtigen Sonderzeichens abstürzt.
    html_content = response.read().decode('utf-8', 'ignore')

    # 3. Filtern nach 'dlib'
    # Wir zerlegen den HTML-Code in Zeilen (split) und behalten nur die,
    # die das Wort "dlib" (case-insensitive) enthalten.
    lines = [line for line in html_content.split('\n') if 'dlib' in line.lower()]

    # 4. Ergebnis ausgeben
    print(f'Gefundene Zeilen mit "dlib": {len(lines)}')
    print('-' * 40)

    # Wir geben die ersten 80 Treffer aus, damit die Konsole nicht geflutet wird.
    # Hier sollten Dateinamen wie "dlib-19.24.1-cp311-cp311-win_amd64.whl" auftauchen.
    for i, line in enumerate(lines[:80]):
        # .strip() entfernt Leerzeichen am Anfang/Ende der HTML-Zeile
        print(f"{i+1}: {line.strip()}")

except Exception as e:
    print(f"\n[FEHLER] Konnte Seite nicht laden: {e}")
    print("Mögliche Ursachen: Keine Internetverbindung oder Seite ist down/blockiert Skripte.")