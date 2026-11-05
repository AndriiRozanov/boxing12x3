#!/usr/bin/env python3
"""Падає, якщо бій з минулою датою не має запису у votes-close.json (голосування лишилося б відкритим)."""
import re, glob, json, sys, datetime
vc = json.load(open('votes-close.json'))
today = datetime.date.today().isoformat()
bad = []
for f in sorted(glob.glob('ua/*.html')):
    s = open(f, encoding='utf-8').read()
    m = re.search(r"FIGHT_ID\s*=\s*'([^']+)'", s)
    d = re.search(r'"startDate":\s*"(\d{4}-\d{2}-\d{2})', s)
    if m and d and d.group(1) < today and m.group(1) not in vc:
        bad.append((m.group(1), d.group(1)))
if bad:
    print('Немає запису у votes-close.json для завершених боїв:')
    for b in bad: print(' ', *b)
    sys.exit(1)
print('votes-close.json: ок')
