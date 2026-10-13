#!/usr/bin/env python3
"""Bake JS-built link lists (boxer catalogs, fights lists) into static HTML (crawlers without JavaScript).

The catalog is still built by build() in the page script from BOXER_PROFILES (source of truth).
This script renders each page in headless Chromium and stores the resulting markup between
<!--bake:start--> and <!--bake:end--> inside each container, so every link exists in the raw HTML.
Run from the repo root after BOXER_PROFILES changes:  python3 scripts/bake_catalog.py
"""
import re, pathlib
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
# (file, container id, selector that signals the render is done, link class)
TARGETS = [
    ('ua/boxers.html', 'catalog', '.div-block', 'boxer-link'),
    ('en/boxers.html', 'catalog', '.div-block', 'boxer-link'),
    ('ua/fights.html', 'archive', '.month-block', 'fight-link'),
    ('ua/fights.html', 'legendary', '.month-block', 'fight-link'),
    ('en/fights.html', 'archive', '.month-block', 'fight-link'),
    ('en/fights.html', 'legendary', '.month-block', 'fight-link'),
    ('ua/boxing-history.html', 'monthGrid', '.month-cell', 'month-cell active'),
    ('en/boxing-history.html', 'monthGrid', '.month-cell', 'month-cell active'),
]
START, END = '<!--bake:start-->', '<!--bake:end-->'

with sync_playwright() as p:
    b = p.chromium.launch()
    ctx = b.new_context()
    ctx.route('**/*', lambda r: r.continue_() if r.request.url.startswith('file:') else r.abort())
    for f, cid, sel, cls in TARGETS:
        path = ROOT / f
        src = path.read_text(encoding='utf-8')
        page = ctx.new_page()
        page.goto(path.as_uri())
        page.wait_for_selector('#%s %s' % (cid, sel))
        html = page.evaluate("document.getElementById('%s').innerHTML" % cid)
        page.close()
        html = re.sub(r'\s*' + re.escape(START) + '.*?' + re.escape(END), '', html, flags=re.S)
        block = START + html + END
        open_tag = '<div class="month-grid" id="%s">' % cid if cid == 'monthGrid' else '<div id="%s">' % cid
        pat = re.compile(re.escape(open_tag) + re.escape(START) + '.*?' + re.escape(END), re.S)
        if pat.search(src):
            src = pat.sub(lambda m: open_tag + block, src, 1)
        else:
            assert open_tag + '</div>' in src, (f, cid)
            src = src.replace(open_tag + '</div>', open_tag + block + '</div>', 1)
        path.write_text(src, encoding='utf-8')
        print(f, cid, 'links:', len(re.findall(r'<a class="%s' % cls, block)))
    b.close()
