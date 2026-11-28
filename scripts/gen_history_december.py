#!/usr/bin/env python3
"""Builds the December "This day in boxing" pages (ua|en/boxing-history/december.html) from the November
template and scripts/history_dec_data.py, adds the home widget data, the hub month cell and sitemap entries.
Idempotent: re-running regenerates the pages and skips already inserted pieces.
After running: python3 scripts/bake_catalog.py ; python3 scripts/bake_home.py ; check git diff."""
import re, os, glob, json, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import history_dec_data as D

def rd(p): return open(f'{ROOT}/{p}', encoding='utf-8').read()
def wr(p, t): open(f'{ROOT}/{p}', 'w', encoding='utf-8').write(t)

# ---- name -> card slug
def cards(lg):
    m = {}
    for f in glob.glob(f'{ROOT}/{lg}/boxers/*.html'):
        t = open(f, encoding='utf-8').read()
        h = re.search(r'<h1>(.*?)</h1>', t).group(1).replace('&#x27;', "'").replace('&amp;', '&')
        m[h] = os.path.basename(f)[:-5]
    return m
ALIAS = {'en': {'Floyd Mayweather': 'floyd-mayweather-jr'}, 'ua': {}}

def link(title, lg):
    m = dict(cards(lg)); m.update({k: v for k, v in ALIAS[lg].items() if v in m.values()})
    pat = re.compile(r"(?<![\w'])(" + '|'.join(re.escape(n) for n in sorted(m, key=len, reverse=True)) + r")(?![\w'])")
    return pat.sub(lambda x: f"<a class='boxer-link' href='/{lg}/boxers/{m[x.group(1)]}'>{x.group(1)}</a>", title)

def days_block(lg):
    k = 0 if lg == 'ua' else 1
    out = ['var DAYS = [']
    for d in sorted({e[0] for e in D.E}):
        out.append('{d:%d,events:[' % d)
        evs = sorted([e for e in D.E if e[0] == d], key=lambda e: e[1])
        lines = []
        for e in evs:
            t = link(e[2 + k], lg); p = e[4 + k]; x = e[6 + k]; v = e[8]
            s = '{y:%d,t:%s,p:%s' % (e[1], json.dumps(t, ensure_ascii=False), json.dumps(p, ensure_ascii=False))
            if v: s += ',v:%s' % json.dumps(v)
            s += ',x:%s}' % json.dumps(x, ensure_ascii=False)
            lines.append(s)
        out.append(',\n'.join(lines)); out.append(']},')
    out[-1] = out[-1][:-1]
    out.append('];')
    return '\n'.join(out)

def page(lg):
    t = rd(f'{lg}/boxing-history/november.html')
    i = t.index('var DAYS = ['); j = t.index('\n];', i) + 3
    t = t[:i] + days_block(lg) + t[j:]
    if lg == 'ua':
        t = t.replace("Хаглер – Дюран, Холіфілд – Тайсон, Льюїс – Рахман, Ф'юрі – Кличко та інші", "Усик – Ф'юрі II, Тейлор – Хопкінс II, Пак'яо – Де Ла Хойя, Віталій Кличко – Вільямс та інші")
        for a, b in (('листопада', 'грудня'), ('листопад', 'грудень'), ('Листопад', 'Грудень')): t = t.replace(a, b)
    else:
        t = t.replace("Hagler vs Duran, Holyfield vs Tyson, Lewis vs Rahman II, Fury vs Klitschko and more", "Usyk vs Fury II, Taylor vs Hopkins II, Pacquiao vs De La Hoya, Vitali Klitschko vs Williams and more")
        t = t.replace('["","January","February","March","April","May","June","July","August","September","November","November","December"]',
                      '["","January","February","March","April","May","June","July","August","September","October","November","December"]')
        t = t.replace('November', 'December')
    t = t.replace('november', 'december').replace('2026-11-', '2026-12-').replace('1 / 30', '1 / 31').replace('n<=30', 'n<=31').replace("' / 30'", "' / 31'")
    assert 'листопад' not in t.lower() and 'november' not in t.lower(), lg
    wr(f'{lg}/boxing-history/december.html', t)

