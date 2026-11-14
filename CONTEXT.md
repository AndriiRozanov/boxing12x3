# CONTEXT.md – boxing12x3.com

Shared domain language and project decisions for AI agents working on this codebase.
Read this file before making any changes to the project.
Last updated: October 8 2026 (rewritten after the September–October rebuild; boxer profile rules added after the 70 legends were finished)

---

## What This Project Is

**boxing12x3.com** – interactive boxing scorecard tool with bilingual SEO pages.
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
| Icons = real files on every page (`/favicon.ico` 16/32/48, `/favicon-32.png`, `/icon-192.png`, `/apple-touch-icon.png`), the same four `<link>` tags everywhere; logo = the simplified 12x3 brand mark used across Telegram/blog. Small sizes use a 75% centre crop for legibility | One brand mark everywhere; real files (not data-URI) so Google can read them; since 30 Oct 2026 |
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

**BOXER_PROFILES** – shared list of boxers who have a profile page. It is copied into FOUR files (`height-compare.html`, `en/height-compare.html`, `ua/boxers.html`, `en/boxers.html`); update all four when a profile ships (full checklist in "Boxer Profile Cards"). Use the profile `slug`, not the short `id`, in URLs.

### CSS Classes

| Class | What it is |
|---|---|
| `.rrow` | Round row container (grid: 1fr 40px 1fr) |
| `.rside` | Clickable half of a round row (left = red, right = blue) |
| `.rside-fill` | Animated fill div inside rside – DO NOT set background on .rside directly |
| `.rpts` | Score number inside rside (Oswald display, z-index:1 above fill) |
| `.rn` | Round number center column (also triggers 10:10 on click) |
| `.won-strip` | "Виграних раундів" counter above scorecard rows |
| `.analytics-block` | Fight stats links block below scorecard |
| `.hint-toggle` | "Як судити?" collapsible button – in-context help for taps; ends with a link to the 10-point guide |
| `.how-block` | "Як працює суддівська картка" text block above the footer (SEO text + internal links) |
| `.main-btn` | Share/CTA button – red when active, gray when disabled |

### JS Functions

| Function | What it does |
|---|---|
| `tapSide(i, 'red'/'blue')` | Handles round scoring tap + closes hint on first use |
| `tapCenter(i)` | Sets/resets 10:10 draw round |
| `renderRound(i)` | Renders a single round – updates fill-div and score colors |
| `getIntensity(diff)` | Returns opacity 0.12–0.80 based on score difference |
| `buildAnalyticsBlock()` | Builds fight links block + guide block, language-aware |
| `updateUI()` | Updates totals, won-strip, leader bar, share button state |
| `buildRounds()` | Generates all round rows – called on fight change |
| `renderAll()` | Full re-render: labels, fights, rounds – called on language change |
| `getDefaultFight()` | Returns nearest upcoming fight (sorted by date) |
| `loadState()` | Loads saved state from localStorage – only restores scores if saved fight still exists in FIGHTS |

### Pour Animation (color fill on scoring)

Each `.rside` contains a `.rside-fill` div (position: absolute, z-index: 0).
When a round is scored, JS sets `background` on the fill div and triggers
`pourFromLeft` or `pourFromRight` CSS animation via clip-path.
**Never set `style.background` directly on `.rside`** – it overrides the fill div.

### localStorage Keys

| Key | What it stores |
|---|---|
| `b12x3_fight` | Last selected fight id |
| `b12x3_scores` | Scored rounds array |
| `b12x3_stop` | Stoppage data |
| `b12x3_hint_seen` | Whether user has seen the hint (closes it after first tap) |

`b12x3_lang` was removed in October 2026 – the language comes from the URL. Do not reintroduce a saved language.

---

**Static catalog links (crawlers without JavaScript):** `/ua/boxers` and `/en/boxers` build the catalog in JS from `BOXER_PROFILES`, but the same markup is also baked into the raw HTML between `<!--bake:start-->` and `<!--bake:end-->` inside `<div id="catalog">`. After every change to `BOXER_PROFILES` (each new boxer batch) run `python3 scripts/bake_catalog.py` from the repo root (needs Playwright) and commit both pages. `build()` clears the container first, so users always see the live render.

**Static fights lists:** `/ua/fights` and `/en/fights` are baked the same way (`#archive` and `#legendary`, data arrays `ARCHIVE` / `LEGENDARY`). After adding a fight to those arrays, run `python3 scripts/bake_catalog.py` and commit `ua/fights.html` and `en/fights.html`. `build()` and `buildLegendary()` clear their container first.

**Static month grid:** `/ua/boxing-history` and `/en/boxing-history` bake `#monthGrid` (the `MONTHS` array) the same way. Run `python3 scripts/bake_catalog.py` whenever a month is activated or the current month changes, and commit both pages.

