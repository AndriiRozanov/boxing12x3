#!/usr/bin/env python3
"""Index 12x3 block for upcoming fight pages.

Reads each upcoming fight page (data already on the page: record, KO count,
pro rounds, last-5 form) plus the WBA/WBC/IBF/WBO placement from
data/rankings.xlsx, computes the index and writes the block between
<!-- Index --> and <!-- /Index --> on ua/<id>.html and en/<id>.html.
Idempotent: re-run after every monthly rankings update.

Formula (weights are NOT shown to users):
  Strength 0-100 = Form 30%, Ranking position 25%, Knockouts 15%, Wins 15%, Experience 15%
  plus adjustments: age (-1.5 pt/yr over 33, max -15), layoff (over 365 days up to -8,
  under 45 days -3), reach (else height) advantage up to +2.
Shown to the reader: win probability = logistic(strength difference / 16), capped 35-65%.
The block is hidden when either boxer has under 15 fights or under 50 pro rounds.
When a fight is finished the block stays on the page as "pre-fight":
  python3 scripts/gen_index.py --freeze <fight-id>     (run once on fight day, after a normal run)
Every run also rewrites data/index-record.json (hit counter, NOT shown on the site).
Run:  python3 scripts/gen_index.py [--dry]
"""
import re, sys, os, json, math, unicodedata, openpyxl
ROOT = __file__.rsplit('/scripts/', 1)[0] + '/'
EXCLUDE = {'paul-doumbe'}                 # crossover fights: no index
ALIAS = {'Jerome Warburton': 'Gerome Warburton'}   # spelling differs in rankings.xlsx
ORGS = ['WBA', 'WBC', 'IBF', 'WBO']
W = dict(F=.30, S=.25, K=.15, W=.15, E=.15)
PT_STOP = ('KO', 'TKO', 'RTD', 'TD')

L = {
 'ua': dict(title='Імовірність перемоги · 12×3', frozen=' · до бою', sub='Розрахунок за фактичними даними',
            lab=['Форма', 'Місце в рейтингах', 'Нокаути', 'Перемоги', 'Досвід', 'Вік, простій, розмах'],
            note='Враховано форму, рекорд, досвід, вік, простій і рейтинги. Не гарантія результату.'),
 'en': dict(title='Win Probability · 12×3', frozen=' · pre-fight', sub='Calculated from factual data',
            lab=['Form', 'Ranking position', 'Knockouts', 'Wins', 'Experience', 'Age, layoff, reach'],
            note='Takes into account form, record, experience, age, layoff and rankings. Not a guarantee of the result.'),
}
SCALE, PMIN, PMAX = 16, 0.35, 0.65
MIN_FIGHTS, MIN_ROUNDS = 15, 50
CSSX = ".ix-sub{text-align:center;font-size:12px;color:var(--muted);margin:-4px 0 12px;}\n"
CSS = """.ix{background:var(--card);border:0.5px solid var(--border);border-radius:var(--r);padding:20px 18px;margin-bottom:10px;}
.ix-t{text-align:center;font-size:10px;font-weight:600;letter-spacing:.12em;text-transform:uppercase;color:var(--muted);margin-bottom:14px;}
.ix-note{font-size:10.5px;color:var(--muted);line-height:1.5;margin-top:14px;text-align:center;}
.ee-top{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-bottom:12px;text-align:center;}
.ee-nm{font-size:11px;font-weight:600;letter-spacing:.08em;text-transform:uppercase;margin-top:4px;}
.ee-sub{font-size:10px;color:var(--muted);margin-top:2px;min-height:14px;}
.ee-t{width:100%;border-collapse:collapse;}
.ee-t td{padding:8px 0;border-top:0.5px solid var(--border);font-size:13px;}
.ee-t td:nth-child(1){text-align:left;width:20%;font-weight:600;color:#bbb;}
.ee-t td:nth-child(2){text-align:center;font-size:10px;color:var(--muted);text-transform:uppercase;letter-spacing:.06em;}
.ee-t td:nth-child(3){text-align:right;width:20%;font-weight:600;color:#bbb;}
.ee-t td.w.r{color:var(--red);font-weight:700;}
.ee-t td.w.b{color:var(--blue);font-weight:700;}
"""

def norm(x):
    return re.sub(r'[^a-z ]', '', unicodedata.normalize('NFKD', x).encode('ascii', 'ignore').decode().lower()).strip()