def home_js():
    byd = {}
    for d, (a, b) in D.PICKS.items():
        def get(p):
            for e in D.E:
                if e[0] == d and e[1] == p[0] and e[2].startswith(p[1]): return e
            raise SystemExit(f'pick not found {d} {p}')
        ea = get(a); s = '%d:{gp:{y:%d,tUk:%s,tEn:%s}' % (d, ea[1], json.dumps(ea[2], ensure_ascii=False), json.dumps(ea[3], ensure_ascii=False))
        if b:
            eb = get(b); s += ',sg:{y:%d,tUk:%s,tEn:%s}' % (eb[1], json.dumps(eb[2], ensure_ascii=False), json.dumps(eb[3], ensure_ascii=False))
        byd[d] = s + '}'
    return 'const HISTORY_DEC = {\n  ' + ',\n  '.join(byd[d] for d in sorted(byd)) + '\n};\n'
MONTH_LINE = "  {idx:11, slug:'december', data:HISTORY_DEC, days:31, lblUk:'Гру', lblEn:'Dec', nameUk:'грудня', nameEn:'Dec'}"

def patch_history(path, marker_nov_end_re):
    t = rd(path)
    t = re.sub(r'const HISTORY_DEC = \{.*?\n\};\n', '', t, flags=re.S)
    t = re.sub(r",\n  \{idx:11, slug:'december'[^\n]*", '', t)
    m = re.search(marker_nov_end_re, t, re.S); assert m, path
    t = t[:m.end()] + home_js() + t[m.end():]
    t = re.sub(r"(  \{idx:10, slug:'november'[^\n]*\})", r"\1,\n" + MONTH_LINE.replace('\\', '\\\\'), t)
    wr(path, t)

def hub(lg):
    p = f'{lg}/boxing-history.html'; t = rd(p)
    if lg == 'ua':
        t = re.sub(r'  \{name:"Грудень",[^\n]*\}', '  {name:"Грудень",active:true,href:"/ua/boxing-history/december",events:["Усик – Ф\'юрі II","Тейлор – Хопкінс II","Пак\'яо – Де Ла Хойя","Віталій Кличко – Вільямс"]}', t)
    else:
        t = re.sub(r'  \{name:"December",[^\n]*\}', '  {name:"December",active:true,href:"/en/boxing-history/december",events:["Usyk vs Fury II","Taylor vs Hopkins II","Pacquiao vs De La Hoya","Vitali Klitschko vs Williams"]}', t)
    wr(p, t)

def sitemap():
    t = rd('sitemap.xml')
    if 'boxing-history/december' in t: return
    def u(lg): return ('  <url>\n    <loc>https://boxing12x3.com/%s/boxing-history/december</loc>\n    <lastmod>2026-11-28</lastmod>\n'
        '    <xhtml:link rel="alternate" hreflang="uk" href="https://boxing12x3.com/ua/boxing-history/december"/>\n'
        '    <xhtml:link rel="alternate" hreflang="en" href="https://boxing12x3.com/en/boxing-history/december"/>\n'
        '    <changefreq>monthly</changefreq>\n    <priority>0.8</priority>\n  </url>\n') % lg
    k = '  <url>\n    <loc>https://boxing12x3.com/ua/boxing-history</loc>'
    assert k in t
    wr('sitemap.xml', t.replace(k, u('ua') + u('en') + k, 1))

if __name__ == '__main__':
    for lg in ('ua', 'en'): page(lg); hub(lg)
    patch_history('data/history-home.js', r'const HISTORY_NOV = \{.*?\n\};\n')
    for p in ('ua/scorecard.html', 'en/scorecard.html'): patch_history(p, r'const HISTORY_NOV = \{.*?\n\};\n')
    sitemap()
    print('ok', len(D.E), 'entries')
