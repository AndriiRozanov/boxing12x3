#!/usr/bin/env python3
"""Internal links between boxer cards and the rest of the site (UA + EN). Idempotent.

1. Fight pages: the two names in the comparison card (.f-name) link to the boxer card when one exists.
2. Boxer cards: block "Бої на сайті" / "Fights on the site" (all fight pages with this boxer, upcoming first)
   and block "У рейтингах" / "In the rankings" (current official positions, from data/rankings.xlsx),
   placed between the last card and <!--related:start-->.
Sources: data/events.json (fights), data/rankings.xlsx (positions), ua|en/boxers/*.html (names).
Run from the repo root after adding fights/cards or after the monthly rankings update:
    python3 scripts/bake_boxer_links.py
Rankings pages themselves are linked by scripts/gen_rankings.py (run it first after a rankings update).
"""
import re, os, json, glob, csv, unicodedata, datetime
import openpyxl

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
TODAY = datetime.date.today().isoformat()
START, END = '<!--bl:start-->', '<!--bl:end-->'
CSS_MARK = '/*bl*/'
CSS_CARD = (CSS_MARK + '.bl-date{font-size:11px;color:var(--muted);font-weight:500;white-space:nowrap;margin-left:10px;}'
            '.bl-end{display:flex;align-items:center;}.bl-sub{font-size:12px;color:var(--muted);font-weight:500;}\n')
CSS_FIGHT = (CSS_MARK + '.f-name a{color:inherit;text-decoration:none;border-bottom:1.5px solid currentColor;}\n')


def norm(s):
    s = unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode().lower()
    return re.sub(r'[^a-z ]', '', s).strip()


def slugify(n):
    return '-'.join(re.sub(r"[.'’]", '', n).lower().split())


# ---- cards and names -------------------------------------------------------------------------
CARD = {}      # slug -> {'ua': name, 'en': name}
for f in sorted(glob.glob('en/boxers/*.html')):
    s = os.path.basename(f)[:-5]
    en = re.search(r'<h1>(.*?)</h1>', open(f, encoding='utf-8').read()).group(1)
    ua = re.search(r'<h1>(.*?)</h1>', open(f'ua/boxers/{s}.html', encoding='utf-8').read()).group(1)
    CARD[s] = {'ua': ua, 'en': en}
BY_NORM = {norm(v['en']): s for s, v in CARD.items()}
CANON = {}
for r in csv.DictReader(open('data/names_ua.csv', encoding='utf-8')):
    CANON[norm(r['en_raw'])] = norm(r['en_canonical'])


def card_of(en_name):
    n = norm(en_name)
    return BY_NORM.get(n) or BY_NORM.get(CANON.get(n, ''))


# ---- fights per boxer ------------------------------------------------------------------------
EV = json.load(open('data/events.json', encoding='utf-8'))['fights']
FIGHTS = {}    # slug -> list of fight dicts
SIDES = {}     # fight id -> (slug or None for red, slug or None for blue)
for x in EV:
    sl = (card_of(x['red']['en']), card_of(x['blue']['en']))
    SIDES[x['id']] = sl
    if x['status'] == 'cancelled':
        continue
    for s in sl:
        if s:
            FIGHTS.setdefault(s, []).append(x)

# ---- rankings per boxer ----------------------------------------------------------------------
src = open('scripts/gen_rankings.py', encoding='utf-8').read()
DIVMETA = eval(re.search(r'DIVMETA=(\{.*?\})\n', src, re.S).group(1))
NAMEFIX = {}
for r in csv.DictReader(open('data/names_ua.csv', encoding='utf-8')):
    NAMEFIX[r['en_raw']] = r['en_canonical']