def load_rankings():
    ws = openpyxl.load_workbook(ROOT + 'data/rankings.xlsx', data_only=True)['All divisions']
    ent, hdr = [], None
    for r in ws.iter_rows(values_only=True):
        if r[0] == 'Rank': hdr = r
        elif r[0] == 'Champion(s)':
            for k, o in enumerate(hdr):
                if o in ORGS and r[k]:
                    for part in str(r[k]).split('|'):
                        tag = re.search(r'\[(\w+)\]', part)
                        kind = 'champ' if tag and tag.group(1) != 'Interim' else 'interim'
                        ent.append((o, kind, 0, norm(re.sub(r'\(.*?\)|\[.*?\]', '', part))))
        elif str(r[0]).isdigit():
            for k, o in enumerate(hdr):
                if o in ORGS and r[k]:
                    ent.append((o, 'rank', int(r[0]), norm(re.sub(r'\(.*?\)', '', str(r[k])))))
    return ent

def status(ent, name):
    n = norm(ALIAS.get(name, name))
    best = 0
    for o, kind, pos, nm in ent:
        if nm != n: continue
        sc = 100 if kind == 'champ' else 70 if kind == 'interim' else 70 if pos <= 5 else 40
        best = max(best, sc)
    return best

def form_score(cells):
    xs = [(c, t) for c, t in cells if c in ('w', 'l', 'd', 'nc')]
    ws = [5, 4, 3, 2, 1][:len(xs)]
    tot = 0
    for (c, t), w in zip(xs, ws):
        m = (t or '').split(' ')[0]
        if c == 'w': p = 100 if m in PT_STOP else 80
        elif c in ('d', 'nc'): p = 50
        else: p = 0 if m in PT_STOP else 20
        tot += p * w
    return tot / sum(ws)

def parse_en(fid):
    s = open(ROOT + f'en/{fid}.html', encoding='utf-8').read()
    names = [re.sub(r'<[^>]*>', '', x).strip() for x in re.findall(r'<div class="f-name[^"]*">(.*?)</div>', s, re.S)[:2]]
    fr = re.search(r'<div class="fcard-rows">(.*?)\n<!-- Stats -->', s, re.S).group(1)
    d = {}
    for row in fr.split('<div class="frow">')[1:]:
        m = re.search(r'<span class="fv r">(.*?)</span>\s*(?:</span>)?\s*<div class="flbl[^"]*">\s*<span>([^<]*)</span>.*?<span class="fv b">(.*?)\n    </div>', row, re.S)
        if m:
            f = lambda t: re.split(r'<', t)[0].strip()
            d[m.group(2)] = (f(m.group(1)), f(m.group(3)))
    blocks = re.findall(r'<div class="form-cells">\n(.*?)\n      </div>', s, re.S)[:2]
    form = [re.findall(r'<div class="fc (\w+)">[^<]*</div>(?:<div class="fc-tip">([^<]*)</div>)?', b) for b in blocks]
    return names, d, form

def _n(t, pat):
    m = re.search(pat, t or '')
    return float(m.group(1).replace(',', '')) if m else None

def parse_extras(fid, d):
    s = open(ROOT + f'en/{fid}.html', encoding='utf-8').read()
    ages = [_n(x, r'^(\d+)') for x in re.findall(r'<div class="f-info">(.*?)</div>', s)[:2]]
    g = lambda k, pat: [_n(x, pat) for x in d.get(k, ('', ''))]
    return [dict(age=ages[i], lay=g('Since last fight', r'([\d,]+) day')[i], h=g('Height', r'(\d+)')[i], r=g('Reach', r'(\d+)')[i]) for i in (0, 1)]

def adjust(me, op):
    age = -min(max(me['age'] - 33, 0) * 1.5, 15) if me['age'] else 0
    l = me['lay']
    lay = 0 if not l else (-min((l - 365) / 365 * 8, 8) if l > 365 else (-3 if l < 45 else 0))
    if me['r'] and op['r']: body = min(max((me['r'] - op['r']) * .4, 0), 2)
    elif me['h'] and op['h']: body = min(max((me['h'] - op['h']) * .3, 0), 2)
    else: body = 0
    return age + lay + body

