# CONTEXT.md — boxing12x3.com

Shared domain language and project decisions for AI agents working on this codebase.
Read this file before making any changes to the project.
Last updated: August 2026

---

## What This Project Is

**boxing12x3.com** — interactive boxing scorecard tool with bilingual SEO pages.
- Owner: Андрій Розанов, boxing editor at Ua.Tribuna.com
- Stack: static HTML + CSS + JS on Vercel (GitHub repo)
- Languages: Ukrainian (primary) and English
- Goal: passive income via affiliate, direct sponsorship, widget licensing

---

## Architecture Decisions

| Decision | Why |
|---|---|
| Static HTML, not Next.js | Free hosting, zero maintenance, no build step |
| Bilingual via separate files /ua/ and /en/ | Better SEO than ?lang= param |
| Flat URLs: /ua/boxing-scoring | Simpler to maintain than /ua/guide/scoring |
| cleanUrls: true in vercel.json | Removes .html from URLs |
| No template literals (backticks) in JS | Caused SyntaxError in browser preview |
| Favicon uses %3C %3E, not raw < > | Raw angle brackets in href break HTML parser |
| Widget via ?widget=1 on index.html | No duplicate file; all updates apply to widget automatically |
| No copy-paste for GitHub uploads | Cyrillic encoding breaks; always use Upload files |
| www → non-www redirect | Cloudflare Page Rule: www.boxing12x3.com/* → https://boxing12x3.com/$1 (301) |

---

## Domain Terminology

### Data Structures

**FIGHTS** — main array in index.html. Each entry:
```javascript
{id, date, dateUk, red, redUk, blue, blueUk, rounds, completed, hasPage}
```
- `hasPage: true` — fight has a SEO stats page at /ua/{id} and /en/{id}
- `completed: true` — fight is over; moves to "Completed" group in dropdown
- `id` — kebab-case identifier matching the file name (e.g. `romero-lopez`)
- Upcoming fights sorted by date ascending (nearest first) via JS sort

**GUIDE_ARTICLES** — array in index.html for evergreen articles.
```javascript
{id, titleUk, titleEn}
```
Must be declared BEFORE `buildAnalyticsBlock()`. Currently has 3 entries:
```javascript
const GUIDE_ARTICLES = [
  {id:'boxing-scoring', titleUk:'Як судять бокс: система 10 балів', titleEn:'How Boxing Scoring Works'},
  {id:'boxing-scorecards', titleUk:'Як читати суддівські картки в боксі', titleEn:'How to Read Boxing Scorecards'},
  {id:'boxing-organizations', titleUk:'WBC, WBA, IBF та WBO: що це за організації і як влаштовані пояси', titleEn:'WBC, WBA, IBF and WBO Explained'},
];
```
Guide block on main page shows when GUIDE_ARTICLES.length ≥ 1.
"Всі бої →" link shows when pages.length > 0 (at least 1 hasPage fight).

**ARCHIVE** — array in fights-ua.html and fights-en.html for the accordion archive.
```javascript
{month, year, fights: [{id, nameUk, dateUk}]}  // UA version
{month, year, fights: [{id, name, date}]}        // EN version
```
New months go at the TOP. Both files must be updated manually.
Only fights with `hasPage: true` appear in archive.

### CSS Classes

| Class | What it is |
|---|---|
| `.rrow` | Round row container (grid: 1fr 40px 1fr) |
| `.rside` | Clickable half of a round row (left = red, right = blue) |
| `.rside-fill` | Animated fill div inside rside — DO NOT set background on .rside directly |
| `.rpts` | Score number inside rside (Bebas Neue, z-index:1 above fill) |
| `.rn` | Round number center column (also triggers 10:10 on click) |
| `.won-strip` | "Виграних раундів" counter above scorecard rows |
| `.analytics-block` | Fight stats links block below scorecard |
| `.hint-toggle` | "Як судити?" collapsible button — auto-opens on first visit |
| `.main-btn` | Share/CTA button — red when active, gray when disabled |

### JS Functions

| Function | What it does |
|---|---|
| `tapSide(i, 'red'/'blue')` | Handles round scoring tap + closes hint on first use |
| `tapCenter(i)` | Sets/resets 10:10 draw round |
| `renderRound(i)` | Renders a single round — updates fill-div and score colors |
| `getIntensity(diff)` | Returns opacity 0.12–0.80 based on score difference |
| `buildAnalyticsBlock()` | Builds fight links block + guide block, language-aware |
| `updateUI()` | Updates totals, won-strip, leader bar, share button state |
| `buildRounds()` | Generates all round rows — called on fight change |
| `renderAll()` | Full re-render: labels, fights, rounds — called on language change |
| `getDefaultFight()` | Returns nearest upcoming fight (sorted by date) |
| `loadState()` | Loads saved state from localStorage — only restores scores if saved fight still exists in FIGHTS |

### Pour Animation (color fill on scoring)

Each `.rside` contains a `.rside-fill` div (position: absolute, z-index: 0).
When a round is scored, JS sets `background` on the fill div and triggers
`pourFromLeft` or `pourFromRight` CSS animation via clip-path.
**Never set `style.background` directly on `.rside`** — it overrides the fill div.

### localStorage Keys

| Key | What it stores |
|---|---|
| `b12x3_fight` | Last selected fight id |
| `b12x3_scores` | Scored rounds array |
| `b12x3_stop` | Stoppage data |
| `b12x3_hint_seen` | Whether user has seen the hint (closes it after first tap) |

---

## File Structure

```
boxing12x3.com/
├── index.html              ← main tool
├── privacy.html            ← Privacy Policy (covers site + Threads API app)
├── sitemap.xml
├── robots.txt
├── og-default.png          ← UA OG image
├── og-default-en.png       ← EN OG image
├── CONTEXT.md              ← this file
├── ua/
│   ├── fights.html         ← fight archive accordion
│   ├── guide.html          ← evergreen article hub (3 articles)
│   ├── boxing-scoring.html ← evergreen: система 10 балів
│   ├── boxing-scorecards.html ← evergreen: як читати картки
│   ├── boxing-organizations.html ← evergreen: WBC/WBA/IBF/WBO
│   ├── garcia-moloney.html
│   ├── nery-casimero.html
│   ├── billam-smith-rozicki.html
│   ├── rodriguez-vargas.html
│   ├── crocker-paro.html
│   ├── zayas-ennis.html
│   ├── mason-bell.html     ← July 5, completed, TKO 12
│   ├── joshua-prenga.html  ← July 25, completed, KO 2
│   ├── spence-tszyu.html   ← July 25, completed, UD 12
│   ├── derevyanchenko-hackett.html ← July 25, completed, UD 10
│   └── romero-lopez.html   ← Aug 22, upcoming
└── en/ [mirrors ua/ structure]
```

---

## Monthly Workflow

### After each fight:
1. Add result block to `/ua/{id}.html` and `/en/{id}.html` (before `.cta`)
2. Set `completed: true` for that fight in `FIGHTS` array in `index.html`

### Result block templates:

**Stoppage (KO/TKO):**
```html
<div class="result">
  <div class="result-top">
    <div class="result-label">Переможець</div>
    <div class="result-winner">Ім'я переможця</div>
    <div class="result-method">ТКО · Раунд N</div>
  </div>
</div>
```

**Decision (UD/SD/MD) with scorecards:**
```html
<div class="result">
  <div class="result-top">
    <div class="result-label">Переможець</div>
    <div class="result-winner">Ім'я переможця</div>
    <div class="result-method">Одностайне рішення суддів · 12 раундів</div>
  </div>
  <div class="result-judges">
    <div class="result-judge-title">Рахунки суддів</div>
    <div class="result-judge-row"><span class="rj-name">Суддя 1</span><div class="rj-scores"><span class="rj-score w">115</span><span class="rj-dash">–</span><span class="rj-score l">113</span></div></div>
    ...
  </div>
</div>
```

**KO with pre-fight knockdown details (Joshua style):**
Use `.result-judges` with custom rows instead of scorecard rows:
```html
<div class="result-judges">
  <div class="result-judge-title">Деталі бою</div>
  <div class="result-judge-row"><span class="rj-name">Раунд 1</span><span class="rj-scores"><span class="rj-score l">2 нокдауни Джошуа</span></span></div>
  <div class="result-judge-row"><span class="rj-name">Раунд 2</span><span class="rj-scores"><span class="rj-score w">КО Пренги</span></span></div>
</div>
```

Result CSS must be added to the page if not present (check with `grep "\.result{"` before adding).

### At the start of new month:
1. Remove ALL previous month's fights from `FIGHTS` (SEO pages stay on server)
2. Add new month's fights to `FIGHTS`
3. Add new month to TOP of `ARCHIVE` in `fights-ua.html` and `fights-en.html`
4. Update `sitemap.xml` with new page URLs

### When adding a guide article:
1. Add entry to `GUIDE_ARTICLES` in `index.html`
2. Create `/ua/{id}.html` and `/en/{id}.html`
3. Add to `ua/guide.html` and `en/guide.html` hub pages
4. Add cross-links between related articles ("Читай далі" block)
5. Update sitemap.xml

---

## SEO Structure

**index.html:**
- `<h1 class="brand-name">Boxing 12×3</h1>` — H1 is the brand name
- hreflang: uk (/) and en (?lang=en)
- Schema.org: WebApplication
- Title: 50+ chars with keywords
- www → non-www: Cloudflare Page Rule (301)

**Fight pages** — `/ua/romero-lopez` etc.
- Schema.org SportsEvent JSON-LD with: name, description, startDate, endDate, eventStatus, location (with address), image, performer, sport
- hreflang UA ↔ EN + x-default
- Result block added after fight (before `.cta`)

**Evergreen articles** — `/ua/boxing-scoring` etc.
- Schema.org Article JSON-LD
- Cross-links between related articles via "Читай далі" block
- `max-width: 65ch` on `article p` for readability
- Sources section at bottom

**Google Search Console** — boxing12x3.com property verified via DNS (Cloudflare)
Sitemap: `https://boxing12x3.com/sitemap.xml`

---

## Infrastructure

**Email:** contact@boxing12x3.com → Cloudflare Email Routing → rozanovandriy88@gmail.com

**DNS:** Cloudflare (proxied). MX records: route1/2/3.mx.cloudflare.net
SPF: `v=spf1 include:_spf.mx.cloudflare.net ~all`

**www redirect:** Cloudflare Page Rule: `www.boxing12x3.com/*` → `https://boxing12x3.com/$1` (301)

---

## Design & Typography Rules

From design skill audit — mandatory:

- **Em-dash ban** — never use `—` (U+2014). Use en-dash `–` (U+2013) everywhere
- **Blockquote** — gray background `#f0ede8`, border-radius: 6px. NO `border-left` colored accent
- **Hover** — always inside `@media (hover: hover) and (pointer: fine)`
- **prefers-reduced-motion** — all pages must include:
  ```css
  @media (prefers-reduced-motion: reduce) {
    *, *::before, *::after { animation-duration: .01ms !important; transition-duration: .01ms !important; }
  }
  ```
- **Article line width** — `article p { max-width: 65ch; }`
- **Focus rings** — `button:focus-visible, a:focus-visible { outline: 2px solid var(--red); outline-offset: 2px; }`
- **DM Sans** — keep (identity preservation, do not replace despite being on reflex-reject list)
- **Background #f7f6f3** — keep (identity preservation)

---

## Widget Mode

Adding `?widget=1` hides: `#uaLinks`, `#analyticsBlock`, `#guideBlock`, `.hint-toggle`
Shows: `#poweredBy` ("Powered by Boxing 12×3 →")

---

## Known Bugs Fixed (do not reintroduce)

- **Favicon** — href must use `%3C` and `%3E` for `<` and `>` inside SVG data URI
- **Template literals** — no backtick strings in JS; use string concatenation
- **Fill div** — pour animation uses `.rside-fill` child div; never set `style.background` on `.rside` parent
- **GUIDE_ARTICLES** — must be declared before any function that references it
- **loadState** — scores only restored if saved fight id still exists in FIGHTS array; otherwise fresh state. Prevents old month's scores appearing on new month's fights
- **Dropdown placeholder** — `ph.disabled = true; ph.hidden = true;` — cannot be selected
- **Default fight** — `getDefaultFight()` returns nearest upcoming by date, not FIGHTS[0]
- **Date sorting** — uses `new Date(f.date + ', 2026')` — works for "Aug 22" format

---

## Working Conventions

1. **Discuss before coding** — always agree on the plan before writing a line
2. **Surgical changes** — `str_replace` on specific lines, not full file rewrites
3. **Validate JS** — always run `node -e "new Function(s)"` before presenting files
4. **Upload files, not copy-paste** — for GitHub; Cyrillic encoding breaks on copy-paste
5. **Em-dash check** — run `python3 -c "c=open('f.html').read(); print(c.count('\u2014'))"` before delivering files
6. **Result CSS check** — `grep -c "\.result{" filename.html` before adding result block
7. **Karpathy principles** — Think Before Coding, Simplicity First, Surgical Changes, Goal-Driven

---

## Monetization Roadmap

| Stage | Mechanism | Condition |
|---|---|---|
| Now | Direct sponsorship "картка вечора за підтримки X" | Any traffic |
| Now | Affiliate Favbet/Parimatch on UA pages | Any traffic |
| Widget live | Sponsorship slot inside widget | Widget embedded anywhere |
| 3k+/month | Fan scorecard aggregation (Supabase free tier) | Meaningful data volume |
| Later | AdSense as passive floor | 5-10k visits/month |

---

## Content Roadmap

**Evergreen articles (done):**
1. Як судять бокс: система 10 балів → /ua/boxing-scoring
2. Як читати суддівські картки → /ua/boxing-scorecards
3. WBC/WBA/IBF/WBO → /ua/boxing-organizations
4. Нокаут і нокдаун → planned (draft ready, awaiting user text)

**Fight pages workflow:**
- Texts written by owner (UA first, then EN translation)
- AI prepares draft structure with stats, owner adds voice, sends back both languages
- AI builds HTML pages following established template

---

## Sources for Evergreen Content

- ABC Unified Rules: `abcboxing.com/unified-rules-boxing/`
- BBBofC Rules 2025: `bbbofc.com`
- WBO 10-point system: `wboboxing.com`
- WBC Championship Rules: `wbcboxing.com`
- WBA Rules: `wbaboxing.com`
