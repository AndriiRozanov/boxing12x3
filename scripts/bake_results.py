#!/usr/bin/env python3
"""Bake ua/results.html and en/results.html: finished fights, newest first, with search.

Run after scripts/build_events.py:  python3 scripts/bake_results.py
Reuses the calendar CSS and helpers (scripts/bake_calendar.py).
"""
import json, os, sys, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bake_calendar as C

R, D, S, BASE, esc = C.R, C.D, C.S, C.BASE, C.esc
T = {
 'uk': dict(title='Результати боксерських боїв: переможці й методи | Boxing 12×3', h1='Результати боксерських боїв', sub='Результати боїв',
   desc='Результати боксерських боїв: переможці, методи перемоги, дати й місця проведення. Пошук за боксером, турніром чи містом.',
   lead='Завершені бої з переможцями й методами. Натисніть на бій, щоб побачити карту вечора, рахунки та суддівську картку.',
   crumb='Результати', search='Боксер, турнір, місто…', empty='За цим запитом результатів не знайдено.', won='переміг', draw='нічия', count='результатів',
   cal='Календар майбутніх боїв →', wait='Очікуємо результат', waitr='Очікуємо результат', up='Майбутні', past='Минулі', more='Показати ще', all='Усі', mon=['Січень','Лютий','Березень','Квітень','Травень','Червень','Липень','Серпень','Вересень','Жовтень','Листопад','Грудень']),
 'en': dict(title='Boxing Results: Winners and Methods | Boxing 12×3', h1='Boxing results', sub='Fight results',
   desc='Boxing results: winners, methods of victory, dates and venues. Search by boxer, event or city.',
   lead='Finished fights with winners and methods. Open a fight for the card, the scores and the scorecard.',
   crumb='Results', search='Boxer, event, city…', empty='No results match this search.', won='won', draw='draw', count='results',
   cal='Upcoming fights calendar →', wait='Awaiting result', waitr='Awaiting result', up='Upcoming', past='Past', more='Show more', all='All', mon=['January','February','March','April','May','June','July','August','September','October','November','December']),
}

GEN = json.load(open(f'{R}/data/names_gen_ua.json', encoding='utf-8'))

def method(m):
    return (m or '').replace('ТКО', 'TKO').replace('КО', 'KO').replace(' · Раунд ', ' ').replace(' · Round ', ' ').strip()

def row(f, lk, pending=False):
    s, t = S[lk], T[lk]; u = lk == 'uk'
    k = 'ua' if u else 'en'
    a, b = f['red'][k], f['blue'][k]
    w = (f.get('result') or {}).get('winner')
    if w == f['red']['ua'] or w == f['red']['en']: wn = a
    elif w == f['blue']['ua'] or w == f['blue']['en']: wn = b
    else: wn = None
    m = method((f.get('result') or {}).get('method'))
    mt = m.replace(' · ', ', ')
    if pending: res = t['waitr']
    elif wn and u and wn in GEN: res = f'Перемога {GEN[wn]}' + (f' · {mt}' if mt else '')
    elif wn:
        if u: print('no genitive for', wn)
        res = (f'Перемога: {wn}' if u else f'Winner: {wn}') + (f' · {mt}' if mt else '')
    else: res = t['draw'].capitalize() + (f' · {mt}' if mt else '')
    rs_html = esc(res) if pending else C.ns_wrap(esc(res), lk)
    v = f['venue']; city = v['cityUa'] if u else v['cityEn']
    iso = v.get('countryIso') or ''
    flag = f'<img class="flag" src="/images/flags/{iso.lower()}.png" width="16" height="12" alt="" loading="lazy"> ' if iso else ''
    div = (f['division'] or {}).get(k) or ''
    meta = flag + esc(city) + (f' · {esc(div)}' if div else '')
    d = datetime.date.fromisoformat(f['date'])
    dc = f'<b>{d.day}</b><small>{s["months"][d.month-1][:3] if u else s["months"][d.month-1]}</small>'
    tour = C.TOUR.get(f.get('tournamentId'))
    q = ' '.join([f['red']['ua'], f['red']['en'], f['blue']['ua'], f['blue']['en'], (tour['name']['ua'] or '') if tour else '', (tour['name']['en'] or '') if tour else '',
                  v['cityUa'] or '', v['cityEn'] or '', v.get('name') or '']).lower()
    ym = f['date'][:7]
    if pending:
        if f['startUtc']: st = (datetime.datetime.strptime(f['startUtc'], '%Y-%m-%dT%H:%MZ') + datetime.timedelta(hours=6)).strftime('%Y-%m-%dT%H:%MZ')
        else: st = (datetime.datetime.fromisoformat(f['date']) + datetime.timedelta(days=1, hours=6)).strftime('%Y-%m-%dT%H:%MZ')
        return (f'<a class="fr wait" data-from="{st}" href="{f["urls"][k]}"><div class="ft">{dc}</div><div class="fd"></div><div class="fi">'
                f'<div class="fp">{esc(a)}<span class="vs">–</span>{esc(b)}</div><div class="rs">{rs_html}</div><div class="fm">{meta}</div></div><div class="fa">›</div></a>')
    return (f'<a class="fr" data-y="{f["date"][:4]}" data-ym="{ym}" href="{f["urls"][k]}" data-q="{esc(q)}"><div class="ft">{dc}</div><div class="fd"></div><div class="fi">'
            f'<div class="fp">{esc(a)}<span class="vs">–</span>{esc(b)}</div><div class="rs">{rs_html}</div><div class="fm">{meta}</div></div><div class="fa">›</div></a>')

