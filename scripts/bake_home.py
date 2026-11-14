#!/usr/bin/env python3
"""Bake the events-first home pages: index.html (UA) and en/index.html (EN).

Run after scripts/build_events.py:
    python3 scripts/build_events.py && python3 scripts/bake_calendar.py && python3 scripts/bake_home.py

Everything is written into the HTML (Google, no-JS). A small page script only picks the first event
that has not finished yet, hides rows that are already in the past, and shows times in the reader's
time zone. The scorecard lives at /ua/scorecard and /en/scorecard.
"""
import json, os, re, datetime, html
from zoneinfo import ZoneInfo

import bake_calendar as C

R = C.R
D = C.D
BASE = C.BASE
esc = C.esc
KYIV = ZoneInfo('Europe/Kyiv')
NOW = datetime.datetime.now(datetime.timezone.utc)
TODAY = NOW.astimezone(KYIV).date()
TOUR = C.TOUR
FIGHT = {f['id']: f for f in D['fights']}
CSS = open(f'{R}/scripts/home.css', encoding='utf-8').read()
SC_IDS = set(re.findall(r"\bid:\s*'([^']+)'", open(f'{R}/ua/scorecard.html', encoding='utf-8').read()))

H = {
 'uk': dict(
   title='Boxing 12×3: календар боксу, час початку й результати',
   desc='Календар боксерських боїв і турнірів: дата, час початку у вашому часовому поясі, де дивитись і результати. Кард кожного вечора й суддівська картка.',
   h1='Карди, час і результати боксерських турнірів',
   nav=[('Події', '#events'), ('Календар', '/ua/calendar'), ('Результати', '/ua/cards'), ('Промоутери', '/ua/promoters'), ('Інструменти', '#tools')],
   sec_events='Найближча подія', sec_next='Найближчі', sec_results='Нещодавні результати', sec_promo='Промоутери', sec_tools='Інструменти',
   all_cal='Увесь календар →', all_res='Усі результати →', all_promo='Всі промоутери →',
   tz_auto='визначено автоматично', tz_chosen='обрано вами', yourtime='Ваш час', tz_default='Київ', tz_fixed='Час показано за Києвом',
   today_eve='Сьогодні ввечері', today='Сьогодні', soon='Найближча подія',
   btn_card='Кард і де дивитись', btn_score='Відсудити', won='Переміг', fights=('бій', 'бої', 'боїв'), tours=('турнір', 'турніри', 'турнірів'),
   cta_t='Ви організовуєте турніри?', cta_p='Безкоштовно зробимо сторінку вашого карду з усіма деталями перегляду. Вашу подію побачать вболівальники з усього світу.', cta_b='Написати нам', cta_href='/contact',
   sc_t='Відсуди бій сам', sc_p='Став бали раунд за раундом і ділися своєю карткою. Без реєстрації.', sc_b='Відкрити суддівську картку', sc_href='/ua/scorecard',
   tools=[('📏', 'Порівняння габаритів', 'Зріст і розмах боксерів', '/height-compare'), ('🥊', 'Боксери', 'Профілі легенд', '/ua/boxers'),
          ('🏆', 'Рейтинги боксу', 'WBC, WBA, IBF, WBO, Ring', '/ua/rankings'), ('📅', 'Цей день в боксі', 'Визначні дати', '/ua/boxing-history'),
          ('📖', 'Довідник боксу', 'Правила, пояси, терміни', '/ua/guide')],
   tba='Час уточнюється', months=['січ', 'лют', 'бер', 'кві', 'тра', 'чер', 'лип', 'сер', 'вер', 'жов', 'лис', 'гру'],
   mfull=['січня', 'лютого', 'березня', 'квітня', 'травня', 'червня', 'липня', 'серпня', 'вересня', 'жовтня', 'листопада', 'грудня'],
   chips_near='📍 Біля мене', chip_all='Усі', path='ua', other_path='en', home='/', other_home='/en', loc='uk_UA', og='og-default.png', loc_js='uk',
   seo='Boxing 12×3 – календар боксерських боїв: дата й час початку у вашому часовому поясі, країна, де дивитись і результати турнірів. Є також <a href="/ua/scorecard">суддівська картка</a> для відсуджування боїв раунд за раундом.',
   footer=[('/about', 'Про проєкт'), ('/ua/rankings', 'Рейтинги'), ('/contact', 'Контакти'), ('/widget', 'Віджет'), ('/privacy', 'Privacy')],
   conts={'Europe': 'Європа', 'Asia': 'Азія', 'North America': 'Пн. Америка', 'South America': 'Пд. Америка', 'Africa': 'Африка', 'Oceania': 'Океанія'},
   rounds='раундів', sub_ua_en=''),
 'en': dict(
   title='Boxing 12×3: boxing calendar, start times and results',
   desc='Boxing fight and event calendar: date, start time in your own time zone, where to watch and results. The card for every night, plus a round-by-round scorecard.',
   h1='Fight cards, times and results of boxing events',
   nav=[('Events', '#events'), ('Calendar', '/en/calendar'), ('Results', '/en/cards'), ('Promoters', '/en/promoters'), ('Tools', '#tools')],
   sec_events='Next event', sec_next='Coming up', sec_results='Recent results', sec_promo='Promoters', sec_tools='Tools',
   all_cal='Full calendar →', all_res='All results →', all_promo='All promoters →',
   tz_auto='detected automatically', tz_chosen='chosen by you', yourtime='Your local time', tz_default='Kyiv', tz_fixed='Times shown in UTC',
   today_eve='Tonight', today='Today', soon='Next event',
   btn_card='Card and where to watch', btn_score='Score it', won='Winner', fights=('fight', 'fights', 'fights'), tours=('event', 'events', 'events'),
   cta_t='Do you promote events?', cta_p='We will build your event page for free, with all the viewing details. Fans from all over the world will see your event.', cta_b='Write to us', cta_href='/en/contact',
   sc_t='Score the fight yourself', sc_p='Score round by round and share your card. No sign-up.', sc_b='Open the scorecard', sc_href='/en/scorecard',
   tools=[('📏', 'Height compare', 'Height and reach of boxers', '/en/height-compare'), ('🥊', 'Boxers', 'Legend profiles', '/en/boxers'),
          ('🏆', 'Boxing rankings', 'WBC, WBA, IBF, WBO, Ring', '/en/rankings'), ('📅', 'This day in boxing', 'Famous dates', '/en/boxing-history'),
          ('📖', 'Boxing guide', 'Rules, belts, terms', '/en/guide')],
   tba='Time TBA', months=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
   mfull=['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'],
   chips_near='📍 Near me', chip_all='All', path='en', other_path='ua', home='/en', other_home='/', loc='en_US', og='og-default-en.png', loc_js='en',
   seo='Boxing 12×3 is a boxing calendar: fight date and start time in your own time zone, country, where to watch and event results. It also has a <a href="/en/scorecard">scorecard</a> for scoring fights round by round.',
   footer=[('/en/about', 'About'), ('/en/rankings', 'Rankings'), ('/en/contact', 'Contact'), ('/widget', 'Widget'), ('/privacy', 'Privacy')],
   conts={'Europe': 'Europe', 'Asia': 'Asia', 'North America': 'North America', 'South America': 'South America', 'Africa': 'Africa', 'Oceania': 'Oceania'},
   rounds='rounds'),
}

