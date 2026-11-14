#!/usr/bin/env python3
"""Bake ua/calendar.html and en/calendar.html from data/events.json.

Run after scripts/build_events.py:  python3 scripts/build_events.py && python3 scripts/bake_calendar.py
The upcoming fights are written straight into the HTML (for Google and for no-JS readers);
the page script only filters, groups by day and shows times in the reader's time zone.
"""
import json, os, datetime, html

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = json.load(open(f'{R}/data/events.json', encoding='utf-8'))
TODAY = datetime.datetime.now(datetime.timezone.utc).date()
TOUR = {t['id']: t for t in D['tournaments']}
BASE = 'https://boxing12x3.com'

S = {
 'uk': dict(lang='uk', path='ua', other='en', loc='uk_UA', og='og-default.png',
   title='Календар боксерських боїв: розклад і час | Boxing 12×3',
   desc='Календар боксерських боїв: дати, час у вашому часовому поясі, країни й трансляції. Фільтри за країною, континентом і датою, пошук і режим «Біля мене».',
   h1='Календар боксерських боїв', sub='Календар боїв', crumb=('Головна', 'Календар'),
   lead='Найближчі боксерські бої світу з часом у вашому часовому поясі. Обирайте країну, континент чи дату або знайдіть бій поруч із собою.',
   months=['січня','лютого','березня','квітня','травня','червня','липня','серпня','вересня','жовтня','листопада','грудня'],
   wd=['неділя','понеділок','вівторок','середа','четвер','пʼятниця','субота'], wds=['Нд','Пн','Вт','Ср','Чт','Пт','Сб'],
   tba='Час уточнюється', fallback_label='за Києвом', fb_tz='Europe/Kyiv', tz_fixed='Час показано за Києвом (увімкніть JavaScript, щоб побачити свій час).',
   search='Боксер, турнір, місто…', f_date='Дата', f_near='Біля мене', f_cont='Континент', f_ctry='Країна', f_tz='Показувати час',
   filters='Фільтри', tz_change='Змінити', d_all='Усі', d_today='Сьогодні', d_7='7 днів', d_month='Місяць', d_pick='Обрати дати…', from_='З', to_='До',
   near_btn='📍 Показати поруч', near_on='📍 Біля мене', near_denied='Дозвіл на місце не надано. Його можна увімкнути в налаштуваннях браузера.',
   near_unsup='Браузер не підтримує визначення місця.', radius='Радіус', radius_all='Весь світ', km='км',
   yourtime='Ваш час', yourtime_lbl='Ваш час', auto_note='визначено автоматично', chosen_note='обрано вами', tz_auto='Автоматично (ваш пояс)',
   empty_near='Поруч із вами боїв не знайдено. Спробуйте збільшити радіус.', today='сьогодні', reset='Скинути фільтри', empty='За цими фільтрами боїв не знайдено.', range_txt='боїв', rounds='раундів', all_fights='Усі бої',
   tz_names={'Europe/Kyiv':'Київ','Europe/London':'Лондон','Europe/Berlin':'Берлін','Europe/Madrid':'Мадрид','America/New_York':'Нью-Йорк','America/Chicago':'Чикаго','America/Los_Angeles':'Лос-Анджелес','Asia/Dubai':'Дубай','Asia/Riyadh':'Ер-Ріяд','Asia/Tokyo':'Токіо','Australia/Sydney':'Сідней','Africa/Johannesburg':'Йоганнесбург','America/Mexico_City':'Мехіко','Asia/Manila':'Маніла','UTC':'UTC'},
   countries={'SA':'Саудівська Аравія','US':'США','GB':'Британія','AU':'Австралія','JP':'Японія','DE':'Німеччина','NL':'Нідерланди','AE':'ОАЕ','UA':'Україна','IE':'Ірландія','CA':'Канада','ZA':'ПАР','MX':'Мексика'},
   conts={'Europe':'Європа','Asia':'Азія','North America':'Пн. Америка','South America':'Пд. Америка','Oceania':'Океанія','Africa':'Африка'},
   footer=[('/', 'Головна'), ('/ua/scorecard', 'Картка'), ('/ua/guide', 'Довідник'), ('/height-compare', 'Порівняй зріст'), ('/about', 'Про нас'), ('/privacy', 'Конфіденційність')],
   home='/', ph_fights=('бій', 'бої', 'боїв')),
 'en': dict(lang='en', path='en', other='ua', loc='en_US', og='og-default-en.png',
   title='Boxing Schedule: Fight Dates and Times | Boxing 12×3',
   desc='Boxing schedule with fight dates, times in your own time zone, countries and broadcasters. Filter by country, continent and date, search, or find fights near you.',
   h1='Boxing fight schedule', sub='Boxing schedule', crumb=('Home', 'Schedule'),
   lead='Upcoming boxing fights worldwide, with times in your own time zone. Pick a country, a continent or a date, or find a fight near you.',
   months=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'],
   wd=['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'], wds=['Sun','Mon','Tue','Wed','Thu','Fri','Sat'],
   tba='Time TBA', fallback_label='UTC', fb_tz='UTC', tz_fixed='Times are shown in UTC (turn on JavaScript to see your local time).',
   search='Boxer, event, city…', f_date='Date', f_near='Near me', f_cont='Continent', f_ctry='Country', f_tz='Show times in',
   filters='Filters', tz_change='Change', d_all='All', d_today='Today', d_7='7 days', d_month='Month', d_pick='Pick dates…', from_='From', to_='To',
   near_btn='📍 Show nearby', near_on='📍 Near me', near_denied='Location permission was not granted. You can allow it in your browser settings.',
   near_unsup='This browser cannot detect your location.', radius='Radius', radius_all='Worldwide', km='km',
   yourtime='Your local time', yourtime_lbl='Your local time', auto_note='detected automatically', chosen_note='chosen by you', tz_auto='Automatic (your zone)',
   empty_near='No fights found near you. Try a larger radius.', today='today', reset='Reset filters', empty='No fights match these filters.', range_txt='fights', rounds='rounds', all_fights='All fights',
   tz_names={'Europe/Kyiv':'Kyiv','Europe/London':'London','Europe/Berlin':'Berlin','Europe/Madrid':'Madrid','America/New_York':'New York','America/Chicago':'Chicago','America/Los_Angeles':'Los Angeles','Asia/Dubai':'Dubai','Asia/Riyadh':'Riyadh','Asia/Tokyo':'Tokyo','Australia/Sydney':'Sydney','Africa/Johannesburg':'Johannesburg','America/Mexico_City':'Mexico City','Asia/Manila':'Manila','UTC':'UTC'},
   countries={'SA':'Saudi Arabia','US':'USA','GB':'UK','AU':'Australia','JP':'Japan','DE':'Germany','NL':'Netherlands','AE':'UAE','UA':'Ukraine','IE':'Ireland','CA':'Canada','ZA':'South Africa','MX':'Mexico'},
   conts={'Europe':'Europe','Asia':'Asia','North America':'N. America','South America':'S. America','Oceania':'Oceania','Africa':'Africa'},
   footer=[('/en', 'Home'), ('/en/scorecard', 'Scorecard'), ('/en/guide', 'Guide'), ('/en/height-compare', 'Height Compare'), ('/en/about', 'About'), ('/privacy', 'Privacy')],
   home='/en', ph_fights=('fight', 'fights', 'fights')),
}

