#!/usr/bin/env python3
"""Static "Other boxers in the division" block on every boxer card (UA + EN).

Source of truth: BOXER_PROFILES + DIV_ORDER in ua/boxers.html and en/boxers.html.
Card division = the one where the boxer has the most belt rows in BOXER_PROFILES (tie: first in DIV_ORDER).
Shown: the next 6 boxers of that division after him, alphabetically by slug, cyclic (fewer if the division is small).
The block sits between <!--related:start--> and <!--related:end--> right before <div class="site-footer">.
Run from the repo root after BOXER_PROFILES changes:  python3 scripts/related_boxers.py
"""
import re, pathlib, collections

ROOT = pathlib.Path(__file__).resolve().parent.parent
START, END = '<!--related:start-->', '<!--related:end-->'
N = 6
CSS_MARK = '/*related*/'
CSS = (CSS_MARK + '.rel-link{display:flex;align-items:center;justify-content:space-between;padding:11px 20px;border-top:0.5px solid var(--border);'
       'text-decoration:none;color:var(--text);font-size:13px;font-weight:500;transition:background .15s;}'
       '.rel-link:hover{background:var(--bg);}.rel-name{display:flex;align-items:center;gap:8px;flex-wrap:wrap;}'
       '.rel-chip{font-size:9px;font-weight:700;color:#fff;padding:2px 6px;border-radius:3px;}.rel-arr{font-size:14px;color:var(--muted);}\n')
LANGS = {
    'ua': dict(key='nameUk', label='Інші боксери дивізіону: %s', names='DIV_NAMES_UK', lower=True),
    'en': dict(key='name', label='Other boxers in the division: %s', names='DIV_NAMES_EN', lower=False),
}

def load(lang):
    src = (ROOT / lang / 'boxers.html').read_text(encoding='utf-8')
    k = LANGS[lang]['key']
    rows = re.findall(r"\{id:'([^']+)', slug:'([^']+)', %s:'((?:[^'\\]|\\.)*)', div:'([^']+)'(?:, org:'([^']*)', orgColor:'([^']*)')?\}" % k, src)
    order = re.search(r"const DIV_ORDER = \[([^\]]+)\]", src).group(1)
    order = re.findall(r"'(\w+)'", order)
    names_m = re.search(r"const %s = \{([^}]+)\}" % LANGS[lang]['names'], src).group(1)
    names = dict(re.findall(r"(\w+):'([^']+)'", names_m))
    return rows, order, names

for lang, cfg in LANGS.items():
    rows, order, names = load(lang)
    name = {}; belts = collections.defaultdict(lambda: collections.defaultdict(list)); members = collections.defaultdict(set)
    for _id, slug, nm, dv, org, col in rows:
        name[slug] = nm.replace("\\'", "'")
        members[dv].add(slug)
        if org:
            belts[slug][dv].append((org, col))
    prim = {}
    for slug in name:
        divs = [d for d in order if slug in members[d]]
        prim[slug] = max(divs, key=lambda d: (len(belts[slug][d]), -order.index(d)))
    total = 0
    for slug in sorted(name):
        dv = prim[slug]
        mem = sorted(members[dv])
        i = mem.index(slug)
        rel = [mem[(i + j) % len(mem)] for j in range(1, len(mem))][:N]
        dname = names[dv].lower() if cfg['lower'] else names[dv]
        items = ''
        for r in rel:
            chips = ''.join(' <span class="rel-chip" style="background:%s">%s</span>' % (c, o) for o, c in belts[r][dv])
            items += '<a class="rel-link" href="/%s/boxers/%s"><span class="rel-name">%s%s</span><span class="rel-arr">›</span></a>' % (lang, r, name[r], chips)
        block = START + '<div class="card"><div class="section-lbl">' + cfg['label'] % dname + '</div>' + items + '</div>\n' + END + '\n'
        path = ROOT / lang / 'boxers' / (slug + '.html')
        s = path.read_text(encoding='utf-8')
        if START in s:
            s = re.sub(re.escape(START) + '.*?' + re.escape(END) + '\n', lambda m: block, s, flags=re.S)
        else:
            assert s.count('<div class="site-footer">') == 1, path
            s = s.replace('<div class="site-footer">', block + '<div class="site-footer">', 1)
        if CSS_MARK not in s:
            assert '.site-footer a:hover{color:var(--red);}\n' in s, path
            s = s.replace('.site-footer a:hover{color:var(--red);}\n', '.site-footer a:hover{color:var(--red);}\n' + CSS, 1)
        path.write_text(s, encoding='utf-8')
        total += len(rel)
    print(lang, 'cards:', len(name), 'links:', total)
