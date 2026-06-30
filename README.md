# Where It Counts

A scrolling data-journalism piece in the tradition of The Pudding and NYT Upshot. The argument: tens of millions of votes don't influence outcomes because of where they're cast — and the next redistricting cycle (2031) is a concrete window where that math can change.

It is not partisan. Both parties' surplus votes are shown. The piece is built on public data, sourced inline.

**Live:** https://where-it-counts.vercel.app

---

## Case study — what's custom-built

The piece runs on a hand-rolled D3 + scrollama pipeline. There is no Mapbox, no Tableau, no Datawrapper embed. Everything in the visualization is computed from raw public data and rendered to SVG in the browser.

### The metric: "surplus votes"

Most political dashboards visualize raw vote totals or margins. This piece introduces a different metric — *surplus votes*, defined as votes cast for the winner of a county beyond what was needed for that county to swing to the loser. It is a per-county measure of how much a vote's geographic placement reduced its marginal influence on the 2020 outcome.

- Computed in [`surplus_calc.py`](data/) from MIT Election Lab county-level 2020 results
- ~3,150 county records joined to TopoJSON county geometry by FIPS
- Output: [`static/data/counties-surplus.json`](static/data/counties-surplus.json)

### The map: D3 choropleth with scroll-driven mode switching

[`src/lib/components/viz/SurplusMapViz.svelte`](src/lib/components/viz/SurplusMapViz.svelte) — 413 lines, no library beyond raw D3.

- Single sticky SVG (viewBox 960×580, `preserveAspectRatio: xMidYMid meet`) reused across all five scroll steps — no remount, no flicker
- Five visualization modes (`intro`, `surplus-blue`, `surplus-red`, `total-surplus`, `zoom-swing`) driven by a reactive `mode` prop that flows from `scrollama.onStepEnter`
- D3 transitions animate fill, opacity, and zoom between modes
- Per-county hover tooltip with party badge, raw totals, and surplus number
- `zoom-swing` mode runs a computed transform to center on AZ/GA/WI and overlays SVG annotations for each state's deciding margin (11,779 / 10,457 / 20,682)
- Quantile color scales (`d3.scaleQuantile`) built per-party so the long-tail distribution of large urban counties doesn't crush the rest of the map

### Scroll orchestration

[`src/lib/components/Scrollytelling.svelte`](src/lib/components/Scrollytelling.svelte) — a generic sticky-viz + narrative-steps shell that takes any viz component as a `<svelte:component>`. It dynamically imports `scrollama` on mount so the SSR/prerender step stays clean.

### Calculator

[`src/lib/components/sections/Calculator.svelte`](src/lib/components/sections/Calculator.svelte) — interactive scoring model. User picks origin city + job type + budget; output ranks nine target metros by a composite `impactScore = legScore × 0.7 + presScore × 0.3`, blended with cost-of-living delta from BEA Regional Price Parities and Zillow ZHVI/ZORI.

---

## Tech stack

- **Framework:** SvelteKit + Vite, static-adapter prerender
- **Visualization:** D3 v7, scrollama, topojson-client
- **Hosting:** Vercel (clean URLs, no server runtime)
- **Fonts:** Playfair Display (serif), Inter (sans), JetBrains Mono (numerals)

All design tokens are global in [`src/app.css`](src/app.css). No component-level token overrides.

---

## Data sources

| Source | Used for |
|---|---|
| MIT Election Lab | County-level 2020 presidential results |
| OpenElections | State legislative race margins |
| U.S. Census ACS | WFH-eligibility by occupation |
| Bureau of Labor Statistics (ATUS 2023) | Telework rates |
| Zillow Research (ZHVI / ZORI) | Metro home values and rents |
| Bureau of Economic Analysis | Regional Price Parities |
| Ballotpedia | State legislative chamber control |

---

## Run locally

```bash
npm install
npm run dev      # http://localhost:5173
npm run build    # static output to /build
npm run preview
```

---

## Project structure

```
src/
  app.css                          # Global tokens, scrolly layout, typography
  routes/
    +page.svelte                   # Landing: hero, two-moves, scrolly map, state races, bridge
    the-case/+page.svelte          # Act two: lines drawn → district shopping → calculator
  lib/components/
    Scrollytelling.svelte          # Generic sticky-viz + steps shell
    viz/SurplusMapViz.svelte       # D3 choropleth, 5 modes, tooltip, annotations
    sections/
      StatBreaker.svelte           # 216× / 146× hero stat module
      HowLinesDrawn.svelte         # Gerrymandering + geographic sorting
      DistrictShopping.svelte      # Candidates as movers
      Nobody.svelte                # Housing costs, brain drain
      LongGame.svelte              # 2031 redistricting horizon
      Calculator.svelte            # Interactive metro ranker
data/                              # Source CSVs + processing scripts
static/data/                       # Built TopoJSON + surplus lookup, served at runtime
```