CSS = """
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
:root{--red:#c0392b;--red-l:#fdf2f2;--red-b:#f5b7b1;--blue:#1a5276;--bg:#f7f6f3;--card:#fff;--text:#1a1a1a;--muted:#888;--border:#e5e3de;--r:10px;--green:#2e7d32}
body{font-family:'Manrope',sans-serif;background:var(--bg);color:var(--text);padding:1.5rem 1rem 4rem;line-height:1.5;font-size:14px;-webkit-font-smoothing:antialiased}
a{color:inherit;text-decoration:none}
.wrap{max-width:1120px;margin:0 auto}
.lang-row{display:flex;justify-content:flex-end;gap:4px;margin-bottom:1rem}
.lang-btn{font-size:11px;font-weight:500;padding:4px 10px;border-radius:20px;border:0.5px solid var(--border);background:transparent;color:var(--muted)}
.lang-btn.on{background:var(--text);color:#fff;border-color:var(--text)}
.brand{text-align:center;margin-bottom:1.25rem}
.brand-name{font-family:'Oswald',sans-serif;text-transform:uppercase;font-size:28px;letter-spacing:.12em;color:var(--text);margin:0;font-weight:700}
.brand-sub{font-size:10px;color:var(--muted);letter-spacing:.18em;text-transform:uppercase}
.breadcrumb{font-size:12px;color:var(--muted);margin-bottom:14px}
.breadcrumb a{color:var(--muted)}
h1{font-size:26px;font-weight:800;line-height:1.15;margin-bottom:6px;letter-spacing:-.01em}
.lead{font-size:13.5px;color:#555;line-height:1.6;margin-bottom:12px;max-width:720px}
.tzl{font-size:11px;color:var(--muted);display:flex;align-items:center;gap:6px;margin-bottom:12px}
.tzl b{color:var(--text);font-weight:700}
.tzedit{display:none;font:inherit;font-size:11px;font-weight:600;color:var(--red);background:none;border:0;cursor:pointer;padding:0 0 0 4px;text-decoration:underline;text-underline-offset:2px}
.tzedit.show{display:inline}
#tzrow{margin:-4px 0 12px}
.tzl i{width:6px;height:6px;border-radius:50%;background:var(--green);display:inline-block;flex-shrink:0}
.layout{display:grid;grid-template-columns:minmax(0,1fr);gap:0 28px}
.layout>div{min-width:0}
@media(min-width:900px){.layout{grid-template-columns:260px minmax(0,1fr)}.filters{position:sticky;top:16px;align-self:start}}
.filters{background:var(--card);border:0.5px solid var(--border);border-radius:var(--r);padding:14px;margin-bottom:14px}
.ftop{display:flex;gap:8px;align-items:stretch;margin-bottom:12px}
.search{flex:1;min-width:0;display:flex;align-items:center;gap:8px;border:0.5px solid var(--border);border-radius:8px;padding:0 10px;background:#fcfbf9}
.fbtn{display:none;align-items:center;gap:6px;font:inherit;font-size:13px;font-weight:600;padding:0 12px;border-radius:8px;border:0.5px solid var(--border);background:#fff;color:#333;cursor:pointer}
.fbtn svg{width:12px;height:12px;transition:transform .25s ease}
.fbtn[aria-expanded=true] svg{transform:rotate(180deg)}
.fbtn .cnt{display:none;min-width:18px;height:18px;border-radius:9px;background:var(--red);color:#fff;font-size:10px;font-weight:700;align-items:center;justify-content:center;padding:0 5px}
.fbtn .cnt.show{display:inline-flex}
@media(max-width:899px){
.fbtn{display:inline-flex}
.ftop{margin-bottom:0}
.fwrap{display:grid;grid-template-rows:0fr;opacity:0;transition:grid-template-rows .28s ease,opacity .2s ease,margin-top .28s ease;margin-top:0}
.fwrap.open{grid-template-rows:1fr;opacity:1;margin-top:12px}
.fbody{overflow:hidden;min-height:0}
}
@media(prefers-reduced-motion:reduce){.fwrap,.fbtn svg{transition:none}}
.search input{flex:1;min-width:0;border:0;background:transparent;font:inherit;font-size:13px;padding:9px 0;outline:none;color:var(--text)}
.fg{margin-bottom:12px}.fg:last-child{margin-bottom:0}
.fgl{font-size:10px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:var(--muted);margin-bottom:6px}
.chips{display:flex;gap:6px;flex-wrap:wrap}
.chip{font:inherit;font-size:12px;font-weight:600;padding:6px 11px;border-radius:20px;border:0.5px solid var(--border);background:#fff;color:#555;cursor:pointer;line-height:1.3}
.chip.on{background:#111;border-color:#111;color:#fff}
.chip small{opacity:.6;margin-left:4px;font-weight:600}
.chip.near.on{background:var(--red);border-color:var(--red);color:#fff}
.flag{width:16px;height:12px;object-fit:cover;border-radius:2px;border:0.5px solid var(--border);vertical-align:-1px;margin-right:2px}
.sel{width:100%;font:inherit;font-size:13px;border:0.5px solid var(--border);border-radius:8px;padding:9px 10px;background:#fff;color:#555}
.sub-row{display:none;gap:8px;margin-top:8px;align-items:center;flex-wrap:wrap}
.sub-row.show{display:flex}
.sub-row label{font-size:11px;color:var(--muted)}
.sub-row input[type=date]{font:inherit;font-size:12px;border:0.5px solid var(--border);border-radius:8px;padding:6px 8px;background:#fff}
.note{font-size:11px;color:var(--red);margin-top:6px;display:none}
.note.show{display:block}
.strip{display:flex;gap:6px;overflow-x:auto;padding-bottom:4px;margin-bottom:14px;scrollbar-width:none}
.strip::-webkit-scrollbar{display:none}
.dc{flex:0 0 auto;width:46px;text-align:center;padding:7px 0;border-radius:10px;border:0.5px solid var(--border);background:#fff;font:inherit;cursor:pointer;color:var(--text)}
.dc small{display:block;font-size:9px;color:var(--muted);text-transform:uppercase}
.dc b{display:block;font-size:15px;margin:2px 0}
.dc i{display:block;width:5px;height:5px;border-radius:50%;background:var(--red);margin:0 auto}
.dc.e i{background:transparent}
.dc.tod{border-color:var(--red)}
.dc.on{background:#111;border-color:#111;color:#fff}.dc.on small{color:#bbb}
.count{font-size:12px;color:var(--muted);margin-bottom:10px}
.dayh{display:flex;justify-content:space-between;align-items:baseline;margin:18px 0 8px}
.dayh:first-child{margin-top:0}
.dayh b{font-size:14px;font-weight:800}.dayh span{font-size:11px;color:var(--muted)}
.list{background:var(--card);border:0.5px solid var(--border);border-radius:var(--r);overflow:hidden}
.fr{display:flex;align-items:stretch;border-bottom:0.5px solid var(--border);position:relative}
.fr:last-child{border-bottom:none}
.fr::before{content:'';position:absolute;left:0;top:0;bottom:0;width:2px;background:var(--red)}
.fr.nolink::before{background:#d8d5cd}
a.fr:hover{background:#fcfbf9}
.ft{flex-shrink:0;width:84px;padding:12px 0 12px 14px;display:flex;flex-direction:column;justify-content:center}
.ft b{font-size:15px;font-weight:700;line-height:1}
.ft b.tba{font-size:10.5px;font-weight:600;color:var(--muted);line-height:1.2;padding-right:6px}
.ft small{font-size:9px;color:var(--muted);text-transform:uppercase;margin-top:3px;letter-spacing:.04em}
.fd{width:0.5px;background:var(--border);margin:10px 12px 10px 0;flex-shrink:0}
.fi{flex:1;min-width:0;padding:11px 0}
.fp{font-size:13.5px;font-weight:700;line-height:1.3}
.fp .vs{font-size:10px;color:var(--muted);margin:0 4px;font-weight:400}
.fm{font-size:11.5px;color:var(--muted);margin-top:3px}
.tags{display:flex;gap:4px;margin-top:6px;flex-wrap:wrap}
.tag{font-size:9px;font-weight:700;letter-spacing:.04em;padding:2px 6px;border-radius:3px;background:#f0ede8;color:#555}
.tag.tour{background:var(--red-l);color:var(--red)}
.tag.watch{background:#111;color:#fff}
.fa{flex-shrink:0;padding:0 14px;display:flex;align-items:center;color:var(--muted);font-size:15px}
.empty{display:none;background:var(--card);border:0.5px solid var(--border);border-radius:var(--r);padding:24px;text-align:center;color:#555}
.empty.show{display:block}
.empty button{margin-top:10px}
.site-footer{display:flex;flex-wrap:wrap;justify-content:center;gap:8px 20px;margin-top:40px;padding-top:20px;border-top:0.5px solid var(--border);font-size:12px}
.site-footer a{color:var(--muted)}
.site-footer a:hover{color:var(--red)}
"""

