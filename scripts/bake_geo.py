#!/usr/bin/env python3
"""GEO layer for upcoming fight pages: lead paragraph under H1 + WebPage JSON-LD (author, publisher, dateModified).

Run after build_events.py / gen_index.py:   python3 scripts/bake_geo.py [--dry]

* Lead paragraph (<!-- Intro -->): hand-checked text per fight, taken from the facts already on the page
  (FAQ answers / SportsEvent). If a time, platform or belt changes on a page, change the text in INTRO below too.
* WebPage JSON-LD: publisher Boxing 12x3, author Andrii Rozanov (sameAs only in markup, no visible links).
* dateModified: moves only when the page facts change (hash of SportsEvent + FAQPage JSON-LD + lead text),
  stored in data/geo-modified.json. Cosmetic edits do not move it.
Idempotent. Upcoming fights come from the same list as gen_index.py (FIGHTS in ua/scorecard.html).
"""
import re, sys, json, hashlib, datetime
sys.path.insert(0, __file__.rsplit('/', 1)[0])
import gen_index as g
ROOT = g.ROOT
MOD = ROOT + 'data/geo-modified.json'

AUTHOR = {
    'ua': dict(name='Андрій Розанов', job='Боксерський журналіст і коментатор'),
    'en': dict(name='Andrii Rozanov', job='Boxing journalist and commentator'),
}
SAMEAS = ['https://ua.tribuna.com/uk/blogs/brave_hearts/']