**Related boxers block:** every boxer card ends with a static "Other boxers in the division" card (6 links) between `<!--related:start-->` and `<!--related:end-->`. Generated by `python3 scripts/related_boxers.py` from `BOXER_PROFILES`: the card's division is the one with the most belt rows (tie: first in `DIV_ORDER`); links are the next 6 boxers of that division by slug, cyclic. Re-run after every new boxer batch and commit all changed cards.


## File Structure

```
boxing12x3.com/   (GitHub: AndriiRozanov/boxing12x3)
├── index.html                 <- main tool, Ukrainian, served at /
├── about.html  contact.html  privacy.html  widget.html  height-compare.html
│                              <- single pages with a UA/EN toggle (about supports ?lang=en)
├── favicon.ico  favicon-32.png  icon-192.png  apple-touch-icon.png   <- real icon files (linked from every page)
├── og-default.png  og-default-en.png
├── sitemap.xml                <- every URL has lastmod = date of the last substantive change
├── robots.txt  vercel.json (cleanUrls)  middleware.js (/?lang=en -> /en, /height-compare?lang=en -> /en/height-compare)
├── votes-close.json           <- fight id -> UTC close time of voting (read by the Worker)
├── scripts/                   <- bake_catalog.py, check_votes_close.py, ...
├── CONTEXT.md  README.md
├── ua/
│   ├── guide.html  fights.html  boxers.html  boxing-history.html      <- hubs
│   ├── boxing-scoring | boxing-scorecards | boxing-organizations | boxing-knockouts | boxing-weight-classes .html
│   │                          <- 5 evergreen guides
│   ├── boxers/{slug}.html                   <- 70 boxer profiles (catalog: boxers.html)
│   ├── boxing-history/september.html  october.html   <- "This day in boxing" months
│   ├── cards.html  cards/{slug}.html       <- tournament (event) hub: list page + one page per event
│   └── {fight-id}.html        <- one page per fight (e.g. tsiupka-beyda, whittaker-wallace, iglesias-zaren, dubois-wardley-2)
├── en/                        <- mirrors ua/ and adds index.html (English homepage, GENERATED) and height-compare.html
├── images/cards/              <- tournament banners and organizer logos
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
6. Add the fight to `votes-close.json` (UTC start of the broadcast evening) as soon as the start time is known.
7. If the fight belongs to a tournament: `tournament:'<slug>'` in `FIGHTS`, the tournament in `TOURNAMENTS`, the tournament strip on the fight page and a row on the card page (see "Tournament cards").
8. Run `python3 scripts/bake_catalog.py` after changes to `ARCHIVE`/`BOXER_PROFILES`, then `git checkout ua/boxing-history.html en/boxing-history.html`.
9. Run `python3 scripts/check_votes_close.py` before every merge: it fails if a fight with a past date has no entry in `votes-close.json`.
10. Run `python3 scripts/gen_index.py` to add/refresh the "12×3 Index" block (ring + 5 rows, after the Stats block) on every upcoming fight page (UA+EN). Data comes from the page itself plus `data/rankings.xlsx`; re-run after every monthly rankings update. Weights (form 30, ranking position 25, knockouts 15, wins 15, experience 15) are not shown to users. Crossover fights go into `EXCLUDE` in the script (no index). Under 15 fights or 50 pro rounds: shrink to average and the label "Not enough data". Completed fights keep their pre-fight index (the script only touches `completed:false`). Names that differ from rankings.xlsx go into `ALIAS`.
11. Request indexing in Search Console as soon as the page is live: search demand peaks in the ~24 hours around the event.

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

From design skill audit – mandatory:

- **Em-dash ban** – never use `–` (U+2014). Use en-dash `–` (U+2013) everywhere
- **Blockquote** – gray background `#f0ede8`, border-radius: 6px. NO `border-left` colored accent
- **Hover** – always inside `@media (hover: hover) and (pointer: fine)`
- **prefers-reduced-motion** – all pages must include:
  ```css
  @media (prefers-reduced-motion: reduce) {
    *, *::before, *::after { animation-duration: .01ms !important; transition-duration: .01ms !important; }
  }
  ```
- **Article line width** – `article p { max-width: 65ch; }`
- **Focus rings** – `button:focus-visible, a:focus-visible { outline: 2px solid var(--red); outline-offset: 2px; }`
- **Fonts (changed 30 Oct 2026)** – Manrope (variable, body) + Oswald 600 (display, always uppercase), both self-hosted in `/fonts/` with `fonts/fonts.css`; same fonts in UA and EN. Replaced DM Sans and Bebas Neue because neither has Cyrillic (UA text fell back to the device system font). Never reintroduce Google Fonts links. Oswald is declared for weights 100-900 so every weight maps to the 600 file
- **Background #f7f6f3** – keep (identity preservation)

---

## Widget Mode