JS = r"""
(function(){
var T=__T__;T.empty_default=document.getElementById('emptytxt').textContent;
var LANG='__LANG__';
var els=[].slice.call(document.querySelectorAll('#list .fr'));
var rows=els.map(function(e){return{el:e,id:e.dataset.id,start:e.dataset.start||'',date:e.dataset.date,iso:e.dataset.iso,cont:e.dataset.cont,
 lat:parseFloat(e.dataset.lat),lon:parseFloat(e.dataset.lon),q:e.dataset.q,tm:e.querySelector('.ft'),meta:e.querySelector('.fm'),metaBase:e.querySelector('.fm').innerHTML};});
var st={q:'',mode:'all',from:'',to:'',day:'',conts:{},ctrs:{},near:false,pos:null,radius:500,tz:'auto'};
try{var saved=localStorage.getItem('b12x3_cal_tz');if(saved)st.tz=saved;}catch(e){}
function zone(){if(st.tz!=='auto')return st.tz;try{return Intl.DateTimeFormat().resolvedOptions().timeZone||'UTC';}catch(e){return 'UTC';}}
function fmt(opts){try{return new Intl.DateTimeFormat('en-GB',opts);}catch(e){return new Intl.DateTimeFormat('en-GB',Object.assign({},opts,{timeZone:'UTC'}));}}
function ymd(d,tz){var p=fmt({timeZone:tz,year:'numeric',month:'2-digit',day:'2-digit'}).formatToParts(d),o={};p.forEach(function(x){o[x.type]=x.value;});return o.year+'-'+o.month+'-'+o.day;}
function hm(d,tz){var p=fmt({timeZone:tz,hour:'2-digit',minute:'2-digit',hourCycle:'h23'}).formatToParts(d),o={};p.forEach(function(x){o[x.type]=x.value;});return o.hour+':'+o.minute;}
function tzName(tz){if(tz==='Europe/Kiev')tz='Europe/Kyiv';if(T.tz_names[tz])return T.tz_names[tz];var s=String(tz).split('/').pop().replace(/_/g,' ');return s;}
function rowDay(r,tz){return r.start?ymd(new Date(r.start),tz):r.date;}
function addDays(s,n){var p=s.split('-');var d=new Date(Date.UTC(+p[0],+p[1]-1,+p[2]+n));return d.toISOString().slice(0,10);}
function dayLabel(s){var p=s.split('-'),d=new Date(Date.UTC(+p[0],+p[1]-1,+p[2]));var w=T.wd[d.getUTCDay()],m=T.months[+p[1]-1],n=+p[2];return LANG==='uk'?(n+' '+m+', '+w):(w+', '+m+' '+n);}
function plural(n){if(LANG!=='uk')return n+' '+(n===1?T.ph[0]:T.ph[1]);var a=n%10,b=n%100;return n+' '+(a===1&&b!==11?T.ph[0]:(a>=2&&a<=4&&(b<12||b>14)?T.ph[1]:T.ph[2]));}
function dist(a,b,c,d){var R=6371,r=Math.PI/180,x=(c-a)*r,y=(d-b)*r;var h=Math.sin(x/2)*Math.sin(x/2)+Math.cos(a*r)*Math.cos(c*r)*Math.sin(y/2)*Math.sin(y/2);return 2*R*Math.asin(Math.sqrt(h));}
function norm(s){return String(s).toLowerCase().replace(/[\u2019\u02bc\u2018\u0060\u00b4]/g,"'");}
function anyOn(o){for(var k in o){if(o[k])return true;}return false;}
function render(){
 var tz=zone(),today=ymd(new Date(),tz),weekEnd=addDays(today,6),monthEnd=addDays(today,29);
 var from='',to='';
 if(st.mode==='today'){from=to=today;}else if(st.mode==='7'){from=today;to=weekEnd;}else if(st.mode==='month'){from=today;to=monthEnd;}else if(st.mode==='range'){from=st.from;to=st.to;}
 var base=[];
 rows.forEach(function(r){
  r.day=rowDay(r,tz);
  if(r.day<today){return;}
  if(st.q&&norm(r.q).indexOf(norm(st.q))<0)return;
  if(from&&r.day<from)return; if(to&&r.day>to)return;
  if(anyOn(st.conts)&&!st.conts[r.cont])return;
  if(anyOn(st.ctrs)&&!st.ctrs[r.iso])return;
  r.km=null;
  if(st.near&&st.pos&&!isNaN(r.lat)){r.km=dist(st.pos.lat,st.pos.lon,r.lat,r.lon);if(st.radius&&r.km>st.radius)return;}
  base.push(r);
 });
 // strip counts (ignore the single-day filter)
 var strip=document.getElementById('strip'),h='';
 for(var i=0;i<14;i++){var dd=addDays(today,i),has=base.some(function(r){return r.day===dd;});var p=dd.split('-'),dt=new Date(Date.UTC(+p[0],+p[1]-1,+p[2]));
  h+='<button type="button" class="dc'+(has?'':' e')+(i===0?' tod':'')+(st.day===dd?' on':'')+'" data-d="'+dd+'"><small>'+T.wds[dt.getUTCDay()]+'</small><b>'+(+p[2])+'</b><i></i></button>';}
 strip.innerHTML=h;
 var vis=base.filter(function(r){return !st.day||r.day===st.day;});
 vis.sort(function(a,b){return a.day<b.day?-1:a.day>b.day?1:((a.start||'9')<(b.start||'9')?-1:(a.start||'9')>(b.start||'9')?1:0);});
 var list=document.getElementById('list');list.innerHTML='';
 var lastDay='',box=null;
 vis.forEach(function(r){
  if(r.day!==lastDay){lastDay=r.day;var n=vis.filter(function(x){return x.day===r.day;}).length;
   var hd=document.createElement('div');hd.className='dayh';hd.innerHTML='<b>'+dayLabel(r.day)+(r.day===today?' · '+T.today:'')+'</b><span>'+plural(n)+'</span>';
   list.appendChild(hd);box=document.createElement('div');box.className='list';list.appendChild(box);}
  var t=r.tm;
  if(r.start){var lbl=st.tz==='auto'?T.yourtime_lbl:tzName(zone());t.innerHTML='<b>'+hm(new Date(r.start),tz)+'</b><small>'+lbl+'</small>';}
  else{t.innerHTML='<b class="tba">'+T.tba+'</b>';}
  r.meta.innerHTML=r.metaBase+(r.km!=null?' · '+Math.round(r.km/10)*10+' '+T.km:'');
  box.appendChild(r.el);
 });
 var cnt=document.getElementById('count');
 cnt.textContent=vis.length?plural(vis.length):'';
 var fc=document.getElementById('fcount'),na=nActive();fc.textContent=na||'';fc.className='cnt'+(na?' show':'');
 document.getElementById('emptytxt').textContent=(st.near&&st.pos&&!vis.length&&!st.q&&!st.day&&st.mode==='all'&&!anyOn(st.conts)&&!anyOn(st.ctrs))?T.empty_near:T.empty_default;
 document.getElementById('empty').className='empty'+(vis.length?'':' show');
 var note=document.getElementById('tznote');
 note.innerHTML=T.yourtime+': <b>'+tzName(zone())+'</b> ('+(st.tz==='auto'?T.auto_note:T.chosen_note)+')';
}
function nActive(){var n=0;if(st.mode!=='all')n++;if(st.near)n++;if(anyOn(st.conts))n++;if(anyOn(st.ctrs))n++;return n;}
function track(a,b){try{if(window.gtag)gtag('event','calendar_filter',{filter:a,value:b});}catch(e){}}
function bind(){
 var fb=document.getElementById('fbtn'),fw=document.getElementById('fwrap');
 fb.addEventListener('click',function(){var o=!fw.classList.contains('open');fw.classList.toggle('open',o);fb.setAttribute('aria-expanded',o?'true':'false');});
 document.getElementById('q').addEventListener('input',function(e){st.q=e.target.value.trim();render();});
 document.getElementById('f-date').addEventListener('click',function(e){var b=e.target.closest('[data-m]');if(!b)return;
  [].forEach.call(this.children,function(c){c.classList.remove('on');});b.classList.add('on');st.mode=b.dataset.m;st.day='';
  document.getElementById('range').className='sub-row'+(st.mode==='range'?' show':'');track('date',st.mode);render();});
 document.getElementById('from').addEventListener('change',function(e){st.from=e.target.value;render();});
 document.getElementById('to').addEventListener('change',function(e){st.to=e.target.value;render();});
 document.getElementById('strip').addEventListener('click',function(e){var b=e.target.closest('[data-d]');if(!b)return;st.day=(st.day===b.dataset.d)?'':b.dataset.d;track('day',st.day||'none');render();});
 document.getElementById('f-cont').addEventListener('click',function(e){var b=e.target.closest('[data-c]');if(!b)return;st.conts[b.dataset.c]=!st.conts[b.dataset.c];b.classList.toggle('on',!!st.conts[b.dataset.c]);track('continent',b.dataset.c);render();});
 document.getElementById('f-ctry').addEventListener('click',function(e){var b=e.target.closest('[data-i]');if(!b)return;st.ctrs[b.dataset.i]=!st.ctrs[b.dataset.i];b.classList.toggle('on',!!st.ctrs[b.dataset.i]);track('country',b.dataset.i);render();});
 var nb=document.getElementById('near'),nn=document.getElementById('nearnote'),nr=document.getElementById('nearrow');
 nb.addEventListener('click',function(){
  if(st.near){st.near=false;nb.classList.remove('on');nb.textContent=T.near_btn;nr.className='sub-row';nn.className='note';render();return;}
  if(!navigator.geolocation){nn.textContent=T.near_unsup;nn.className='note show';return;}
  navigator.geolocation.getCurrentPosition(function(p){st.pos={lat:p.coords.latitude,lon:p.coords.longitude};st.near=true;nb.classList.add('on');nb.textContent=T.near_on;nn.className='note';nr.className='sub-row show';track('near','on');render();},
   function(){nn.textContent=T.near_denied;nn.className='note show';},{maximumAge:600000,timeout:10000});
 });
 document.getElementById('radius').addEventListener('change',function(e){st.radius=parseInt(e.target.value,10)||0;render();});
 document.getElementById('tz').addEventListener('change',function(e){st.tz=e.target.value;try{localStorage.setItem('b12x3_cal_tz',st.tz);}catch(x){}track('timezone',st.tz);render();document.getElementById('tzrow').classList.remove('show');document.getElementById('tzedit').setAttribute('aria-expanded','false');});
 document.getElementById('reset').addEventListener('click',function(){
  st.q='';st.mode='all';st.from=st.to=st.day='';st.conts={};st.ctrs={};st.near=false;
  document.getElementById('q').value='';document.getElementById('from').value='';document.getElementById('to').value='';
  [].forEach.call(document.querySelectorAll('#f-date .chip'),function(c){c.classList.toggle('on',c.dataset.m==='all');});
  [].forEach.call(document.querySelectorAll('#f-cont .chip,#f-ctry .chip'),function(c){c.classList.remove('on');});
  nb.classList.remove('on');nb.textContent=T.near_btn;nr.className='sub-row';document.getElementById('range').className='sub-row';render();});
}
var te=document.getElementById('tzedit'),tr=document.getElementById('tzrow');te.className='tzedit show';
te.addEventListener('click',function(){var o=!tr.classList.contains('show');tr.classList.toggle('show',o);te.setAttribute('aria-expanded',o?'true':'false');});
var sel=document.getElementById('tz');if(st.tz!=='auto'){var ok=[].some.call(sel.options,function(o){return o.value===st.tz;});if(ok)sel.value=st.tz;else st.tz='auto';}
bind();
try{var qp=new URLSearchParams(location.search),qc=qp.get('c');
 if(qc){var cb=document.querySelector('#f-cont [data-c="'+qc.replace(/"/g,'')+'"]');if(cb){st.conts[qc]=true;cb.classList.add('on');}}
 if(qp.get('near')==='1'){var nb2=document.getElementById('near');if(nb2)nb2.click();}
}catch(e){}
render();
})();
"""