# id -> (ua, en)
INTRO = {
 'yabuki-fajardo': (
  "Бій Ябукі – Фахардо на 12 раундів: на кону пояс IBF в найлегшій вазі, для Масаміці Ябукі це четвертий захист. Бій відбудеться 26 листопада в Токіо, трансляція на Lemino, турнір розпочнеться о 10:00 за Києвом.",
  "Yabuki vs Fajardo is a scheduled 12-round fight for the IBF flyweight title, Masamichi Yabuki's fourth defense. It takes place on November 26 in Tokyo and is streamed on Lemino; the event starts at 3:00 AM ET / 8:00 AM GMT."),
 'chukhadzhian-arganaras': (
  "Бій Чухаджян – Арганарас на 12 раундів у першій напівсередній вазі відбудеться 27 листопада в Русті, Німеччина; титул на кону поки не оголошено. Трансляція на ARD 1 Mediathek, початок не раніше 18:00 за Києвом.",
  "Chukhadzhian vs Arganaras is a scheduled 12-round super lightweight fight on November 27 in Rust, Germany; no title has been announced yet. It is broadcast on ARD 1 Mediathek, starting no earlier than 11:00 AM ET / 4:00 PM GMT."),
 'kabayel-hysa': (
  "Бій Кабаєл – Хіса на 12 раундів: на кону пояс WBC в надважкій вазі, для Агіта Кабаєла це перший захист. Бій відбудеться 28 листопада в Дюссельдорфі, трансляція на DAZN починається о 20:00 за Києвом, головний бій – орієнтовно о 23:00.",
  "Kabayel vs Hysa is a scheduled 12-round fight for the WBC heavyweight title, Agit Kabayel's first defense. It takes place on November 28 in Düsseldorf and is streamed on DAZN from 1:00 PM ET / 6:00 PM GMT; the main event is expected around 4:00 PM ET / 9:00 PM GMT."),
 'kraus-deines': (
  "Бій Краус – Дейнес на 10 раундів у напівважкій вазі: на кону європейський пояс IBF (IBF European). Бій відбудеться 28 листопада в Амстердамі, трансляція на Videoland, трансляція карду починається о 21:30 за Києвом.",
  "Kraus vs Deines is a scheduled 10-round light heavyweight fight for the IBF European title. It takes place on November 28 in Amsterdam and is broadcast on Videoland; the card broadcast starts at 2:30 PM ET / 7:30 PM GMT."),
 'lozan-burgos': (
  "Бій Лозан – Бургос на 8 раундів у напівсередній вазі: на кону пояс чемпіона світу WBC серед молоді. Бій відбудеться 5 грудня в Києві, трансляція на Київстар ТБ, час початку ще не оголошено.",
  "Lozan vs Burgos is a scheduled 8-round welterweight fight for the WBC Youth World title. It takes place on December 5 in Kyiv and is shown on Kyivstar TV; the start time has not been announced yet."),
 'sorokin-serguta': (
  "Бій Сорокін – Сергута на 10 раундів у надважкій вазі: на кону пояс чемпіона України. Бій відбудеться 5 грудня в Києві, у карді вечора Лозан – Бургос, трансляція на Київстар ТБ, час початку ще не оголошено.",
  "Sorokin vs Serguta is a scheduled 10-round heavyweight fight for the Ukrainian title. It takes place on December 5 in Kyiv on the Lozan vs Burgos card and is shown on Kyivstar TV; the start time has not been announced yet."),
 'petrosyan-jara': (
  "Бій Петросян – Хара на 8 раундів у напівсередній вазі, без пояса. Бій відбудеться 5 грудня в Києві, у карді вечора Лозан – Бургос, трансляція на Київстар ТБ, час початку ще не оголошено.",
  "Petrosyan vs Jara is a scheduled 8-round non-title welterweight fight. It takes place on December 5 in Kyiv on the Lozan vs Burgos card and is shown on Kyivstar TV; the start time has not been announced yet."),
 'mckenna-aleksejevs': (
  "Бій Маккена – Алексєєв на 12 раундів: на кону пояс IBF у середній вазі. Це головний бій турніру Zuffa Boxing 14, він відбудеться 4 грудня в Ер-Ріяді; трансляція на Setanta Sports, турнір починається о 19:00 за Києвом.",
  "McKenna vs Aleksejevs is the main event of Zuffa Boxing 14, a scheduled 12-round fight for the IBF middleweight title. It takes place on December 4 in Riyadh; the broadcast starts at 12:00 PM ET / 5:00 PM GMT on Sky Sports (UK and Ireland), Paramount+ (US and Canada) and Setanta Sports (Ukraine)."),
 'massey-tabiti': (
  "Бій Мессі – Табіті на 10 раундів у важкій вазі, без пояса, у програмі турніру Zuffa Boxing 14. Бій відбудеться 4 грудня в Ер-Ріяді; трансляція на Setanta Sports, турнір починається о 19:00 за Києвом.",
  "Massey vs Tabiti is a scheduled 10-round non-title cruiserweight fight on the Zuffa Boxing 14 card. It takes place on December 4 in Riyadh; the broadcast starts at 12:00 PM ET / 5:00 PM GMT on Sky Sports (UK and Ireland), Paramount+ (US and Canada) and Setanta Sports (Ukraine)."),
 'chelli-hart': (
  "Бій Келлі – Гарт на 10 раундів у напівважкій вазі, без пояса, у програмі турніру Zuffa Boxing 14. Бій відбудеться 4 грудня в Ер-Ріяді; трансляція на Setanta Sports, турнір починається о 19:00 за Києвом.",
  "Chelli vs Hart is a scheduled 10-round non-title light heavyweight fight on the Zuffa Boxing 14 card. It takes place on December 4 in Riyadh; the broadcast starts at 12:00 PM ET / 5:00 PM GMT on Sky Sports (UK and Ireland), Paramount+ (US and Canada) and Setanta Sports (Ukraine)."),
 'rozicki-ntambwe': (
  "Бій Розицький – Нтамбве на 10 раундів у важкій вазі, без пояса, у програмі турніру Zuffa Boxing 14. Бій відбудеться 4 грудня в Ер-Ріяді; трансляція на Setanta Sports, турнір починається о 19:00 за Києвом.",
  "Rozicki vs Ntambwe is a scheduled 10-round non-title cruiserweight fight on the Zuffa Boxing 14 card. It takes place on December 4 in Riyadh; the broadcast starts at 12:00 PM ET / 5:00 PM GMT on Sky Sports (UK and Ireland), Paramount+ (US and Canada) and Setanta Sports (Ukraine)."),
 'sirenko-martin': (
  "Бій Сіренко – Мартін на 10 раундів у надважкій вазі, без пояса, у програмі турніру Zuffa Boxing 14. Бій відбудеться 4 грудня в Ер-Ріяді; трансляція на Setanta Sports, турнір починається о 19:00 за Києвом.",
  "Sirenko vs Martin is a scheduled 10-round non-title heavyweight fight on the Zuffa Boxing 14 card. It takes place on December 4 in Riyadh; the broadcast starts at 12:00 PM ET / 5:00 PM GMT on Sky Sports (UK and Ireland), Paramount+ (US and Canada) and Setanta Sports (Ukraine)."),
 'talley-musah': (
  "Бій Таллі – Муса на 8 раундів у важкій вазі, без пояса, у програмі турніру Zuffa Boxing 14. Бій відбудеться 4 грудня в Ер-Ріяді; трансляція на Setanta Sports, турнір починається о 19:00 за Києвом.",
  "Talley vs Musah is a scheduled 8-round non-title cruiserweight fight on the Zuffa Boxing 14 card. It takes place on December 4 in Riyadh; the broadcast starts at 12:00 PM ET / 5:00 PM GMT on Sky Sports (UK and Ireland), Paramount+ (US and Canada) and Setanta Sports (Ukraine)."),
 'fury-joshua': (
  "Бій Ф'юрі – Джошуа на 12 раундів: на кону вакантний пояс WBA (Super) у надважкій вазі. Бій відбудеться 11 грудня в Кардіффі на Principality Stadium, трансляція на Netflix, головний бій – приблизно о 03:00 за Києвом у ніч на 12 грудня.",
  "Fury vs Joshua is a scheduled 12-round fight for the vacant WBA Super heavyweight title. It takes place on December 11 at the Principality Stadium in Cardiff and is streamed on Netflix; the main event is expected around 8:00 PM ET / 1:00 AM GMT (Dec 12)."),
 'bakole-wilder': (
  "Бій Баколе – Вайлдер на 10 раундів у надважкій вазі, без пояса, у карді вечора Ф'юрі – Джошуа. Бій відбудеться 11 грудня в Кардіффі, трансляція на Netflix, час початку цього бою ще не оголошено.",
  "Bakole vs Wilder is a scheduled 10-round non-title heavyweight fight on the Fury vs Joshua card. It takes place on December 11 in Cardiff and is streamed on Netflix; the start time of this fight has not been announced yet."),
 'haney-paro': (
  "Бій Хейні – Паро на 12 раундів – об'єднання поясів у напівсередній вазі: Девін Хейні захищає пояс WBO, Ліам Паро – пояс IBF. Бій відбудеться 19 грудня в Сан-Франциско, трансляція на DAZN починається 20 грудня о 03:00 за Києвом, головний бій – орієнтовно о 06:00.",
  "Haney vs Paro is a scheduled 12-round welterweight unification fight: Devin Haney is the WBO champion and Liam Paro is the IBF champion. It takes place on December 19 in San Francisco and is streamed on DAZN from 8:00 PM ET / 1:00 AM GMT; the main event is expected around 11:00 PM ET / 4:00 AM GMT."),
}

