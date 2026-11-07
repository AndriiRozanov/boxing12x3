#!/usr/bin/env python3
"""Share images (1200x630) for promoter pages: ropes + logo plate + 'BOXING 12x3'.
Usage: python3 scripts/og_promoter.py logo <logo.png> <out.png>
       python3 scripts/og_promoter.py title "Промоутери" "РЕЗУЛЬТАТИ · КАРДИ · СТАТИСТИКА БОЇВ" <out.png>
Fonts: needs `npm i @fontsource/oswald` in FONTDIR (default: ./node_modules). Playwright required."""
import sys,base64,os
from playwright.sync_api import sync_playwright
FD=os.environ.get('FONTDIR','node_modules')+'/@fontsource/oswald/files/oswald-'
def f(n): return base64.b64encode(open(f'{FD}{n}-normal.woff2','rb').read()).decode()
def ropes(yc):
    out=''
    for y in (yc-200,yc-100,yc,yc+100,yc+200):
        yi=yc+(y-yc)*0.42
        for x0,x1 in ((48,318),(1152,882)):
            out+=f'<polygon points="{x0},{y-5.5} {x1},{yi-3.5} {x1},{yi+3.5} {x0},{y+5.5}" fill="#fff"/>'
    return f'<svg style="position:absolute;left:0;top:0" width="1200" height="630">{out}</svg>'
def page(center,yc=290):
    return f'''<html><style>
@font-face{{font-family:O;font-weight:600;src:url(data:font/woff2;base64,{f('latin-600')})}}
@font-face{{font-family:O;font-weight:700;src:url(data:font/woff2;base64,{f('latin-700')})}}
@font-face{{font-family:O;font-weight:600;unicode-range:U+0400-04FF;src:url(data:font/woff2;base64,{f('cyrillic-600')})}}
@font-face{{font-family:O;font-weight:700;unicode-range:U+0400-04FF;src:url(data:font/woff2;base64,{f('cyrillic-700')})}}
*{{margin:0;box-sizing:border-box}}body{{width:1200px;height:630px;background:#181818;font-family:O;color:#fff;position:relative;overflow:hidden}}
.r{{position:absolute;left:0;top:0;bottom:0;width:16px;background:#c0392b}}.b{{position:absolute;right:0;top:0;bottom:0;width:16px;background:#1a5276}}
.url{{position:absolute;right:50px;top:36px;font-size:17px;letter-spacing:.18em;color:#9a9a9a}}
.c{{position:absolute;left:0;right:0;top:{yc}px;transform:translateY(-50%);text-align:center}}
.plate{{display:inline-flex;align-items:center;justify-content:center;background:#fff;border-radius:18px;width:520px;height:190px}}.plate img{{width:420px}}
h1{{font-size:84px;font-weight:700;letter-spacing:.04em;text-transform:uppercase}}.s{{font-size:24px;letter-spacing:.14em;color:#bbb;margin-top:10px}}
.foot{{position:absolute;left:0;right:0;bottom:34px;text-align:center;font-size:30px;font-weight:700;letter-spacing:.14em}}
</style><body><div class="r"></div><div class="b"></div><div class="url">BOXING12X3.COM</div>{ropes(yc)}<div class="c">{center}</div><div class="foot">BOXING 12×3</div></body></html>'''
def shot(html,out):
    open('/tmp/_og.html','w',encoding='utf-8').write(html)
    with sync_playwright() as p:
        b=p.chromium.launch(); pg=b.new_page(viewport={'width':1200,'height':630}); pg.goto('file:///tmp/_og.html'); pg.wait_for_timeout(300); pg.screenshot(path=out); b.close()
m=sys.argv[1]
if m=='logo':
    d=base64.b64encode(open(sys.argv[2],'rb').read()).decode()
    shot(page(f'<div class="plate"><img src="data:image/png;base64,{d}"></div>'),sys.argv[3])
else:
    shot(page(f'<h1>{sys.argv[2]}</h1><div class="s">{sys.argv[3]}</div>'),sys.argv[4])
