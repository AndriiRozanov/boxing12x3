#!/usr/bin/env python3
"""Generate ALIASES (nicknames + Ukrainian names) for the height-compare search.

Source: BOXER_PROFILES (id, slug, nameUk) in height-compare.html and Person.alternateName on each card.
Writes the block between /*aliases:start*/ and /*aliases:end*/ in height-compare.html and en/height-compare.html.
Extra hand-made aliases (no card yet) go into MANUAL below. Idempotent.
"""
import re, json, pathlib
R = pathlib.Path(__file__).resolve().parent.parent
MANUAL = {'alvarez_s': ['Canelo', 'Сауль Альварес']}

def build():
    src = (R/'height-compare.html').read_text(encoding='utf-8')
    prof = {}
    for m in re.finditer(r"\{id:'([^']+)',\s*slug:'([^']+)',\s*name:'([^']*)',\s*nameUk:'([^']*)'", src):
        prof.setdefault(m.group(1), (m.group(2), m.group(3), m.group(4)))
    out = {}
    for pid, (slug, name, nameUk) in prof.items():
        al = [nameUk]
        card = (R/'en'/'boxers'/(slug+'.html')).read_text(encoding='utf-8')
        m = re.search(r'"@type":"Person".*?"alternateName":(\[.*?\])', card)
        if m:
            for a in json.loads(m.group(1)):
                if re.search('[А-Яа-яІіЇїЄєҐґ]', a) or a == name: continue
                al.append(a)
        out[pid] = [a for i, a in enumerate(al) if a and a not in al[:i]]
    for k, v in MANUAL.items():
        out[k] = list(dict.fromkeys(out.get(k, []) + v))
    return out

def main():
    al = build()
    block = '/*aliases:start*/\nconst ALIASES = ' + json.dumps(al, ensure_ascii=False, separators=(',', ':')) + ';\n/*aliases:end*/\n'
    for f in ('height-compare.html', 'en/height-compare.html'):
        p = R/f; s = p.read_text(encoding='utf-8')
        s = re.sub(r'/\*aliases:start\*/.*?/\*aliases:end\*/\n', '', s, flags=re.S)
        k = s.index('const BOXER_PROFILES = [')
        p.write_text(s[:k] + block + s[k:], encoding='utf-8')
    print('boxers with aliases:', len(al), 'nicknames:', sum(len(v) - 1 for v in al.values()))

if __name__ == '__main__':
    main()
