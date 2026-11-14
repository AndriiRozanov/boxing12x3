#!/usr/bin/env python3
"""Write official results of finished fights into the scorecard pages (const RESULTS between markers).

Run after scripts/build_events.py:  python3 scripts/bake_scorecard_data.py
The scorecard uses it to tell a visitor how the official result compares with their saved card.
"""
import json, os, re

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = json.load(open(f'{R}/data/events.json', encoding='utf-8'))
page0 = open(f'{R}/ua/scorecard.html', encoding='utf-8').read()
IDS = set(re.findall(r"\bid:\s*'([^']+)'", page0))
res = {}
for f in D['fights']:
    r = f.get('result') or {}
    if f['status'] != 'completed' or f['id'] not in IDS or not r.get('winner'):
        continue
    w = r['winner']
    if w in (f['red']['ua'], f['red']['en']): side = 'red'
    elif w in (f['blue']['ua'], f['blue']['en']): side = 'blue'
    else: side = 'draw'
    m = (r.get('method') or '').replace('ТКО', 'TKO').replace('КО', 'KO')
    m = re.sub(r'\s*·\s*(Раунд|Round)\s*(\d+)', r' \2', m).strip()
    res[f['id']] = {'w': side, 'm': m}
block = '/* results:start */\nconst RESULTS = ' + json.dumps(res, ensure_ascii=False, separators=(',', ':')) + ';\n/* results:end */'
for p in ('ua/scorecard.html', 'en/scorecard.html'):
    s = open(f'{R}/{p}', encoding='utf-8').read()
    s2 = re.sub(r'/\* results:start \*/.*?/\* results:end \*/', lambda m: block, s, flags=re.S)
    assert s2 != s or block in s
    open(f'{R}/{p}', 'w', encoding='utf-8').write(s2)
print(f'{len(res)} results written')
