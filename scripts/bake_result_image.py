#!/usr/bin/env python3
"""Add the "Результат вечора" image block to a finished tournament card page (UA and EN).

Usage:
    python3 scripts/bake_result_image.py zuffa-boxing-13
    python3 scripts/bake_result_image.py zuffa-boxing-12 --out /tmp/preview   # test copy, repo untouched

Run it after the tournament is finished and its fights in data/events.json have status "completed" with winner
and method (python3 scripts/build_events.py first). It is safe to run again: the block sits between the markers
<!-- result-image:start --> and <!-- result-image:end -->.
Needs `pip install segno` (QR code). The promoter logo is shown on the picture only for promoters listed in
data/promoters-confirmed.json ({"confirmed": ["zuffa-boxing"]}); otherwise only our logo is used.
"""
import json, os, re, sys, html
import segno

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = 'https://boxing12x3.com'
D = json.load(open(f'{R}/data/events.json', encoding='utf-8'))
CONF = set(json.load(open(f'{R}/data/promoters-confirmed.json', encoding='utf-8')).get('confirmed', []))
FIGHT = {f['id']: f for f in D['fights']}
ORG = {'Zuffa Boxing': 'zuffa-boxing', 'Usyk 17 Promotions': 'usyk-17-promotions'}
MONTH = {'uk': ['січня', 'лютого', 'березня', 'квітня', 'травня', 'червня', 'липня', 'серпня', 'вересня', 'жовтня', 'листопада', 'грудня'],
         'en': ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']}
L = {
 'uk': dict(path='ua', k='ua', kicker='РЕЗУЛЬТАТИ ВЕЧОРА', foot='Кард, рахунки, відсудити', copied='Скопійовано',
            f_post='Пост 4:5 · Instagram', f_square='Квадрат 1:1 · X, Telegram', f_story='Сторіз 9:16',
            strip_t='Картинка з результатами вечора', strip_p='Для соцмереж: промоутер, глядач чи журналіст', open='Зберегти картинку',
            modal_t='Картинка з результатами', save='⬇ Зберегти', copy='Копіювати посилання', share='Поділитись', close='Закрити',
            conf_note='Сторінку підтверджено промоутером: на картинці його логотип і наш', conf_pill='Підтверджено промоутером',
            beat='переміг', draw='Нічия', date='{d} {m} {y}'),
 'en': dict(path='en', k='en', kicker="NIGHT'S RESULTS", foot='Card, scores, score it', copied='Copied',
            f_post='Post 4:5 · Instagram', f_square='Square 1:1 · X, Telegram', f_story='Story 9:16',
            strip_t="Picture of the night's results", strip_p='For social media: promoters, fans and journalists', open='Save image',
            modal_t='Results picture', save='⬇ Save', copy='Copy link', share='Share', close='Close',
            conf_note='Page confirmed by the promoter: his logo and ours are on the picture', conf_pill='Promoter verified',
            beat='beat', draw='Draw', date='{m} {d}, {y}'),
}

def seg(lk, tid):
    s = L[lk]; t = next(x for x in D['tournaments'] if x['id'] == tid)
    fl = [FIGHT[i] for i in t['fights'] if i in FIGHT]
    bad = [f['id'] for f in fl if f['status'] != 'completed' or not (f.get('result') or {}).get('winner')]
    if bad:
        sys.exit(f'Not finished or no winner in data/events.json: {", ".join(bad)}')
    k = s['k']; rows = []
    for f in fl:
        a, b = f['red'][k], f['blue'][k]; r = f['result']; w = r['winner']
        names = {f['red']['ua']: (a, b), f['red']['en']: (a, b), f['blue']['ua']: (b, a), f['blue']['en']: (b, a)}
        if w in names:
            win, lose = names[w]; rows.append({'w': win, 's': f'{s["beat"]} {lose}', 'm': r.get('method') or ''})
        else:
            rows.append({'w': f'{a} – {b}', 's': w if w else s['draw'], 'm': r.get('method') or ''})
    y, m, d = t['startDate'].split('-')
    v = fl[0]['venue']; city = v['cityUa'] if lk == 'uk' else v['cityEn']
    when = s['date'].format(d=int(d), m=MONTH[lk][int(m) - 1], y=y)
    arena = t.get('venue') or v.get('name') or ''
    pid = ORG.get(t.get('organizer'))
    url = f'{BASE}{t["urls"][k]}?utm_source=result_image'
    qr = segno.make(url, error='m', boost_error=False)
    matrix = [''.join('1' if c else '0' for c in row) for row in qr.matrix]
    data = {'lang': lk, 'slug': tid, 'title': t['name'][k], 'dateLine': f'{when} · {arena}, {city}', 'rows': rows,
            'url': f'{BASE}{t["urls"][k]}', 'qr': matrix,
            'promoter': {'name': t.get('organizer'), 'logo': f'/images/cards/{pid}.png' if pid else None, 'confirmed': bool(pid and pid in CONF)},
            't': {x: s[x] for x in ('kicker', 'foot', 'copied', 'f_post', 'f_square', 'f_story')}}
    return s, data

CSS = """
.ri-strip{background:var(--card);border:0.5px solid var(--border);border-radius:var(--r);padding:14px 16px;margin:0 0 20px;display:flex;align-items:center;gap:14px;flex-wrap:wrap}
.ri-strip .ri-txt{flex:1;min-width:200px}.ri-strip b{display:block;font-size:14px;font-weight:700}.ri-strip span{display:block;font-size:12px;color:var(--muted);margin-top:2px}
.ri-btn{font:inherit;font-size:13px;font-weight:700;padding:10px 16px;border-radius:8px;border:0.5px solid var(--border);background:#fff;color:var(--text);cursor:pointer}
.ri-btn.red{background:var(--red);border-color:var(--red);color:#fff}
.ri-modal{position:fixed;inset:0;background:rgba(0,0,0,.55);z-index:50;display:flex;align-items:center;justify-content:center;padding:16px}
.ri-modal[hidden]{display:none}
.ri-box{background:#fff;border-radius:16px;width:100%;max-width:440px;max-height:calc(100vh - 32px);overflow:auto;padding:18px;position:relative}
.ri-box h3{font-size:16px;font-weight:800;margin:0 28px 12px 0}
.ri-x{position:absolute;top:10px;right:12px;border:0;background:none;font-size:22px;line-height:1;color:#777;cursor:pointer;padding:6px}
.ri-tabs{display:flex;gap:6px;flex-wrap:wrap;margin-bottom:12px}
.ri-tabs button{font:inherit;font-size:12px;font-weight:600;padding:6px 11px;border-radius:20px;border:0.5px solid var(--border);background:#fff;color:#555;cursor:pointer}
.ri-tabs button.on{background:#111;border-color:#111;color:#fff}
.ri-prev{background:#eee;border-radius:10px;padding:10px;display:flex;justify-content:center}
.ri-prev canvas{display:block;max-width:100%;max-height:52vh;width:auto;height:auto;border-radius:6px}
.ri-note{font-size:11.5px;color:#777;text-align:center;margin:10px 0 0}
.ri-pill{display:inline-flex;align-items:center;gap:6px;background:#fbf1cf;color:#6b520a;font-size:11.5px;font-weight:700;border-radius:20px;padding:4px 10px;margin-top:6px}
.ri-pill i{width:12px;height:12px;border-radius:50%;background:#c9a227;display:inline-block}
.ri-acts{display:flex;gap:8px;margin-top:14px;flex-wrap:wrap}.ri-acts .ri-btn{flex:1;min-width:130px;text-align:center}
"""

def block(lk, data, s):
    conf = ''
    if data['promoter']['confirmed']:
        conf = f'<p class="ri-note">{html.escape(s["conf_note"])}<br><span class="ri-pill"><i></i>{html.escape(s["conf_pill"])}</span></p>'
    tabs = ''.join(f'<button type="button" data-f="{k}">{html.escape(s[l])}</button>' for k, l in (('post', 'f_post'), ('square', 'f_square'), ('story', 'f_story')))
    js = json.dumps(data, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')
    return f"""<!-- result-image:start -->
<style>{CSS}</style>
<div class="ri-strip"><div class="ri-txt"><b>{html.escape(s['strip_t'])}</b><span>{html.escape(s['strip_p'])}</span></div><button type="button" class="ri-btn red" id="ri-open">{html.escape(s['open'])}</button></div>
<div class="ri-modal" id="ri-modal" hidden role="dialog" aria-modal="true" aria-labelledby="ri-h"><div class="ri-box">
<button type="button" class="ri-x" id="ri-close" aria-label="{html.escape(s['close'])}">×</button>
<h3 id="ri-h">{html.escape(s['modal_t'])}</h3><div class="ri-tabs" id="ri-tabs">{tabs}</div>
<div class="ri-prev"><canvas id="ri-canvas"></canvas></div>{conf}
<div class="ri-acts"><button type="button" class="ri-btn red" id="ri-save">{html.escape(s['save'])}</button><button type="button" class="ri-btn" id="ri-share" hidden>{html.escape(s['share'])}</button><button type="button" class="ri-btn" id="ri-copy">{html.escape(s['copy'])}</button></div>
</div></div>
<script type="application/json" id="result-image-data">{js}</script>
<script src="/js/result-image.js" defer></script>
<!-- result-image:end -->
"""

def end_of_div(page, start):
    depth = 0
    for m in re.finditer(r'<div\b|</div>', page[start:]):
        depth += 1 if m.group(0) != '</div>' else -1
        if depth == 0:
            return start + m.end()
    raise ValueError('unbalanced prog block')

def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    out = sys.argv[sys.argv.index('--out') + 1] if '--out' in sys.argv else None
    if out and out in args: args.remove(out)
    tid = args[0]
    for lk in ('uk', 'en'):
        s, data = seg(lk, tid)
        src = f'{R}/{s["path"]}/cards/{tid}.html'
        page = open(src, encoding='utf-8').read()
        page = re.sub(r'<!-- result-image:start -->.*?<!-- result-image:end -->\n?', '', page, flags=re.S)
        i = page.index('<div class="prog">')
        j = end_of_div(page, i)
        page = page[:j] + '\n\n' + block(lk, data, s) + page[j:]
        assert chr(8212) not in block(lk, data, s)
        dst = f'{out}/{s["path"]}/cards/{tid}.html' if out else src
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        open(dst, 'w', encoding='utf-8').write(page)
        print(f'{dst}: {len(data["rows"])} rows, promoter confirmed={data["promoter"]["confirmed"]}')

if __name__ == '__main__':
    main()
