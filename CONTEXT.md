# CONTEXT.md — boxing12x3.com

Shared domain language and project decisions for AI agents working on this codebase.
Read this file before making any changes to the project.
Last updated: October 2026 (rewritten after the September–October rebuild; the older text described the August state)

---

## What This Project Is

**boxing12x3.com** — interactive boxing scorecard tool with bilingual SEO pages.
- Owner: Андрій Розанов, author of the boxing and combat sports section at Ua.Tribuna.com
- Stack: static HTML + CSS + JS on Vercel; GitHub repo `AndriiRozanov/boxing12x3` is public (live files can be read from `raw.githubusercontent.com/AndriiRozanov/boxing12x3/main/<path>`); DNS on Cloudflare
- Languages: Ukrainian (primary, served at `/`) and English (served at `/en`)
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
| Homepage icon = real files (`/favicon.ico`, `/favicon.svg`, `/apple-touch-icon.png`); other pages keep an inline data-URI icon (with `%3C` `%3E`) | Google reads the favicon from the homepage and cannot use a data-URI; raw angle brackets in an href break the HTML parser |
| Widget via ?widget=1 on index.html | No duplicate file; all updates apply to widget automatically |
| No copy-paste for GitHub uploads | Cyrillic encoding breaks; always use Upload files |
| The apex `boxing12x3.com` is the primary host; `www` redirects to it | Vercel → project → Settings → Domains: `boxing12x3.com` has NO redirect, `www.boxing12x3.com` redirects to `boxing12x3.com` (308). Set on Oct 5 2026; before that it was the opposite (apex → www), which contradicted every canonical, hreflang and sitemap URL. The Cloudflare Page Rule described in older versions was not what served the redirect |
| The page decides the language: `/` = Ukrainian, `/en` = English, `?lang=` overrides | A language saved in localStorage used to override the URL and rendered Ukrainian on `/en`; it is no longer read or written |
| `en/index.html` is GENERATED from `index.html` | Never edit it by hand; see "Building en/index.html" |

---

## Domain Terminology

### Data Structures

**FIGHTS** – main array in index.html. Each entry:
```javascript
{id, date, dateUk, dateEn, dateNum, monthUk, monthIdx, red, redUk, redEn, blue, blueUk, blueEn,
 divUk, divEn, rounds, belts, completed, hasPage, featured, [unlisted]}
```
- `id` – kebab-case, matches the page file name (e.g. `dubois-wardley-2`)
- `monthIdx` – 0-11 (JS `getMonth()`): completed fights show in the dropdown only while their month is the current one. They stay on `/fights` and on their own pages, so no manual clean-up
- `belts` – array. Plain strings for international abbreviations (`'WBC'`), or `{uk, en}` objects for words that must translate (`{uk:'Україна', en:'Ukraine'}`)
- `hasPage: true` – an SEO page exists at `/ua/{id}` and `/en/{id}`
- `completed: true` – fight is over; moves to the "Completed" group
- `featured: true` – the homepage "Ваш прогноз" tile links to this fight. Exactly one upcoming fight with a page should carry it; move it to the next fight when the current one completes, otherwise the tile falls back to "Скоро"
- `unlisted: true` – kept only so the scorecard widget can embed a historical fight; hidden from the dropdown
- Upcoming fights are sorted by date ascending via JS

**GUIDE_ARTICLES** – array in index.html for evergreen articles (`{id, titleUk, titleEn}`). Must be declared BEFORE `buildAnalyticsBlock()`. Currently 5 entries:
```javascript
const GUIDE_ARTICLES = [
  {id:'boxing-scoring', titleUk:'Як судять бокс: система 10 балів', titleEn:'How Boxing Scoring Works: The 10-Point Must System'},
  {id:'boxing-scorecards', titleUk:'Як читати суддівські картки в боксі', titleEn:'How to Read Boxing Scorecards'},
  {id:'boxing-organizations', titleUk:'WBC, WBA, IBF та WBO: що це за організації і як влаштовані пояси', titleEn:'WBC, WBA, IBF and WBO Explained: Boxing Organizations'},
  {id:'boxing-knockouts', titleUk:'Нокаут і нокдаун у боксі: що це таке і як влаштований відлік рефері', titleEn:'Knockout and knockdown in boxing: what they are and how the referee\'},
  {id:'boxing-weight-classes', titleUk:'Вагові категорії в боксі: скільки їх і чим відрізняються', titleEn:'Boxing weight classes: how many there are and how they differ'},
];
```
Guide block on main page shows when GUIDE_ARTICLES.length ≥ 1.
"Всі бої →" link shows when pages.length > 0 (at least 1 hasPage fight).

