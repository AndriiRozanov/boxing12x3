#!/usr/bin/env python3
"""Bake ua/tools.html and en/tools.html: a hub of all site tools.  Run: python3 scripts/bake_tools.py"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bake_calendar as C

R, S, BASE, esc = C.R, C.S, C.BASE, C.esc
T = {
 'uk': dict(title='Інструменти для боксерських вболівальників | Boxing 12×3', h1='Інструменти', sub='Інструменти',
   desc='Інструменти Boxing 12×3: рейтинги організацій, порівняння габаритів боксерів, цей день в боксі, профілі легенд, суддівська картка й довідник боксу.',
   lead='Усе, що допомагає стежити за боксом і розбиратися в ньому.', crumb='Інструменти',
   items=[('🏆', 'Рейтинги', 'WBC, WBA, IBF, WBO та The Ring за дивізіонами', '/ua/rankings'),
          ('📏', 'Порівняння габаритів', 'Зріст і розмах боксерів поруч', '/height-compare'),
          ('📅', 'Цей день в боксі', 'Визначні дати та бої за календарем', '/ua/boxing-history'),
          ('🥊', 'Боксери', 'Профілі легенд: рекорд, титули, останній бій', '/ua/boxers'),
          ('📝', 'Суддівська картка', 'Відсуджуйте бій раунд за раундом і діліться карткою', '/ua/scorecard'),
          ('📖', 'Довідник боксу', 'Правила, пояси, терміни та вагові категорії', '/ua/guide')]),
 'en': dict(title='Boxing Tools for Fans | Boxing 12×3', h1='Tools', sub='Tools',
   desc='Boxing 12×3 tools: organisation rankings, boxer height and reach comparison, this day in boxing, legend profiles, an interactive scorecard and a boxing guide.',
   lead='Everything that helps you follow boxing and understand it.', crumb='Tools',
   items=[('🏆', 'Rankings', 'WBC, WBA, IBF, WBO and The Ring by division', '/en/rankings'),
          ('📏', 'Height compare', 'Boxers\' height and reach side by side', '/en/height-compare'),
          ('📅', 'This day in boxing', 'Famous dates and fights by calendar', '/en/boxing-history'),
          ('🥊', 'Boxers', 'Legend profiles: record, titles, last fight', '/en/boxers'),
          ('📝', 'Scorecard', 'Score a fight round by round and share your card', '/en/scorecard'),
          ('📖', 'Boxing guide', 'Rules, belts, terms and weight classes', '/en/guide')]),
}
EXTRA = '.tgrid{display:grid;grid-template-columns:1fr;gap:10px;margin-top:6px}@media(min-width:640px){.tgrid{grid-template-columns:1fr 1fr}}.tc{display:flex;align-items:center;gap:14px;background:var(--card);border:0.5px solid var(--border);border-radius:var(--r);padding:16px}a.tc:hover{background:#fcfbf9}.tc .ic{font-size:24px;width:40px;height:40px;display:flex;align-items:center;justify-content:center;background:var(--bg);border-radius:10px;flex-shrink:0}.tc b{display:block;font-size:14.5px;font-weight:800}.tc small{display:block;font-size:12px;color:var(--muted);margin-top:2px;line-height:1.4}.tc .go{margin-left:auto;color:var(--muted);font-size:16px}'

def build(lk):
    s, t = S[lk], T[lk]; u = lk == 'uk'; k = s['path']; url = f'{BASE}/{k}/tools'
    cards = ''.join(f'<a class="tc" href="{h}"><div class="ic">{ic}</div><div><b>{esc(n)}</b><small>{esc(d)}</small></div><span class="go">›</span></a>' for ic, n, d, h in t['items'])
    ld = {'@context': 'https://schema.org', '@graph': [
        {'@type': 'CollectionPage', 'name': t['h1'], 'description': t['desc'], 'url': url, 'inLanguage': s['lang'],
         'mainEntity': {'@type': 'ItemList', 'numberOfItems': len(t['items']), 'itemListElement': [{'@type': 'ListItem', 'position': i + 1, 'url': BASE + h, 'name': n} for i, (ic, n, d, h) in enumerate(t['items'])]}},
        {'@type': 'BreadcrumbList', 'itemListElement': [{'@type': 'ListItem', 'position': 1, 'name': s['crumb'][0], 'item': BASE + ('/' if u else '/en')}, {'@type': 'ListItem', 'position': 2, 'name': t['crumb'], 'item': url}]}]}
    footer = ''.join(f'<a href="{h}">{x}</a>' for h, x in s['footer'])
    page = f"""<!DOCTYPE html>
<html lang="{s['lang']}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{esc(t['title'])}</title>
<link rel="icon" href="/favicon.ico" sizes="48x48">
<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32.png">
<link rel="icon" type="image/png" sizes="192x192" href="/icon-192.png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<meta name="description" content="{esc(t['desc'])}">
<link rel="canonical" href="{url}">
<link rel="alternate" hreflang="uk" href="{BASE}/ua/tools">
<link rel="alternate" hreflang="en" href="{BASE}/en/tools">
<link rel="alternate" hreflang="x-default" href="{BASE}/en/tools">
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False, separators=(',', ':'))}</script>
<meta property="og:type" content="website">
<meta property="og:url" content="{url}">
<meta property="og:title" content="{esc(t['title'])}">
<meta property="og:description" content="{esc(t['desc'])}">
<meta property="og:image" content="{BASE}/{s['og']}">
<meta property="og:locale" content="{s['loc']}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(t['title'])}">
<meta name="twitter:description" content="{esc(t['desc'])}">
<meta name="twitter:image" content="{BASE}/{s['og']}">
<script async src="https://www.googletagmanager.com/gtag/js?id=G-GYWWVSZKGY"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','G-GYWWVSZKGY');</script>
<link rel="preload" href="/fonts/manrope-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/fonts/oswald-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/fonts/manrope-cyrillic.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/fonts/fonts.css">
<style>{C.CSS}{EXTRA}</style>
</head>
<body>
<div class="wrap">
<div class="lang-row">
  <a class="lang-btn{' on' if not u else ''}" href="/en/tools">EN</a>
  <a class="lang-btn{' on' if u else ''}" href="/ua/tools">UA</a>
</div>
<div class="brand">
  <a href="{s['home']}"><div class="brand-name">Boxing 12×3</div></a>
  <div class="brand-sub">{t['sub']}</div>
</div>
<div class="breadcrumb"><a href="{s['home']}">{s['crumb'][0]}</a> / {t['crumb']}</div>
<h1>{t['h1']}</h1>
<p class="lead">{t['lead']}</p>
<div class="tgrid">{cards}</div>
<div class="site-footer">{footer}</div>
</div>
</body>
</html>
"""
    assert chr(8212) not in page
    open(f'{R}/{k}/tools.html', 'w', encoding='utf-8').write(page)
    print(f'{k}/tools.html')

if __name__ == '__main__':
    for lk in ('uk', 'en'): build(lk)
