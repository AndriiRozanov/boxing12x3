#!/usr/bin/env python3
"""Bake the /ua/boxers and /en/boxers catalog into static HTML (crawlers without JavaScript).

The catalog is still built by build() in the page script from BOXER_PROFILES (source of truth).
This script renders each page in headless Chromium and stores the resulting markup between
<!--bake:start--> and <!--bake:end--> inside <div id="catalog">, so every boxer link exists in the raw HTML.
Run from the repo root after BOXER_PROFILES changes:  python3 scripts/bake_catalog.py
"""
import re, pathlib
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
FILES = ['ua/boxers.html', 'en/boxers.html']
START, END = '<!--bake:start-->', '<!--bake:end-->'

with sync_playwright() as p:
    b = p.chromium.launch()
    ctx = b.new_context()
    ctx.route('**/*', lambda r: r.continue_() if r.request.url.startswith('file:') else r.abort())
    for f in FILES:
        path = ROOT / f
        src = path.read_text(encoding='utf-8')
        page = ctx.new_page()
        page.goto(path.as_uri())
        page.wait_for_selector('#catalog .div-block')
        html = page.evaluate("document.getElementById('catalog').innerHTML")
        page.close()
        html = re.sub(r'\s*' + re.escape(START) + '.*?' + re.escape(END), '', html, flags=re.S)
        block = START + html + END
        if START in src:
            src = re.sub(re.escape(START) + '.*?' + re.escape(END), lambda m: block, src, flags=re.S)
        else:
            assert '<div id="catalog"></div>' in src, f
            src = src.replace('<div id="catalog"></div>', '<div id="catalog">' + block + '</div>', 1)
        path.write_text(src, encoding='utf-8')
        print(f, 'links:', len(re.findall(r'<a class="boxer-link"', block)))
    b.close()