**ARCHIVE** – array in `ua/fights.html` and `en/fights.html` for the accordion archive (the same pages also hold a second accordion, "Легендарні бої" / "Legendary fights", grouped by year).
```javascript
{month, year, fights: [{id, nameUk, dateUk}]}  // UA version
{month, year, fights: [{id, name, date}]}        // EN version
```
New months go at the TOP. Both files must be updated manually.
Only fights with a page (`hasPage: true`) appear in the archive.

**HISTORY_MONTHS** – array in index.html (`{idx, slug, data, days, ...}`) driving the "This day in boxing" homepage widget; add a month when its `ua/boxing-history/{slug}.html` page exists. If the current month is not covered, the widget falls back to the last covered month.

**BOXER_PROFILES** – shared list of boxers who have a profile page. It is copied into FOUR files (`height-compare.html`, `en/height-compare.html`, `ua/boxers.html`, `en/boxers.html`); update all four when a profile ships. Use the profile `slug`, not the short `id`, in URLs.

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
| `.hint-toggle` | "Як судити?" collapsible button – in-context help for taps; ends with a link to the 10-point guide |
| `.how-block` | "Як працює суддівська картка" text block above the footer (SEO text + internal links) |
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

`b12x3_lang` was removed in October 2026 – the language comes from the URL. Do not reintroduce a saved language.

---

## File Structure

```
boxing12x3.com/   (GitHub: AndriiRozanov/boxing12x3)
├── index.html                 <- main tool, Ukrainian, served at /
├── about.html  contact.html  privacy.html  widget.html  height-compare.html
│                              <- single pages with a UA/EN toggle (about supports ?lang=en)
├── favicon.ico  favicon.svg  apple-touch-icon.png   <- real icon files (linked only from the two homepages)
├── og-default.png  og-default-en.png
├── sitemap.xml                <- every URL has lastmod = date of the last substantive change
├── robots.txt  vercel.json (cleanUrls)  middleware.js (/?lang=en -> /en, /height-compare?lang=en -> /en/height-compare)
├── CONTEXT.md  README.md
├── ua/
│   ├── guide.html  fights.html  boxers.html  boxing-history.html      <- hubs
│   ├── boxing-scoring | boxing-scorecards | boxing-organizations | boxing-knockouts | boxing-weight-classes .html
│   │                          <- 5 evergreen guides
│   ├── boxers/acelino-freitas.html          <- boxer profiles (catalog: boxers.html)
│   ├── boxing-history/september.html  october.html   <- "This day in boxing" months
│   └── {fight-id}.html        <- one page per fight (e.g. tsiupka-beyda, whittaker-wallace, iglesias-zaren, dubois-wardley-2)
├── en/                        <- mirrors ua/ and adds index.html (English homepage, GENERATED) and height-compare.html
└── images/history/            <- photos and comparison images for the history pages
```

---

## Monthly Workflow

### Before a fight (new fight page)
1. Add the fight to `FIGHTS` in `index.html` (fields above), then rebuild `en/index.html`.
2. Create `/ua/{id}.html` and `/en/{id}.html` from the latest fight page (see "Fight Page Template").
3. Add the fight to the current month block of `ARCHIVE` in `ua/fights.html` and `en/fights.html` (only fights with a page).
4. Add two `<url>` blocks (ua and en, mutual hreflang) to `sitemap.xml` with `lastmod` = today.
5. If it is the next fight, move `featured: true` to it.
6. Request indexing in Search Console as soon as the page is live: search demand peaks in the ~24 hours around the event.

### After a fight
1. Append the result sections to both pages (see template). Set `completed: true` and move `featured` to the next fight.
2. Update the pages' `lastmod` in `sitemap.xml` and request re-indexing.
3. Big English-language fights: publish the result the same night; smaller fights: next day.

### Month change
Nothing to remove from `FIGHTS` (`monthIdx` hides completed fights). Add the new month block at the TOP of `ARCHIVE`, and the new "This day in boxing" page plus its `HISTORY_MONTHS` entry when ready.

### When adding a guide article
1. Add an entry to `GUIDE_ARTICLES` in `index.html`.
2. Create `/ua/{id}.html` and `/en/{id}.html` (visible "Оновлено/Updated" date in the `.meta` line, author box under the article, Article JSON-LD with the Person author and `datePublished`/`dateModified`).
3. Add to `ua/guide.html` and `en/guide.html` hub pages.
4. Add cross-links between related articles ("Читай також" block).
5. Update `sitemap.xml`.

### lastmod rule
`lastmod` is the date of the last SUBSTANTIVE change (new content, result added). Cosmetic edits (a byline, a label) do not change it. It can be read from git: `github.com/AndriiRozanov/boxing12x3/commits/main/<path>.atom`.

