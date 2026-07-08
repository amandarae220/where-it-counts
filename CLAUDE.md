# Where It Counts — Project Context

## What This Is

A single-page scrolling data-journalism piece in the tradition of The Pudding and NYT Upshot. The argument: tens of millions of votes don't influence outcomes because of where they're cast, and the next redistricting cycle (2031) is a concrete personal window where that math can change.

It is not a call to pick a side. It is a case — built on public data, grounded in civics — for Americans to think differently about where they live and how much their voice actually matters.

## Author Context

Government contractor. The piece must stay non-partisan and data-forward. No sensationalism, no inflammatory framing, no "cheap grabs at attention."

## Editorial Commitments

**ROI thesis committed; essay thesis cut.** The piece runs one argument — *where you live compresses or amplifies your marginal influence; here's the math; here's where it would be different.* An earlier version ran a parallel sociological thesis (housing costs, identity flattening, cross-partisan contact). That essay content is preserved on disk in inert component files but is not shipped. See "Inert component files" below.

**Single-page architecture.** The reader gets the full arc + both interactive tools + the closer without a nav click. The former `/the-case` route was deleted when the piece collapsed to one page.

**Interactive tools deliver the payoff.** MapMoves and MoversBudget together carry the ROI thesis. Neither is a "showcase" — each answers a specific question the reader has been given.

## Tone Rules (enforced — do not drift from these)

**Words/phrases to never use:** wasted, fraud, rigged, stolen, suppressed, shut out, piled up, already decided, already set, structural problem, geographic concentration, intellectual flight, classism, brain drain, inflection point, organically (in political context), legally defensible, accountable (as policy-speak), organic undoing.

Grep before any substantive copy change. If a banned concept is genuinely load-bearing (e.g., "geographic concentration" in an academic citation) rewrite in plain language ("how Democratic voters have clustered into safe corners") rather than smuggle it in.

**Voice:** Direct. Concrete. Like explaining something real to someone smart who isn't a policy wonk. Think: the way a good teacher explains, not the way a think-tank paper is written.

**Model:** Republican direct-messaging clarity. Make people feel like they understand and relate — not like they're being lectured.

**Not:** Academic, polemic, partisan, or preachy.

**Global voice skill:** `~/.claude/skills/global/voice.md` — Amanda's tone across everything she writes. This project's voice is a strict-register instance of that broader voice.

**Global portfolio-writing skill:** `~/.claude/skills/global/portfolio-writing.md` — data-journalism portfolio structural rules (one thesis, hero-stat dominance, WCAG, sourced feasibility). Applies to this piece specifically.

## Tech Stack

- **Framework:** SvelteKit + Vite, static-adapter prerender
- **Visualization:** D3 v7 (choropleth, projections, transitions), scrollama (scroll triggering), topojson-client
- **Fonts:** Playfair Display (serif headings), Inter (sans body), JetBrains Mono (stats/data)
- **Styling:** Global tokens in `src/app.css` — no component-level token overrides
- **Deploy:** Vercel with `cleanUrls: true` and `trailingSlash: false`

## Design Tokens (`src/app.css`)

```
--color-bg:          #fafaf8
--color-bg-dark:     #111110
--color-text:        #1a1a1a
--color-text-muted:  #6b6b6b
--color-text-light:  #fafaf8
--color-dem:         #2563eb   (blue)
--color-rep:         #dc2626   (red)
--color-competitive: #d97706   (amber — the key accent)
--max-prose:         680px
--max-wide:          1100px
```

## Currently Shipped Section Structure

Single-page site. Full arc lives in `+page.svelte`.