def calc(ent, name, rec, ko, rounds, cells, me=None, op=None):
    w, l, d = [int(x) for x in rec.split('-')]
    n = w + l + d; k = int(ko.split()[0]); r = int(rounds.replace(',', ''))
    low = n < 15 or r < 50
    F = form_score(cells); S = status(ent, name)
    K = (k + (2.5 if low else 0)) / (w + (5 if low else 0)) * 100
    Wn = (w + (3.75 if low else 0)) / (n + (5 if low else 0)) * 100
    E = min(r / 250, 1) * 100
    idx = W['F'] * F + W['S'] * S + W['K'] * K + W['W'] * Wn + W['E'] * E
    adj = adjust(me, op) if me and op else 0
    return dict(I=min(max(round(idx + adj), 0), 100), F=round(F), S=round(S), K=round(K), W=round(Wn), E=round(E),
                A=round(adj), low=n < MIN_FIGHTS or r < MIN_ROUNDS)

def probs(a, b):
    p = 1 / (1 + math.exp(-(a['I'] - b['I']) / SCALE))
    p = min(max(p, PMIN), PMAX); pa = round(p * 100)
    return pa, 100 - pa

def ring(v, color, label, suf=''):
    r = 44; c = 2 * math.pi * r
    return (f'<svg width="112" height="112" viewBox="0 0 112 112" role="img" aria-label="{label}: {v}">'
            f'<circle cx="56" cy="56" r="{r}" fill="none" stroke="#e8e6e0" stroke-width="9"/>'
            f'<circle cx="56" cy="56" r="{r}" fill="none" stroke="{color}" stroke-width="9" stroke-linecap="round" '
            f'stroke-dasharray="{c * v / 100:.1f} {c:.1f}" transform="rotate(-90 56 56)"/>'
            f'<text x="56" y="68" text-anchor="middle" font-family="Oswald,sans-serif" font-weight="700" font-size="{34 if suf else 38}" fill="{color}">{v}{suf}</text></svg>')

def block(lg, names, a, b):
    t = L[lg]; keys = ['F', 'S', 'K', 'W', 'E', 'A']; pa, pb = probs(a, b)
    sg = lambda v: ('+' if v > 0 else '\u2212' if v < 0 else '') + str(abs(v))
    show = lambda k, x: sg(x[k]) if k == 'A' else x[k]
    rows = ''.join(
        f'<tr><td class="{"w r" if a[k] >= b[k] else ""}">{show(k, a)}</td><td>{t["lab"][i]}</td>'
        f'<td class="{"w b" if b[k] >= a[k] else ""}">{show(k, b)}</td></tr>' for i, k in enumerate(keys))
    return (f'<!-- Index -->\n<div class="ix" data-pa="{pa}" data-pb="{pb}">\n  <div class="ix-t">' + t['title'] + '</div>\n'
            '  <div class="ee-top">\n'
            f'    <div>{ring(pa, "#c0392b", names[0], "%")}<div class="ee-nm" style="color:var(--red)">{names[0]}</div></div>\n'
            f'    <div>{ring(pb, "#1a5276", names[1], "%")}<div class="ee-nm" style="color:var(--blue)">{names[1]}</div></div>\n'
            f'  </div>\n  <div class="ix-sub">{t["sub"]}</div>\n  <table class="ee-t">' + rows + '</table>\n'
            f'  <div class="ix-note">{t["note"]}</div>\n</div>\n<!-- /Index -->\n')

def upcoming_ids():
    s = open(ROOT + 'ua/scorecard.html', encoding='utf-8').read()   # FIGHTS lives in the scorecard page since the events-first redesign
    i = s.index('const FIGHTS'); j = s.index('\n];', i)
    out = []
    for m in re.finditer(r"\{id:'([^']+)'.*?completed:(\w+), hasPage:(\w+)", s[i:j]):
        if m.group(2) == 'false' and m.group(3) == 'true' and m.group(1) not in EXCLUDE: out.append(m.group(1))
    return out

def inject(path, lg, names, a, b):
    s = open(path, encoding='utf-8').read()
    new = block(lg, names, a, b)
    if '<!-- Index -->' in s:
        s = re.sub(r'<!-- Index -->.*?<!-- /Index -->\n', lambda m: new, s, flags=re.S)
    else:
        i = s.index('<!-- Stats -->'); j = s.index('\n<!-- ', i + 10)
        s = s[:j + 1] + new + '\n' + s[j + 1:]
    if '.ix-t{' not in s:
        s = s.replace('</style>', CSS + '</style>', 1)
    if '.ix-sub{' not in s:
        s = s.replace('</style>', CSSX + '</style>', 1)
    open(path, 'w', encoding='utf-8').write(s)