Adding `?widget=1` hides: the brand, `#uaLinks`, `#analyticsBlock`, `#guideBlock`, `#sectionsWrap`, `#howBlock`, `.hint-toggle`. The language buttons do not rewrite the URL in widget mode.
Shows: `#poweredBy` ("Powered by Boxing 12×3 →")

---

## Known Bugs Fixed (do not reintroduce)

- **Favicon** – href must use `%3C` and `%3E` for `<` and `>` inside SVG data URI
- **Template literals** – no backtick strings in JS; use string concatenation
- **Fill div** – pour animation uses `.rside-fill` child div; never set `style.background` on `.rside` parent
- **GUIDE_ARTICLES** – must be declared before any function that references it
- **loadState** – scores only restored if saved fight id still exists in FIGHTS array; otherwise fresh state. Prevents old month's scores appearing on new month's fights
- **Dropdown placeholder** – `ph.disabled = true; ph.hidden = true;` – cannot be selected
- **Default fight** – `getDefaultFight()` returns nearest upcoming by date, not FIGHTS[0]
- **Date sorting** – uses `new Date(f.date + ', 2026')` – works for "Aug 22" format
- **Saved language overriding the URL (fixed Oct 2026)** – `/en` rendered Ukrainian for anyone who had used the Ukrainian version; incognito hid it. Test homepage changes with a pre-set opposite language in localStorage
- **Footer labels** – set in `renderAll()` (load AND toggle); "Вбудувати картку" used to stay Ukrainian after the toggle
- **Language buttons copied from a template** – once pointed to another fight's slug; every page must link to its own
- **EN scorecard CTA** – must be `/en?fight=ID`; `/?fight=ID&lang=en` loses the fight in the `/?lang=en` redirect
- **Internal links never use `?lang=`:** UA = `/`, `/height-compare?a=X&b=Y`, `/?fight=ID`; EN = `/en`, `/en/height-compare?a=X&b=Y`, `/en?fight=ID`. The middleware redirects stay only for old external links. Exceptions: `/about?lang=en` (no `/en/about` yet) and the widget generator URLs (`?widget=1&lang=`).
- **Root assets keep their file names** – icons were once uploaded as `1-favicon.ico`; strip any numbering from delivered files and verify the live repo afterwards
- **Byte-based shell tools on Cyrillic** – `cut -c` and similar corrupt UTF-8 output; use Python

---

## Working Conventions

1. **Discuss before coding** – always agree on the plan before writing a line
2. **Surgical changes** – `str_replace` on specific lines, not full file rewrites
3. **Validate JS** – always run `node -e "new Function(s)"` before presenting files
4. **Upload files, not copy-paste** – for GitHub; Cyrillic encoding breaks on copy-paste
5. **Em-dash check** – run `python3 -c "c=open('f.html').read(); print(c.count('\u2014'))"` before delivering files
6. **Result CSS check** – `grep -c "\.result{" filename.html` before adding result block
7. **Karpathy principles** – Think Before Coding, Simplicity First, Surgical Changes, Goal-Driven
8. **Code only on an explicit "кодимо"** – questions get answers and proposals first
9. **Confirm time-zone conversions with the owner before building a fight page**
10. **Verify every delivery in the live repo** (`raw.githubusercontent.com/AndriiRozanov/boxing12x3/main/<path>?n=<random>`): file names, content markers, 404s
11. **Fight pages already published stay as they are** unless he asks; new pages follow the current template
12. **Validation before delivery:** em-dash count 0, `<div>` balance, JSON-LD parses, render test in jsdom (both languages), `I18N` key parity, `/en` static text equals rendered text

---

## Boxer Profile Cards

70 legend profiles are live (UA + EN, `ua/boxers/{slug}.html` and `en/boxers/{slug}.html`), catalogue at `/ua/boxers` and `/en/boxers`. Data source was the owner's table `rtfight_legends.numbers` (open the .numbers file, not the .xlsx: titles and nicknames live only there). 55 more legends ("Not on RTFight" sheet) are not done and need a separate list of height and reach.

### Every new boxer touches
1. Both HTML cards (copy the latest card, change data only; never write a card from scratch).
2. `BOXER_PROFILES` in all four files (`height-compare.html`, `en/height-compare.html`, `ua/boxers.html`, `en/boxers.html`): one row per title division `{id, slug, nameUk/name, div, org, orgColor}` (height-compare files carry both `name` and `nameUk`; `ua/boxers.html` only `nameUk`; `en/boxers.html` only `name`).
3. The `ItemList` JSON-LD at the top of `ua/boxers.html` and `en/boxers.html` (`numberOfItems` and positions, alphabetical by slug).
4. `sitemap.xml`: two URLs per boxer (UA with hreflang pair), priority 0.6, monthly.
5. Height and reach in the `height-compare` database must match the card; the id (`hc`) there is the link key, the `slug` is used in URLs.