JS = r"""
(function(){
var T=__T__;
var tz=null;try{tz=localStorage.getItem('b12x3_cal_tz');}catch(e){}
if(!tz||tz==='auto'){try{tz=Intl.DateTimeFormat().resolvedOptions().timeZone;}catch(e){tz=null;}}
if(tz==='Europe/Kiev')tz='Europe/Kyiv';
var fmtT=null,fmtD=null,fmtK=null;
try{
  fmtT=new Intl.DateTimeFormat('en-GB',{hour:'2-digit',minute:'2-digit',hour12:false,timeZone:tz});
  fmtD=new Intl.DateTimeFormat('en-CA',{year:'numeric',month:'2-digit',day:'2-digit',timeZone:tz});
}catch(e){fmtT=null;}
var now=Date.now();
function localDate(d){return fmtD?fmtD.format(d):d.toISOString().slice(0,10);}
function dayOf(iso){var p=iso.split('-');return +p[2]+' '+T.months[+p[1]-1];}
function dayFull(iso){var p=iso.split('-');return T.lang==='uk'?(+p[2]+' '+T.mfull[+p[1]-1]):(T.mfull[+p[1]-1]+' '+(+p[2]));}
// time zone note
var note=document.getElementById('tznote');
if(note&&fmtT){
  var nm=T.tz_names[tz]||String(tz).split('/').pop().replace(/_/g,' ');
  var auto=true;try{var s=localStorage.getItem('b12x3_cal_tz');auto=!s||s==='auto';}catch(e){}
  note.innerHTML=T.yourtime+': <b></b> ('+(auto?T.tz_auto:T.tz_chosen)+')';
  note.querySelector('b').textContent=nm;
}
// times in the reader's zone
var rows=document.querySelectorAll('[data-start]');
for(var i=0;i<rows.length;i++){
  var r=rows[i],st=r.getAttribute('data-start');
  if(!st||!fmtT)continue;
  var d=new Date(st);if(isNaN(d))continue;
  var ft=r.querySelector('.ft');if(!ft)continue;
  ft.innerHTML='<b>'+fmtT.format(d)+'</b><small></small>';
  ft.querySelector('small').textContent=dayOf(localDate(d));
}
// event blocks: show the first one that has not ended
var boxes=document.querySelectorAll('.evbox'),shown=-1;
for(i=0;i<boxes.length;i++){
  var end=Date.parse(boxes[i].getAttribute('data-end'));
  if(shown<0&&end>now){shown=i;boxes[i].hidden=false;}else{boxes[i].hidden=true;}
}
var skip={};
if(shown>=0){
  var b=boxes[shown],ids=(b.getAttribute('data-ids')||'').split(',');
  for(i=0;i<ids.length;i++)skip[ids[i]]=1;
  var dd=b.getAttribute('data-date'),lab=b.querySelector('.live');
  if(lab){
    var td=localDate(new Date());
    var txt=dd===td?T.today_eve:T.soon+' · '+dayFull(dd);
    lab.querySelector('span').textContent=txt;
  }
  var sh=document.getElementById('evlabel');
  if(sh){sh.textContent=(dd===localDate(new Date())?T.today:T.soon)+' · '+dayFull(dd);}
}
// upcoming list: drop what is shown above or already over, keep the first 6
var up=document.querySelectorAll('#next .fr'),n=0;
for(i=0;i<up.length;i++){
  var r2=up[i],id=r2.getAttribute('data-id'),e2=Date.parse(r2.getAttribute('data-end'));
  var over=e2<=now;
  if(skip[id]||over||n>=6){r2.hidden=true;}else{r2.hidden=false;n++;}
}
var nx=document.getElementById('nextsec');if(nx&&n===0)nx.hidden=true;
})();
"""