def esc(s): return html.escape(s or '', quote=True)

def plural(lk, n):
    p = S[lk]['ph_fights']
    if lk == 'en': return f'{n} {p[0] if n == 1 else p[1]}'
    a, b = n % 10, n % 100
    return f"{n} {p[0] if a == 1 and b != 11 else (p[1] if 2 <= a <= 4 and not 12 <= b <= 14 else p[2])}"

def day_label(lk, d):
    s = S[lk]
    wd = s['wd'][(d.weekday() + 1) % 7]
    return f'{d.day} {s["months"][d.month-1]}, {wd}' if lk == 'uk' else f'{wd}, {s["months"][d.month-1]} {d.day}'

def row_html(f, lk):
    s = S[lk]; u = lk == 'uk'
    a = f['red'][ 'ua' if u else 'en']; b = f['blue']['ua' if u else 'en']
    v = f['venue']; city = v['cityUa'] if u else v['cityEn']
    div = (f['division'] or {}).get('ua' if u else 'en') or ''
    iso = (v.get('countryIso') or '')
    t = TOUR.get(f.get('tournamentId'))
    tname = (t['name']['ua' if u else 'en'] if t else None)
    href = f['urls']['ua' if u else 'en']
    bc = (f['broadcast']['ua' if u else 'en'] or [None])[0]
    tags = ''
    if bc: tags += f'<span class="tag watch">{esc(bc.split(" · ")[0])}</span>'
    for x in (f['belts'] or [])[:2]: tags += f'<span class="tag">{esc(x)}</span>'
    if tname: tags += f'<span class="tag tour">{esc(tname)}</span>'
    flag = f'<img class="flag" src="/images/flags/{iso.lower()}.png" width="16" height="12" alt="" loading="lazy"> ' if iso else ''
    meta = f'{flag}{esc(city)} · {esc(div)} · {f["rounds"]} {s["rounds"]}'
    if f['startUtc']:
        dt = datetime.datetime.strptime(f['startUtc'], '%Y-%m-%dT%H:%MZ').replace(tzinfo=datetime.timezone.utc)
        from zoneinfo import ZoneInfo
        loc = dt.astimezone(ZoneInfo(s['fb_tz']))
        tcell = f'<b>{loc.strftime("%H:%M")}</b><small>{s["fallback_label"]}</small>'
        start = f['startUtc']
    else:
        tcell = f'<b class="tba">{s["tba"]}</b>'; start = ''
    q = ' '.join([f['red']['ua'], f['red']['en'], f['blue']['ua'], f['blue']['en'], (t['name']['ua'] or '') if t else '', (t['name']['en'] or '') if t else '', f['venue']['cityUa'] or '', f['venue']['cityEn'] or '',
                  s['countries'].get(iso, iso), S['uk']['countries'].get(iso, ''), S['en']['countries'].get(iso, ''), v.get('name') or '']).lower()
    attrs = (f'data-id="{f["id"]}" data-start="{start}" data-date="{f["date"]}" data-iso="{iso}" data-cont="{esc(v.get("continent"))}" '
             f'data-lat="{v.get("lat") if v.get("lat") is not None else ""}" data-lon="{v.get("lon") if v.get("lon") is not None else ""}" data-q="{esc(q)}"')
    inner = (f'<div class="ft">{tcell}</div><div class="fd"></div><div class="fi"><div class="fp">{esc(a)}<span class="vs">–</span>{esc(b)}</div>'
             f'<div class="fm">{meta}</div><div class="tags">{tags}</div></div>')
    return f'<a class="fr" href="{href}" {attrs}>{inner}<div class="fa">›</div></a>'

