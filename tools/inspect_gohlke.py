import urllib.request
s = urllib.request.urlopen('https://www.lfd.uci.edu/~gohlke/pythonlibs/').read().decode('utf-8','ignore')
lines = [l for l in s.split('\n') if 'dlib' in l.lower()]
print('found', len(lines))
for i,l in enumerate(lines[:80]):
    print(i+1, l.strip())
