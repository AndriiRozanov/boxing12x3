#!/usr/bin/env python3
"""Fails (exit 1) when a boxer with a card is not linked where he should be.
Checks: (1) fight pages link every carded fighter (comparison card or the "Boxer profiles" line); (2) each card lists all its fights
and its ranking positions. (Ranking pages are linked by gen_rankings.py itself.)
Run after bake_boxer_links.py / gen_rankings.py:  python3 scripts/check_boxer_links.py"""
import re, os, sys, importlib.util
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
spec = importlib.util.spec_from_file_location('b', 'scripts/bake_boxer_links.py')
b = importlib.util.module_from_spec(spec); spec.loader.exec_module(b)
bad = []
for fid, sl in b.SIDES.items():
    for lg in ('ua', 'en'):
        p = f'{lg}/{fid}.html'
        if not os.path.exists(p): continue
        t = open(p, encoding='utf-8').read()
        for s in sl:
            if s and f'href="/{lg}/boxers/{s}"' not in t: bad.append(f'{p}: no link to {s}')
for s in b.CARD:
    for lg in ('ua', 'en'):
        t = open(f'{lg}/boxers/{s}.html', encoding='utf-8').read()
        blk = re.search(r'<!--bl:start-->(.*?)<!--bl:end-->', t, re.S)
        blk = blk.group(1) if blk else ''
        for x in b.FIGHTS.get(s, []):
            if f'href="/{lg}/{x["id"]}"' not in blk: bad.append(f'{lg}/boxers/{s}.html: missing fight {x["id"]}')
        if s in b.RANK and 'rel-chip' not in blk: bad.append(f'{lg}/boxers/{s}.html: missing rankings block')
print('problems:', len(bad))
for x in bad[:40]: print(' ', x)
sys.exit(1 if bad else 0)
