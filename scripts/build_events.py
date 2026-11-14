#!/usr/bin/env python3
"""Build data/events.json (lean event database) from the site pages.

Reads FIGHTS/TOURNAMENTS from index.html, votes-close.json, ua|en fight pages and ua|en/cards pages.
Run from anywhere: python3 scripts/build_events.py   (needs: beautifulsoup4, node)
data/events.json feeds scripts/bake_calendar.py. Do not edit events.json by hand.
"""
import re, json, glob, os, subprocess, datetime, tempfile
from zoneinfo import ZoneInfo
from bs4 import BeautifulSoup
R=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT=tempfile.mkdtemp()
TODAY=datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d')

issues=[]
# ---------- 1. index.html arrays via node ----------
src=open(f'{R}/index.html',encoding='utf-8').read()
a=src.index('var TOURNAMENTS'); b=src.index('const FIGHTS = [')
e=src.index('\n];',b)+3
js=src[a:e]+"\nconsole.log(JSON.stringify({TOURNAMENTS:TOURNAMENTS,FIGHTS:FIGHTS}));"
open(f'{OUT}/_arr.js','w').write(js)
arr=json.loads(subprocess.check_output(['node',f'{OUT}/_arr.js']))
TOUR=arr['TOURNAMENTS']; FIGHTS={f['id']:f for f in arr['FIGHTS']}
VC=json.load(open(f'{R}/votes-close.json'))

# ---------- helpers ----------
def soup(p): return BeautifulSoup(open(p,encoding='utf-8').read(),'html.parser')
def ldjson(s):
    out=[]
    for t in s.find_all('script',type='application/ld+json'):
        try: out.append(json.loads(t.string))
        except Exception: pass
    return out
def txt(el,sep=' '): return el.get_text(sep,strip=True) if el else None
UKM={'січня':1,'лютого':2,'березня':3,'квітня':4,'травня':5,'червня':6,'липня':7,'серпня':8,'вересня':9,'жовтня':10,'листопада':11,'грудня':12}
COUNTRY={'USA':('US','North America'),'United States':('US','North America'),'United Kingdom':('GB','Europe'),'England':('GB','Europe'),
 'Wales':('GB','Europe'),'Ukraine':('UA','Europe'),'Ireland':('IE','Europe'),'Canada':('CA','North America'),'UAE':('AE','Asia'),
 'Germany':('DE','Europe'),'Japan':('JP','Asia'),'Saudi Arabia':('SA','Asia'),'Netherlands':('NL','Europe'),'Australia':('AU','Oceania'),
 'South Africa':('ZA','Africa')}
TZ={'Riyadh':'Asia/Riyadh','Dubai':'Asia/Dubai','Tokyo':'Asia/Tokyo','Koto-Ku':'Asia/Tokyo','Johannesburg':'Africa/Johannesburg','Melbourne':'Australia/Melbourne',
 'London':'Europe/London','Manchester':'Europe/London','Sheffield':'Europe/London','Birmingham':'Europe/London','Bournemouth':'Europe/London','Cardiff':'Europe/London',
 'Dublin':'Europe/Dublin','Düsseldorf':'Europe/Berlin','Rust':'Europe/Berlin','Amsterdam':'Europe/Amsterdam','Kyiv':'Europe/Kyiv','Lviv':'Europe/Kyiv','Lisnyky':'Europe/Kyiv','Vinnytsia':'Europe/Kyiv',
 'Las Vegas':'America/Los_Angeles','Carson':'America/Los_Angeles','San Diego':'America/Los_Angeles','San Francisco':'America/Los_Angeles','New York':'America/New_York',
 'Mashantucket':'America/New_York','San Antonio':'America/Chicago','Quebec City':'America/Toronto'}