ORGS = ['WBA', 'WBC', 'IBF', 'WBO', 'The Ring']
ORGC = {'WBA': '#1a5276', 'WBC': '#2e7d32', 'IBF': '#7d2942', 'WBO': '#111', 'The Ring': '#b8860b'}
ORGP = {'WBA': 'wba', 'WBC': 'wbc', 'IBF': 'ibf', 'WBO': 'wbo'}   # The Ring has no org page
CH_UA = {'World': 'Чемпіон світу', 'Super': 'Суперчемпіон', 'Interim': 'Тимчасовий чемпіон', 'Champion': 'Чемпіон'}
CH_EN = {'World': 'World champion', 'Super': 'Super champion', 'Interim': 'Interim champion', 'Champion': 'Champion'}
RANK = {}      # slug -> list of (org, division key, 'C:<type>' or int)
rows = list(openpyxl.load_workbook('data/rankings.xlsx', data_only=True)['All divisions'].iter_rows(values_only=True))
cur = None
for r in rows:
    a = r[0]
    if a and str(a).isupper() and r[1] is None and a in DIVMETA:
        cur = dict(name=a, date=None, champ=None, top=[]); RANK.setdefault('_divs', []).append(cur)
    elif a == 'List date':
        cur['date'] = r[1:6]
    elif a == 'Champion(s)':
        cur['champ'] = r[1:6]
    elif a and str(a).isdigit():
        cur['top'].append((int(a), r[1:6]))
DIVS = RANK.pop('_divs')


def person(raw):
    m = re.match(r'(.*?)\s*\((.*?)\)\s*$', raw.strip())
    n = m.group(1).strip() if m else raw.strip()
    return NAMEFIX.get(n, n)


for d in DIVS:
    for i, org in enumerate(ORGS):
        dt = (d['date'][i] or '')
        if dt.startswith('n/a') or dt.startswith('not collected'):
            continue
        if d['champ'][i]:
            for p in d['champ'][i].split('|'):
                p = p.strip(); m = re.match(r'(.*)\[(.*?)\]', p); st = 'Champion'
                if m: p, st = m.group(1).strip(), m.group(2)
                if p.startswith('VACANT'): continue
                s = BY_NORM.get(norm(person(p)))
                if s: RANK.setdefault(s, []).append((org, d['name'], 'C:' + st))
        for k, row in d['top']:
            v = row[i]
            if v and not str(v).startswith('VACANT'):
                s = BY_NORM.get(norm(person(str(v))))
                if s: RANK.setdefault(s, []).append((org, d['name'], k))


# ---- helpers ---------------------------------------------------------------------------------
MON_UA = ['січня', 'лютого', 'березня', 'квітня', 'травня', 'червня', 'липня', 'серпня', 'вересня', 'жовтня', 'листопада', 'грудня']
MON_EN = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']


def fdate(iso, lg):
    y, m, d = map(int, iso.split('-'))
    return f'{d} {MON_UA[m - 1]} {y}' if lg == 'ua' else f'{MON_EN[m - 1]} {d}, {y}'


def esc(s):
    return s.replace('&', '&amp;').replace('<', '&lt;')


def fights_block(slug, lg):
    fl = FIGHTS.get(slug, [])
    if not fl:
        return ''
    up = sorted([x for x in fl if x['status'] != 'completed'], key=lambda x: x['date'])
    done = sorted([x for x in fl if x['status'] == 'completed'], key=lambda x: x['date'], reverse=True)
    lab = 'Бої на сайті' if lg == 'ua' else 'Fights on the site'
    out = f'<div class="card"><div class="section-lbl">{lab}</div>'
    for x in up + done:
        sep = ' – ' if lg == 'ua' else ' vs '
        title = esc(x['red'][lg] + sep + x['blue'][lg])
        if x['status'] == 'completed':
            chip = '<span class="rel-chip" style="background:#888">%s</span>' % ('Результат' if lg == 'ua' else 'Result')
        else:
            chip = '<span class="rel-chip" style="background:#111">%s</span>' % ('Скоро' if lg == 'ua' else 'Upcoming')
        out += (f'<a class="rel-link" href="/{lg}/{x["id"]}"><span class="rel-name">{title} {chip}</span>'
                f'<span class="bl-end"><span class="bl-date">{fdate(x["date"], lg)}</span><span class="rel-arr">›</span></span></a>')
    return out + '</div>\n'


