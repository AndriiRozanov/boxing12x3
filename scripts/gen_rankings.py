#!/usr/bin/env python3
"""Generates /ua|en/rankings (hub), /rankings/<org> and /rankings/<division> pages from data/rankings.xlsx.
Run from repo root: python3 scripts/gen_rankings.py  (needs openpyxl). Monthly update = replace data/rankings.xlsx + P4P sheet, rerun."""
import openpyxl,re,html,os,shutil,json,datetime,sys
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
TODAY=datetime.date.today().isoformat()
wb=openpyxl.load_workbook('data/rankings.xlsx'); ws=wb['All divisions'] if 'All divisions' in wb.sheetnames else wb.worksheets[0]
rows=list(ws.iter_rows(values_only=True))
ORGS=['WBA','WBC','IBF','WBO','The Ring']
ORGC={'WBA':'#1a5276','WBC':'#2e7d32','IBF':'#7d2942','WBO':'#8a8a8a','The Ring':'#b8860b'}
RING_P4P='https://www.ringmagazine.com/fighters/rankings?org=p4p'
P4P_DATE='Oct 2026'
SRC={'WBA':'https://www.wbaboxing.com/wba-ranking','WBC':'https://wbcboxing.com/en/ratings-en/','IBF':'https://www.ibf-usba-boxing.com/ratings/','WBO':'https://wboboxing.com/rankings'}
DIVMETA={ # file name: (slug, UA, EN)
'HEAVYWEIGHT':('heavyweight','Надважка вага','Heavyweight'),'BRIDGERWEIGHT':('bridgerweight','Бріджервейт','Bridgerweight'),
'CRUISERWEIGHT':('cruiserweight','Важка вага','Cruiserweight'),'LIGHT HEAVYWEIGHT':('light-heavyweight','Напівважка вага','Light Heavyweight'),
'SUPER MIDDLEWEIGHT':('super-middleweight','Друга середня вага','Super Middleweight'),'MIDDLEWEIGHT':('middleweight','Середня вага','Middleweight'),
'SUPER WELTERWEIGHT':('super-welterweight','Перша середня вага','Super Welterweight'),'WELTERWEIGHT':('welterweight','Напівсередня вага','Welterweight'),
'SUPER LIGHTWEIGHT':('super-lightweight','Перша напівсередня вага','Super Lightweight'),'LIGHTWEIGHT':('lightweight','Легка вага','Lightweight'),
'SUPER FEATHERWEIGHT':('super-featherweight','Друга напівлегка вага','Super Featherweight'),'FEATHERWEIGHT':('featherweight','Напівлегка вага','Featherweight'),
'SUPER BANTAMWEIGHT':('super-bantamweight','Друга легша вага','Super Bantamweight'),'BANTAMWEIGHT':('bantamweight','Легша вага','Bantamweight'),
'SUPER FLYWEIGHT':('super-flyweight','Друга найлегша вага','Super Flyweight'),'FLYWEIGHT':('flyweight','Найлегша вага','Flyweight'),
'LIGHT FLYWEIGHT':('light-flyweight','Перша найлегша вага','Light Flyweight'),'MINIMUMWEIGHT':('minimumweight','Мінімальна вага','Minimumweight')}
CUA={'Albania':'Албанія','Argentina':'Аргентина','Armenia':'Вірменія','Australia':'Австралія','Austria':'Австрія','Belarus':'Білорусь','Belgium':'Бельгія','Brazil':'Бразилія','Cameroon':'Камерун','Canada':'Канада','Chile':'Чилі','China':'Китай','Colombia':'Колумбія','Congo':'Конго','Costa Rica':'Коста-Рика','Croatia':'Хорватія','Cuba':'Куба','Denmark':'Данія','Dominican Republic':'Домініканська Республіка','France':'Франція','Gambia':'Гамбія','Georgia':'Грузія','Germany':'Німеччина','Ghana':'Гана','Greece':'Греція','Guatemala':'Гватемала','Honduras':'Гондурас','Ireland':'Ірландія','Italy':'Італія','Japan':'Японія','Kazakhstan':'Казахстан','Kosovo':'Косово','Kyrgyzstan':'Киргизстан','Latvia':'Латвія','Libya':'Лівія','Lithuania':'Литва','Mexico':'Мексика','Mongolia':'Монголія','Montenegro':'Чорногорія','Morocco':'Марокко','N. Ireland':'Північна Ірландія','Namibia':'Намібія','Netherlands':'Нідерланди','New Zealand':'Нова Зеландія','Nicaragua':'Нікарагуа','Nigeria':'Нігерія','Panama':'Панама','Philippines':'Філіппіни','Poland':'Польща','Puerto Rico':'Пуерто-Рико','Russia':'Росія','Serbia':'Сербія','South Africa':'ПАР','South Korea':'Південна Корея','Spain':'Іспанія','Sweden':'Швеція','Switzerland':'Швейцарія','Tajikistan':'Таджикистан','Thailand':'Таїланд','Turkey':'Туреччина','Ukraine':'Україна','United Kingdom':'Велика Британія','United States':'США','Uzbekistan':'Узбекистан','Venezuela':'Венесуела','Wales':'Уельс','Zimbabwe':'Зімбабве'}
ISO={'Albania':'al','Argentina':'ar','Armenia':'am','Australia':'au','Austria':'at','Belarus':'by','Belgium':'be','Brazil':'br','Cameroon':'cm','Canada':'ca','Chile':'cl','China':'cn','Colombia':'co','Congo':'cd','Costa Rica':'cr','Croatia':'hr','Cuba':'cu','Denmark':'dk','Dominican Republic':'do','France':'fr','Gambia':'gm','Georgia':'ge','Germany':'de','Ghana':'gh','Greece':'gr','Guatemala':'gt','Honduras':'hn','Ireland':'ie','Italy':'it','Japan':'jp','Kazakhstan':'kz','Kosovo':'xk','Kyrgyzstan':'kg','Latvia':'lv','Libya':'ly','Lithuania':'lt','Mexico':'mx','Mongolia':'mn','Montenegro':'me','Morocco':'ma','N. Ireland':'gb-nir','Namibia':'na','Netherlands':'nl','New Zealand':'nz','Nicaragua':'ni','Nigeria':'ng','Panama':'pa','Philippines':'ph','Poland':'pl','Puerto Rico':'pr','Russia':'ru','Serbia':'rs','South Africa':'za','South Korea':'kr','Spain':'es','Sweden':'se','Switzerland':'ch','Tajikistan':'tj','Thailand':'th','Turkey':'tr','Ukraine':'ua','United Kingdom':'gb','United States':'us','Uzbekistan':'uz','Venezuela':'ve','Wales':'gb-wls','Zimbabwe':'zw'}
for c in sorted(set(ISO.values())):
    if not os.path.exists(f'images/flags/{c}.png'): print('missing flag',c,file=sys.stderr)