def fdt(f):
    if not f.get('startUtc'):
        return None
    return datetime.datetime.strptime(f['startUtc'], '%Y-%m-%dT%H:%MZ').replace(tzinfo=datetime.timezone.utc)

def fend(f):
    d = fdt(f)
    if d:
        return d + datetime.timedelta(hours=6)
    return datetime.datetime.fromisoformat(f['date']).replace(tzinfo=datetime.timezone.utc) + datetime.timedelta(days=1, hours=6)

def pl(forms, n):
    if n % 10 == 1 and n % 100 != 11: return f'{n} {forms[0]}'
    if 2 <= n % 10 <= 4 and not 12 <= n % 100 <= 14: return f'{n} {forms[1]}'
    return f'{n} {forms[2]}'

def pl_en(forms, n):
    return f'{n} {forms[0] if n == 1 else forms[1]}'

def count(lk, forms, n):
    return pl(forms, n) if lk == 'uk' else pl_en(forms, n)

def short_date(lk, iso):
    p = iso.split('-')
    return f'{int(p[2])} {H[lk]["months"][int(p[1]) - 1]}'

def long_date(lk, iso):
    p = iso.split('-')
    m = H[lk]['mfull'][int(p[1]) - 1]
    return f'{int(p[2])} {m}' if lk == 'uk' else f'{m} {int(p[2])}'