CSS = ".lede{font-size:14px;line-height:1.6;color:var(--text);margin:0 0 16px;}\n"

def bake(fid, lg, mod, today, dry):
    path = ROOT + f'{lg}/{fid}.html'
    s = open(path, encoding='utf-8').read()
    text = INTRO[fid][0 if lg == 'ua' else 1]
    block = f'<!-- Intro -->\n<p class="lede">{text}</p>\n<!-- /Intro -->\n'
    if '<!-- Intro -->' in s:
        s = re.sub(r'<!-- Intro -->.*?<!-- /Intro -->\n', lambda m: block, s, flags=re.S)
    else:
        m = re.search(r'<div class="meta">.*?</div>\n', s, flags=re.S)
        s = s[:m.end()] + block + s[m.end():]
    if '.lede{' not in s:
        s = s.replace('</style>', CSS + '</style>', 1)
    lds = re.findall(r'<script type="application/ld\+json">(.*?)</script>', s, flags=re.S)
    se = next(json.loads(x) for x in lds if '"SportsEvent"' in x[:120])
    faq = next(x for x in lds if '"FAQPage"' in x)
    h = hashlib.sha256((json.dumps(se, sort_keys=True) + faq + text).encode()).hexdigest()[:16]
    key = f'{lg}/{fid}'
    if mod.get(key, {}).get('hash') != h:
        mod[key] = {'hash': h, 'date': today}
    a = AUTHOR[lg]
    title = re.search(r'<title>(.*?)</title>', s).group(1)
    canon = re.search(r'<link rel="canonical" href="([^"]+)"', s).group(1)
    wp = {"@context": "https://schema.org", "@type": "WebPage", "name": title, "url": canon,
          "inLanguage": 'uk' if lg == 'ua' else 'en', "dateModified": mod[key]['date'],
          "about": {"@type": "SportsEvent", "name": se['name'], "startDate": se['startDate']},
          "author": {"@type": "Person", "name": a['name'], "url": "https://boxing12x3.com/about", "jobTitle": a['job'], "sameAs": SAMEAS},
          "publisher": {"@type": "Organization", "name": "Boxing 12×3", "url": "https://boxing12x3.com"}}
    tag = '<script type="application/ld+json">' + json.dumps(wp, ensure_ascii=False, separators=(',', ':')) + '</script>\n'
    if '"@type":"WebPage"' in s:
        s = re.sub(r'<script type="application/ld\+json">\{[^\n]*?"@type":"WebPage".*?</script>\n', lambda m: tag, s, count=1, flags=re.S)
    else:
        i = s.index('<script type="application/ld+json">{"@context":"https://schema.org","@type":"FAQPage"')
        s = s[:i] + tag + s[i:]
    if not dry:
        open(path, 'w', encoding='utf-8').write(s)

if __name__ == '__main__':
    dry = '--dry' in sys.argv
    try: mod = json.load(open(MOD))
    except FileNotFoundError: mod = {}
    today = datetime.date.today().isoformat()
    ids = g.upcoming_ids()
    missing = [i for i in ids if i not in INTRO]
    if missing: sys.exit('No INTRO text for: ' + ', '.join(missing))
    for fid in ids:
        for lg in ('ua', 'en'): bake(fid, lg, mod, today, dry)
    if not dry: json.dump(mod, open(MOD, 'w'), indent=1, sort_keys=True)
    print(f'{len(ids)} fights x 2 languages', '(dry)' if dry else 'written')