### Working loop (batches of five, table order)
The owner sends each boxer's last fight (method, rounds, date, opponent); Claude reads the table row, lists discrepancies and questions, the owner answers, Claude builds on a branch `boxers-batchN`, shows UA and EN screenshots at 480 px, and merges fast-forward into `main` only after "Затверджую". Verify the live commit via `raw.githubusercontent.com/.../<commit>/...`. Never code before the owner confirms.

### Card content rules
- Blocks: header with the brand logo and caption, breadcrumb "Головна / Боксери / Ім'я", name and status line, Wins / Losses / KOs cells, record bar, fact grid, "Порівняти зріст" row (3 peers), last fight, titles, optional achievements, footer.
- KO cell: "N% перемог нокаутом" / "N% of wins by KO" (share of wins by KO). The "з них N нокаутом" line under Losses shows only when it is above 0.
- Draws are never shown as 0: only when above 0 a legend under the record bar ("Нічиї · N" / "Draws · N", colour #5c6bc0). No contests: grey legend "Без результату · N" / "No contests · N", only when above 0.
- "Дивізіони" / "Divisions" cell lists every division where the boxer held a title; with 3 or more divisions it is full-width and the debut sits beside the birthplace. No nickname means no nickname cell (birthplace/division cell becomes full-width). Southpaw: "Шульга" / "Southpaw".
- Titles: one line per title division in chronological order; pills coloured by organisation (WBO #111, WBA #1a5276, WBC #2e7d32, IBF #7d2942, The Ring gold, IBO purple); open-ended period written "з РРРР". Interim belts and Inter-Continental belts are NOT counted; WBU/WBF are not written. Regular WBA is "WBA (регулярний)" / "WBA (Regular)", super is "WBA (Super)". A promotion to Super is not a separate line, it is written as "2010–2016 (Super з 2015)". The cruiserweight is called "Важка" on the site (the table says "Перша важка").
- Undisputed ("Абсолютний чемпіон", boxed tag above the belts plus status "Абсолютний чемпіон світу в ...") is the OWNER's call, not a formula: three main belts overlapping is not enough (Darchinyan and Wladimir Klitschko were deliberately left without it). Ask when in doubt.
- "Досягнення" card: Olympic medals (gold default dot, silver #9aa0a6), Ring Fighter of the Year, European (EBU) titles, big tournaments. A boxer with no pro titles gets only this card (Tua).
- Last fight: result in colour (win green, loss red, draw #5c6bc0). The owner's notation "9/12" means ended in round 9 of 12 scheduled; for a fight that did not go the distance the card says "Бій на N раундів" / "Scheduled for N rounds", for a full distance "N раундів" / "N rounds".
- A deceased boxer's status line ends "помер у ГГГГ році" only if the owner stated it.
- Nicknames stay in English in both languages; a boxer with two nicknames keeps both as written in the table.
- Peers for "Порівняти зріст" are chosen by Claude from the same division; the owner checks them.

### SEO rules for cards
Title up to 60 characters ("Ім'я: рекорд, титули, останній бій | Boxing 12×3"), description up to 160, og:image `og-default.png` (UA) / `og-default-en.png` (EN), JSON-LD `Person` (alternateName = nicknames plus the name in the other language, birthPlace, nationality, url) and `BreadcrumbList`. The English transliteration of a UA name appears only in markup, never in visible text. No em-dashes anywhere (check `\u2014` count is 0 before delivery).

### Spelling decisions (UA names, keep consistent across cards and peer links)
Кальзаге, Мастернак, Хопкінс, Фроч, Мікель Кесслер, Ноніто Донейр, Пак'яо, Ріккі Хаттон, Ріддік Боу, Шейн Мозлі, Свен Оттке, Тоні Белью, Аарон Прайор, Томас Хернс, Террі Норріс, Володимир і Віталій Кличко, Вік Дарчинян.

### Planned next for profiles
Personal OG images per boxer; "Важливі бої" block (clickable fight card to a historical fight page with an already-published YouTube video and a short "when, for what, where" text); the 55 legends not on RTFight; submit the new URLs in Search Console.

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

**Also live:** 70 boxer profiles (`/ua/boxers`; rules in "Boxer Profile Cards"), "This day in boxing" months (September, October), legendary fights archive, height comparison.

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

## Brand mark (30 Oct 2026)
- The simplified 12x3 logo (same as Telegram/blog) is used in: favicon/apple-touch-icon (`/icon-192.png`, `/apple-touch-icon.png`, `/favicon-32.png`, `/favicon.ico`), og-default images (dark, logo centred), the share-card header (canvas + preview, replaces the text 12×3/SCORE), a small mark above the footer on every page, and the 72px mark in the About page. The site header stays text-only (Oswald wordmark) by decision.

## OG image cache busting (1 Nov 2026)
- Telegram, Facebook and Threads cache link-preview images by URL, so a changed `og-default.png` / `og-default-en.png` kept showing the old picture. All `og:image`, `twitter:image` and JSON-LD `image` references now use `https://boxing12x3.com/og-default.png?v=2` and `og-default-en.png?v=2` (102 pages, UA and EN).
- Rule: new pages must use the `?v=2` URLs. If the images are changed again, bump the number (`?v=3`) on all pages, then refresh previews via @WebpageBot (Telegram) and the Facebook Sharing Debugger.

## Voting close (5 Nov 2026)
- Voting (Cloudflare Worker, KV `PICKS`) closes per fight. `votes-close.json` at the site root maps a fight id to a UTC ISO time; the Worker's `isClosed(fightId)` fetches it (`CLOSE_URL`, cache 300 s). When closed, `POST /vote` returns `{ok:false, closed:true, data}` and `GET /picks` returns `closed:true`. The Worker fails OPEN: no entry (or unreachable file) means voting stays open. The Worker source is not in the repo (pasted into Cloudflare by the owner).
- Close time = start of the broadcast evening in UTC. Finished fights without an entry stay votable forever, so every fight needs an entry; `scripts/check_votes_close.py` enforces it for past dates. 14 fights from Sep 19 to Oct 24 were added on 5 Nov 2026 (close time = the event date at 00:00Z).
- Front end: fight pages use `closeVoting()` + `loadResults()` ("Голосування закрито" / "Voting is closed", results visible). Tournament card pages use `closeRow()` in `loadRow()`/`vote()`; the cookie `pick_v2_<id>` is NOT set when the Worker answers `closed`. Any new voting UI must react to `closed`, not only the Worker.
- Bug found 5 Nov: card pages had their own vote script that ignored `closed`, so finished fights stayed votable from the card even with a `votes-close.json` entry.

## Tournament cards (Oct-Nov 2026)
- A tournament (event) has a page `ua|en/cards/<slug>.html`, an entry in `TOURNAMENTS` in `index.html`/`en/index.html`, a banner in `images/cards/` and optionally an organizer logo. Generated pages: do not edit by hand in bulk; the generator lives outside the repo, so patch all 8+ files with a script and check each.
- List page `ua|en/cards.html`: nearest event as a large banner, the rest as compact rows grouped by month, `ItemList` JSON-LD. Add every new card to it and to `sitemap.xml` (priority 0.9, weekly).
- Card page: main event is the first, highlighted row of the programme; fights WITHOUT their own page are plain rows (no link, no vote); fights with a page have the full row with Judge/Page buttons and a vote under the pair. Optional blocks only when data exists. Voting in the row also counts on the fight page.
- Every fight page of a card carries the tournament strip (`.tstrip`: previous/next fight of the card, link to the card page, breadcrumb to the card). Card page and fight pages are always cross-linked.
- Build a card page as soon as the main event is announced and add fights as rows when announced (first used for Fury vs Joshua, Dec 11, Cardiff; Opetaia–Wilder is the first announced fight).
- Planned: "Після бою" block on card pages (results + pre-fight vote vs outcome), starting with Zuffa Boxing 12 (Nov 7).

## CSS fixes of Nov 2026 (apply to every new page)
- Footer: `.site-footer{display:flex;flex-wrap:wrap;justify-content:center;gap:8px 20px}`.
- FAQ: `.faq details[open] summary::after{content:"\2013"}` (the open-state icon was a corrupted byte sequence on 62 pages).
- Form tooltips: `.fc-tip{width:max-content;max-width:150px;white-space:normal}` with left/right alignment by cell position so they never leave the viewport (360-390 px checked); strip tooltips `.stip{width:max-content;max-width:220px;white-space:normal}`.
- Old pages with the pre-grid form: `.form-cells` grid with `.fc{width:100%;max-width:30px;aspect-ratio:1}`; the "✕" cell on Tsiupka–Beyda stays "✕", not "NC".
- Overflow check at 360/390 px was run on all 399 pages; repeat it after layout changes.

## Editorial pre-fight text (`.pretext`, Nov 2026)
- Optional block with the owner's own text, placed right after the "До бою" divider and BEFORE the venue block. Markup: `<div class="pretext"><h2>…</h2><p>…</p></div>`; CSS `.pretext{background:var(--card);border:0.5px solid var(--border);border-radius:var(--r);padding:18px 18px 6px;margin-bottom:20px}` plus h2 15px/700, p 14px/1.7 #333, links underlined with a muted line. In the generator: fight dict keys `pre_h2_uk/en`, `pre_html_uk/en`.
- The text is written by the owner (UA first, then EN); Claude only fits and links it (e.g. links to the page of a related fight). It stays after the fight next to the result. First used on Billam-Smith–Clarke.
- Card pages (`cards/<slug>`) take optional `name_uk`, organizer name/logo and a banner; blocks that have no data are not rendered.

## Promoters and past events (Nov 2026)
- Promoter hub `ua|en/promoters.html` and promoter pages `ua|en/promoters/<slug>.html` (first: `zuffa-boxing`). Homepage section "Промоутери" / "Promoters" (`#promoBlock`, between Tournaments and Fight archive): label, "All promoters" link, one-sentence description (for Google), one row per promoter (logo, name, "11 events · 88 fights"; no KO percentage). Add a row per new promoter.
- Past Zuffa events: 11 card pages `cards/zuffa-boxing-01..11` + 23 fight pages (UA+EN, copied from `fisher-protton`, data from the Zuffa PDF; user-supplied reach/rounds in `OVR`). Past-fight pages get ARCHIVE entries in `ua|en/fights.html` (then `python3 scripts/bake_catalog.py`; `git checkout ua/boxing-history.html en/boxing-history.html`) and sitemap URLs, but NOT `FIGHTS` or `votes-close.json` entries.
- Promoter page lists past events with links to the card and to every fight page that exists. Never create a page again for a fight that already has one: link to it (check sitemap/slug list and H1 before generating; checked Nov 7, no duplicates).
- Tstrip label: "Головний бій турніру" / "Співголовний бій турніру" / "Бій турніру".

## Video blocks (Nov 2026)
- 16 past-fight pages carry a YouTube block placed after the result (editorial pages: before the CTA): SEO `<h2 class="res-h2">Відео бою X – Y</h2>` (EN "X vs Y fight video"), lite embed (`.vid` with `data-id`, thumbnail button, iframe `youtube-nocookie` created on click), fallback link "Дивитись на YouTube ›", `VideoObject` JSON-LD with `uploadDate` = fight date. Names in the heading follow the page H1 order. Script: scratchpad `vid/addvid.py` (idempotent per page).
- Sandbox cannot reach YouTube: embed playback must be checked live by the owner.

## Promoter page polish and share images (Nov 7 2026)
- Share images: `og-promoter-<slug>.png` (one for UA+EN, promoter logo on a white plate between the 12×3 ropes, "BOXING 12×3" at the bottom, no promoter-name text, no figures that change) and `og-promoters.png` / `og-promoters-en.png` for the hub. Generated by `scripts/og_promoter.py` (`logo <logo.png> <out.png>` or `title "<H>" "<sub>" <out.png>`; needs `npm i @fontsource/oswald` and set `FONTDIR`). All references use `?v=1`; bump the number everywhere if an image changes, then refresh Telegram (@WebpageBot) and Facebook previews.
- Promoter page: stat tiles centered vertically (no reserved label space); tile "53% of stoppages by round 3" replaces "average stoppage round"; "countries hosting events" with a countries line under the arenas list; title fights as colored belt plates linking to fight pages (`.tf`); fastest win in a dark card with stopwatch count-up and round bar (`.fast`, respects prefers-reduced-motion); "% нокаутів на турнірах" / "Stoppage rate by event".
- Long lists: 3 latest past events + `<details class="more">` "Show N more events" (cards and result accordions), year label above the cards. All events stay in the HTML for Google.
- Scaling plan: at 15+ events (about early 2027) move the archive to per-year pages `/promoters/<slug>/<year>`, promoter page keeps ~5 latest; 100-200 event promoters get year pages with filters and fighter search; one structured data file per promoter, built by script; format fixed when the second promoter appears; hub sorted by activity, homepage shows 3-5 promoters.
- Homepage "Промоутери" row: logo on a white plate (`.promo-logo`), "11 турнірів · 88 боїв".
- Fix: "3 боїв" to "3 бої" on the Zuffa 13 row (UA plural).

## This Day in Boxing, Nov 7 (Nov 2026)
- Day 7: ГП = Gervonta Davis born (1994), СГ = Hasim Rahman born (1972); Monzon–Benvenuti (1970) and Leonard–Lalonde (1988) stay on the month page only. `HISTORY_NOV` in `index.html` and `en/index.html` holds one gp and one sg per day.

## Zuffa 12 results and tournament card UI (Nov 8)
- Zuffa 12 (Nov 7) is closed: card page in the Mexico vs World style (results in rows, `pr mut done` for bouts without a page, single button "Результат і статистика" / "Result and stats" on finished bouts, no Score/vote on finished bouts, pre-fight records in main event rows on cards 01-12). Fight pages billam-smith-clarke (Clarke TKO 7, 1:24), bentley-mosley (UD 10), parker-dzambekov (KO 4) converted to result state (result block after picks, judges, record after the fight, visible FAQ, EventCompleted); their `FIGHTS` entries are `completed:true`.
- Homepage "Архів боїв" shows 5 fights + "Показати ще N" (`.fights-more`); `/ua|en/cards` past events show 5 + "Показати ще N турнірів" (`.past-more`). Zuffa 13 is the banner of "Найближчі турніри".
- Zuffa promoter page after Zuffa 12: 12 events, 97 fights, 44 stoppages (45%), 22 of 44 by round 3 (50%), average stoppage round 4.14, UK 3 events, Copper Box 2 events / 18 fights, Las Vegas 57%. Allen-Igel counted as lightweight (Zuffa has no super lightweight; catchweight list stays 133, 150, 157 lb). Zuffa 12 weights: Kemp, Hickey, Bentley = middleweight; Roehrig, Billam-Smith = cruiserweight; Vanhouter = heavyweight; Abdulah = featherweight; Parker = light heavyweight.
- EN spellings used: Da'Mazion Vanhouter, Lucas Roehrig, Masood Abdulah (UA unchanged: Ванхаутер, Реріг, Абдула).

## Usyk 17 Promotions (Nov 14 2026)
- Promoter page `ua|en/promoters/usyk-17-promotions.html` (built like Zuffa: stat tiles, next event, past events, how fights end, fastest win, stoppage rate by event, divisions and title fights, arenas, results accordions, FAQ/CollectionPage/BreadcrumbList JSON-LD). Logo `images/cards/usyk-17-promotions.png` (transparent wordmark, about 16:9, so plate height 56px, tbanner 36px, share image `og-promoter-usyk-17-promotions.png` made with `og_promoter.py` using a 150px-high logo).
- 4 events (all past), 42 fights, data from the promoter's PDF (13.11.2026): `cards/big-boxing-night-2020`, `cards/ultimate-boxing-night`, `cards/rising-stars`, `cards/rising-stars-ii`; posters in `images/cards/<slug>.jpg`. 8 fight pages (main + co-main per event): `lapin-krapshyla`, `sirenko-krolenko`, `gadzhyiev-murashkin`, `lapin-koros`, `lapin-bulmeistars`, `khyzhnyak-baron`, `khyzhnyak-palacio`, `illiusha-jordelli`. Past fights: ARCHIVE + sitemap only, not `FIGHTS`/`votes-close.json`.
- Upcoming: Rising Stars III: Constellation, Dec 19 2026, Lviv, Khyzhnyak vs TBA. Block on the promoter page only; no card page, no arena/time/broadcast until the promoter announces them. Wording: "Деталі та кард оголосять згодом" (never "картку" for a fight programme).
- Weight classes: traditional, exactly the site's table (`boxing-weight-classes`), NOT Zuffa's 8-division scheme. Raw PDF names are normalized (Cruiser = Важка/Cruiserweight, Super middle = Друга середня/Super middleweight, Super heavyweight and Heavy = Надважка). Bakhshyieu–Fennell: MD 8 (78-74, 76-76, 79-74), scores in the PDF are listed from Fennell's side.
- Belarus flag: `images/flags/by.png` is the white-red-white (БЧБ) flag everywhere. Spellings: Кулієв, Іллюша. No word "title"/"Титул" on belt plates; "Вакантний"/"Vacant" stays.
- Capacity row (Місткість/Capacity) shown on fight and card venue blocks for these events (500, 200, 500, 2000).
- Promoters hub rule: whenever a promoter or its events change, refresh every row of `ua|en/promoters.html` (next event name/date, poster, "N upcoming events" tag); Zuffa's row now shows Zuffa Boxing 13.
- Known leftover: older EN pages (about 24) still show Cyrillic "КО"/"см" in stats; not fixed yet.

## Calendar and events data (Nov 14 2026, step 1 of the events-first redesign)
- `scripts/build_events.py` builds `data/events.json` (lean database: fights with UTC start, venue city/country/continent/timezone/coordinates, broadcasters, results; tournaments; promoters) by parsing `index.html` (FIGHTS, TOURNAMENTS), `votes-close.json` and the ua|en fight and card pages. Never edit `events.json` by hand. Start time priority: page JSON-LD datetime > `votes-close.json` with a time > date only. Broadcast-block-only times are NOT treated as a start time (fight shows "Час уточнюється" / "Time TBA").
- `scripts/bake_calendar.py` writes `ua/calendar.html` and `en/calendar.html` from that file. Upcoming fights are baked into the HTML (Google, no-JS); the page script only filters, groups by day and converts times to the reader's time zone (Intl, label "Ваш час" / "Your local time", selectable zone saved in localStorage `b12x3_cal_tz`). No-JS fallback: UA Kyiv time, EN UTC.
- After adding or changing any fight page: `python3 scripts/build_events.py && python3 scripts/bake_calendar.py`, then commit `data/events.json` and both calendar pages. A new venue needs its city in `VM`, `TZ` and `COORDS` in `build_events.py` (the script prints issues).
- Filters: search (names in both languages, tournament, city, country), date chips + range, day strip, continent and country chips (only values that exist), "Near me" (browser geolocation only after the click, default radius 500 km, up to 5000 km). Mobile: filters collapse behind a "Фільтри"/"Filters" button. The time zone select is NOT in the filters: it opens from a small "Змінити"/"Change" link next to the "Ваш час" line. GA4 event `calendar_filter`.
- Flags `images/flags/sa.png` and `ae.png` added (flag-icons, MIT). Russia is white-blue-white, Belarus white-red-white (existing files).
- Sitemap: `/ua/calendar` and `/en/calendar`, daily, 0.9. Not yet linked from the homepage (step 2).


## Home page and scorecard move (Nov 14 2026, step 2, branch home-step2)

- Home pages `/` (index.html) and `/en` (en/index.html) are now events-first and are generated, do not edit by hand: `python3 scripts/build_events.py && python3 scripts/bake_calendar.py && python3 scripts/bake_home.py`. CSS lives in `scripts/home.css`. Up to 4 event blocks are baked; the page script shows the first that has not ended, hides past rows and converts times to the reader's zone. Results block = last 4 completed fights with names and a winner. Promoter fight totals are the `PROMO_FIGHTS` dict in `bake_home.py` (taken from the promoter pages, update by hand).
- The scorecard moved to `/ua/scorecard` and `/en/scorecard` (copies of the old index files, only canonical/hreflang/og:url and the language-switch path changed). Old links keep working through `middleware.js`: `/?fight=ID`, `/en?fight=ID`, `/?widget=1&lang=..` redirect 308 to the scorecard with the query. Internal links and `widget.html` already use the new addresses.
- Calendar accepts `?c=Europe` (continent chip) and `?near=1` (starts "near me") so the home chips can deep-link.
- Not built yet: ICS feed (the banner from the mockup is left out), comparison with judges (scorecard text on the home does not promise it).

## Scorecard page layout (Nov 14 2026, step 3, branch scorecard-step3)

- `/ua/scorecard` and `/en/scorecard` keep only: the card, "How to score?", the fight archive block, the "How the card works" SEO text and the footer. The Telegram/podcast/blog block, tournaments, promoters, guide and tools sections were removed (owner decision: the author's links do not go under the scorecard; if placed at all, only as minimal buttons on the home page and on the contact page). Added: site navigation pills (same as the home page, hidden in widget mode) and an "All events and calendar" link to the home page.

## "Результат вечора" picture (Nov 14 2026, step 4, branch result-image-step4)

- A finished tournament card page gets a strip "Зберегти картинку" and a modal with three formats (post 4:5 = 2160x2700, square 1:1 = 2160x2160, story 9:16 = 1080x1920). The PNG is drawn in the browser on a canvas by `js/result-image.js`; no server. The QR code (made with segno at bake time, drawn from a matrix) opens the tournament card page with `?utm_source=result_image`. Where supported, a "Share" button uses the phone's share sheet. GA4 event `result_image` (action open/format/save/share/copy_link).
- Add or refresh it for a tournament after the fights are finished: `python3 scripts/build_events.py && python3 scripts/bake_result_image.py zuffa-boxing-13` (also bake_calendar/bake_home if needed). It refuses unless every fight of the tournament is `completed` with a winner in `data/events.json`. Needs `pip install segno`. `--out DIR` writes test copies and leaves the repo untouched. Only Zuffa Boxing 13 and later tournaments get the picture (owner decision); older cards are not touched.
- Promoter logo with a gold check circle appears on the picture only for promoters listed in `data/promoters-confirmed.json` (`{"confirmed": ["zuffa-boxing"]}`), added when a promoter really confirms. Today the list is empty, so pictures carry only our logo.

## Step 5a: "Мої картки" (Nov 2026)
- Each fight card is saved separately in localStorage key `b12x3_cards` ({fightId:{scores,stop,t}}, max 60); old single slot is migrated. Never sent anywhere.
- `#myCardsBlock` on /ua|en/scorecard lists saved cards (hidden in widget mode). Rows link to `?fight=ID`.
- Official results come from `const RESULTS` baked by `python3 scripts/bake_scorecard_data.py` (run after build_events.py). Neutral styling, no right/wrong colours.

## Nov 14 fixes (branch fixes-nov14)
- Pages: `/ua|en/results` (scripts/bake_results.py), `/ua|en/tools` (scripts/bake_tools.py); both in sitemap. Run after build_events.py with bake_calendar/bake_home.
- Mobile header variant A (brand left, language switch right) = `<style id="hdr-mobile">` in every page; generators (bake_calendar, gen_rankings) carry the same rule. New pages copied from existing ones inherit it.
- Scorecard: top nav replaced by "back to home" link; logo links to home.
- Home: chips filter "Найближчі" in place (continent / near me, 1000 km); "This day" widget after results, data in `data/history-home.js` (add a month there and to HISTORY_MONTHS); live dot pulses (respects reduced motion).
- Search normalises apostrophes.