MON_UA=['січня','лютого','березня','квітня','травня','червня','липня','серпня','вересня','жовтня','листопада','грудня']
MON_UA_N=['січень','лютий','березень','квітень','травень','червень','липень','серпень','вересень','жовтень','листопад','грудень']
MON_EN=['January','February','March','April','May','June','July','August','September','October','November','December']
MABBR={m[:3]:i for i,m in enumerate(MON_EN)}
def fdate(s,l):
    m=re.match(r'(\d+)\s+(\w{3})\s+(\d{4})',s)
    if m:
        i=MABBR[m.group(2)]; return f'{int(m.group(1))} {MON_UA[i]} {m.group(3)}' if l=='ua' else f'{MON_EN[i]} {int(m.group(1))}, {m.group(3)}'
    m=re.match(r'(\w{3})\s+(\d{4})',s); i=MABBR[m.group(1)]
    return f'{MON_UA_N[i]} {m.group(2)}' if l=='ua' else f'{MON_EN[i]} {m.group(2)}'
divs=[];cur=None
for r in rows:
    a=r[0]
    if a and str(a).isupper() and r[1] is None and a in DIVMETA: cur=dict(name=a,date=None,champ=None,top=[]);divs.append(cur)
    elif a=='List date': cur['date']=r[1:6]
    elif a=='Champion(s)': cur['champ']=r[1:6]
    elif a and str(a).isdigit(): cur['top'].append(r[1:6])
ODATE={o:divs[0]['date'][i] for i,o in enumerate(ORGS)}
def has_org(d,i): 
    dt=d['date'][i] or ''
    return not(dt.startswith('n/a') or dt.startswith('not collected')) and (d['champ'][i] or any(t[i] for t in d['top']))
P4P=[]; 
if 'P4P Ring' in wb.sheetnames:
    for r in list(wb['P4P Ring'].iter_rows(values_only=True))[1:]:
        if r[0]: P4P.append(r)
import csv
NAMEFIX={}; UA_NAME={}
for _r in csv.DictReader(open('data/names_ua.csv',encoding='utf-8')):
    NAMEFIX[_r['en_raw']]=_r['en_canonical']; UA_NAME[_r['en_canonical']]=_r['ua']
def parse(s):
    m=re.match(r'(.*?)\s*\((.*?)\)\s*$',s.strip()); n,c=(m.group(1).strip(),m.group(2)) if m else (s.strip(),'')
    return NAMEFIX.get(n,n),c
def slug(n): return '-'.join(re.sub(r"[.'’]",'',n).lower().split())
CARDS={l:{f[:-5] for f in os.listdir(f'{l}/boxers')} for l in('ua','en')}
def e(s): return html.escape(str(s))
def disp(n,l):
    n=NAMEFIX.get(n,n)
    if l=='ua':
        if n not in UA_NAME: print('NO UA NAME',n,file=sys.stderr)
        return UA_NAME.get(n,n)
    return n
def nm(n,l): 
    n=NAMEFIX.get(n,n); s=slug(n); t=disp(n,l); return f'<a href="/{l}/boxers/{s}">{e(t)}</a>' if s in CARDS[l] else e(t)
def flag(c,l):
    k=ISO.get(c)
    if not k: return ''
    alt=CUA.get(c,c) if l=='ua' else c.replace('N. Ireland','Northern Ireland')
    return f'<img class="fl" src="/images/flags/{k}.png" alt="{e(alt)}" title="{e(alt)}" width="20" height="15" loading="lazy">'