def rank_block(slug, lg):
    rl = RANK.get(slug, [])
    if not rl:
        return ''
    lab = 'У рейтингах' if lg == 'ua' else 'In the rankings'
    out = f'<div class="card"><div class="section-lbl">{lab}</div>'
    dv = {d['name']: d for d in DIVS}
    order = {o: i for i, o in enumerate(ORGS)}
    rl = sorted(rl, key=lambda t: (isinstance(t[2], int), order[t[0]]))
    for org, dname, pos in rl:
        meta = DIVMETA[dname]
        dn = meta[1] if lg == 'ua' else meta[2]
        if isinstance(pos, str):
            st = pos[2:]
            if org == 'The Ring':
                txt = 'Чемпіон The Ring' if lg == 'ua' else 'The Ring champion'
            else:
                txt = (CH_UA if lg == 'ua' else CH_EN).get(st, st) + (' ' + org if lg == 'ua' else ' ' + org)
        else:
            txt = (f'№{pos} у рейтингу {org}' if lg == 'ua' else f'No. {pos} in {org if org == "The Ring" else "the " + org} ranking')
        chip = f'<span class="rel-chip" style="background:{ORGC[org]}">{org}</span>'
        inner = f'<span class="rel-name">{chip} {esc(txt)} <span class="bl-sub">· {dn}</span></span><span class="rel-arr">›</span>'
        if org in ORGP:
            out += f'<a class="rel-link" href="/{lg}/rankings/{ORGP[org]}#{meta[0]}">{inner}</a>'
        else:
            out += f'<a class="rel-link" href="/{lg}/rankings/{meta[0]}">{inner}</a>'
    return out + '</div>\n'


def bake_card(slug, lg):
    p = f'{lg}/boxers/{slug}.html'
    t = open(p, encoding='utf-8').read()
    t = re.sub(re.escape(START) + r'.*?' + re.escape(END) + r'\n?', '', t, flags=re.S)
    block = fights_block(slug, lg) + rank_block(slug, lg)
    if block:
        assert '<!--related:start-->' in t, p
        t = t.replace('<!--related:start-->', START + block + END + '\n<!--related:start-->', 1)
        if CSS_MARK not in t:
            m = re.search(r'/\*related\*/[^\n]*\n', t)
            assert m, p
            t = t[:m.end()] + CSS_CARD + t[m.end():]
    open(p, 'w', encoding='utf-8').write(t)
    return bool(block)


F_NAME = re.compile(r'(<div class="fighter(?: r| b)?">.*?<div class="f-name[^"]*">)(.*?)(</div>)', re.S)


def bake_fight(fid, lg):
    p = f'{lg}/{fid}.html'
    if not os.path.exists(p):
        return 0
    t = open(p, encoding='utf-8').read()
    sl = SIDES[fid]
    n = [0]

    def rep(m):
        s = sl[1] if 'fighter b' in m.group(1) else sl[0]
        inner = re.sub(r'^<a href="/(?:ua|en)/boxers/[^"]*">(.*)</a>$', r'\1', m.group(2), flags=re.S)
        if not s:
            return m.group(1) + inner + m.group(3)
        n[0] += 1
        return m.group(1) + f'<a href="/{lg}/boxers/{s}">{inner}</a>' + m.group(3)
    t2 = F_NAME.sub(rep, t)
    if n[0] and CSS_MARK not in t2:
        i = t2.index('</style>')
        t2 = t2[:i] + CSS_FIGHT + t2[i:]
    if t2 != t:
        open(p, 'w', encoding='utf-8').write(t2)
    return n[0]


if __name__ == '__main__':
    cards = sum(bake_card(s, lg) for s in CARD for lg in ('ua', 'en'))
    links = sum(bake_fight(fid, lg) for fid in SIDES for lg in ('ua', 'en'))
    print(f'boxer cards with new blocks: {cards} (of {2 * len(CARD)}); name links on fight pages: {links}')