def strip(path):
    s = open(path, encoding='utf-8').read()
    if '<!-- Index -->' not in s: return False
    s = re.sub(r'<!-- Index -->.*?<!-- /Index -->\n\n?', '', s, flags=re.S)
    open(path, 'w', encoding='utf-8').write(s)
    return True

def freeze(fid):
    for lg in ('ua', 'en'):
        path = ROOT + f'{lg}/{fid}.html'
        s = open(path, encoding='utf-8').read()
        if '<!-- Index -->' not in s: print(f'{fid} {lg}: no Index block (hidden for low data?)'); continue
        if 'data-frozen' in s: print(f'{fid} {lg}: already frozen'); continue
        t = L[lg]
        s = s.replace('<div class="ix" ', '<div class="ix" data-frozen="1" ', 1)
        s = s.replace('<div class="ix-t">' + t['title'] + '</div>', '<div class="ix-t">' + t['title'] + t['frozen'] + '</div>', 1)
        open(path, 'w', encoding='utf-8').write(s); print(f'{fid} {lg}: frozen')

def cancelled_ids():
    s = open(ROOT + 'ua/scorecard.html', encoding='utf-8').read()
    i = s.index('const FIGHTS'); j = s.index('\n];', i)
    return [m.group(1) for m in re.finditer(r"\{id:'([^']+)'[^\n]*?cancelled:true", s[i:j])]

def record(dry=False):
    ev = json.load(open(ROOT + 'data/events.json', encoding='utf-8'))
    out = []; hit = tot = 0
    for f in ev['fights']:
        res = f.get('result')
        if f['status'] != 'completed' or not res: continue
        s = open(ROOT + f'en/{f["id"]}.html', encoding='utf-8').read() if os.path.exists(ROOT + f'en/{f["id"]}.html') else ''
        m = re.search(r'<div class="ix" data-frozen="1" data-pa="(\d+)" data-pb="(\d+)"', s) or re.search(r'<div class="ix" data-pa="(\d+)" data-pb="(\d+)" data-frozen="1"', s)
        if not m: continue
        w = res['winner']; red, blue = f['red']['ua'], f['blue']['ua']
        side = 'r' if w == red or red.split()[-1] in w else 'b' if w == blue or blue.split()[-1] in w else None
        pa, pb = int(m.group(1)), int(m.group(2))
        if side is None: continue
        counted = pa != pb
        ok = counted and ((pa > pb) == (side == 'r'))
        out.append(dict(id=f['id'], pa=pa, pb=pb, winner=side, counted=counted, hit=ok))
        tot += counted; hit += ok
    data = dict(hits=hit, total=tot, show_from=30, fights=out)
    if not dry: json.dump(data, open(ROOT + 'data/index-record.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(f'Index record: {hit} of {tot} (hidden until 30 fights)')

def short_names(path):
    s = open(path, encoding='utf-8').read()
    i = s.index('<!-- Stats -->')
    r = re.search(r'<span style="color:var\(--red\)">([^<]*)</span>', s[i:]).group(1)
    b = re.search(r'<span style="color:var\(--blue\)">([^<]*)</span>', s[i:]).group(1)
    return [r, b]

if __name__ == '__main__':
    if '--freeze' in sys.argv:
        freeze(sys.argv[sys.argv.index('--freeze') + 1]); record(); sys.exit()
    dry = '--dry' in sys.argv
    ent = load_rankings()
    for fid in cancelled_ids():
        for lg in ('ua', 'en'):
            if not dry and os.path.exists(ROOT + f'{lg}/{fid}.html') and strip(ROOT + f'{lg}/{fid}.html'): print(f'{fid} {lg}: cancelled, Index block removed')
    for fid in upcoming_ids():
        names, d, form = parse_en(fid)
        ex = parse_extras(fid, d)
        res = [calc(ent, names[i], d['Record'][i], d['Stoppages'][i], d['Rounds'][i], form[i], ex[i], ex[1 - i]) for i in (0, 1)]
        hide = res[0]['low'] or res[1]['low']
        pa, pb = probs(*res)
        print(f'{fid:26} {names[0]} {res[0]["I"]} ({res[0]["A"]:+d}) / {names[1]} {res[1]["I"]} ({res[1]["A"]:+d})  ->  {pa}% / {pb}%' + ('  HIDDEN: low data' if hide else ''))
        if not dry:
            for lg in ('ua', 'en'):
                p = ROOT + f'{lg}/{fid}.html'
                if hide: strip(p)
                else: inject(p, lg, short_names(p), res[0], res[1])
    record(dry)
