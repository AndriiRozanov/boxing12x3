#!/usr/bin/env python3
"""Personal share images (1200x630) for ACTIVE boxer cards: name, country + division,
birthplace + debut year, flag, height and reach. No record and no titles (they change).
Data is read from the cards themselves (ua|en/boxers/<slug>.html, cards with 'Активний боксер').
Usage: python3 scripts/og_boxer.py            # all active cards, UA + EN
       python3 scripts/og_boxer.py slug ...   # selected slugs
Output: og/boxers/ua/<slug>.png, og/boxers/en/<slug>.png. Playwright required.
A new active boxer needs: a city in CITY_LOC (UA locative) and a country in COUNTRY."""
import re, sys, os, glob, tempfile
from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# nationality (JSON-LD, English) -> (iso flag, UA name)
COUNTRY = {
    'Albania': ('al', 'Албанія'), 'Armenia': ('am', 'Вірменія'), 'Australia': ('au', 'Австралія'),
    'Canada': ('ca', 'Канада'), 'Croatia': ('hr', 'Хорватія'), 'Cuba': ('cu', 'Куба'),
    'Democratic Republic of the Congo': ('cd', 'ДР Конго'), 'France': ('fr', 'Франція'),
    'Germany': ('de', 'Німеччина'), 'Italy': ('it', 'Італія'), 'Japan': ('jp', 'Японія'),
    'Kosovo': ('xk', 'Косово'), 'Netherlands': ('nl', 'Нідерланди'), 'New Zealand': ('nz', 'Нова Зеландія'),
    'Nigeria': ('ng', 'Нігерія'), 'Poland': ('pl', 'Польща'), 'South Africa': ('za', 'ПАР'),
    'Sweden': ('se', 'Швеція'), 'Ukraine': ('ua', 'Україна'), 'United Kingdom': ('gb', 'Велика Британія'),
    'United States': ('us', 'США'), 'Uzbekistan': ('uz', 'Узбекистан'), 'Venezuela': ('ve', 'Венесуела'), 'Ghana': ('gh', 'Гана'), 'Puerto Rico': ('pr', 'Пуерто-Рико'),
}
# UA birthplace city (nominative, as on the card) -> locative after "Народився в/у"
CITY_LOC = {
    'Леверкузен': 'Леверкузені', 'Квебек': 'Квебеку', 'Уотфорд': 'Уотфорді', 'Стокгольм': 'Стокгольмі',
    'Сариосіо': 'Сариосіо', 'Лейкленд': 'Лейкленді', 'Епсом': 'Епсомі', 'Камагуей': 'Камагуеї',
    'Лондон': 'Лондоні', 'Фінікс': 'Фініксі', 'Гамільтон': 'Гамільтоні', 'Таскалуса': 'Таскалусі',
    'Угелі': 'Угелі', 'Загреб': 'Загребі', 'Те-Авамуту': 'Те-Авамуту', 'Гуантанамо': 'Гуантанамо',
    'Рим': 'Римі', 'Гюмрі': 'Гюмрі', 'Морон': 'Мороні', 'Кананга': 'Кананзі', 'Сідней': 'Сіднеї',
    'Бруклін': 'Брукліні', 'Окленд': 'Окленді', 'Медоубрук': 'Медоубруку', 'Косьцежина': 'Косьцежині',
    'Йоганнесбург': 'Йоганнесбурзі', 'Кадуна': 'Кадуні', 'Косово': 'Косові', 'Армавір': 'Армавірі',
    'Сан-Ігнасіо-де-Сабанета': 'Сан-Ігнасіо-де-Сабанеті', 'Козенице': 'Козеницях',
    'Сьєго-де-Авіла': 'Сьєго-де-Авілі', 'Хекінан': 'Хекінані', 'Кежмарок': 'Кежмарку',
    'Шкодер': 'Шкодері', 'Сімферополь': 'Сімферополі', 'Туларе': 'Туларе',
    'Берген-оп-Зом': 'Бергені-оп-Зомі', 'Кемпбеллтаун': 'Кемпбеллтауні', 'Манчестер': 'Манчестері',
    'Світловодськ': 'Світловодську', 'Сьєнфуегос': 'Сьєнфуегосі',
    'Ель-Вігія': 'Ель-Вігії', 'Ліверпуль': 'Ліверпулі', 'Вест-Бромвіч': 'Вест-Бромвічі', 'Белград': 'Белграді', 'Аккра': 'Аккрі', 'Атланта': 'Атланті',
}


def cell(t, lbl):
    m = re.search(r'<div class="fact-lbl">(?:%s)</div><div class="fact-val">(.*?)</div>' % lbl, t, re.S)
    return re.sub(r'<a.*?</a>', '', m.group(1)).strip() if m else None