VM={ '!FESTrepublic':('Lviv','Ukraine'),'3Arena':('Dublin','Ireland'),'Bournemouth International Centre':('Bournemouth','United Kingdom'),
 'Capitole de Quebec':('Quebec City','Canada'),'Chase Center':('San Francisco','USA'),'Coca-Cola Arena':('Dubai','UAE'),'Copper Box Arena':('London','United Kingdom'),
 'Dignity Health Sports Park':('Carson','USA'),'ESPRIT arena':('Düsseldorf','Germany'),'Ebara Wave Arena Ota':('Tokyo','Japan'),'Equides Club':('Lisnyky','Ukraine'),
 'EuropaPark Rust':('Rust','Germany'),'Foxwoods Resort':('Mashantucket','USA'),'Frost Bank Center':('San Antonio','USA'),
 'Infosys Theater at Madison Square Garden':('New York','USA'),'Kingdom Arena':('Riyadh','Saudi Arabia'),'Manchester Arena':('Manchester','United Kingdom'),
 'Meta Apex':('Las Vegas','USA'),'O2 Arena':('London','United Kingdom'),'Passenger Terminal Amsterdam':('Amsterdam','Netherlands'),'Pechanga Arena':('San Diego','USA'),
 'Principality Stadium':('Cardiff','United Kingdom'),'Pullman Melbourne Albert Park':('Melbourne','Australia'),'Sandton Convention Centre':('Johannesburg','South Africa'),
 'T-Mobile Arena':('Las Vegas','USA'),'The Chelsea at The Cosmopolitan':('Las Vegas','USA'),'The Cosmopolitan of Las Vegas':('Las Vegas','USA'),
 'The Venue (Riyadh Season)':('Riyadh','Saudi Arabia'),'Toyota Arena Tokyo':('Tokyo','Japan'),'Utilita Arena Sheffield':('Sheffield','United Kingdom'),
 'Utilita Arena':('Birmingham','United Kingdom'),'Vinnytsia':('Vinnytsia','Ukraine'),'Вінниця':('Vinnytsia','Ukraine'),'WePlay Esports Arena':('Kyiv','Ukraine'),
 'Wembley Arena':('London','United Kingdom')}

def split_addr(addr):
    if not addr: return None,None
    parts=[x.strip() for x in addr.split(',')]
    return parts[0], parts[-1]

def parse_fight(p, lang):
    s=soup(p); d={}
    lds=ldjson(s)
    ev=next((o for o in lds if o.get('@type')=='SportsEvent'),{})
    d['h1']=txt(s.find('h1'))
    d['name_ld']=ev.get('name'); d['startDate']=ev.get('startDate'); d['status_ld']=(ev.get('eventStatus') or '').split('/')[-1]
    loc=ev.get('location',{}); d['venue_ld']=loc.get('name'); d['address_ld']=loc.get('address')
    d['performers']=[x.get('name') for x in ev.get('performer',[])]
    se=ev.get('superEvent'); d['tournament']=(se or {}).get('url','').rstrip('/').split('/')[-1] or None
    d['tournament_name']=(se or {}).get('name')
    d['meta']=txt(s.select_one('.meta'))
    # fighters
    fi={}
    for side in ('r','b'):
        f=s.select_one(f'.fighter.{side}')
        if f:
            info=[x.strip() for x in (txt(f.select_one('.f-info')) or '').split('·')]
            fi[side]={'name':txt(f.select_one('.f-name')),'flag':txt(f.select_one('.f-flag')),'age':info[0] if info else None,'origin':info[1] if len(info)>1 else None}
    d['fighters']=fi
    rows={}
    for fr in s.select('.frow'):
        lab=fr.select_one('.flbl span'); 
        r=fr.select_one('.fv.r'); bl=fr.select_one('.fv.b')
        if lab: rows[txt(lab)]=(txt(r,' | '),txt(bl,' | '))
    d['rows']=rows
    # form
    form={}
    cells=s.select('.form-cells')
    for side,c in zip(('r','b'),cells):
        form[side]=[{'res':txt(x.select_one('.fc')),'tip':txt(x.select_one('.fc-tip'))} for x in c.select('.fc-wrap')]
    d['form']=form
    ix={}
    for tr in s.select('.ee-t tr'):
        tds=[txt(td) for td in tr.find_all('td')]
        if len(tds)==3: ix[tds[1]]=(tds[0],tds[2])
    d['index12x3']=ix
    ven={}
    for vr in s.select('.venue-row'): ven[txt(vr.select_one('.venue-lbl'))]=txt(vr.select_one('.venue-val'))
    d['venue_block']=ven
    bc=[]
    for br in s.select('.broadcast-row'):
        pl=br.select_one('.broadcast-platform'); lb=pl.select_one('.broadcast-label') if pl else None
        lab=txt(lb); 
        if lb: lb.extract()
        bc.append({'platform':txt(pl),'label':(lab or '').strip(' ·') or None,'time':txt(br.select_one('.broadcast-time'))})
    d['broadcast']=bc
    d['belts']=[txt(x) for x in s.select('.belts .belt-tag')]
    d['belt_info']=txt(s.select_one('.belts .belt-info'))
    w=s.select_one('.result-winner')
    if w:
        d['result']={'winner':txt(w),'method':txt(s.select_one('.result-method')),'note':txt(s.select_one('.result-note')),
                     'judges':[txt(x) for x in s.select('.result-judge-row')]}
    return d

