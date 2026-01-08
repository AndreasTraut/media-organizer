"""
Downloads a suitable dlib wheel from Christoph Gohlke's unofficial binaries
and installs it into the active venv. Prints progress and final status.
"""
import sys
import sysconfig
import platform
import re
import urllib.request
import ssl
import os
import tempfile
import subprocess

GOLKLE_URL = "https://www.lfd.uci.edu/~gohlke/pythonlibs/"

def py_tag():
    vi = sys.version_info
    return f"cp{vi.major}{vi.minor}"

def arch_tag():
    mach = platform.machine().lower()
    if mach in ("amd64", "x86_64"):
        return "win_amd64"
    if "arm" in mach:
        return "win_arm64"
    return mach

def fetch_page(url):
    ctx = ssl.create_default_context()
    with urllib.request.urlopen(url, context=ctx, timeout=30) as r:
        return r.read().decode("utf-8", errors="ignore")


def find_best_wheel(html, py, arch):
    # match filenames like dlib-19.24.0-cp39-cp39-win_amd64.whl
    pattern = re.compile(r'href="(?P<href>[^"]*dlib[^"]*%s[^"]*%s\.whl)"' % (py, arch), re.IGNORECASE)
    matches = pattern.findall(html)
    if not matches:
        # try a more permissive match
        pattern2 = re.compile(r'href="(?P<href>[^"]*dlib[^"]*%s[^"]*\.whl)"' % (py), re.IGNORECASE)
        matches = pattern2.findall(html)
    return matches


def download(url, dst):
    print("Downloading:", url)
    urllib.request.urlretrieve(url, dst)
    print("Saved to:", dst)


def pip_install(path):
    py = sys.executable
    print("Installing wheel via pip:", path)
    subprocess.check_call([py, "-m", "pip", "install", "--upgrade", path])


def main():
    py = py_tag()
    arch = arch_tag()
    print("Detected Python tag:", py)
    print("Detected arch:", arch)
    try:
        html = fetch_page(GOLKLE_URL)
    except Exception as e:
        print("Failed to fetch Gohlke page:", e)
        sys.exit(2)

    matches = find_best_wheel(html, py, arch)
    if not matches:
        print("No dlib wheel found matching Python tag/arch on Gohlke page.")
        print("You can download manually from:", GOLKLE_URL)
        sys.exit(3)

    # prefer the first (they are not ordered reliably); construct absolute URL
    href = matches[0]
    if href.startswith("/"):
        url = "https://www.lfd.uci.edu" + href
    elif href.startswith("http"):
        url = href
    else:
        url = GOLKLE_URL + href

    tmpdir = tempfile.gettempdir()
    fname = os.path.join(tmpdir, os.path.basename(url))
    try:
        download(url, fname)
        pip_install(fname)
        # then install face_recognition
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