| Order | Section | File | Description |
|---|---|---|---|
| 1 | Hero | inline in `+page.svelte` | Dark opener, 76M-votes lede, "See the data" CTA |
| 2 | Two Moves | inline in `+page.svelte` *(currently commented out)* | Politicians pick a spot / draw the lines. "What this affects" per-card footers. |
| 3 | StatBreaker | `sections/StatBreaker.svelte` | Dark module — orientation lede on "surplus votes", CA (2,552,143) vs GA margin (11,779) → 216×, 6.3M vs 43K → 146× |
| 4 | Scrollytelling map | `Scrollytelling.svelte` + `viz/SurplusMapViz.svelte` | D3 choropleth cycling through 5 modes as user scrolls |
| 5 | State Races | inline in `+page.svelte` | Dark section, 3 stat callouts (139, 280, 582 votes) + gerrymandering tail paragraph |
| 6 | MapMoves | `sections/MapMoves.svelte` | Interactive leverage ranker: 9 states ranked, per-state drill-in with mini-map + top-6 counties |
| 7 | MoversBudget | `sections/MoversBudget.svelte` | Census-anchored what-if allocator: distribute a slice of the 8M annual interstate movement, watch the AllocationMap recolor and EC recompute live |
| 8 | Closer | inline in `+page.svelte` | Dark section, 2030 Census timing + Rodden *Why Cities Lose* citation |
| 9 | Footer | inline in `+page.svelte` | Sourced data attribution |

## Interactive Tools Architecture

### MapMoves (leverage ranker)

**Answers:** *"Where does leverage exist?"*

- 9 battleground states ranked by a normalized combined score (presidential leverage + state-leg leverage), weighted by a live slider (0-100% presidential)
- Both leverage axes normalized to 0-100 against the dataset's own maximum, so the slider blends comparable scales
- `animate:flip` on the state list so rank changes animate as the reader drags the slider
- Per-state drill-in loads county data on demand from `static/data/counties-surplus.json`, filters to that state, ranks top 6 by leverage (`total_votes / (1 + |margin_pct|)`)
- Drill-in includes a `StateMiniMap` (per-state Mercator projection fit to a 320×220 viewBox) with the state's outer boundary rendered on top of its county paths
- Hovering a county card highlights that county on the mini-map via `hoveredFips` state

### MoversBudget (allocation + sensitivity)

**Answers:** *"What actually happens if you move people?"*