def data(slug):
    ua = open(f'{ROOT}/ua/boxers/{slug}.html', encoding='utf-8').read()
    en = open(f'{ROOT}/en/boxers/{slug}.html', encoding='utf-8').read()
    nat = re.search(r'"nationality":\{"@type":"Country","name":"([^"]*)"', ua).group(1)
    iso, cu = COUNTRY[nat]
    city_ua = cell(ua, 'Місце народження').split(',')[0].strip()
    city_en = cell(en, 'Born|Birthplace|Place of birth').split(',')[0].strip()
    loc = CITY_LOC[city_ua]
    pre = 'у' if loc[0] in 'ВвФф' else 'в'
    h = cell(ua, 'Зріст'); r = cell(ua, 'Розмах рук'); debut = cell(ua, 'Дебют')
    num = lambda s: re.match(r'\d+', s).group(0) if s and re.match(r'\d+', s) else None
    divs_ua = [d.strip() for d in cell(ua, 'Дивізіон[и]*').split(',')]
    divs_en = [d.strip() for d in cell(en, 'Divisions?').split(',')]
    return dict(
        slug=slug, iso=iso, h=num(h), reach=num(r), debut=debut,
        ua=dict(name=re.search(r'<h1>(.*?)</h1>', ua).group(1),
                line2=f'{cu} · ' + ' / '.join(divs_ua) + ' вага',
                line3=f'Народився {pre} {loc} · дебют у {debut}', lh='Зріст', lr='Розмах', cm='см'),
        en=dict(name=re.search(r'<h1>(.*?)</h1>', en).group(1),
                line2=f'{nat if nat != "United Kingdom" else "Great Britain"} · ' + ' / '.join(divs_en),
                line3=f'Born in {city_en} · debuted in {debut}', lh='Height', lr='Reach', cm='cm'))


def html():
    css = open(f'{ROOT}/fonts/fonts.css', encoding='utf-8').read().replace("url('/fonts/", f"url('file://{ROOT}/fonts/")
    return f'''<!doctype html><meta charset=utf-8><style>{css}
body{{margin:0}}
#c{{width:1200px;height:630px;background:#111;position:relative;font-family:Manrope,sans-serif;color:#fff;border-left:14px solid #c0392b;box-sizing:border-box;padding:56px 66px;overflow:hidden}}
.top{{display:flex;justify-content:space-between;font-size:30px;letter-spacing:.2em;font-weight:700}}
.top span:last-child{{font-size:24px;letter-spacing:.05em;color:#888;font-weight:500}}
#name{{font-size:112px;font-weight:700;line-height:1.05;margin-top:36px;white-space:nowrap;width:max-content}}
#l2{{font-family:Oswald,sans-serif;font-size:46px;color:#c0392b;letter-spacing:.06em;margin-top:18px;text-transform:uppercase;white-space:nowrap;font-weight:600;width:max-content}}
#l3{{font-size:34px;color:#aaa;margin-top:22px;font-weight:500;white-space:nowrap;width:max-content}}
.row{{position:absolute;left:66px;bottom:52px;display:flex;gap:46px;align-items:flex-end}}
.big{{font-family:Oswald,sans-serif;font-size:76px;line-height:1;font-weight:600}}
.lbl{{font-size:20px;color:#888;letter-spacing:.1em;text-transform:uppercase;margin-bottom:6px;font-weight:500}}
#flag{{height:60px;width:80px;border-radius:5px;margin-bottom:6px}}
</style><div id=c><div class=top><span>Boxing 12×3</span><span>boxing12x3.com</span></div>
<div id=name></div><div id=l2></div><div id=l3></div>
<div class=row><img id=flag><div id=bh><div class=lbl id=lh></div><div class=big id=vh></div></div><div id=br><div class=lbl id=lr></div><div class=big id=vr></div></div></div></div>'''


FIT = '''(d)=>{const $=i=>document.getElementById(i);
$('flag').src='file://%s/images/flags/'+d.iso+'.png';
$('name').textContent=d.t.name;$('l2').textContent=d.t.line2;$('l3').textContent=d.t.line3;
$('lh').textContent=d.t.lh;$('vh').textContent=d.h+' '+d.t.cm;
$('br').style.display=d.reach?'':'none';$('lr').textContent=d.t.lr;$('vr').textContent=d.reach?d.reach+' '+d.t.cm:'';
$('bh').style.display=d.h?'':'none';
for(const [id,px] of [['name',112],['l2',46],['l3',34]]){let s=px;$(id).style.fontSize=s+'px';while($(id).offsetWidth>1050&&s>20){s-=2;$(id).style.fontSize=s+'px';}}
return document.fonts.ready.then(()=>true);}''' % ROOT


def main():
    slugs = sys.argv[1:] or sorted(
        os.path.basename(f)[:-5] for f in glob.glob(f'{ROOT}/ua/boxers/*.html')
        if 'Активний боксер' in open(f, encoding='utf-8').read())
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1200, 'height': 630})
        tmp = os.path.join(tempfile.mkdtemp(), 'og.html'); open(tmp, 'w', encoding='utf-8').write(html())
        pg.goto('file://' + tmp); pg.wait_for_timeout(500)
        for s in slugs:
            d = data(s)
            for lg in ('ua', 'en'):
                pg.evaluate(FIT, dict(iso=d['iso'], h=d['h'], reach=d['reach'], t=d[lg]))
                pg.wait_for_timeout(120)
                pg.evaluate(FIT, dict(iso=d['iso'], h=d['h'], reach=d['reach'], t=d[lg]))
                pg.locator('#c').screenshot(path=f'{ROOT}/og/boxers/{lg}/{s}.png')
            print('ok', s)
        b.close()


if __name__ == '__main__':
    main()