JS = r"""
(function(){
var PAGE=30,rows=[].slice.call(document.querySelectorAll('#list .fr')),shown=PAGE,yr='',q='';
function norm(s){return String(s).toLowerCase().replace(/[\u2019\u02bc\u2018\u0060\u00b4]/g,"'");}
function render(){
 var n=0,total=0;
 rows.forEach(function(r){
  var ok=(!yr||r.getAttribute('data-ym')===yr)&&(!q||norm(r.getAttribute('data-q')).indexOf(q)>=0);
  if(ok){total++;if(n<shown){r.style.display='';n++;}else{r.style.display='none';}}else{r.style.display='none';}
 });
 [].slice.call(document.querySelectorAll('#list .grp')).forEach(function(g){var any=false;[].slice.call(g.querySelectorAll('.fr')).forEach(function(r){if(r.style.display!=='none')any=true;});g.style.display=any?'':'none';});
 document.getElementById('more').className='more'+(total>n?' show':'');
 document.getElementById('empty').className='empty'+(total?'':' show');
}
document.getElementById('q').addEventListener('input',function(e){q=norm(e.target.value.trim());shown=PAGE;render();});
document.getElementById('more').addEventListener('click',function(){shown+=PAGE;render();});
[].slice.call(document.querySelectorAll('#years .chip')).forEach(function(c){c.addEventListener('click',function(){
 yr=this.getAttribute('data-yr');shown=PAGE;
 [].slice.call(document.querySelectorAll('#years .chip')).forEach(function(x){x.className='chip'+(x===c?' on':'');});render();});});
render();
var pend=document.getElementById('pend');
if(pend){var nowt=Date.now(),any=false;[].slice.call(pend.querySelectorAll('.fr')).forEach(function(r){var on=Date.parse(r.getAttribute('data-from'))<=nowt;r.style.display=on?'':'none';if(on)any=true;});if(any)pend.className='pend show';}
})();
"""

