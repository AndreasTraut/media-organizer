"""
Downloads a suitable dlib wheel from Christoph Gohlke's unofficial binaries
and installs it into the active venv. Prints progress and final status.

Zweck: Dieses Skript automatisiert die schwierige dlib-Installation unter Windows.
Es sucht auf der Webseite von Christoph Gohlke nach einer vor-kompilierten
Wheel-Datei (.whl), die genau zur aktuellen Python-Version und Architektur passt.
Related Files:
- requirements-phase2.txt (Enthält dlib und face_recognition Dependencies)
- tools/inspect_gohlke.py (Debugging bei Fehlern)
- phase2_photo_intelligence/photo_insights.py (Nutzt DeepFace/dlib für Gesichtserkennung)"""
import sys
import sysconfig
import platform
import re
import urllib.request
import ssl
import os
import tempfile
import subprocess

# URL zu den inoffiziellen Windows-Binaries (Gohlke)
GOLKLE_URL = "https://www.lfd.uci.edu/~gohlke/pythonlibs/"

def py_tag():
    """
    Ermittelt das Python-Versions-Tag des aktuellen Interpreters.
    Beispiel: Python 3.9 -> 'cp39', Python 3.11 -> 'cp311'.
    Dies wird benötigt, um die richtige Wheel-Datei auszuwählen.
    """
    vi = sys.version_info
    return f"cp{vi.major}{vi.minor}"

def arch_tag():
    """
    Ermittelt die System-Architektur.
    dlib benötigt unter Windows meist 'win_amd64' (64-Bit).
    """
    mach = platform.machine().lower()
    if mach in ("amd64", "x86_64"):
        return "win_amd64"
    if "arm" in mach:
        return "win_arm64"
    return mach

def fetch_page(url):
    """
    Lädt den HTML-Quelltext der Gohlke-Webseite herunter.
    Verwendet einen SSL-Kontext, um HTTPS-Verbindungsfehler zu vermeiden.
    """
    ctx = ssl.create_default_context()
    # Timeout ist wichtig, falls die Seite langsam antwortet
    with urllib.request.urlopen(url, context=ctx, timeout=30) as r:
        return r.read().decode("utf-8", errors="ignore")


def find_best_wheel(html, py, arch):
    """
    Durchsucht den HTML-Code nach Links (.whl Dateien), die zum Python-Tag (py)
    und zur Architektur (arch) passen.
    
    Beispiel gesucht: 'dlib-19.24.0-cp39-cp39-win_amd64.whl'
    """
    # Regulärer Ausdruck: Sucht nach href="..." Attributen, die 'dlib', das py-Tag und das arch-Tag enthalten
    pattern = re.compile(r'href="(?P<href>[^"]*dlib[^"]*%s[^"]*%s\.whl)"' % (py, arch), re.IGNORECASE)
    matches = pattern.findall(html)
    
    if not matches:
        # Fallback: Versuche eine weniger strikte Suche (nur Python-Version, ohne explizite Architektur im Namen)
        # falls die Namenskonvention leicht abweicht.
        pattern2 = re.compile(r'href="(?P<href>[^"]*dlib[^"]*%s[^"]*\.whl)"' % (py), re.IGNORECASE)
        matches = pattern2.findall(html)
    return matches


def download(url, dst):
    """
    Lädt die Datei von der URL herunter und speichert sie am Zielort (dst).
    """
    print("Downloading:", url)
    urllib.request.urlretrieve(url, dst)
    print("Saved to:", dst)


def pip_install(path):
    """
    Installiert die heruntergeladene .whl Datei mit pip.
    WICHTIG: Nutzt 'sys.executable', um sicherzustellen, dass pip im 
    aktuellen Environment (venv) ausgeführt wird.
    """
    py = sys.executable
    print("Installing wheel via pip:", path)
    # subprocess ruft den Befehl auf der Kommandozeile auf: python -m pip install ...
    subprocess.check_call([py, "-m", "pip", "install", "--upgrade", path])


def main():
    # 1. Systemumgebung analysieren
    py = py_tag()
    arch = arch_tag()
    print("Detected Python tag:", py)
    print("Detected arch:", arch)

    # 2. HTML-Seite abrufen
    try:
        html = fetch_page(GOLKLE_URL)
    except Exception as e:
        print("Failed to fetch Gohlke page:", e)
        sys.exit(2)

    # 3. Passenden Download-Link suchen
    matches = find_best_wheel(html, py, arch)
    if not matches:
        print("No dlib wheel found matching Python tag/arch on Gohlke page.")
        print("You can download manually from:", GOLKLE_URL)
        sys.exit(3)

    # Den ersten Treffer nehmen und URL zusammenbauen (oft sind Links relativ)
    href = matches[0]
    if href.startswith("/"):
        url = "https://www.lfd.uci.edu" + href
    elif href.startswith("http"):
        url = href
    else:
        url = GOLKLE_URL + href

    # 4. Temporären Ordner für den Download bestimmen
    tmpdir = tempfile.gettempdir()
    fname = os.path.join(tmpdir, os.path.basename(url))
    
    try:
        # 5. Herunterladen und Installieren
        download(url, fname)
        pip_install(fname)
        
        # 6. Nach erfolgreicher dlib-Installation auch face_recognition nachziehen
        # face_recognition hängt von dlib ab, ließ sich aber vorher nicht installieren
        print("Installing face_recognition via pip...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "face_recognition"]) 
        print("Success: dlib and face_recognition should now be installed.")
        
    except subprocess.CalledProcessError as e:
        print("pip install failed:", e)
        sys.exit(4)
    except Exception as e:
        print("Error:", e)
        sys.exit(5)

if __name__ == '__main__':
    main()