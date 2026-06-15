# CONTEXT.md — boxing12x3.com

Shared domain language and project decisions for AI agents working on this codebase.
Read this file before making any changes to the project.

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
| index-v2.html test pattern | Test at boxing12x3.com/index-v2 before replacing index.html |

---

## Domain Terminology

### Data Structures

**FIGHTS** — main array in index.html. Each entry:
```javascript
{id, date, dateUk, red, redUk, blue, blueUk, rounds, completed, hasPage}
```
- `hasPage: true` — fight has a SEO stats page at /ua/{id} and /en/{id}
- `completed: true` — fight is over; moves to "Completed" group in dropdown
- `id` — kebab-case identifier matching the file name (e.g. `garcia-moloney`)

**GUIDE_ARTICLES** — array in index.html for evergreen articles.
```javascript
{id, titleUk, titleEn}
```
Must be declared BEFORE `buildAnalyticsBlock()` function. Currently empty — guide block is hidden until first article is added.

**ARCHIVE** — array in fights-ua.html and fights-en.html for the accordion archive.
```javascript
{month, year, fights: [{id, nameUk, dateUk}]}  // UA version
{month, year, fights: [{id, name, date}]}        // EN version
```
New months go at the TOP of the array. Both files must be updated manually.

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
| `.hint-toggle` | "Як судити?" collapsible button |

### JS Functions

| Function | What it does |
|---|---|
| `tapSide(i, 'red'/'blue')` | Handles round scoring tap — smart default 10:9, then cycles |
| `tapCenter(i)` | Sets/resets 10:10 draw round |
| `renderRound(i)` | Renders a single round — updates fill-div and score colors |
| `getIntensity(diff)` | Returns opacity 0.12–0.80 based on score difference |
| `buildAnalyticsBlock()` | Builds fight links block + guide block, language-aware |
| `updateUI()` | Updates totals, won-strip, leader bar, share button state |
| `buildRounds()` | Generates all round rows — called on fight change |
| `renderAll()` | Full re-render: labels, fights, rounds — called on language change |

### Pour Animation (color fill on scoring)

Each `.rside` contains a `.rside-fill` div (position: absolute, z-index: 0).
When a round is scored, JS sets `background` on the fill div and triggers
`pourFromLeft` or `pourFromRight` CSS animation via clip-path.
**Never set `style.background` directly on `.rside`** — it overrides the fill div.

---

## File Structure

```
boxing12x3.com/
├── index.html              ← main tool (scorecard + fight selector + analytics)
├── sitemap.xml             ← update when adding new pages
├── robots.txt
├── og-default.png          ← bilingual OG image for main page
├── og-default-en.png       ← English OG image for /en/ pages
├── ua/
│   ├── fights.html         ← fight archive accordion (update ARCHIVE array)
│   ├── guide.html          ← evergreen article hub (create when 1st article ready)
│   ├── garcia-moloney.html ← fight SEO page
│   ├── nery-casimero.html
│   ├── billam-smith-rozicki.html
│   ├── rodriguez-vargas.html
│   ├── crocker-paro.html
│   ├── zayas-ennis.html
│   └── boxing-scoring.html ← first evergreen article (to be created)
└── en/
    └── [mirrors ua/ structure]
```

---

## Monthly Workflow

### After each fight:
1. Add result block to `/ua/{id}.html` and `/en/{id}.html` (after `.info` block, before `.cta`)
2. Set `completed: true` for that fight in `FIGHTS` array in `index.html`

### At the start of new month:
1. Remove previous month's fights from `FIGHTS` in `index.html` (keep `hasPage` SEO pages on server)
2. Add new month's fights to `FIGHTS`
3. Add new month to TOP of `ARCHIVE` in `fights-ua.html` and `fights-en.html`
4. Update `sitemap.xml` with new page URLs
5. For new fights with SEO pages: set `hasPage: true` when page is uploaded

### When adding a guide article:
1. Add entry to `GUIDE_ARTICLES` in `index.html`:
   ```javascript
   {id:'boxing-scoring', titleUk:'Як судять бокс', titleEn:'How boxing scoring works'}
   ```
2. Create `/ua/{id}.html` and `/en/{id}.html`
3. Add to `ua/guide.html` and `en/guide.html` hub pages

---

## SEO Structure

**Fight pages** — `/ua/garcia-moloney` etc.
- Schema.org SportsEvent JSON-LD in `<head>`
- hreflang UA ↔ EN
- OG image: Ukrainian pages use `og-default.png`, English use `og-default-en.png`
- Result block added after fight (after `.info`, before `.cta`)

**Archive** — `/ua/fights` and `/en/fights`
- Accordion by month, newest first
- Only fights with `hasPage: true` appear here

**Guide** — `/ua/guide` and `/en/guide`
- Hub page listing evergreen articles
- Hidden on main page until `GUIDE_ARTICLES` has ≥1 entry

**Google Search Console** — boxing12x3.com property verified via DNS (Cloudflare)
Sitemap submitted: `https://boxing12x3.com/sitemap.xml`

---

## Widget Mode

Adding `?widget=1` to any URL hides:
- `#uaLinks` (Telegram, podcast, blog links)
- `#analyticsBlock` and `#guideBlock`
- `.hint-toggle` (how to score guide)

Shows: `#poweredBy` ("Powered by Boxing 12×3 →" link)

Embed code template:
```html
<iframe
  src="https://boxing12x3.com/?fight=zayas-ennis&lang=en&widget=1"
  width="100%" height="600" frameborder="0" style="border-radius:12px;border:none;">
</iframe>
```

---

## Known Bugs Fixed (do not reintroduce)

- **Favicon** — href must use `%3C` and `%3E` for `<` and `>` inside SVG data URI
- **Template literals** — no backtick strings in JS; use string concatenation
- **Fill div** — pour animation uses `.rside-fill` child div; never set `style.background` on `.rside` parent
- **GUIDE_ARTICLES** — must be declared at top of script, before any function that references it
- **innerHTML with `<br>`** — avoid HTML tags inside JS strings in `<script>` tags; use `textContent` + CSS wrapping

---

## Working Conventions

1. **Discuss before coding** — always agree on the plan before writing a line
2. **Surgical changes** — `str_replace` on specific lines, not full file rewrites
3. **Test with index-v2.html** — major changes go to v2 first; replace index.html only after testing
4. **Validate JS** — always run `node -e "new Function(s)"` before presenting files
5. **Upload files, not copy-paste** — for GitHub; Cyrillic encoding breaks on copy-paste
6. **Karpathy principles** — Think Before Coding, Simplicity First, Surgical Changes, Goal-Driven

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

## Sources for Evergreen Content

- ABC Unified Rules: `abcboxing.com/unified-rules-boxing/`
- BBBofC Rules 2025: `bbbofc.com/build/documents/Rules_and_Regulations_2025.pdf`
- BBBofC How to Score: `bbbofc.com/how-to-score`
- WBO 10-point system: `wboboxing.com`
- WBC Championship Rules: `wbcboxing.com`
