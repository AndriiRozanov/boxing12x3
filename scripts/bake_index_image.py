#!/usr/bin/env python3
"""Data for the shareable Index 12x3 picture (js/index-image.js). Reads the finished index block of a fight page.
Usage (preview data): python3 scripts/bake_index_image.py haney-paro uk > data.json
"""
import json, os, re, sys
import segno

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = 'https://boxing12x3.com'
D = json.load(open(f'{R}/data/events.json', encoding='utf-8'))
FIGHT = {f['id']: f for f in D['fights']}
MONTH = {'uk': ['січня','лютого','березня','квітня','травня','червня','липня','серпня','вересня','жовтня','листопада','грудня'],
         'en': ['January','February','March','April','May','June','July','August','September','October','November','December']}
L = {
 'uk': dict(path='ua', k='ua', kicker='ІМОВІРНІСТЬ ПЕРЕМОГИ · 12×3', foot='Кард, прогноз, відсудити', note='Не гарантія результату', copied='Скопійовано',
            f_post='Пост 4:5 · Instagram', f_square='Квадрат 1:1 · X, Telegram', f_story='Сторіз 9:16', date='{d} {m} {y}'),
 'en': dict(path='en', k='en', kicker='WIN PROBABILITY · 12×3', foot='Card, pick, score it', note='Not a guarantee of the result', copied='Copied',
            f_post='Post 4:5 · Instagram', f_square='Square 1:1 · X, Telegram', f_story='Story 9:16', date='{m} {d}, {y}'),
}

def data_for(fid, lk):
    s = L[lk]; k = s['k']; f = FIGHT[fid]
    page = open(f'{R}/{s["path"]}/{fid}.html', encoding='utf-8').read()
    m = re.search(r'<div class="ix"[^>]*data-pa="(\d+)" data-pb="(\d+)"', page)
    pa, pb = int(m.group(1)), int(m.group(2))
    blk = page[page.index('<div class="ix"'):page.index('<!-- /Index -->')]
    rows = []
    for tr in re.findall(r'<tr>(.*?)</tr>', blk, flags=re.S):
        td = re.findall(r'<td class="([^"]*)">([^<]*)</td>|<td>([^<]*)</td>', tr)
        (c1, v1, _), (_, _, lab), (c3, v3, _) = td
        rows.append({'l': v1, 'label': lab, 'r': v3, 'w': ('' if ('w' in c1.split()) == ('w' in c3.split()) else ('r' if 'w' in c1.split() else 'b'))})
    y, mo, d = f['date'].split('-'); v = f['venue']
    city = v['cityUa'] if lk == 'uk' else v['cityEn']
    sn = lambda n: n.split()[-1]
    a, b = f['red'][k], f['blue'][k]
    url = f'{BASE}/{s["path"]}/{fid}'
    qr = segno.make(url + '?utm_source=index_image', error='m', boost_error=False)
    return {'lang': lk, 'slug': fid, 'title': f'{sn(a)} – {sn(b)}', 'names': [sn(a), sn(b)], 'pa': pa, 'pb': pb,
            'dateLine': f'{s["date"].format(d=int(d), m=MONTH[lk][int(mo)-1], y=y)} · {v.get("name") or ""}, {city}', 'rows': rows, 'url': url,
            'qr': [''.join('1' if c else '0' for c in row) for row in qr.matrix], 't': {x: s[x] for x in ('kicker','foot','note','copied','f_post','f_square','f_story')}}

if __name__ == '__main__':
    print(json.dumps(data_for(sys.argv[1], sys.argv[2]), ensure_ascii=False))