---

## Fight Page Template (settled, October 2026)

Order of blocks on a pre-fight page:
1. Breadcrumb `Головна / Архів боїв / X vs Y` (links to `/ua/fights`; never to the guide), H1 `X vs Y` (rematches add " 2"), meta line (date · city · rounds · division).
2. Divider "До бою" / "Before the fight" – directly under the meta line, ABOVE the fighter card (all pre-fight data sits under it).
3. Fighter card (record, stoppages, rounds, height, reach with advantage arrows; a row is dropped when neither side has data; equal values show "порівну"/"even") and the stats card (stoppage % bars, rounds bars, last-5 form squares with tooltips `FORMAT ROUND · Opponent`, newest fight first; a missing fight is a grey square with a cross).
4. Belts card: H2 "Що на кону: X – Y" / "What's on the Line: X vs Y", dark `#111` badge(s), then `division · limit kg · lbs`. UA badge text is descriptive ("Чемпіон WBO"), EN uses the abbreviation. Never write "захищає X"/"defended by X". Rematch: extra "Реванш"/"Rematch" badge plus a "Перший бій" strip. No title on the line: omit the belts card.
5. Venue map card (arena, city, capacity).
6. Broadcast card: H2 "Де дивитись X – Y в Україні?" / "How to watch X vs Y?". One row per start (event start, main card) with the platform name and a muted label. UA shows Kyiv time (`17 жовтня · 21:00 за Києвом`); EN shows `Oct 17 · 2:00 PM ET / 11:00 AM PT / 7:00 PM BST`. No prices, no affiliate links.
7. Picks card: H2 with both names ("Прогноз на X – Y: хто переможе?" / "X vs Y Prediction: Who Wins?"). Results stay hidden until the visitor has voted.
8. Visible FAQ: collapsed `<details>` block built from the SAME questions and answers as the FAQPage JSON-LD (they must match).
9. After the fight: divider "Результат", result block (winner, method, "Рекорд після бою" with +1 logic), scorecards with judge names when supplied, CTA to the scorecard (EN link `/en?fight=ID`, because the middleware drops the query on the `/?lang=en` redirect). Insert these BEFORE the FAQ block; the FAQ questions become result-oriented. Title becomes `X – Y: результат, UD 10 і суддівські записки`; SportsEvent `eventStatus` becomes `EventCompleted`.
10. "Читай також" and the footer.

Rules: names transliterated in the UA version (judges best-effort, flagged to the owner); results W/L/D/NC identical in both languages; one language per page, only the result letters are shared; `eventStatus`/`startDate`/`endDate` in SportsEvent; language buttons and the logo link point to the page's own slug and to `/en` (not `/?lang=en`); em-dash is forbidden (use en-dash).

Time zones: calculate through UTC and confirm every conversion with the owner BEFORE building the page. Kyiv (EEST, UTC+3) until the last Sunday of October, UK (BST, UTC+1) until the last Sunday of October, US (EDT/PDT) until the first Sunday of November. A card can fall on a different date in Kyiv than at the venue.

## Building en/index.html

`en/index.html` is derived from `index.html`: patch title, meta, OG/Twitter and JSON-LD strings, set `let lang = 'en'` and the `on` class on the toggle, then make every STATIC label English so the HTML equals what the scripts render (no flash of Ukrainian, English text for crawlers): ids `lbl-*`, `footer-*`, `how-*`, `hint-*`, `wonLbl`, `statBannerText`, `analyticsMore` (href `/en/fights`), `guideMore` (href `/en/guide`), and hide `#uaLinks` statically. Any new UI string needs BOTH dictionaries in `I18N` (64 keys each at the time of writing) plus a static default. Checks: static text equals rendered text; no Cyrillic in visible text except `#uaLinks`; one H1.

## SEO Structure (current)

**Homepage:** the small subtitle is the only H1 ("Боксерська суддівська картка" / "Boxing scorecard"); the logo is a plain div. WebApplication JSON-LD; hreflang uk (`/`), en (`/en`), x-default (`/`); text block "Як працює суддівська картка Boxing 12×3" above the footer; real icon files.

**Fight pages:** SportsEvent (with `endDate`) and FAQPage JSON-LD; the FAQ is also visible. hreflang uk/en/x-default with self-reference. x-default is inconsistent across page types (guides -> EN, fights and homepage -> UA); new pages should use EN.