- Budget slider anchored to the 8M Americans who move between states each year (Census ACS 2022), expressed as a percentage 0.5-25%
- Live anchor context lines: *"N× Katrina's Houston displacement (~250K, 2005)"* and *"N× the combined 2020 margin that decided GA + AZ + WI (43K)"*
- 9 allocation cards (3×3 grid on desktop, single column mobile) — each card has an independent slider, live per-state margin recomputation, tier reclassification, and a "Flipped" indicator that lights up when a card crosses the party line
- Per-slider **flip-target tick** below each slider showing the exact allocation that would flip the state (only when the direction opposes the state's current lean AND the flip point sits within the current budget). Grey when unmet, amber when reached.
- **AllocationMap** at the top of the impact panel — national choropleth (all 50 states) that recolors on every slider drag. Swing states gradient by projected margin; flipped states get an amber outer stroke. Hover tooltip with per-state 2020 vs projected numbers.
- **Sticky mobile summary bar** — under 900px, a compact bar with live EC totals and flip count sticks to the top of the viewport as the reader scrolls through 9 allocation cards
- Impact panel: EC totals (D vs R with deltas from 303/235 baseline), state-flip chips, movers-per-EC-vote-gained efficiency

## Shared Modules

The single-source-of-truth pattern is enforced across three data/logic files that both interactive tools import from.

### `src/lib/data/swingStates.js`

- `SWING_STATES` — the 9 states with margin_votes, margin_pct, EV count, competitive-legislative-district count, total legislature seats
- `BASELINE_D_EV = 303` / `BASELINE_R_EV = 235` — 2020 result recomputed under post-2020 EV apportionment (applies from 2024)
- `SWING_STATE_FIPS` — Census FIPS codes for the 9 states; consumed by StateMiniMap and AllocationMap to join simulation results to TopoJSON state features
- `REFERENCES` — anchor object with `value`, `label`, `source` for annual interstate movement (Census ACS 2022), Katrina Houston displacement (US Census/HUD 2005), Maria Puerto Rico → Florida, net Georgia movers, and the combined 2020 swing margin

### `src/lib/data/simulation.js`

- `simulate(state, direction, movers)` — pure sim math. Preserves the state's vote-to-pct ratio from the 2020 baseline; drifts slightly at extreme shifts, acceptable at MVP scale and documented in the method note.
- `stateTier(marginPct)` — Razor thin / Competitive / Shifting classifier (1pt / 3pt thresholds)
- `countyTier(marginPct)` — same three tiers but wider thresholds (2pt / 8pt) because a 5pt county margin is still very much in play

### `src/lib/stores/direction.js`

- `direction` — Svelte `writable('D' | 'R')`. Shared across MapMoves and MoversBudget so toggling in one tool updates the other in real time. Prerender-safe.

## Scrollytelling Map — 5 Modes

Defined in `+page.svelte` as `surplusSteps[]`, rendered by `SurplusMapViz.svelte`:

1. `intro` — full choropleth, both parties
2. `surplus-blue` — highlight Dem counties only (11.8M stat)
3. `surplus-red` — highlight GOP counties only (8.6M stat)
4. `total-surplus` — full choropleth (76M stat)
5. `zoom-swing` — zooms to AZ/GA/WI with annotated margins (11,779 / 10,457 / 20,682)

Small "hover any county for details" hint sits top-right of the map, fades out on first hover.

## Data Files

| File | Source | Used For |
|---|---|---|
| `data/county_pres_2020.csv` | MIT Election Lab | Raw county-level 2020 presidential results |
| `data/surplus_2020.json` | Computed via `surplus_calc.py` | Surplus votes by county |
| `data/state_leg_and_wfh.json` | OpenElections + BLS ATUS 2023 | State-leg margins + WFH eligibility rates *(currently unused — Calculator disabled)* |
| `data/zhvi_metro.csv` | Zillow ZHVI 2024–25 | Median home values by metro *(Calculator only)* |
| `data/zori_metro.csv` | Zillow ZORI 2024–25 | Median rent by metro *(Calculator only)* |
| `data/bea_rpp_raw.json` | Bureau of Economic Analysis | Regional price parities *(Calculator only)* |
| `data/census_wfh_raw.json` | U.S. Census ACS | WFH eligibility by occupation *(Calculator only)* |

**Static assets the map viz components expect at runtime:**

- `static/data/counties-10m.json` — US TopoJSON (counties + states + nation layers, 10m resolution). Shared by `SurplusMapViz`, `StateMiniMap`, and `AllocationMap` via a module-level fetch cache in each — the ~10MB file is downloaded once per page load and reused across every viz component that needs it.
- `static/data/counties-surplus.json` — per-county surplus lookup keyed by 5-digit FIPS. Loaded lazily by MapMoves' drill-in when the reader expands a state.

## Calculator (currently disabled)

`sections/Calculator.svelte` still exists on disk. Its import is commented out in `+page.svelte:6`. The file is preserved in case it returns in a future iteration.

If re-enabled: 9 metros hardcoded (Atlanta suburbs, Phoenix suburbs, Milwaukee metro, Raleigh–Durham, Charlotte metro, Columbus metro, Pittsburgh metro, Las Vegas metro, Richmond metro). Scoring: `impactScore = legScore × 0.7 + presScore × 0.3`. Sort options: savings / civic impact / balanced.

## Inert Component Files

These files still live on disk but are no longer imported anywhere. Preserved for future prose salvage; delete when convenient.

- `sections/Hero.svelte` — the pre-inline hero component (was already unused before the ROI cut)
- `sections/HowLinesDrawn.svelte` — "My vote doesn't matter" hook
- `sections/DistrictShopping.svelte` — the "Two Moves" alternate version
- `sections/Nobody.svelte` — the essay content (housing, identity, condescension arc). Contains banned vocabulary in comments; do not import.
- `sections/LongGame.svelte` — 2030 Census + "know your neighbors" beat. The timing math was rewritten into the current inline closer.

## Key Numbers (verify before changing)

**Presidential surplus:**
- 76M votes cast outside the decisive margin (2020)
- GA margin: 11,779 · AZ margin: 10,457 · WI margin: 20,682
- Combined swing margin: 43K
- CA surplus: 2,552,143 → 216× GA margin
- Dem surplus: 11.8M · GOP surplus: 8.6M · 9-safe-blue-states surplus: 6.3M → 146× combined swing margin

**State-legislative:**
- 139 votes decided WI Assembly District 73 (2020)
- 280 votes decided GA House District 35 (2020)
- 582 votes decided WI State Senate District 32 (2020)

**MoversBudget baselines:**
- Baseline EC under post-2020 apportionment: D 303 / R 235
- US annual interstate migration: ~8,000,000 (Census ACS 2022)
- Katrina Houston displacement: ~250,000 (US Census / HUD 2005)

## Screenshots Workflow

`docs/screenshots/capture.mjs` — puppeteer-core script that points at the installed Chrome (no chromium download needed) and captures three portfolio-quality shots at 2× device pixel ratio:

1. Hero — top of the page
2. MapMoves with Georgia drilled in
3. MoversBudget mid-allocation (100K to NC → flips)

Regenerate: `npm i --no-save puppeteer-core && node docs/screenshots/capture.mjs`. Requires the dev/preview server running at `SITE_URL` (defaults to `http://localhost:5199/`).

The script uses `Object.getOwnPropertyDescriptor(HTMLInputElement.prototype, 'value').set` + `input` event dispatch to trigger Svelte's `bind:value` reactivity from puppeteer — direct `.value = X` assignment does not fire Svelte's compiled listener.

## Testing Portfolio Notes

- Every animation must honor `@media (prefers-reduced-motion: reduce)`
- Every interactive element must be keyboard-reachable with a visible `focus-visible` outline
- Slider thumbs are 22px baseline (`::-webkit-slider-thumb` + `::-moz-range-thumb`) — hits WCAG 2.1 AA touch target size on mobile
- Toggle buttons stretch to 44px min-height on mobile
- Grep for banned vocabulary before shipping any copy change

---

## Changelog

| Date | Commit | Description |
|---|---|---|
| 2026-06-12 | `1266127` | Initial commit — full project scaffold: all sections, D3 map, Calculator, scrollytelling wired |
| 2026-06-12 | `63a188e` | Language audit: banned vocabulary swept (rigged, piled up, structural problem, intellectual flight, classism, organically, legally defensible, inflection point, organic undoing all replaced) |
| 2026-06-29 | *(review response)* | Fixed dead `/the-case` link with Vercel `cleanUrls`; boosted 216×/146× hero stat visual dominance; strengthened State Races visual weight; mobile audit pass; wrote README case study |
| 2026-06-30 | `1fb3dc9` | Added shared data module (`swingStates.js`) — 9 states, baseline EV counts, references |
| 2026-06-30 | `ca70f51` | Mobile updates across MapMoves and MoversBudget (sticky summary bar, slider thumb sizing, touch targets) |
| 2026-06-30 | `76e6940` | README rewritten as portfolio case study with orchestration positioning + editorial standards section |
| 2026-06-30 | `a407df5` | Meta tag banned-vocab fix — swapped "already decided" for "never in question" in OG description; rewrote meta description to match ROI thesis |
| 2026-06-30 | `58f54cf` | Movers Budget added — Census-anchored allocation tool with AllocationMap national choropleth, sticky mobile summary, live EC recomputation |
| 2026-07-01 | *(local)* | Shared direction store across MapMoves + MoversBudget (`stores/direction.js`) |
| 2026-07-01 | *(local)* | Added state outline in StateMiniMap via `topojson.objects.states` lookup + heavy-stroke overlay |
| 2026-07-01 | *(local)* | Fixed AllocationMap reactivity bug — Svelte function-hidden dependency trap (same class as MapMoves' original weight-slider bug). Precomputed pathAttrs in reactive derivation; tooltip made live via fips-based lookup |
| 2026-07-01 | *(local)* | Screenshots captured via `docs/screenshots/capture.mjs`; wired into README opening |
| 2026-07-01 | *(local)* | Simulation logic extracted to `src/lib/data/simulation.js` (simulate + stateTier + countyTier). Both tools now import; no duplicated math |
| 2026-07-01 | *(local)* | Flip-target tick marks on MoversBudget allocation card sliders — grey when unmet, amber when reached |