T={'ua':dict(home='Головна',rk='Рейтинги',tag_s='Super',tag_i='Тимчасовий',tag_r='Regular',champ='Чемпіон',vac='Вакантний пояс',vpos='Вакантна позиція',all_orgs='Усі організації в цій вазі',src='Джерело',src_t='офіційний рейтинг',asof='станом на',monthly='Рейтинги оновлюються щомісяця за офіційними списками організацій.',only_wbc='Дивізіон є лише в рейтингу WBC.',read='Читай також',p4p='Найкращі боксери незалежно від ваги (P4P) за версією The Ring',ko='КО',top10='Топ-10',more='Показати всі дивізіони',champs_h='Чемпіони за дивізіонами',orgs_h='Рейтинги за організаціями',divs_h='Рейтинги за дивізіонами',list_h='Топ-10 рейтингу',ndiv='дивізіонів',vk='Вакантний'),
'en':dict(home='Home',rk='Rankings',tag_s='Super',tag_i='Interim',tag_r='Regular',champ='Champion',vac='Vacant title',vpos='Vacant position',all_orgs='All organizations in this division',src='Source',src_t='official ranking',asof='as of',monthly='Rankings are updated monthly from the organizations\' official lists.',only_wbc='This division is only rated by the WBC.',read='Read next',p4p='Best fighters regardless of weight (P4P) according to The Ring',ko='KO',top10='Top 10',more='Show all divisions',champs_h='Champions by division',orgs_h='Rankings by organization',divs_h='Rankings by division',list_h='Top 10 ranking',ndiv='divisions',vk='Vacant')}
BASE=re.search(r'<style>(.*?)</style>',open('ua/promoters.html',encoding='utf-8').read(),re.S).group(1)
CSS='''
.rk-tabs{display:flex;gap:6px;overflow-x:auto;margin:0 0 12px;padding-bottom:2px}
.rk-tb{flex:none;font-family:inherit;font-size:12px;font-weight:700;padding:7px 14px;border-radius:6px;background:var(--card);border:.5px solid var(--border);color:var(--text);text-decoration:none;cursor:pointer;line-height:1.4}
.rk-tb.on{background:var(--oc);color:#fff;border-color:var(--oc)}
.rk-chips{display:flex;gap:6px;overflow-x:auto;margin:0 0 16px;padding-bottom:4px}
.rk-chip{flex:none;font-size:12px;padding:6px 12px;border-radius:20px;border:.5px solid var(--border);background:var(--card);color:var(--text);text-decoration:none;line-height:1.4}
.rk-intro{font-size:13.5px;color:#444;line-height:1.7;margin:0 0 18px}
.rk-heros{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin:0 0 18px}
.rk-heros.one{grid-template-columns:1fr;margin:0 0 10px}
.rk-ch{border-radius:12px;padding:12px 14px;background:color-mix(in srgb,var(--oc) 5%,#fff);box-shadow:0 0 22px -2px var(--oc),0 8px 20px -10px var(--oc)}
.rk-ch.wide{grid-column:1/-1}
.rk-o{font-family:'Oswald',sans-serif;font-size:12px;letter-spacing:.16em;color:#fff;background:var(--oc);display:inline-block;padding:2px 8px;border-radius:4px}
.rk-nm{font-family:'Oswald',sans-serif;font-size:20px;text-transform:uppercase;margin:8px 0;line-height:1.15;color:var(--text);letter-spacing:.01em}
.rk-nm a{color:var(--text);text-decoration:none;border-bottom:1.5px solid var(--red)}
.rk-ct{display:flex;gap:7px;align-items:center;font-size:12px;color:var(--muted)}
.rk-ct em{margin-left:auto;font-style:normal;font-size:9px;font-weight:700;padding:2px 6px;border-radius:3px;background:#c9a54a;color:#111;text-transform:uppercase}
.rk-ch.vacant{background:repeating-linear-gradient(135deg,#f1efea,#f1efea 8px,#ebe8e1 8px,#ebe8e1 16px);box-shadow:none;border:.5px dashed #bbb}
.rk-ch.vacant .rk-nm{font-family:'Manrope',sans-serif;text-transform:none;font-size:13px;font-weight:600;color:var(--muted);margin:10px 0 4px}
.fl{width:20px;height:15px;border-radius:2px;box-shadow:0 0 0 .5px rgba(0,0,0,.25);object-fit:cover;flex:none;display:inline-block}
ol.rk-list{list-style:none;border-radius:12px;overflow:hidden;border:.5px solid var(--border);background:var(--card);box-shadow:0 4px 14px -8px rgba(0,0,0,.3);margin:0 0 12px}
.rk-r{display:flex;align-items:center;gap:12px;padding:10px 14px;border-bottom:.5px solid #f0ede8;font-size:14px;font-weight:600;line-height:1.35}
.rk-r:last-child{border:0}
.rk-r .n{width:24px;text-align:right;font-family:'Oswald',sans-serif;font-size:16px;color:var(--muted);flex:none}
.rk-r .p{flex:1}
.rk-r .p a{color:var(--text);text-decoration:none;border-bottom:1px solid var(--red)}
.rk-r .rec{font-size:11.5px;font-weight:500;color:var(--muted);white-space:nowrap}
.rk-r.g{background:linear-gradient(90deg,#f6ecd2,#fffaf0 70%);border-left:4px solid #c9a54a;padding-left:10px}
.rk-r.g .n{color:#a8821f;font-size:20px}
.rk-r.vp .p{font-weight:500;font-style:italic;color:var(--muted)}
details.rk-dv{margin-bottom:22px}
details.rk-dv>summary{list-style:none;cursor:pointer;display:flex;justify-content:space-between;align-items:baseline;gap:10px;padding-left:10px;border-left:4px solid var(--oc);margin-bottom:10px}
details.rk-dv>summary::-webkit-details-marker{display:none}
details.rk-dv>summary h2{font-size:18px;font-weight:700;line-height:1.3}
details.rk-dv>summary span{font-size:11px;color:var(--muted);flex:none}
details.rk-dv>summary::after{content:"+";color:var(--muted);font-size:20px;line-height:1;margin-left:auto}
details.rk-dv[open]>summary::after{content:"\\2013"}
.rk-more{display:block;text-align:right;font-size:12px;font-weight:600;color:var(--muted);text-decoration:none;margin:-2px 2px 0}
.rk-more:hover{color:var(--red)}
.rk-note{font-size:12px;color:var(--muted);line-height:1.6;margin:18px 0}
.rk-note a{color:var(--muted);text-decoration:underline}
.rk-orgs{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin:0 0 22px}
.rk-org{position:relative;display:flex;flex-direction:column;gap:3px;overflow:hidden;text-decoration:none;color:var(--text);background:#fff;border:.5px solid var(--border);border-radius:12px;padding:14px;box-shadow:0 0 22px -6px var(--oc)}
.rk-org::after{content:'';position:absolute;right:-18px;bottom:-18px;width:70px;height:70px;border-radius:50%;background:var(--oc);opacity:.12}
.rk-org b{font-family:'Oswald',sans-serif;font-weight:500;font-size:30px;letter-spacing:.06em;line-height:1;color:var(--oc)}
.rk-org i{font-style:normal;font-size:10.5px;color:var(--muted)}
.rk-org em{font-style:normal;font-size:12px;font-weight:700;margin-top:4px}
.rk-org small{font-size:10.5px;color:var(--muted)}
.rk-org .ar{position:absolute;right:12px;top:10px;font-size:20px;color:var(--muted)}
.rk-dt{display:grid;grid-template-columns:1fr 1fr;gap:10px}
.rk-dtl{display:block;text-decoration:none;color:var(--text);background:var(--card);border:.5px solid var(--border);border-radius:12px;padding:12px 12px 8px}
.rk-dtl b{display:block;font-family:'Oswald',sans-serif;font-weight:500;font-size:14px;letter-spacing:.04em;text-transform:uppercase;margin-bottom:8px}
.rk-dr{display:flex;align-items:center;gap:6px;font-size:12px;padding:5px 0 5px 8px;border-left:3px solid var(--oc);margin-bottom:5px;background:color-mix(in srgb,var(--oc) 7%,#fff);border-radius:0 6px 6px 0}
.rk-dr i{font-style:normal;font-size:9px;font-weight:700;color:var(--oc);width:26px;letter-spacing:.03em}
.rk-dr span{flex:1;font-weight:600;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.rk-dr .fl{margin-right:6px}.rk-dr.vc span{color:var(--muted);font-weight:500;font-style:italic}
@keyframes rkf{from{opacity:0}to{opacity:1}}
.rk-pane:not([hidden]){animation:rkf .18s ease}
.rk-drow{display:block;text-decoration:none;color:var(--text);background:var(--card);border:.5px solid var(--border);border-radius:10px;padding:12px 14px;margin-bottom:8px}
.rk-drow b{font-size:14px}
.rk-drow div{font-size:12px;color:var(--muted);margin-top:4px;line-height:1.5}
h2.rk-h{font-size:16px;font-weight:700;margin:26px 0 12px}
.rk-wide-note{font-size:12px;color:var(--muted);margin:-4px 0 12px}
'''
def head(l,title,desc,path,ld,sub,bc):
    alt={'ua':'en','en':'ua'}[l]
    url=f'https://boxing12x3.com/{l}{path}'; ogimg='og-default.png' if l=='ua' else 'og-default-en.png'
    loc='uk_UA' if l=='ua' else 'en_US'
    ldj=''.join(f'<script type="application/ld+json">{json.dumps(x,ensure_ascii=False,separators=(",",":"))}</script>\n' for x in ld)
    return f'''<!DOCTYPE html>
<html lang="{'uk' if l=='ua' else 'en'}">
<head>
<script async src="https://www.googletagmanager.com/gtag/js?id=G-GYWWVSZKGY"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','G-GYWWVSZKGY');</script>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<meta property="og:type" content="website">
<meta property="og:url" content="{url}">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:image" content="https://boxing12x3.com/{ogimg}?v=2">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:locale" content="{loc}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{e(title)}">
<meta name="twitter:description" content="{e(desc)}">
<meta name="twitter:image" content="https://boxing12x3.com/{ogimg}?v=2">
<link rel="canonical" href="{url}">
<link rel="alternate" hreflang="uk" href="https://boxing12x3.com/ua{path}">
<link rel="alternate" hreflang="en" href="https://boxing12x3.com/en{path}">
<link rel="alternate" hreflang="x-default" href="https://boxing12x3.com/en{path}">
<link rel="icon" href="/favicon.ico" sizes="48x48">
<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32.png">
<link rel="icon" type="image/png" sizes="192x192" href="/icon-192.png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
{ldj}<link rel="preload" href="/fonts/manrope-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/fonts/oswald-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/fonts/manrope-cyrillic.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/fonts/fonts.css">
<style>{BASE}{CSS}</style>
</head>
<body>
<div class="wrap">
<div class="lang-row">
  <a class="lang-btn{' on' if l=='en' else ''}" href="/en{path}">EN</a>
  <a class="lang-btn{' on' if l=='ua' else ''}" href="/ua{path}">UA</a>
</div>
<div class="brand">
  <a href="/"><div class="brand-name">Boxing 12×3</div></a>
  <div class="brand-sub">{e(sub)}</div>
</div>
<div class="breadcrumb">{bc}</div>
'''
FOOT={'ua':'''<div class="read-next">
  <div class="rn-lbl">Читай також</div>
  <a class="rn-link" href="/ua/boxing-organizations"><div><div class="rn-title">WBC, WBA, IBF і WBO</div><div class="rn-sub">Великі боксерські організації</div></div><span class="rn-arr">›</span></a>
  <a class="rn-link" href="/ua/boxers"><div><div class="rn-title">Профілі боксерів</div><div class="rn-sub">Рекорди, титули, зріст і розмах</div></div><span class="rn-arr">›</span></a>
</div>
<a href="/" aria-label="Boxing 12×3" style="display:block;margin:28px 0 0"><img src="/icon-192.png" width="36" height="36" alt="" loading="lazy" style="display:block;margin:0 auto;border-radius:8px"></a>
<div class="site-footer"><a href="/">Картка</a><a href="/ua/guide">Довідник</a><a href="/height-compare">Порівняй зріст</a><a href="/about">Про нас</a><a href="/privacy">Конфіденційність</a></div>
</div>
</body>
</html>
''','en':'''<div class="read-next">
  <div class="rn-lbl">Read next</div>
  <a class="rn-link" href="/en/boxing-organizations"><div><div class="rn-title">WBC, WBA, IBF and WBO</div><div class="rn-sub">The major boxing organizations</div></div><span class="rn-arr">›</span></a>
  <a class="rn-link" href="/en/boxers"><div><div class="rn-title">Boxer profiles</div><div class="rn-sub">Records, titles, height and reach</div></div><span class="rn-arr">›</span></a>
</div>
<a href="/" aria-label="Boxing 12×3" style="display:block;margin:28px 0 0"><img src="/icon-192.png" width="36" height="36" alt="" loading="lazy" style="display:block;margin:0 auto;border-radius:8px"></a>
<div class="site-footer"><a href="/en">Scorecard</a><a href="/en/guide">Guide</a><a href="/en/height-compare">Height Compare</a><a href="/en/about">About</a><a href="/privacy">Privacy</a></div>
</div>
</body>
</html>
'''}
def dname(d,l): return DIVMETA[d['name']][1 if l=='ua' else 2]
def bc(l,*parts):
    t=T[l]; s=f'<a href="/">{t["home"]}</a> / <a href="/{l}/rankings">{t["rk"]}</a>'
    for p in parts: s+=' / '+p
    return s
