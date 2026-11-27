#!/usr/bin/env python3
"""Bake the "Also on" block (other fights the same day + next on the calendar) into every fight page.

Source: data/events.json (run build_events.py first). The block is placed right before <!-- Read next -->
between the markers <!-- Also on --> ... <!-- /Also on -->. Pages without the Read next marker are skipped.
Idempotent. Run after any change of fights, dates, times or results:  python3 scripts/bake_also_on.py
"""
import json, re, sys, datetime as dt
from zoneinfo import ZoneInfo

R = __file__.rsplit('/scripts/', 1)[0]
ET, KYIV = ZoneInfo('America/New_York'), ZoneInfo('Europe/Kyiv')
MON_EN = 'Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec'.split()
MON_UA = 'січня лютого березня квітня травня червня липня серпня вересня жовтня листопада грудня'.split()
START, END = '<!-- Also on -->', '<!-- /Also on -->'
ANCHOR = '<!-- Read next -->'
VISIBLE = 3      # same-day rows shown before the expander
NEXT_N = 2       # calendar rows when there are same-day fights
NEXT_N_ALONE = 3  # calendar rows when there are none

CSS = (
    '.also-on{background:var(--card);border:0.5px solid var(--border);border-radius:var(--r);padding:20px 18px;margin-bottom:20px;}'
    '.ao-lbl{font-size:10px;color:var(--muted);text-transform:uppercase;letter-spacing:.06em;margin-bottom:4px;font-weight:600;}'
    '.ao-lbl+.ao-lbl,.ao-row+.ao-lbl,.ao-more+.ao-lbl{margin-top:16px;}'
    '.ao-row{display:flex;align-items:center;justify-content:space-between;gap:12px;padding:11px 0;border-bottom:0.5px solid var(--border);text-decoration:none;color:var(--text);transition:opacity .15s;}'
    '.ao-row:hover{opacity:.7;}'
    '.ao-name{font-size:13px;font-weight:600;line-height:1.3;min-width:0;}'
    '.ao-meta{font-size:11px;color:var(--muted);text-align:right;flex-shrink:0;line-height:1.3;}'
    '.ao-res{color:#2e7d32;font-weight:600;}'
    'html.ns .ao-res{display:none}'
    '.ao-more summary{list-style:none;cursor:pointer;font-size:12px;font-weight:600;color:var(--muted);padding:11px 0;border-bottom:0.5px solid var(--border);}'
    '.ao-more summary::-webkit-details-marker{display:none}'
    '.ao-more[open] summary{display:none}'
    '.ao-all{display:block;font-size:12px;font-weight:600;color:var(--muted);text-decoration:none;padding-top:12px;}'
    '.ao-all:hover{opacity:.7}'
)
GA = ("<script>try{if(localStorage.getItem('b12ns')==='1')document.documentElement.classList.add('ns')}catch(e){}"
      "document.querySelectorAll('.also-on a[data-ao]').forEach(function(a){a.addEventListener('click',function(){"
      "if(window.gtag)gtag('event','also_on_click',{group:a.dataset.ao,target_fight:a.dataset.f,source_fight:a.dataset.s});});});</script>")

L = {
    'en': dict(also='Also on {d}', nxt='Next on the calendar', more='+{n} more', cal='Full calendar ›', cal_href='/en/calendar',
               draw='Draw'),
    'ua': dict(also='Також цього дня · {d}', nxt='Далі в календарі', more='ще {n}', cal='Весь календар ›', cal_href='/ua/calendar',
               draw='Нічия'),
}


def read(p):
    return open(p, encoding='utf-8').read()


