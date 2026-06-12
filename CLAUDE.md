# Where It Counts — Project Context

## What This Is

A scrolling data journalism piece in the tradition of The Pudding and NYT Upshot. The argument: geographic sorting and gerrymandering mean that tens of millions of votes don't influence outcomes, and moving to a competitive metro before the 2031 redistricting is a concrete, personal way to change that math.

It is not a call to pick a side. It is a case — built on public data, grounded in civics — for Americans to think differently about the relationship between where they live and how much their voice actually matters.

## Author Context

Government contractor. The piece must stay non-partisan and data-forward. No sensationalism, no inflammatory framing, no "cheap grabs at attention."

## Tone Rules (enforced — do not drift from these)

**Words/phrases to never use:** wasted, fraud, rigged, stolen, suppressed, shut out, piled up, already decided, already set, structural problem, geographic concentration, intellectual flight, classism, inflection point, organically (in political context), legally defensible, accountable (as policy-speak), organic undoing.

**Voice:** Direct. Concrete. Like explaining something real to someone smart who isn't a policy wonk. Think: the way a good teacher explains, not the way a think-tank paper is written.

**Model:** Republican direct-messaging clarity. Make people feel like they understand and relate — not like they're being lectured.

**Not:** Academic, polemic, partisan, or preachy.

## Tech Stack

- **Framework:** SvelteKit + Vite
- **Visualization:** D3.js (choropleth map), scrollama (scroll triggering), topojson-client
- **Fonts:** Playfair Display (serif headings), Inter (sans body), JetBrains Mono (stats/data)
- **Styling:** Global tokens in `src/app.css` — no component-level token overrides

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

## Section Structure

| Order | Component | File | Description |
|---|---|---|---|
| 1 | Hero | `sections/Hero.svelte` | Full-screen dark opener, 76M votes lede |
| 2 | How the Lines Got Drawn | `sections/HowLinesDrawn.svelte` | Gerrymandering + geographic sorting narrative |
| 3 | What the Data Actually Shows | `sections/StatBreaker.svelte` | Dark module — CA surplus vs GA margin (216×), 6.3M vs 43K (146×) |
| 4 | Scrollytelling map | `Scrollytelling.svelte` + `viz/SurplusMapViz.svelte` | D3 choropleth cycling through 5 modes as user scrolls |
| 5 | State Leg Races | inline in `+page.svelte` | 3 stat callouts showing tiny margins (280, 139, 582 votes) |
| 6 | The Part Nobody's Talking About | `sections/Nobody.svelte` | Housing costs, brain drain, zip-code-as-identity |
| 7 | The Map Resets in 2030 | `sections/LongGame.svelte` | 2031 redistricting horizon + contact theory |
| 8 | Calculator | `sections/Calculator.svelte` | Interactive: origin city + job type + budget → ranked competitive metros |
| 9 | Footer | inline in `+page.svelte` | Data source attribution |

## Scrollytelling Map — 5 Modes

Defined in `+page.svelte` as `surplusSteps[]`, rendered by `SurplusMapViz.svelte`:

1. `intro` — full choropleth, both parties
2. `surplus-blue` — highlight Dem counties only
3. `surplus-red` — highlight GOP counties only
4. `total-surplus` — full choropleth, 76M stat
5. `zoom-swing` — zooms to AZ/GA/WI with annotated margins (11,779 / 10,457 / 20,682)

## Data Files

| File | Source | Used For |
|---|---|---|
| `data/county_pres_2020.csv` | MIT Election Lab | Raw county-level 2020 presidential results |
| `data/surplus_2020.json` | Computed via `surplus_calc.py` | Surplus votes by county |
| `data/state_leg_and_wfh.json` | OpenElections + BLS ATUS 2023 | State leg margins + WFH eligibility rates |
| `data/zhvi_metro.csv` | Zillow ZHVI 2024–25 | Median home values by metro |
| `data/zori_metro.csv` | Zillow ZORI 2024–25 | Median rent by metro |
| `data/bea_rpp_raw.json` | Bureau of Economic Analysis | Regional price parities |
| `data/census_wfh_raw.json` | U.S. Census ACS | WFH eligibility by occupation |

**Static assets the map viz expects at runtime:**
- `static/data/counties-10m.json` — US county TopoJSON (10m resolution)
- `static/data/counties-surplus.json` — county surplus lookup for the D3 map

## Calculator — Destination Metros

9 metros hardcoded in `Calculator.svelte`: Atlanta suburbs, Phoenix suburbs, Milwaukee metro, Raleigh–Durham, Charlotte metro, Columbus metro, Pittsburgh metro, Las Vegas metro, Richmond metro.

Scoring: `impactScore = legScore × 0.7 + presScore × 0.3`. Sort options: savings / civic impact / balanced.

## Key Numbers (verify before changing)

- 76M votes cast outside the decisive margin (2020)
- GA margin: 11,779 · AZ margin: 10,457 · WI margin: 20,682
- CA surplus: 2,552,143 · GA margin: 11,779 → 216× multiplier
- Dem surplus: 11.8M · GOP surplus: 8.6M → 146× vs combined swing margin (43K)
- NYC median rent: $3,406 · Columbus: $1,515 → $1,891/mo savings

---

## Changelog

| Date | Commit | Description |
|---|---|---|
| 2026-06-12 | `1266127` | Initial commit — full project scaffold: all sections, D3 map, Calculator, scrollytelling wired |
| 2026-06-12 | `63a188e` | Language audit: removed sensationalist framing (rigged → HowLinesDrawn rename, piled up → accumulated, structural problem, intellectual flight, classism, organically, legally defensible, inflection point, organic undoing all replaced with plain language) |