def names(f, lk):
    k = 'ua' if lk == 'uk' else 'en'
    return f['red'][k], f['blue'][k]

def row(f, lk, kind='up'):
    """One fight row. kind: 'up' (upcoming) or 'done' (result)."""
    h = H[lk]; k = 'ua' if lk == 'uk' else 'en'; v = f['venue']
    a, b = names(f, lk)
    href = f['urls'][k]
    if kind == 'done':
        w = (f.get('result') or {}).get('winner') or ''
        meth = (f.get('result') or {}).get('method') or ''
        rw = bool(w) and w in (f['red']['ua'], f['red']['en'])
        bw = bool(w) and w in (f['blue']['ua'], f['blue']['en'])
        wa = f'<span class="w">{esc(a)}</span>' if rw else esc(a)
        wb = f'<span class="w">{esc(b)}</span>' if bw else esc(b)
        p = f['date'].split('-')
        left = f'<b>{int(p[2])}</b><small>{h["months"][int(p[1]) - 1]}</small>'
        sub = f'{h["won"]}: {esc(w)}{" · " + esc(meth) if meth else ""}' if w else esc(meth)
        return (f'<a class="fr done" href="{href}"><div class="ft">{left}</div><div class="fd"></div><div class="fi">'
                f'<div class="fp">{wa}<span class="vs">–</span>{wb}</div><div class="fm">{sub}</div></div><div class="fa">›</div></a>')
    city = v['cityUa'] if lk == 'uk' else v['cityEn']
    iso = (v.get('countryIso') or '').lower()
    flag = f'<img class="flag" src="/images/flags/{iso}.png" width="16" height="11" alt=""> ' if iso else ''
    div = (f.get('division') or {}).get(k) or ''
    meta = f'{flag}{esc(city)}' + (f' · {esc(div)}' if div else '') + (f' · {f["rounds"]} {h["rounds"]}' if f.get('rounds') else '')
    tags = ''
    bc = (f['broadcast'][k] or [None])[0]
    if bc: tags += f'<span class="tag watch">{esc(bc.split(" · ")[0])}</span>'
    for x in (f['belts'] or [])[:2]: tags += f'<span class="tag">{esc(x)}</span>'
    t = TOUR.get(f.get('tournamentId'))
    if t and not tags: tags += f'<span class="tag tour">{esc(t["name"][k])}</span>'
    d = fdt(f)
    if d:
        loc = d.astimezone(KYIV)
        left = f'<b>{loc.strftime("%H:%M")}</b><small>{short_date(lk, loc.date().isoformat())}</small>'
        start = f['startUtc']
    else:
        left = f'<b class="tba">{h["tba"]}</b><small>{short_date(lk, f["date"])}</small>'
        start = ''
    return (f'<a class="fr" href="{href}" data-id="{f["id"]}" data-start="{start}" data-date="{f["date"]}" data-end="{fend(f).strftime("%Y-%m-%dT%H:%MZ")}">'
            f'<div class="ft">{left}</div><div class="fd"></div><div class="fi"><div class="fp">{esc(a)}<span class="vs">–</span>{esc(b)}</div>'
            f'<div class="fm">{meta}</div><div class="tags">{tags}</div></div><div class="fa">›</div></a>')

