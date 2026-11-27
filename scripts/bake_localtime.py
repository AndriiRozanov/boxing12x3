#!/usr/bin/env python3
"""Add data-utc to broadcast rows of UPCOMING fight pages and tournament cards, and include /js/local-time.js.

Source of truth for the instant is the EN row text (first ET time on the row, date from the row).
The UA row is cross-checked: its Kyiv time must equal the same instant, otherwise the script reports it.
Rows without a clock time ("start time to be confirmed", date only) are left untouched.
Idempotent. Run after any change of broadcast times:  python3 scripts/bake_localtime.py
"""
import json, re, sys, datetime as dt
from zoneinfo import ZoneInfo

R = __file__.rsplit('/scripts/', 1)[0]
ET, KYIV, UTC = ZoneInfo('America/New_York'), ZoneInfo('Europe/Kyiv'), ZoneInfo('UTC')
MON = {m: i + 1 for i, m in enumerate('Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec'.split())}
SCRIPT = '<script src="/js/local-time.js" defer></script>'
ROW = re.compile(r'(<div class="broadcast-row">)(.*?)(</div>)', re.S)
TIME = re.compile(r'<span class="broadcast-time"(?: data-utc="[^"]*")?(?: data-q="[^"]*")?>([^<]*)</span>')
EN_T = re.compile(r'([A-Z][a-z]{2}) (\d{1,2}) · .*?(\d{1,2}):(\d{2}) (AM|PM) ET')


def qual(row_html):
    low = row_html.lower()
    if 'not before' in low or 'не раніше' in low:
        return 'notbefore'
    if 'approx' in low or 'близько' in low or 'орієнтовно' in low:
        return 'approx'
    return ''


def read(p):
    return open(p, encoding='utf-8').read()


def pages():
    d = json.load(open(f'{R}/data/events.json', encoding='utf-8'))
    out = [(f['id'], f'{{lg}}/{f["id"]}.html', f['date'][:4]) for f in d['fights'] if f['status'] == 'scheduled']
    today = dt.date.today().isoformat()
    for t in d['tournaments']:
        if (t.get('startDate') or '') >= today:
            out.append((t['id'], f'{{lg}}/cards/{t["id"]}.html', t['startDate'][:4]))
    return out


def instants(en_html, year):
    res = []
    for m in ROW.finditer(en_html):
        tm = TIME.search(m.group(2))
        if not tm:
            res.append(None); continue
        x = EN_T.search(tm.group(1))
        if not x:
            res.append(None); continue
        mon, day, hh, mi, ap = x.groups()
        hh = int(hh) % 12 + (12 if ap == 'PM' else 0)
        local = dt.datetime(int(year), MON[mon], int(day), hh, int(mi), tzinfo=ET)
        res.append(local.astimezone(UTC))
    return res


def apply(html, utcs):
    idx = [0]

    def row(m):
        i = idx[0]; idx[0] += 1
        u = utcs[i] if i < len(utcs) else None
        if u is None:
            return m.group(0)
        q = qual(m.group(2))
        attr = f' data-utc="{u.strftime("%Y-%m-%dT%H:%M:%SZ")}"' + (f' data-q="{q}"' if q else '')
        new = TIME.sub(lambda t: f'<span class="broadcast-time"{attr}>{t.group(1)}</span>', m.group(2), count=1)
        return m.group(1) + new + m.group(3)

    html = ROW.sub(row, html)
    if SCRIPT not in html and 'data-utc=' in html:
        html = html.replace('</body>', SCRIPT + '\n</body>', 1)
    return html


def main():
    bad = 0; changed = 0
    for fid, tpl, year in pages():
        en_p, ua_p = f'{R}/' + tpl.format(lg='en'), f'{R}/' + tpl.format(lg='ua')
        en = read(en_p); ua = read(ua_p)
        utcs = instants(en, year)
        # cross-check UA
        ua_rows = [TIME.search(m.group(2)) for m in ROW.finditer(ua)]
        for i, u in enumerate(utcs):
            if u is None or i >= len(ua_rows) or not ua_rows[i]:
                continue
            k = u.astimezone(KYIV)
            if f'{k.hour:02d}:{k.minute:02d}' not in ua_rows[i].group(1):
                print(f'MISMATCH {fid} row {i}: EN -> Kyiv {k:%d.%m %H:%M}, UA text "{ua_rows[i].group(1)}"'); bad += 1
        for p, h in ((en_p, en), (ua_p, ua)):
            new = apply(h, utcs)
            if new != h:
                open(p, 'w', encoding='utf-8').write(new); changed += 1
        print(f'{fid}: {sum(1 for u in utcs if u)} timed row(s)')
    print(f'files changed: {changed}, mismatches: {bad}')
    sys.exit(1 if bad else 0)


main()