def build(lk):
    s = S[lk]; u = lk == 'uk'
    fl = [f for f in D['fights'] if f['status'] == 'scheduled' and f['date'] >= (TODAY - datetime.timedelta(days=1)).isoformat()]
    fl.sort(key=lambda f: (f['date'], f['startUtc'] or 'z'))
    # baked fallback grouping by fallback-tz day
    from zoneinfo import ZoneInfo
    groups = {}
    for f in fl:
        if f['startUtc']:
            dt = datetime.datetime.strptime(f['startUtc'], '%Y-%m-%dT%H:%MZ').replace(tzinfo=datetime.timezone.utc).astimezone(ZoneInfo(s['fb_tz']))
            d = dt.date()
        else:
            d = datetime.date.fromisoformat(f['date'])
        groups.setdefault(d, []).append(f)
    body = ''
    for d in sorted(groups):
        body += f'<div class="dayh"><b>{day_label(lk, d)}</b><span>{plural(lk, len(groups[d]))}</span></div><div class="list">{"".join(row_html(f, lk) for f in groups[d])}</div>'
    cont = {}; ctr = {}
    for f in fl:
        c = f['venue'].get('continent'); i = f['venue'].get('countryIso')
        if c: cont[c] = cont.get(c, 0) + 1
        if i: ctr[i] = ctr.get(i, 0) + 1
    chip_c = ''.join(f'<button type="button" class="chip" data-c="{esc(c)}">{s["conts"].get(c, c)}<small>{n}</small></button>' for c, n in sorted(cont.items(), key=lambda kv: -kv[1]))
    chip_k = ''.join(f'<button type="button" class="chip" data-i="{i}"><img class="flag" src="/images/flags/{i.lower()}.png" width="16" height="12" alt=""> {s["countries"].get(i, i)}<small>{n}</small></button>' for i, n in sorted(ctr.items(), key=lambda kv: -kv[1]))
    zones = ['Europe/Kyiv', 'Europe/London', 'Europe/Berlin', 'America/New_York', 'America/Chicago', 'America/Los_Angeles', 'Asia/Dubai', 'Asia/Riyadh', 'Asia/Tokyo', 'Australia/Sydney', 'Africa/Johannesburg', 'Asia/Manila', 'UTC']
    zopts = f'<option value="auto">{s["tz_auto"]}</option>' + ''.join(f'<option value="{z}">{s["tz_names"][z]}</option>' for z in zones)
    radius = ''.join(f'<option value="{v}"{" selected" if v == 500 else ""}>{v} {s["km"]}</option>' for v in (500, 1000, 2500, 5000)) + f'<option value="0">{s["radius_all"]}</option>'
    url = f'{BASE}/{s["path"]}/calendar'
    ua_url, en_url = f'{BASE}/ua/calendar', f'{BASE}/en/calendar'
    items = [{'@type': 'ListItem', 'position': i + 1, 'url': BASE + f['urls']['ua' if u else 'en'], 'name': f"{f['red']['ua' if u else 'en']} – {f['blue']['ua' if u else 'en']}"} for i, f in enumerate(fl[:50])]
    ld = {'@context': 'https://schema.org', '@graph': [
        {'@type': 'CollectionPage', 'name': s['h1'], 'description': s['desc'], 'url': url, 'inLanguage': s['lang'],
         'mainEntity': {'@type': 'ItemList', 'numberOfItems': len(items), 'itemListElement': items}},
        {'@type': 'BreadcrumbList', 'itemListElement': [
            {'@type': 'ListItem', 'position': 1, 'name': s['crumb'][0], 'item': BASE + ('/' if u else '/en')},
            {'@type': 'ListItem', 'position': 2, 'name': s['crumb'][1], 'item': url}]}]}
    tdata = {k: s[k] for k in ('tba', 'yourtime', 'yourtime_lbl', 'auto_note', 'chosen_note', 'today', 'km', 'empty_near', 'near_btn', 'near_on', 'near_denied', 'near_unsup', 'tz_names', 'months', 'wd', 'wds')}
    tdata['ph'] = list(s['ph_fights'])
    js = JS.replace('__T__', json.dumps(tdata, ensure_ascii=False)).replace('__LANG__', s['lang'])
    footer = ''.join(f'<a href="{h}">{t}</a>' for h, t in s['footer'])
    date_chips = ''.join(f'<button type="button" class="chip{" on" if m == "all" else ""}" data-m="{m}">{s[k]}</button>' for m, k in (('all', 'd_all'), ('today', 'd_today'), ('7', 'd_7'), ('month', 'd_month'), ('range', 'd_pick')))
    page = f"""<!DOCTYPE html>
<html lang="{s['lang']}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{esc(s['title'])}</title>
<link rel="icon" href="/favicon.ico" sizes="48x48">
<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32.png">
<link rel="icon" type="image/png" sizes="192x192" href="/icon-192.png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<meta name="description" content="{esc(s['desc'])}">
<link rel="canonical" href="{url}">
<link rel="alternate" hreflang="uk" href="{ua_url}">
<link rel="alternate" hreflang="en" href="{en_url}">
<link rel="alternate" hreflang="x-default" href="{en_url}">
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False, separators=(',', ':'))}</script>
<meta property="og:type" content="website">
<meta property="og:url" content="{url}">
<meta property="og:title" content="{esc(s['title'])}">
<meta property="og:description" content="{esc(s['desc'])}">
<meta property="og:image" content="{BASE}/{s['og']}">
<meta property="og:locale" content="{s['loc']}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(s['title'])}">
<meta name="twitter:description" content="{esc(s['desc'])}">
<meta name="twitter:image" content="{BASE}/{s['og']}">
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-GYWWVSZKGY"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','G-GYWWVSZKGY');</script>
<link rel="preload" href="/fonts/manrope-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/fonts/oswald-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/fonts/manrope-cyrillic.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/fonts/fonts.css">
<style>{CSS}</style>
</head>
<body>
<div class="wrap">
<div class="lang-row">
  <a class="lang-btn{' on' if not u else ''}" href="/en/calendar">EN</a>
  <a class="lang-btn{' on' if u else ''}" href="/ua/calendar">UA</a>
</div>
<div class="brand">
  <a href="{s['home']}"><div class="brand-name">Boxing 12×3</div></a>
  <div class="brand-sub">{s['sub']}</div>
</div>
<div class="breadcrumb"><a href="{s['home']}">{s['crumb'][0]}</a> / {s['crumb'][1]}</div>
<h1>{s['h1']}</h1>
<p class="lead">{s['lead']}</p>
<div class="tzl"><i></i><span id="tznote">{s['tz_fixed']}</span><button type="button" class="tzedit" id="tzedit" aria-expanded="false" aria-controls="tzrow">{s['tz_change']}</button></div>
<div class="sub-row" id="tzrow"><label>{s['f_tz']} <select class="sel" id="tz" aria-label="{esc(s['f_tz'])}" style="width:auto">{zopts}</select></label></div>
<div class="layout">
<div>
<div class="filters">
  <div class="ftop"><div class="search">🔎 <input id="q" type="search" placeholder="{esc(s['search'])}" aria-label="{esc(s['search'])}" autocomplete="off"></div>
    <button type="button" class="fbtn" id="fbtn" aria-expanded="false" aria-controls="fbody">{s['filters']}<span class="cnt" id="fcount"></span><svg viewBox="0 0 12 12" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M2 4.5l4 4 4-4"/></svg></button></div>
  <div class="fwrap" id="fwrap"><div class="fbody" id="fbody">
  <div class="fg"><div class="fgl">{s['f_date']}</div><div class="chips" id="f-date">{date_chips}</div>
    <div class="sub-row" id="range"><label>{s['from_']} <input type="date" id="from"></label><label>{s['to_']} <input type="date" id="to"></label></div></div>
  <div class="fg"><div class="fgl">{s['f_near']}</div><div class="chips"><button type="button" class="chip near" id="near">{s['near_btn']}</button></div>
    <div class="sub-row" id="nearrow"><label>{s['radius']} <select class="sel" id="radius" style="width:auto">{radius}</select></label></div><div class="note" id="nearnote"></div></div>
  <div class="fg"><div class="fgl">{s['f_cont']}</div><div class="chips" id="f-cont">{chip_c}</div></div>
  <div class="fg"><div class="fgl">{s['f_ctry']}</div><div class="chips" id="f-ctry">{chip_k}</div></div>
  </div></div>
</div>
</div>
<div>
<div class="strip" id="strip"></div>
<div class="count" id="count"></div>
<div id="list">{body}</div>
<div class="empty" id="empty"><div id="emptytxt">{s['empty']}</div><button type="button" class="chip" id="reset">{s['reset']}</button></div>
</div>
</div>
<div class="site-footer">{footer}</div>
</div>
<script>{js}</script>
</body>
</html>
"""
    assert chr(8212) not in page
    open(f'{R}/{s["path"]}/calendar.html', 'w', encoding='utf-8').write(page)
    print(f'{s["path"]}/calendar.html: {len(fl)} fights, {len(page)//1024} KB')

if __name__ == '__main__':
    for lk in ('uk', 'en'):
        build(lk)