def events(upcoming):
    """Group scheduled fights into events (a tournament or a single fight), earliest first."""
    ev = {}
    for f in upcoming:
        key = f.get('tournamentId') or f['id']
        ev.setdefault(key, []).append(f)
    out = []
    for key, fl in ev.items():
        fl.sort(key=lambda f: (f['date'], f['startUtc'] or 'z'))
        out.append((min((f['date'], f['startUtc'] or 'z') for f in fl), key, fl))
    out.sort()
    return [(k, fl) for _, k, fl in out]

def hero(lk, key, fl, upcoming):
    h = H[lk]; k = 'ua' if lk == 'uk' else 'en'
    t = TOUR.get(key)
    main = fl[0]
    if t:
        for fid in t['fights']:
            if fid in FIGHT and FIGHT[fid]['status'] == 'scheduled':
                main = FIGHT[fid]; break
    a, b = names(main, lk)
    name = t['name'][k] if t else f'{a} – {b}'
    v = main['venue']; city = v['cityUa'] if lk == 'uk' else v['cityEn']
    bc = (main['broadcast'][k] or [None])[0]
    line1 = f'{a} – {b}' + (f' · {count(lk, h["fights"], len(fl))}' if len(fl) > 1 else '')
    line2 = esc(city) + (f' · {esc(bc.split(" · ")[0])}' if bc else '')
    img = ''
    if t and t.get('poster') and os.path.exists(f'{R}{t["poster"]}'):
        img = f'<img src="{t["poster"]}" alt="{esc(name)}" fetchpriority="high">'
    href = t['urls'][k] if t else main['urls'][k]
    sid = main['id'] if main['id'] in SC_IDS else next((x['id'] for x in fl if x['id'] in SC_IDS), None)
    score = f'<a class="btn" href="{h["sc_href"]}?fight={sid}">{h["btn_score"]}</a>' if sid else ''
    dates = sorted(f['date'] for f in fl)
    d0 = dates[0]
    # same-day fights from other events
    ids = [f['id'] for f in fl]
    same = [f for f in upcoming if f['date'] == d0 and f['id'] not in ids]
    same.sort(key=lambda f: (f['startUtc'] or 'z'))
    same = same[:3]
    ids += [f['id'] for f in same]
    end = max(fend(f) for f in fl + same).strftime('%Y-%m-%dT%H:%MZ')
    live = f'<div class="live"><i></i><span>{h["soon"]} · {long_date(lk, d0)}</span></div>'
    box = (f'<div class="evbox" hidden data-end="{end}" data-date="{d0}" data-ids="{",".join(ids)}">'
           f'<div class="hero">{img}<div class="hb">{live}<div class="hn">{esc(name)}</div>'
           f'<div class="hs">{esc(line1)}<br>{line2}</div>'
           f'<div class="acts"><a class="btn red" href="{href}">{h["btn_card"]}</a>{score}</div></div></div>')
    if same:
        box += '<div class="list">' + ''.join(row(f, lk) for f in same) + '</div>'
    box += '</div>'
    return box, ids, name