**Evergreen guides:** Article JSON-LD with a Person author (Андрій Розанов / Andrii Rozanov, `url` = `/about`, `sameAs` = his Tribuna blog), `datePublished`, `dateModified`; BreadcrumbList; visible "Оновлено/Updated" date in the meta line; author box under the text (label "Автор"/"Author", name linked to `/about` or `/about?lang=en`, role line). "Читай також" cross-links; sources at the bottom.

**Sitemap:** 75 URLs with mutual hreflang and `lastmod`; `changefreq`/`priority` are ignored by Google. **Search Console:** property verified via DNS (Cloudflare); sitemap `https://boxing12x3.com/sitemap.xml`. Both hosts used to appear in reports; after Oct 5 2026 the apex is primary and the mix should resolve over a few weeks.

Note on external audits: a browser-based audit cannot see `<head>` or `<script>` content, so it reports missing schema, hreflang and analytics that are in fact present. Verify claims against the repo.

---

## Infrastructure

**Email:** contact@boxing12x3.com → Cloudflare Email Routing → rozanovandriy88@gmail.com

**DNS:** Cloudflare (proxied). MX records: route1/2/3.mx.cloudflare.net
SPF: `v=spf1 include:_spf.mx.cloudflare.net ~all`

**www redirect:** configured in Vercel (Settings -> Domains): `www.boxing12x3.com` redirects to `boxing12x3.com` (308). An older note mentioned a Cloudflare Page Rule; if redirect loops ever appear, check Cloudflare first.

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

Adding `?widget=1` hides: the brand, `#uaLinks`, `#analyticsBlock`, `#guideBlock`, `#sectionsWrap`, `#howBlock`, `.hint-toggle`. The language buttons do not rewrite the URL in widget mode.
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
- **Saved language overriding the URL (fixed Oct 2026)** – `/en` rendered Ukrainian for anyone who had used the Ukrainian version; incognito hid it. Test homepage changes with a pre-set opposite language in localStorage
- **Footer labels** – set in `renderAll()` (load AND toggle); "Вбудувати картку" used to stay Ukrainian after the toggle
- **Language buttons copied from a template** – once pointed to another fight's slug; every page must link to its own
- **EN scorecard CTA** – must be `/en?fight=ID`; `/?fight=ID&lang=en` loses the fight in the `/?lang=en` redirect
- **Root assets keep their file names** – icons were once uploaded as `1-favicon.ico`; strip any numbering from delivered files and verify the live repo afterwards
- **Byte-based shell tools on Cyrillic** – `cut -c` and similar corrupt UTF-8 output; use Python

---

## Working Conventions

1. **Discuss before coding** — always agree on the plan before writing a line
2. **Surgical changes** — `str_replace` on specific lines, not full file rewrites
3. **Validate JS** — always run `node -e "new Function(s)"` before presenting files
4. **Upload files, not copy-paste** — for GitHub; Cyrillic encoding breaks on copy-paste
5. **Em-dash check** — run `python3 -c "c=open('f.html').read(); print(c.count('\u2014'))"` before delivering files
6. **Result CSS check** — `grep -c "\.result{" filename.html` before adding result block
7. **Karpathy principles** — Think Before Coding, Simplicity First, Surgical Changes, Goal-Driven
8. **Code only on an explicit "кодимо"** – questions get answers and proposals first
9. **Confirm time-zone conversions with the owner before building a fight page**
10. **Verify every delivery in the live repo** (`raw.githubusercontent.com/AndriiRozanov/boxing12x3/main/<path>?n=<random>`): file names, content markers, 404s
11. **Fight pages already published stay as they are** unless he asks; new pages follow the current template
12. **Validation before delivery:** em-dash count 0, `<div>` balance, JSON-LD parses, render test in jsdom (both languages), `I18N` key parity, `/en` static text equals rendered text

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

**Evergreen articles (done):** how boxing is judged (`boxing-scoring`), how to read scorecards (`boxing-scorecards`), WBC/WBA/IBF/WBO (`boxing-organizations`), knockout and knockdown (`boxing-knockouts`), weight classes (`boxing-weight-classes`).

**Also live:** boxer profiles (`/ua/boxers`, first profile Acelino Freitas; BOXER_PROFILES sync rule above), "This day in boxing" months (September, October), legendary fights archive, height comparison.

**Fight pages workflow:**
- Texts and results come from the owner (UA first, then EN translation)
- AI prepares the page from the latest template with stats, the owner confirms data (and any time conversions) before coding
- Results are sent after the fight; big English-language fights the same night

---

## Sources for Evergreen Content

- ABC Unified Rules: `abcboxing.com/unified-rules-boxing/`
- BBBofC Rules 2025: `bbbofc.com`
- WBO 10-point system: `wboboxing.com`
- WBC Championship Rules: `wbcboxing.com`
- WBA Rules: `wbaboxing.com`