def esc(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def fdate(iso, lg):
    y, m, d = map(int, iso.split('-'))
    return f'{MON_EN[m-1]} {d}' if lg == 'en' else f'{d} {MON_UA[m-1]}'


def ftime(f, lg):
    if f.get('startPrecision') != 'time' or not f.get('startUtc'):
        return ''
    u = dt.datetime.strptime(f['startUtc'], '%Y-%m-%dT%H:%MZ').replace(tzinfo=dt.timezone.utc)
    if lg == 'en':
        e = u.astimezone(ET)
        return f'{e.hour % 12 or 12}:{e.minute:02d} {"AM" if e.hour < 12 else "PM"} ET'
    k = u.astimezone(KYIV)
    return f'{k.hour:02d}:{k.minute:02d} за Києвом'


_titles = {}


def title(lg, fid):
    k = (lg, fid)
    if k not in _titles:
        _titles[k] = re.search(r'<title>(.*?)</title>', read(f'{R}/{lg}/{fid}.html'), re.S).group(1)
    return _titles[k]


def names(lg, fid):
    t = title(lg, fid).split(':')[0].strip()
    sep = ' vs ' if lg == 'en' else ' – '
    a, b = t.split(sep, 1)
    return t, a, b


def result_txt(f, lg):
    r = f.get('result') or {}
    t = title(lg, f['id'])
    if lg == 'en':
        m = re.search(r'Result, (.*?)(?:, Scorecards)? \|', t)
    else:
        m = re.search(r'результат, (.*?)(?: і суддівські записки)? \|', t)
    method = m.group(1) if m else ''
    w = r.get('winner')
    _, a, b = names(lg, f['id'])
    if w == f['red']['ua']:
        who = a
    elif w == f['blue']['ua']:
        who = b
    else:
        who = L[lg]['draw']
    return f'{who} · {method}' if method else who


def row(f, lg, src, grp, mode):
    name = names(lg, f['id'])[0]
    if f['status'] == 'completed' and f.get('result'):
        meta = f'<span class="ao-res">{esc(result_txt(f, lg))}</span>'
    else:
        tm = ftime(f, lg)
        if mode == 'cal':
            meta = esc(fdate(f['date'], lg) + (' · ' + tm if tm else ''))
        else:
            meta = esc(tm)
    return (f'<a class="ao-row" href="/{lg}/{f["id"]}" data-ao="{grp}" data-f="{f["id"]}" data-s="{src}">'
            f'<span class="ao-name">{esc(name)}</span><span class="ao-meta">{meta}</span></a>')


MAIN = set(json.load(open(f'{R}/data/main_events.json', encoding='utf-8'))['ids'])


def pick_main(day):
    """Main fight of a date: hand list data/main_events.json, then events.json main flag, then latest start (a title fight wins a tie)."""
    for f in day:
        if f['id'] in MAIN:
            return f
    for f in day:
        if f.get('main'):
            return f
    return sorted(day, key=lambda f: (f.get('startUtc') or '', bool(f.get('belts')), f['id']))[-1]


def sort_key(f):
    return (f['date'], f.get('startUtc') or '9999')


def build(fights, f, lg, today):
    same = sorted((x for x in fights if x['date'] == f['date'] and x['id'] != f['id'] and x['status'] != 'cancelled'),
                  key=sort_key)
    floor = max((dt.date.fromisoformat(f['date']) + dt.timedelta(days=1)).isoformat(), today)
    cand = [x for x in fights if x['status'] == 'scheduled' and x['date'] >= floor and x['id'] != f['id']]
    # one fight per date: the main fight of that day
    by = {}
    for x in cand:
        by.setdefault(x['date'], []).append(x)
    nxt = [pick_main(by[d]) for d in sorted(by)][: NEXT_N if same else NEXT_N_ALONE]
    t = L[lg]
    out = [START, '<div class="also-on">']
    if same:
        out.append(f'<div class="ao-lbl">{t["also"].format(d=fdate(f["date"], lg))}</div>')
        rows = [row(x, lg, f['id'], 'same_day', 'same') for x in same]
        out += rows[:VISIBLE]
        rest = rows[VISIBLE:]
        if rest:
            out.append(f'<details class="ao-more"><summary>{t["more"].format(n=len(rest))}</summary>')
            out += rest
            out.append('</details>')
    if nxt:
        out.append(f'<div class="ao-lbl">{t["nxt"]}</div>')
        out += [row(x, lg, f['id'], 'calendar', 'cal') for x in nxt]
    out.append(f'<a class="ao-all" href="{t["cal_href"]}">{t["cal"]}</a>')
    out.append('</div>')
    out.append(f'<style>{CSS}</style>')
    out.append(GA)
    out.append(END)
    return '\n'.join(out) + '\n\n'


def main():
    d = json.load(open(f'{R}/data/events.json', encoding='utf-8'))
    fights = d['fights']
    today = dt.date.today().isoformat()
    changed = skipped = bad = 0
    block = re.compile(re.escape(START) + r'.*?' + re.escape(END) + r'\n\n', re.S)
    for f in fights:
        for lg in ('en', 'ua'):
            p = f'{R}/{lg}/{f["id"]}.html'
            try:
                h = read(p)
            except FileNotFoundError:
                continue
            if ANCHOR not in h:
                skipped += 1
                continue
            try:
                new = build(fights, f, lg, today)
            except Exception as e:  # noqa
                print(f'ERROR {p}: {e}'); bad += 1
                continue
            h2 = block.sub('', h)
            h2 = h2.replace(ANCHOR, new + ANCHOR, 1)
            if h2 != h:
                open(p, 'w', encoding='utf-8').write(h2)
                changed += 1
    print(f'changed {changed}, skipped (no Read next) {skipped}, errors {bad}')
    sys.exit(1 if bad else 0)


main()