def bcld(l,parts):
    items=[('Головна' if l=='ua' else 'Home','https://boxing12x3.com/'),(T[l]['rk'],f'https://boxing12x3.com/{l}/rankings')]+parts
    return {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":i+1,"name":n,"item":u} for i,(n,u) in enumerate(items)]}
def champ_list(d,i):
    raw=d['champ'][i]
    if not raw: return []
    res=[]
    for p in raw.split('|'):
        p=p.strip(); m=re.match(r'(.*)\[(.*?)\]',p); st=''
        if m: p=m.group(1).strip(); st=m.group(2)
        n,c=parse(p); res.append((n,c,st))
    return res
def card(l,org,n,c,st,wide=False):
    t=T[l]; col=ORGC[org]
    if n.startswith('VACANT'): return f'<div class="rk-ch vacant{" wide" if wide else ""}" style="--oc:{col}"><span class="rk-o">{org}</span><div class="rk-nm">{t["vac"]}</div></div>'
    tag={'Super':t['tag_s'],'Interim':t['tag_i'],'Regular':t['tag_r']}.get(st,'')
    return f'<div class="rk-ch{" wide" if wide else ""}" style="--oc:{col}"><span class="rk-o">{org}</span><div class="rk-nm">{nm(n,l)}</div><div class="rk-ct">{flag(c,l)}<span>{e(CUA.get(c,c) if l=="ua" else c)}</span>'+(f'<em>{tag}</em>' if tag else '')+'</div></div>'
def vac_parts(raw):
    pass
def rlist(l,d,i):
    out=['<ol class="rk-list">']
    for k,r in enumerate(d['top'][:10],1):
        v=r[i]
        if not v: continue
        if v=='VACANT': out.append(f'<li class="rk-r vp"><span class="n">{k}</span><span class="p">{T[l]["vpos"]}</span></li>'); continue
        n,c=parse(v); out.append(f'<li class="rk-r{" g" if k<=3 else ""}"><span class="n">{k}</span><span class="p">{nm(n,l)}</span>{flag(c,l)}</li>')
    out.append('</ol>'); return ''.join(out)
def write(path,txt):
    os.makedirs(os.path.dirname(path),exist_ok=True); open(path,'w',encoding='utf-8').write(txt)
URLS=[]
def src_links(l,orgs):
    t=T[l]; parts=[f'<a href="{SRC[o]}" target="_blank" rel="noopener nofollow">{o}</a> ({t["asof"]} {fdate(ODATE[o],l)})' for o in orgs]
    return f'{t["src"]}: '+', '.join(parts)+'. '+t['monthly']
ANIM='<script>(function(){if(matchMedia("(prefers-reduced-motion:reduce)").matches)return;document.querySelectorAll("details.rk-dv>summary").forEach(function(s){s.addEventListener("click",function(ev){var d=s.parentNode;if(d._a){return ev.preventDefault()}ev.preventDefault();var h0=d.offsetHeight,op=d.open;d.style.overflow="hidden";if(!op){d.open=true}var h1=op?s.offsetHeight+10:d.scrollHeight;d._a=d.animate([{height:h0+"px"},{height:h1+"px"}],{duration:240,easing:"ease"});d._a.onfinish=function(){d._a=null;d.style.overflow="";d.style.height="";if(op)d.open=false}})})})()</script>'
# ---------- ORG pages
OPEN_N=4
for l in('ua','en'):
    t=T[l]
    for o in ['WBA','WBC','IBF','WBO']:
        i=ORGS.index(o); date=fdate(ODATE[o],l)
        ds=[d for d in divs if has_org(d,i)]
        if l=='ua':
            title=f'Рейтинг {o}: чемпіони й топ-10 за дивізіонами | Boxing 12×3'
            desc=f'Актуальний рейтинг {o} у всіх вагових категоріях: чинні чемпіони та топ-10 претендентів. Офіційний список, станом на {date}.'
            h1=f'Рейтинг {o}: чемпіони та топ-10 за дивізіонами'
            intro=f'Чинні чемпіони {o} і перша десятка претендентів у {len(ds)} вагових категоріях. Список офіційний, станом на {date}. Для кожного дивізіону можна перейти до порівняння всіх організацій.'
        else:
            title=f'{o} Rankings: Champions and Top 10 by Division | Boxing 12×3'
            desc=f'Current {o} rankings in every weight class: reigning champions and the top 10 contenders. Official list, as of {date}.'
            h1=f'{o} Rankings: Champions and Top 10 by Division'
            intro=f'Reigning {o} champions and the top 10 contenders in {len(ds)} weight classes. The list is official, as of {date}. Each division links to a side-by-side view of all organizations.'
        ld=[bcld(l,[(f'{o}',f'https://boxing12x3.com/{l}/rankings/{o.lower()}')])]
        b=head(l,title,desc,f'/rankings/{o.lower()}',ld,t['rk'] if l=='ua' else 'Boxing rankings',bc(l,o))
        b+=f'<h1>{e(h1)}</h1>\n<div class="meta">{t["asof"].capitalize()} {date} · {t["src"]}: {t["src_t"]} {o}</div>\n<p class="rk-intro">{e(intro)}</p>\n'
        b+='<nav class="rk-tabs" aria-label="'+e(t['orgs_h'])+'">'+''.join(f'<a class="rk-tb{" on" if x==o else ""}" style="--oc:{ORGC[x]}" href="/{l}/rankings/{x.lower()}">{x}</a>' for x in ['WBA','WBC','IBF','WBO'])+'</nav>\n'
        b+='<nav class="rk-chips">'+''.join(f'<a class="rk-chip" href="#{DIVMETA[d["name"]][0]}">{e(dname(d,l)).replace(" вага","")}</a>' for d in ds)+'</nav>\n'
        for k,d in enumerate(ds):
            sl_=DIVMETA[d['name']][0]
            b+=f'<details class="rk-dv" id="{sl_}" style="--oc:{ORGC[o]}"{" open" if k<OPEN_N else ""}><summary><h2>{e(dname(d,l))}</h2><span>{e(DIVMETA[d["name"]][2]) if l=="ua" else ""}</span></summary>\n'
            cl=champ_list(d,i)
            if not cl: cl=[('VACANT','','')]
            b+='<div class="rk-heros one">'+''.join(card(l,o,n,c,st) for n,c,st in cl)+'</div>\n'
            b+=rlist(l,d,i)
            if d['name']!='BRIDGERWEIGHT': b+=f'<a class="rk-more" href="/{l}/rankings/{sl_}">{t["all_orgs"]} ›</a>\n'
            b+='</details>\n'
        b+=f'<p class="rk-note">{src_links(l,[o])}</p>\n'+ANIM+FOOT[l]
        write(f'{l}/rankings/{o.lower()}.html',b); URLS.append(f'/{l}/rankings/{o.lower()}')
# ---------- DIVISION pages
for l in('ua','en'):
    t=T[l]
    for d in divs:
        sl_,uan,enn=DIVMETA[d['name']]; name=dname(d,l)
        orgs4=[o for o in ['WBA','WBC','IBF','WBO'] if has_org(d,ORGS.index(o))]
        orgl=', '.join(orgs4)
        if l=='ua':
            title=f'{name}: рейтинг {orgl} | Boxing 12×3'; h1=f'{name}: чемпіони та рейтинг {orgl}'
            desc=f'{name}: чинні чемпіони WBA, WBC, IBF, WBO і The Ring та топ-10 рейтингу кожної організації. Офіційні списки, оновлюється щомісяця.'
            intro=f'Хто чемпіон світу в категорії «{name.lower()}» і хто в рейтингу. Нижче чемпіони організацій та топ-10 за офіційними списками {orgl}.'
        else:
            title=f'{name}: {orgl} Rankings | Boxing 12×3'; h1=f'{name}: Champions and {orgl} Rankings'
            desc=f'{name}: reigning WBA, WBC, IBF, WBO and The Ring champions plus each organization\'s top 10. Official lists, updated monthly.'
            intro=f'Who is the world champion at {name.lower()} and who is ranked. Below are the champions of each organization and the top 10 from the official {orgl} lists.'
        if d['name']=='BRIDGERWEIGHT':
            desc=desc.replace('WBA, WBC, IBF, WBO і The Ring','WBC').replace('WBA, WBC, IBF, WBO and The Ring','WBC')
        ld=[bcld(l,[(name,f'https://boxing12x3.com/{l}/rankings/{sl_}')])]
        b=head(l,title,desc,f'/rankings/{sl_}',ld,t['rk'] if l=='ua' else 'Boxing rankings',bc(l,e(name)))
        b+=f'<h1>{e(h1)}</h1>\n<div class="meta">{e(enn) if l=="ua" else ""}{" · " if l=="ua" else ""}{t["src"]}: {t["src_t"]} {orgl}</div>\n<p class="rk-intro">{e(intro)}</p>\n'
        cards=[]
        for oi,o in enumerate(ORGS):
            if o=='The Ring':
                if not d['champ'][oi]: continue
            elif o not in orgs4: continue
            cl=champ_list(d,oi) or [('VACANT','','')]
            for n,c,st in cl: cards.append((o,n,c,st))
        b+='<div class="rk-heros">'+''.join(card(l,o,n,c,st,wide=(len(cards)%2==1 and k==len(cards)-1)) for k,(o,n,c,st) in enumerate(cards))+'</div>\n'
        if d['name']=='BRIDGERWEIGHT': b+=f'<p class="rk-wide-note">{t["only_wbc"]}</p>\n'
        if len(orgs4)>1:
            b+='<div class="rk-tabs" role="tablist">'+''.join(f'<button type="button" class="rk-tb{" on" if k==0 else ""}" style="--oc:{ORGC[o]}" data-o="{o}" role="tab">{o}</button>' for k,o in enumerate(orgs4))+'</div>\n'
        for k,o in enumerate(orgs4):
            oi=ORGS.index(o)
            b+=f'<section class="rk-pane" data-o="{o}"{"" if k==0 else " hidden"}><h2 class="rk-h" style="margin-top:0">{o}: {t["list_h"] if l=="ua" else t["top10"]} <span style="font-weight:500;font-size:12px;color:var(--muted)">· {fdate(d["date"][oi],l) if not d["date"][oi].startswith("n/a") else ""}</span></h2>'+rlist(l,d,oi)+f'<a class="rk-more" href="/{l}/rankings/{o.lower()}#{sl_}">{o}: {"усі дивізіони" if l=="ua" else "all divisions"} ›</a></section>\n'
        b+=f'<p class="rk-note">{src_links(l,orgs4)}</p>\n'
        if len(orgs4)>1:
            b+='<script>(function(){var tb=document.querySelectorAll(".rk-tabs button"),pn=document.querySelectorAll(".rk-pane");tb.forEach(function(x){x.addEventListener("click",function(){tb.forEach(function(y){y.classList.toggle("on",y===x)});pn.forEach(function(p){p.hidden=p.getAttribute("data-o")!==x.getAttribute("data-o")});if(window.gtag)gtag("event","rankings_tab",{org:x.getAttribute("data-o"),division:"'+sl_+'"})})})})();</script>\n'
        b+=FOOT[l]
        write(f'{l}/rankings/{sl_}.html',b); URLS.append(f'/{l}/rankings/{sl_}')
# ---------- HUB
def rec(r,l): 
    return r.replace('KO',T[l]['ko'])
for l in('ua','en'):
    t=T[l]
    if l=='ua':
        title='Рейтинги боксу: WBA, WBC, IBF, WBO, чемпіони | Boxing 12×3'
        desc='Чемпіони світу з боксу за дивізіонами та рейтинги WBA, WBC, IBF, WBO. Топ-10 кожної організації та P4P The Ring, оновлюється щомісяця.'
        h1='Рейтинги боксерських організацій'; intro='Чемпіони світу у всіх вагових категоріях і рейтинги чотирьох головних організацій: WBA, WBC, IBF та WBO. Усе за офіційними списками, оновлюється щомісяця.'
    else:
        title='Boxing Rankings: WBA, WBC, IBF, WBO Champions | Boxing 12×3'
        desc='World boxing champions by division and WBA, WBC, IBF, WBO rankings. Top 10 for each organization plus The Ring P4P, updated monthly.'
        h1='Boxing Organization Rankings'; intro='World champions in every weight class and the rankings of the four major organizations: WBA, WBC, IBF and WBO. Everything comes from the official lists and is updated monthly.'
    ld=[{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":t['home'],"item":"https://boxing12x3.com/"},{"@type":"ListItem","position":2,"name":t['rk'],"item":f"https://boxing12x3.com/{l}/rankings"}]}]
    if P4P: ld.append({"@context":"https://schema.org","@type":"ItemList","name":t['p4p'],"numberOfItems":len(P4P),"itemListElement":[{"@type":"ListItem","position":int(p[0]),"item":{"@type":"Person","name":p[1]}} for p in P4P]})
    b=head(l,title,desc,'/rankings',ld,t['rk'] if l=='ua' else 'Boxing rankings',f'<a href="/">{t["home"]}</a> / {t["rk"]}')
    b+=f'<h1>{e(h1)}</h1>\n<div class="meta">{t["asof"].capitalize()} {fdate(ODATE["WBC"],l)}</div>\n<p class="rk-intro">{e(intro)}</p>\n'
    FULL={'WBA':'World Boxing Association','WBC':'World Boxing Council','IBF':'International Boxing Federation','WBO':'World Boxing Organization'}
    b+=f'<h2 class="rk-h">{t["orgs_h"]}</h2><div class="rk-orgs">'+''.join(f'<a class="rk-org" style="--oc:{ORGC[o]}" href="/{l}/rankings/{o.lower()}"><b>{o}</b><i>{FULL[o]}</i><em>{len([d for d in divs if has_org(d,ORGS.index(o))])} {t["ndiv"]}</em><small>{t["asof"]} {fdate(ODATE[o],l)}</small><span class="ar">›</span></a>' for o in ['WBA','WBC','IBF','WBO'])+'</div>\n'
    if P4P:
        b+=f'<h2 class="rk-h">P4P The Ring</h2><p class="rk-wide-note">{t["p4p"]}.</p><ol class="rk-list">'
        for p in P4P:
            n=p[1]; c=p[2]; r=p[3]; k=int(p[0])
            b+=f'<li class="rk-r{" g" if k<=3 else ""}"><span class="n">{k}</span><span class="p">{nm(n,l)} <span class="rec">{e(rec(r,l))}</span></span>{flag(c,l)}</li>'
        b+='</ol>\n'
        b+=f'<p class="rk-note">{t["src"]}: <a href="{RING_P4P}" target="_blank" rel="noopener nofollow">The Ring</a> ({t["asof"]} {fdate(P4P_DATE,l)}).</p>\n'
    b+=f'<h2 class="rk-h">{t["champs_h"]}</h2>\n<div class="rk-dt">'
    for d in divs:
        sl_=DIVMETA[d['name']][0]; rows=''
        for oi,o in enumerate(ORGS[:4]):
            if not has_org(d,oi) or not d['champ'][oi]: continue
            n,cc,st=champ_list(d,oi)[0]
            if n.startswith('VACANT'): rows+=f'<div class="rk-dr vc" style="--oc:{ORGC[o]}"><i>{o}</i><span>{t["vk"]}</span></div>'; continue
            full=disp(n,l); rows+=f'<div class="rk-dr" style="--oc:{ORGC[o]}"><i>{o}</i><span title="{e(full)}">{e(full.split(" ")[-1])}</span>{flag(cc,l)}</div>'
        b+=f'<a class="rk-dtl" href="/{l}/rankings/{sl_}"><b>{e(dname(d,l))}</b>{rows}</a>\n'
    b+='</div>\n'
    b+=f'<p class="rk-note">{src_links(l,["WBA","WBC","IBF","WBO"])}</p>\n'+FOOT[l]
    write(f'{l}/rankings.html',b); URLS.append(f'/{l}/rankings')
# ---------- sitemap
sm=open('sitemap.xml',encoding='utf-8').read()
sm=re.sub(r'\s*<url>\s*<loc>https://boxing12x3.com/(?:ua|en)/rankings[^<]*</loc>.*?</url>','',sm,flags=re.S)
def sm_entry(u):
    tail=u[3:]
    return (f'  <url>\n    <loc>https://boxing12x3.com{u}</loc>\n    <lastmod>{TODAY}</lastmod>\n'
            f'    <xhtml:link rel="alternate" hreflang="uk" href="https://boxing12x3.com/ua{tail}"/>\n'
            f'    <xhtml:link rel="alternate" hreflang="en" href="https://boxing12x3.com/en{tail}"/>\n'
            f'    <changefreq>monthly</changefreq>\n    <priority>0.8</priority>\n  </url>\n')
add=''.join(sm_entry(u) for u in URLS)
sm=sm.replace('</urlset>',add+'</urlset>')
open('sitemap.xml','w',encoding='utf-8').write(sm)
print(len(URLS),'pages')
