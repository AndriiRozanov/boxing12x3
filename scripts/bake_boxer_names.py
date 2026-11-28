#!/usr/bin/env python3
"""Birth names and native names of active boxers: visible 'Повне ім'я' / 'Full name' cell
(only for birth names) and extra alternateName entries in Person JSON-LD (UA + EN cards).
Idempotent. Only names listed in NAMES (confirmed by the owner) are used.
Usage: python3 scripts/bake_boxer_names.py"""
import re, os, json

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# slug: (birth name or None, [native/spelling variants for markup only])
NAMES = {
    'tyson-fury': ('Tyson Luke Fury', []),
    'anthony-joshua': ('Anthony Oluwafemi Olaseni Joshua', []),
    'deontay-wilder': ('Deontay Leshun Wilder', []),
    'dainier-pero': ('Dainier Christian Peró Justiz', []),
    'moses-itauma': ('Enriko Moses Itauma', []),
    'joseph-parker': ('Joseph Dennis Parker', []),
    'rico-verhoeven': ('Ricardo Verhoeven', []),
    'kingsley-ibeh': ('Kingsley C Ibeh', []),
    'teremoana-teremoana': ('Teremoana Samson Junior Leon Teremoana', []),
    'david-benavidez': ('Anthony David Benavidez', []),
    'jai-opetaia': ('Jai Tapu Opetaia', []),
    'mike-perez': ('Ismaikel Pérez', []),
    'ilunga-makabu': ('Junior Ilunga Makabu', []),
    'oleksandr-usyk': (None, ['Усик Олександр Олександрович']),
    'viktor-vykhryst': (None, ['Вихрист Віктор Вікторович']),
    'gurgen-hovhannisyan': (None, ['Գուրգեն Հովհաննիսյան']),
    'filip-hrgovic': (None, ['Filip Hrgović']),
    'yuniel-dorticos': (None, ['Yunier Dorticos']),
}
LBL = {'ua': "Повне ім'я", 'en': 'Full name'}
BIRTH = re.compile(r'<div class="fact-cell full"><div class="fact-lbl">(?:Місце народження|Place of birth)</div>')
ALT = re.compile(r'"alternateName":(\[[^\]]*\])')


def bake(lg, slug, birth, extra):
    p = f'{ROOT}/{lg}/boxers/{slug}.html'
    t = open(p, encoding='utf-8').read()
    o = t
    t = re.sub(r'<!--fn:start-->.*?<!--fn:end-->\n?    ', '', t, flags=re.S)
    if birth:
        cell = f'<!--fn:start--><div class="fact-cell full"><div class="fact-lbl">{LBL[lg]}</div><div class="fact-val">{birth}</div></div><!--fn:end-->\n    '
        m = BIRTH.search(t); assert m, p
        t = t[:m.start()] + cell + t[m.start():]
    m = ALT.search(t); assert m, p
    alt = json.loads(m.group(1))
    for v in ([birth] if birth else []) + extra:
        if v.lower() not in [a.lower() for a in alt]: alt.append(v)
    t = t[:m.start(1)] + json.dumps(alt, ensure_ascii=False, separators=(',', ':')) + t[m.end(1):]
    if t != o: open(p, 'w', encoding='utf-8').write(t); return 1
    return 0


if __name__ == '__main__':
    n = 0
    for slug, (b, ex) in NAMES.items():
        for lg in ('ua', 'en'): n += bake(lg, slug, b, ex)
    print('changed files:', n)
