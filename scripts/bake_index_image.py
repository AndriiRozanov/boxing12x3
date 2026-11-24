#!/usr/bin/env python3
"""Data for the shareable Index 12x3 picture (js/index-image.js). Reads the finished index block of a fight page.
Usage (preview data): python3 scripts/bake_index_image.py haney-paro uk > data.json
"""
import json, os, re, sys, html, glob

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = 'https://boxing12x3.com'
D = json.load(open(f'{R}/data/events.json', encoding='utf-8'))
FIGHT = {f['id']: f for f in D['fights']}
MONTH = {'uk': ['січня','лютого','березня','квітня','травня','червня','липня','серпня','вересня','жовтня','листопада','грудня'],
         'en': ['January','February','March','April','May','June','July','August','September','October','November','December']}
L = {
 'uk': dict(path='ua', k='ua', kicker='ІНДЕКС 12×3 · ІМОВІРНІСТЬ ПЕРЕМОГИ', foot='Кард, прогноз, відсудити', note='Не гарантія результату', copied='Скопійовано',
            f_post='Пост 4:5', f_square='Пост 1:1', f_story='Сторіс 9:16', date='{d} {m} {y}',
            open='Поділитися індексом 12×3',
            modal_t='Поділитися індексом 12×3', save='⬇ Зберегти', copy='Копіювати посилання', share='Поділитись', close='Закрити'),
 'en': dict(path='en', k='en', kicker='INDEX 12×3 · WIN PROBABILITY', foot='Card, pick, score it', note='Not a guarantee of the result', copied='Copied',
            f_post='Post 4:5', f_square='Post 1:1', f_story='Story 9:16', date='{m} {d}, {y}',
            open='Share 12×3 Index',
            modal_t='Share 12×3 Index', save='⬇ Save', copy='Copy link', share='Share', close='Close'),
}

FACTS = {'uk': [('Рекорд', 'Рекорд'), ('Дострокові', 'Нокаути'), ('_age', 'Вік'), ('Розмах', 'Розмах')],
         'en': [('Record', 'Record'), ('Stoppages', 'Knockouts'), ('_age', 'Age'), ('Reach', 'Reach')]}

def data_for(fid, lk):
    s = L[lk]; k = s['k']; f = FIGHT[fid]
    page = open(f'{R}/{s["path"]}/{fid}.html', encoding='utf-8').read()
    m = re.search(r'<div class="ix"[^>]*data-pa="(\d+)" data-pb="(\d+)"', page)
    pa, pb = int(m.group(1)), int(m.group(2))
    fr = re.search(r'<div class="fcard-rows">(.*?)<!-- Stats -->', page, re.S).group(1)
    facts = {}
    for row in fr.split('<div class="frow">')[1:]:
        mm = re.search(r'<span class="fv r">(.*?)</span>\s*(?:</span>)?\s*<div class="flbl[^"]*">\s*<span>([^<]*)</span>.*?<span class="fv b">(.*?)\n\s*</div>', row, re.S)
        if mm: facts[mm.group(2)] = (re.split('<', mm.group(1))[0].strip(), re.split('<', mm.group(3))[0].strip())
    ages = [re.match(r'(\d+)', x).group(1) if re.match(r'(\d+)', x) else None for x in re.findall(r'<div class="f-info">(.*?)</div>', page)[:2]]
    fk = FACTS[lk]
    rows = []
    for key, lab in fk:
        v = ages if key == '_age' else facts.get(key)
        if not v or not v[0] or not v[1] or '–' in (v[0], v[1]): continue
        rows.append({'l': v[0], 'label': lab, 'r': v[1]})
    y, mo, d = f['date'].split('-'); v = f['venue']
    city = v['cityUa'] if lk == 'uk' else v['cityEn']
    sn = lambda n: n.split()[-1]
    a, b = f['red'][k], f['blue'][k]
    url = f'{BASE}/{s["path"]}/{fid}'
    return {'lang': lk, 'slug': fid, 'title': f'{sn(a)} – {sn(b)}', 'names': [sn(a), sn(b)], 'pa': pa, 'pb': pb,
            'dateLine': f'{s["date"].format(d=int(d), m=MONTH[lk][int(mo)-1], y=y)} · {v.get("name") or ""}, {city}', 'rows': rows, 'url': url,
            't': {x: s[x] for x in ('kicker','foot','note','copied','f_post','f_square','f_story')}}

CSS_EXTRA = '.ix-share{text-align:center;margin:0 0 20px}.ix-share .ri-btn{padding:11px 22px}'
CSS = open(f'{R}/scripts/bake_result_image.py', encoding='utf-8').read().split('CSS = """')[1].split('"""')[0]

def block(lk, data):
    s = L[lk]
    tabs = ''.join(f'<button type="button" data-f="{k}">{html.escape(s[l])}</button>' for k, l in (('post', 'f_post'), ('square', 'f_square'), ('story', 'f_story')))
    js = json.dumps(data, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')
    return f"""<!-- index-image:start -->
<style>{CSS}{CSS_EXTRA}</style>
<div class="ix-share"><button type="button" class="ri-btn" id="ri-open">{html.escape(s['open'])}</button></div>
<div class="ri-modal" id="ri-modal" hidden role="dialog" aria-modal="true" aria-labelledby="ri-h"><div class="ri-box">
<button type="button" class="ri-x" id="ri-close" aria-label="{html.escape(s['close'])}">×</button>
<h3 id="ri-h">{html.escape(s['modal_t'])}</h3><div class="ri-tabs" id="ri-tabs">{tabs}</div>
<div class="ri-prev"><canvas id="ri-canvas"></canvas></div>
<div class="ri-acts"><button type="button" class="ri-btn red" id="ri-save">{html.escape(s['save'])}</button><button type="button" class="ri-btn" id="ri-share" hidden>{html.escape(s['share'])}</button><button type="button" class="ri-btn" id="ri-copy">{html.escape(s['copy'])}</button></div>
</div></div>
<script type="application/json" id="index-image-data">{js}</script>
<script src="/js/index-image.js" defer></script>
<!-- index-image:end -->
"""

def main():
    n = 0
    for fid in sorted(FIGHT):
        for lk in ('uk', 'en'):
            path = f'{R}/{L[lk]["path"]}/{fid}.html'
            if not os.path.exists(path): continue
            page = open(path, encoding='utf-8').read()
            if 'data-pa="' not in page or '<!-- /Index -->' not in page: continue
            page = re.sub(r'<!-- index-image:start -->.*?<!-- index-image:end -->\n?', '', page, flags=re.S)
            blk = block(lk, data_for(fid, lk))
            assert chr(8212) not in blk
            page = page.replace('<!-- /Index -->', '<!-- /Index -->\n' + blk.rstrip('\n'), 1)
            open(path, 'w', encoding='utf-8').write(page); n += 1; print(path)
    print(n, 'pages')

if __name__ == '__main__':
    if len(sys.argv) > 2: print(json.dumps(data_for(sys.argv[1], sys.argv[2]), ensure_ascii=False))
    else: main()