# ---------- 2. fights ----------
fight_ids=sorted(os.path.basename(p)[:-5] for p in glob.glob(f'{R}/ua/*.html') if 'class="fcard"' in open(p,encoding='utf-8').read())
fights=[]
for fid in fight_ids:
    rec={'id':fid}
    for lang in ('ua','en'):
        p=f'{R}/{lang}/{fid}.html'
        rec[lang]=parse_fight(p,lang) if os.path.exists(p) else None
    fights.append(rec)

def kyiv_to_utc(meta_time, startdate):
    # "14 листопада · 19:00 за Києвом"
    m=re.search(r'(\d{1,2})\s+([а-яі]+)\s*·\s*(?:близько\s*)?(\d{1,2}):(\d{2})\s+за Києвом',meta_time or '')
    if not m: return None
    day,mon,hh,mm=int(m.group(1)),UKM.get(m.group(2)),int(m.group(3)),int(m.group(4))
    if not mon: return None
    year=int((startdate or '2026')[:4])
    dt=datetime.datetime(year,mon,day,hh,mm,tzinfo=ZoneInfo('Europe/Kyiv'))
    return dt.astimezone(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%MZ')

DB={'fights':[]}
for r in fights:
    fid=r['id']; ua=r['ua'] or {}; en=r['en'] or {}
    F=FIGHTS.get(fid,{})
    addr=en.get('address_ld') or ua.get('address_ld')
    vname=ua.get('venue_ld') or en.get('venue_ld')
    if vname in VM: city,country=VM[vname]
    else:
        city,country=split_addr(en.get('address_ld') if en.get('address_ld') and re.match(r'[A-Za-z]',en['address_ld']) else None)
        issues.append((fid,'venue not in VM',vname))
    iso,cont=COUNTRY.get(country,(None,None))
    tzname=TZ.get(city)
    if not iso: issues.append((fid,'country unmapped',country))
    if not tzname: issues.append((fid,'tz unmapped',city))
    vc=VC.get(fid)
    sd=ua.get('startDate') or ''
    ldt=None
    if 'T' in sd:
        ldt=datetime.datetime.fromisoformat(sd).astimezone(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%MZ')
    kyiv=[kyiv_to_utc(b.get('time'),ua.get('startDate')) for b in ua.get('broadcast',[])]
    kyiv=[x for x in kyiv if x]
    rec={
     'id':fid,'urls':{'ua':f'/ua/{fid}','en':f'/en/{fid}'},
     'date':ua.get('startDate') or en.get('startDate'),
     'startUtc':None,'startUtcSource':None,'startUtcPrecision':None,
     'broadcastStartsUtc':kyiv,
     'status':'cancelled' if F.get('cancelled') else ('completed' if (F.get('completed') or ((ua.get('startDate') or '9999')[:10]<TODAY)) else 'scheduled'),
     'status_ld':ua.get('status_ld'),'featured':F.get('featured'),'hasPage':True,
     'tournamentId':F.get('tournament') or ua.get('tournament'),
     'title':{'ua':ua.get('h1'),'en':en.get('h1')},
     'fighters':{'red':{'en':(F.get('redEn')),'ua':(F.get('redUk')),'page_ua':ua.get('fighters',{}).get('r'),'page_en':en.get('fighters',{}).get('r')},
                 'blue':{'en':(F.get('blueEn')),'ua':(F.get('blueUk')),'page_ua':ua.get('fighters',{}).get('b'),'page_en':en.get('fighters',{}).get('b')}},
     'stats_ua':ua.get('rows'),'form':ua.get('form'),'index12x3':ua.get('index12x3'),
     'division':{'ua':F.get('divUk'),'en':F.get('divEn')},'rounds':F.get('rounds'),
     'meta':{'ua':ua.get('meta'),'en':en.get('meta')},
     'belts':ua.get('belts') or F.get('belts'),'belt_info':{'ua':ua.get('belt_info'),'en':en.get('belt_info')},
     'venue':{'name':ua.get('venue_ld') or en.get('venue_ld'),'city_en':city,'country_en':country,'country_iso':iso,'continent':cont,'timezone':tzname,
              'address_ua':ua.get('address_ld'),'address_en':en.get('address_ld'),
              'capacity':ua.get('venue_block',{}).get('Місткість'),'city_ua':ua.get('venue_block',{}).get('Місто')},
     'broadcast':{'ua':ua.get('broadcast'),'en':en.get('broadcast')},
     'result':ua.get('result'),
    }
    # cross checks
    if vc and not vc.endswith('T00:00:00Z') and kyiv and all(vc[:16]+'Z'!=k for k in kyiv):
        issues.append((fid,'votes-close time differs from broadcast block',vc,kyiv))
    if F and (F.get('dateUk') and ua.get('startDate')):
        pass
    if not F: rec_notin=True
    if (ua.get('startDate') or '')[:10]!=(en.get('startDate') or '')[:10]: issues.append((fid,'UA/EN date mismatch',ua.get('startDate'),en.get('startDate')))
    # best start time: JSON-LD datetime > votes-close precise > earliest Kyiv broadcast time > votes-close date-only > date only
    if ldt: rec['startUtc'],rec['startUtcSource'],rec['startUtcPrecision']=ldt,'page JSON-LD','time'
    elif vc and not vc.endswith('T00:00:00Z'): rec['startUtc'],rec['startUtcSource'],rec['startUtcPrecision']=vc[:16]+'Z','votes-close.json','time'
    elif kyiv: rec['startUtc'],rec['startUtcSource'],rec['startUtcPrecision']=min(kyiv),'broadcast block (Kyiv time)','broadcast-start'
    elif vc: rec['startUtc'],rec['startUtcSource'],rec['startUtcPrecision']=vc[:16]+'Z','votes-close.json','date-only'
    elif rec['date']: rec['startUtc'],rec['startUtcSource'],rec['startUtcPrecision']=rec['date'][:10]+'T00:00Z','page date','date-only'
    DB['fights'].append(rec)

# fights in FIGHTS without page (completed old) 
page_ids={r['id'] for r in DB['fights']}
for fid,F in FIGHTS.items():
    if fid not in page_ids:
        DB['fights'].append({'id':fid,'hasPage':False,'date':None,'status':'completed' if F.get('completed') else 'scheduled',
          'title':{'ua':f"{F.get('redUk')} vs {F.get('blueUk')}",'en':f"{F.get('redEn')} vs {F.get('blueEn')}"},'unlisted':F.get('unlisted',False),
          'division':{'ua':F.get('divUk'),'en':F.get('divEn')},'rounds':F.get('rounds'),'belts':F.get('belts'),'date_text':F.get('dateEn')})

# ---------- 3. tournaments (cards) ----------
DB['tournaments']=[]
for p in sorted(glob.glob(f'{R}/ua/cards/*.html')):
    tid=os.path.basename(p)[:-5]
    out={'id':tid,'urls':{'ua':f'/ua/cards/{tid}','en':f'/en/cards/{tid}'}}
    for lang in ('ua','en'):
        pp=f'{R}/{lang}/cards/{tid}.html'
        if not os.path.exists(pp): out[lang]=None; continue
        s=soup(pp); lds=ldjson(s)
        ev=next((o for o in lds if o.get('@type')=='SportsEvent'),{})
        loc=ev.get('location',{})
        bc=[]
        for br in s.select('.broadcast-row'):
            pl=br.select_one('.broadcast-platform'); lb=pl.select_one('.broadcast-label') if pl else None
            lab=txt(lb)
            if lb: lb.extract()
            bc.append({'platform':txt(pl),'label':(lab or '').strip(' ·') or None,'time':txt(br.select_one('.broadcast-time'))})
        ven={txt(vr.select_one('.venue-lbl')):txt(vr.select_one('.venue-val')) for vr in s.select('.venue-row')}
        out[lang]={'h1':txt(s.find('h1')),'name':ev.get('name'),'startDate':ev.get('startDate'),'venue':loc.get('name'),'address':loc.get('address'),
                   'organizer':(ev.get('organizer') or {}).get('name'),'fights':[x.get('url','').rstrip('/').split('/')[-1] for x in ev.get('subEvent',[])],
                   'broadcast':bc,'venue_block':ven,'status_ld':(ev.get('eventStatus') or '').split('/')[-1]}
    T=TOUR.get(tid,{})
    out['inHomepageArray']=bool(T)
    out['posterImage']=T.get('img') or (f'/images/cards/{tid}.jpg' if os.path.exists(f'{R}/images/cards/{tid}.jpg') else None)
    DB['tournaments'].append(out)

# ---------- 4. promoters ----------
DB['promoters']=[]
for p in sorted(glob.glob(f'{R}/ua/promoters/*.html')):
    pid=os.path.basename(p)[:-5]; s=soup(p)
    links=sorted({a['href'].rstrip('/').split('/')[-1] for a in s.find_all('a',href=True) if '/cards/' in a['href']})
    DB['promoters'].append({'id':pid,'urls':{'ua':f'/ua/promoters/{pid}','en':f'/en/promoters/{pid}'},'h1':txt(s.find('h1')),'events_linked':links})

# ---------- 5. lean export ----------
COORDS={'Riyadh':(24.71,46.68),'Dubai':(25.20,55.27),'Tokyo':(35.68,139.69),'Johannesburg':(-26.20,28.04),'Melbourne':(-37.81,144.96),
 'London':(51.51,-0.13),'Manchester':(53.48,-2.24),'Sheffield':(53.38,-1.47),'Birmingham':(52.48,-1.90),'Bournemouth':(50.72,-1.88),'Cardiff':(51.48,-3.18),
 'Dublin':(53.35,-6.26),'Düsseldorf':(51.23,6.78),'Rust':(48.27,7.73),'Amsterdam':(52.37,4.90),'Kyiv':(50.45,30.52),'Lviv':(49.84,24.03),'Lisnyky':(50.20,30.40),
 'Vinnytsia':(49.23,28.47),'Las Vegas':(36.17,-115.14),'Carson':(33.83,-118.28),'San Diego':(32.72,-117.16),'San Francisco':(37.77,-122.42),'New York':(40.71,-74.01),
 'Mashantucket':(41.47,-71.96),'San Antonio':(29.42,-98.49),'Quebec City':(46.81,-71.21)}
def first_platforms(arr):
    out=[]
    for b in arr or []:
        p=(b.get('platform') or '').strip()
        if not p or p.startswith('До початку') or p.startswith('Broadcast starts') or p in ('Трансляція','Broadcast'): continue
        if p not in out: out.append(p)
    return out
lean={'generated':TODAY,'fights':[],'tournaments':[],'promoters':[]}
for r in DB['fights']:
    if not r.get('hasPage') or not r.get('date'): continue
    v=r['venue']; city=v.get('city_en'); co=COORDS.get(city)
    if not co: issues.append((r['id'],'no coords for city',city))
    prec='time' if r['startUtcPrecision']=='time' else 'date'
    res=r.get('result') or {}
    lean['fights'].append({'id':r['id'],'urls':r['urls'],'date':r['date'][:10],'startUtc':r['startUtc'] if prec=='time' else None,'startPrecision':prec,
      'startSource':r['startUtcSource'],'status':r['status'],'tournamentId':r['tournamentId'],
      'red':{'ua':r['fighters']['red']['ua'],'en':r['fighters']['red']['en']},'blue':{'ua':r['fighters']['blue']['ua'],'en':r['fighters']['blue']['en']},
      'division':r['division'],'rounds':r['rounds'],'belts':r['belts'] or [],
      'venue':{'name':v.get('name'),'cityUa':v.get('city_ua'),'cityEn':city,'countryIso':v.get('country_iso'),'continent':v.get('continent'),'tz':v.get('timezone'),
               'lat':co[0] if co else None,'lon':co[1] if co else None},
      'broadcast':{'ua':first_platforms(r['broadcast']['ua']),'en':first_platforms(r['broadcast']['en'])},
      'result':({'winner':res.get('winner'),'method':res.get('method')} if res.get('winner') else None)})
lean['fights'].sort(key=lambda x:(x['date'],x['startUtc'] or '',x['id']))
for t in DB['tournaments']:
    ua=t.get('ua') or {}; en=t.get('en') or {}
    lean['tournaments'].append({'id':t['id'],'urls':t['urls'],'name':{'ua':ua.get('name'),'en':en.get('name')},'startDate':(ua.get('startDate') or '')[:10],
      'venue':ua.get('venue'),'organizer':ua.get('organizer'),'fights':ua.get('fights') or [],'poster':t.get('posterImage')})
for p in DB['promoters']: lean['promoters'].append({'id':p['id'],'urls':p['urls']})
os.makedirs(f'{R}/data',exist_ok=True)
json.dump(lean,open(f'{R}/data/events.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
print('data/events.json:',len(lean['fights']),'fights,',len(lean['tournaments']),'tournaments,',len(lean['promoters']),'promoters; issues:',len(issues))
for i in issues: print(' ',i)