def build(lk):
    s, t = S[lk], T[lk]; u = lk == 'uk'
    fl = [f for f in D['fights'] if f['status'] == 'completed' and f['red']['ua'] and (f.get('result') or {}).get('winner') and f['urls'].get(k := ('ua' if u else 'en'))]
    fl.sort(key=lambda f: (f['date'], f['startUtc'] or ''), reverse=True)
    today = datetime.datetime.now(datetime.timezone.utc).date()
    pend = [f for f in D['fights'] if f['status'] == 'scheduled' and f['red']['ua'] and f['urls'].get(k) and (today - datetime.timedelta(days=14)).isoformat() <= f['date'] <= today.isoformat()]
    pend.sort(key=lambda f: (f['date'], f['startUtc'] or ''))
    pend_html = (f'<div class="pend" id="pend"><div class="dayh"><b>{t["wait"]}</b></div><div class="list">{"".join(row(f, lk, True) for f in pend)}</div></div>') if pend else ''
    groups = {}
    for f in fl: groups.setdefault(f['date'][:7], []).append(f)
    body = ''
    for ym, g in sorted(groups.items(), reverse=True):
        y, m = int(ym[:4]), int(ym[5:])
        body += f'<div class="grp" data-y="{y}"><div class="dayh"><b>{t["mon"][m-1]} {y}</b><span>{C.plural(lk, len(g))}</span></div><div class="list">{"".join(row(f, lk) for f in g)}</div></div>'
    yms = sorted({f['date'][:7] for f in fl}, reverse=True)
    ychips = f'<button type="button" class="chip on" data-yr="">{t["all"]}</button>' + ''.join(f'<button type="button" class="chip" data-yr="{ym}">{t["mon"][int(ym[5:])-1][:3]} {ym[:4]}</button>' for ym in yms)
    k = s['path']; url = f'{BASE}/{k}/results'
    items = [{'@type': 'ListItem', 'position': i + 1, 'url': BASE + f['urls'][('ua' if u else 'en')], 'name': f"{f['red']['ua' if u else 'en']} – {f['blue']['ua' if u else 'en']}"} for i, f in enumerate(fl[:50])]
    ld = {'@context': 'https://schema.org', '@graph': [
        {'@type': 'CollectionPage', 'name': t['h1'], 'description': t['desc'], 'url': url, 'inLanguage': s['lang'], 'mainEntity': {'@type': 'ItemList', 'numberOfItems': len(items), 'itemListElement': items}},
        {'@type': 'BreadcrumbList', 'itemListElement': [{'@type': 'ListItem', 'position': 1, 'name': s['crumb'][0], 'item': BASE + ('/' if u else '/en')}, {'@type': 'ListItem', 'position': 2, 'name': t['crumb'], 'item': url}]}]}
    footer = ''.join(f'<a href="{h}">{x}</a>' for h, x in s['footer'])
    css = C.CSS + '.more{display:none;width:100%;margin:14px 0 4px;font:inherit;font-size:13px;font-weight:700;padding:11px;border:0.5px solid var(--border);border-radius:10px;background:#fff;color:#333;cursor:pointer}.more.show{display:block}#years::-webkit-scrollbar{display:none}#years .chip{flex:0 0 auto}.rs{font-size:12.5px;font-weight:600;color:#333;margin-top:3px}.grp{margin-bottom:6px}.grp .dayh:first-child{margin-top:18px}'
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
<link rel="alternate" hreflang="uk" href="{BASE}/ua/results">
<link rel="alternate" hreflang="en" href="{BASE}/en/results">
<link rel="alternate" hreflang="x-default" href="{BASE}/en/results">
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
<style>{css}</style>
{C.NS_HEAD}
</head>
<body>
<div class="wrap">
<div class="lang-row">
  <a class="lang-btn{' on' if not u else ''}" href="/en/results">EN</a>
  <a class="lang-btn{' on' if u else ''}" href="/ua/results">UA</a>
</div>
<div class="brand">
  <a href="{s['home']}"><div class="brand-name">Boxing 12×3</div></a>
  <div class="brand-sub">{t['sub']}</div>
</div>
<div class="breadcrumb"><a href="{s['home']}">{s['crumb'][0]}</a> / {t['crumb']}</div>
<h1>{t['h1']}</h1>
<div class="chips seg"><a class="chip" href="/{k}/calendar">{t['up']}</a><a class="chip on" href="/{k}/results">{t['past']}</a></div>
<p class="lead">{t['lead']}</p>
{C.ns_bar(lk)}
<div class="filters"><div class="ftop" style="margin-bottom:0"><div class="search">🔎 <input id="q" type="search" placeholder="{esc(t['search'])}" aria-label="{esc(t['search'])}" autocomplete="off"></div></div></div>
<div class="chips" id="years" style="margin:12px 0 4px;flex-wrap:nowrap;overflow-x:auto">{ychips}</div>
{pend_html}<div id="list">{body}</div>
<button type="button" class="more" id="more">{t['more']}</button>
<div class="empty" id="empty"><div>{t['empty']}</div></div>
<p class="lead" style="margin-top:18px"><a href="/{k}/calendar" style="color:var(--red);font-weight:600">{t['cal']}</a></p>
<div class="site-footer">{footer}</div>
</div>
<script>{JS}</script>
</body>
</html>
"""
    assert chr(8212) not in page
    open(f'{R}/{k}/results.html', 'w', encoding='utf-8').write(page)
    print(f'{k}/results.html: {len(fl)} fights')

if __name__ == '__main__':
    for lk in ('uk', 'en'): build(lk)