def build(lk):
    h = H[lk]; k = 'ua' if lk == 'uk' else 'en'; u = lk == 'uk'
    up = [f for f in D['fights'] if f['status'] == 'scheduled' and f['date'] >= (TODAY - datetime.timedelta(days=1)).isoformat()]
    up.sort(key=lambda f: (f['date'], f['startUtc'] or 'z'))
    evs = events(up)[:4]
    boxes = ''.join(hero(lk, key, fl, up)[0] for key, fl in evs)
    # unhide the first candidate so no-JS readers see an event
    boxes = boxes.replace('<div class="evbox" hidden', '<div class="evbox"', 1)
    nxt = ''.join(row(f, lk) for f in up[:16]).replace('<a class="fr"', '<a class="fr" hidden')
    cont = {}
    for f in up:
        c = f['venue'].get('continent')
        if c: cont[c] = cont.get(c, 0) + 1
    chips = (''.join(f'<a class="chip" href="/{h["path"]}/calendar?c={esc(c)}">{h["conts"].get(c, c)}<small>{n}</small></a>'
                     for c, n in sorted(cont.items(), key=lambda kv: -kv[1]))
             + f'<a class="chip near" href="/{h["path"]}/calendar?near=1">{h["chips_near"]}</a>')
    done = [f for f in D['fights'] if f['status'] == 'completed' and f['red']['ua'] and f['blue']['ua'] and (f.get('result') or {}).get('winner')]
    done.sort(key=lambda f: f['date'], reverse=True)
    res = ''.join(row(f, lk, 'done') for f in done[:4])
    # promoters
    prom = ''
    # fights per promoter come from the promoter pages (undercards included); update when those pages change
    PROMO_FIGHTS = {'zuffa-boxing': 97, 'usyk-17-promotions': 42}
    for p in sorted(D['promoters'], key=lambda p: -PROMO_FIGHTS.get(p['id'], 0)):
        orgname = {'zuffa-boxing': 'Zuffa Boxing', 'usyk-17-promotions': 'Usyk 17 Promotions'}.get(p['id'], p['id'])
        tl = [t for t in D['tournaments'] if t.get('organizer') == orgname]
        nf = PROMO_FIGHTS.get(p['id']) or sum(len(t['fights']) for t in tl)
        logo = f'/images/cards/{p["id"]}.png'
        if not os.path.exists(f'{R}{logo}'): continue
        prom += (f'<a class="pr" href="{p["urls"][k]}"><img class="pl" src="{logo}" alt="{esc(orgname)}" loading="lazy">'
                 f'<div><div class="pn">{orgname}</div><div class="ps">{count(lk, h["tours"], len(tl))} · {count(lk, h["fights"], nf)}</div></div></a>')
    tools = ''.join(f'<a class="tr" href="{href}"><div class="ti">{ic}</div><div><div class="tn">{esc(n)}</div><div class="td">{esc(d)}</div></div></a>'
                    for ic, n, d, href in h['tools'])
    nav = ''.join(f'<a class="nv{" on" if i == 0 else ""}" href="{href}">{esc(t)}</a>' for i, (t, href) in enumerate(h['nav']))
    foot = ''.join(f'<a href="{href}">{esc(t)}</a>' for href, t in h['footer'])
    url = BASE + h['home']
    ld = {'@context': 'https://schema.org', '@graph': [
        {'@type': 'WebSite', 'name': 'Boxing 12×3', 'url': url, 'inLanguage': 'uk' if u else 'en', 'description': h['desc'],
         'publisher': {'@type': 'Organization', 'name': 'Boxing 12×3', 'url': BASE}},
        {'@type': 'ItemList', 'name': h['sec_next'], 'itemListElement': [
            {'@type': 'ListItem', 'position': i + 1, 'url': BASE + f['urls'][k], 'name': ' – '.join(names(f, lk))} for i, f in enumerate(up[:10])]}]}
    tdata = {x: C.S[lk][x] for x in ('tz_names',)}
    tdata.update({'months': h['months'], 'mfull': h['mfull'], 'lang': h['loc_js'], 'yourtime': h['yourtime'], 'tz_auto': h['tz_auto'], 'tz_chosen': h['tz_chosen'], 'today_eve': h['today_eve'], 'today': h['today'], 'soon': h['soon']})
    js = JS.replace('__T__', json.dumps(tdata, ensure_ascii=False))
    ua_url, en_url = f'{BASE}/', f'{BASE}/en'
    page = f"""<!DOCTYPE html>
<html lang="{h['loc_js']}">
<head>
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-GYWWVSZKGY"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','G-GYWWVSZKGY');</script>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{esc(h['title'])}</title>
<meta name="description" content="{esc(h['desc'])}">
<link rel="canonical" href="{url}">
<link rel="alternate" hreflang="uk" href="{ua_url}">
<link rel="alternate" hreflang="en" href="{en_url}">
<link rel="alternate" hreflang="x-default" href="{ua_url}">
<meta property="og:type" content="website">
<meta property="og:url" content="{url}">
<meta property="og:title" content="{esc(h['title'])}">
<meta property="og:description" content="{esc(h['desc'])}">
<meta property="og:image" content="{BASE}/{h['og']}?v=2">
<meta property="og:locale" content="{h['loc']}">
<meta property="og:site_name" content="Boxing 12×3">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(h['title'])}">
<meta name="twitter:description" content="{esc(h['desc'])}">
<meta name="twitter:image" content="{BASE}/{h['og']}?v=2">
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False, separators=(',', ':'))}</script>
<link rel="icon" href="/favicon.ico" sizes="48x48">
<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32.png">
<link rel="icon" type="image/png" sizes="192x192" href="/icon-192.png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="preload" href="/fonts/manrope-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/fonts/oswald-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/fonts/manrope-cyrillic.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/fonts/fonts.css">
<script defer src="/_vercel/insights/script.js"></script>
<style>{CSS}</style>
</head>
<body>
<div class="wrap">
<div class="top"><div><a class="brand-link" href="{h['home']}"><div class="brand-name">Boxing 12×3</div></a><h1 class="brand-sub">{h['h1']}</h1></div>
<div class="lang-bar"><a class="lb{' on' if not u else ''}" href="/en" hreflang="en">EN</a><a class="lb{' on' if u else ''}" href="/" hreflang="uk">UA</a></div></div>
<nav class="nav">{nav}</nav>
<div class="grid"><div>
<div class="sec" id="events"><div class="sh"><span class="sl" id="evlabel">{h['sec_events']}</span><div class="tzl"><i></i><span id="tznote">{h['tz_fixed']}</span></div></div>
{boxes}
</div>
<div class="sec" id="nextsec"><div class="sh"><span class="sl">{h['sec_next']}</span><a class="sa" href="/{h['path']}/calendar">{h['all_cal']}</a></div>
<div class="chips" style="margin-bottom:10px">{chips}</div>
<div class="list" id="next">{nxt}</div></div>
<div class="sec" id="results"><div class="sh"><span class="sl">{h['sec_results']}</span><a class="sa" href="/{h['path']}/cards">{h['all_res']}</a></div>
<div class="list">{res}</div></div>
</div><div class="side">
<div class="sec" id="promoters"><div class="sh"><span class="sl">{h['sec_promo']}</span><a class="sa" href="/{h['path']}/promoters">{h['all_promo']}</a></div>
<div class="list">{prom}</div>
<div class="dark" style="margin-top:10px"><b>{h['cta_t']}</b><p>{h['cta_p']}</p><a class="btn" href="{h['cta_href']}">{h['cta_b']}</a></div></div>
<div class="box"><b class="t">{h['sc_t']}</b><p>{h['sc_p']}</p><a class="btn red" style="margin-top:12px;display:block" href="{h['sc_href']}">{h['sc_b']}</a></div>
<div class="sec" id="tools"><div class="sh"><span class="sl">{h['sec_tools']}</span></div><div class="list">{tools}</div></div>
</div></div>
<p class="seo">{h['seo']}</p>
<div class="foot">{foot}</div>
</div>
<script>{js}</script>
</body>
</html>
"""
    assert chr(8212) not in page, 'em-dash'
    out = f'{R}/index.html' if u else f'{R}/en/index.html'
    open(out, 'w', encoding='utf-8').write(page)
    print(f'{os.path.relpath(out, R)}: {len(evs)} event candidates, {len(up)} upcoming fights, {len(page) // 1024} KB')

if __name__ == '__main__':
    for lk in ('uk', 'en'):
        build(lk)
