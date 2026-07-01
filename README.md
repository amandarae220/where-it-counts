# Where It Counts

A scrolling data-journalism piece in the tradition of The Pudding and NYT Upshot. The argument: tens of millions of votes don't influence outcomes because of where they're cast — and the next redistricting cycle (2031) is a concrete window where that math can change.

It is not partisan. Both parties' surplus votes are shown. The piece is built on public data, sourced inline.

**Live:** https://where-it-counts.vercel.app

---

## About this portfolio piece

This project was designed, written, coded, tested for accessibility, and shipped by a single author across every layer — data pipeline, D3 visualizations, interactive tooling, editorial voice, copy, UX judgment, mobile behavior, and deploy config. In the age of AI-assisted execution, the differentiator isn't typing speed — it's the *judgment stack*: what to build, how it should feel, how copy shapes UX, how the accessibility model interacts with the animation model, when to add and when to cut. This piece is a case study in that stack, not just a demo of one part of it.

Every decision below — the metric, the leverage formula, the sensitivity budget's Census anchor, the sticky mobile summary, the banned-vocabulary list — is a judgment call, made and defended in code and copy simultaneously.

---

## The two interactive tools

**MapMoves** answers *"where does leverage exist?"* — ranks the 9 battleground states by combined presidential + state-legislative leverage, drills into county-level detail for any state. Read-only view of the current map, with a live D/R direction toggle and presidential-vs.-state-leg weight slider.

**MoversBudget** answers *"what actually happens if you move people?"* — gives the reader a budget of relocations (anchored as a percentage of the ~8M Americans who already move between states each year, per Census ACS 2022) and lets them distribute across the 9 states. Recomputes the Electoral College live from a 2020 baseline, shows which states flipped, and computes movers-per-EC-vote-gained efficiency.

They complement rather than repeat: one shows the *map*, the other shows the *response to intervention*.

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

### MapMoves — leverage ranking + county drill-in

[`src/lib/components/sections/MapMoves.svelte`](src/lib/components/sections/MapMoves.svelte) — two-level exploration tool with a symmetric direction toggle (D/R) and a live weight slider.

- **Level 1** ranks the 9 states by a normalized combined score (presidential leverage + state-leg leverage) with `svelte/animate` FLIP transitions on rank changes and CSS `transition: width` on score bars — the sort order updates visibly as the reader drags the slider.
- **Level 2** lazy-loads county-level surplus data on demand, filters to the selected state, and ranks the top 6 counties by leverage per mover. Hovering a card highlights that county on an inline [`StateMiniMap`](src/lib/components/viz/StateMiniMap.svelte) — shared component, per-state Mercator projection fit to a 320×220 viewBox.
- **Vocabulary consistency** — every state and county carries a tier pill ("Razor thin" / "Competitive" / "Shifting") that uses the same palette and thresholds as MoversBudget and the (currently-disabled) Calculator, so a reader learning the vocabulary in one tool reads the others fluently.

### MoversBudget — Census-anchored what-if allocator

[`src/lib/components/sections/MoversBudget.svelte`](src/lib/components/sections/MoversBudget.svelte) — Concept A of the "model your own remedy" pattern: give the reader a real, sourced budget and let them distribute it across the 9 states.

- **Budget slider** expressed as a percentage of the 8M Americans who move between states each year (Census ACS 2022) — every value the reader picks is a fraction of a real baseline, not an aspirational number. Live anchors display *"1.6× Katrina's Houston displacement"* and *"9.3× the combined 2020 margin that decided GA + AZ + WI"* underneath the slider.
- **9 allocation cards** with independent sliders, live per-state margin recomputation, tier reclassification, and a "Flipped" indicator that lights up when a card's projected result crosses the party line.
- **Impact panel** aggregates in real time: Electoral College totals with deltas from a 2020 baseline recomputed under post-2020 census apportionment (D 303 / R 235), count of states flipped with color-coded chips, and a movers-per-EC-vote-gained efficiency ratio.
- **Sticky mobile summary bar** — under 900px, a compact bar shows live EC totals and flip count as the reader scrolls through the allocation cards. Solves the biggest mobile UX problem for this pattern (long scroll = losing context of what your allocations are producing).

### Calculator *(currently disabled — import commented out)*

[`src/lib/components/sections/Calculator.svelte`](src/lib/components/sections/Calculator.svelte) — interactive scoring model: origin city + job type + budget → ranked destination metros. Composite `impactScore = legScore × 0.7 + presScore × 0.3` blended with cost-of-living deltas from BEA Regional Price Parities and Zillow ZHVI/ZORI. Preserved in the codebase; may return in a future iteration.

---

## Case study — technical challenges worth calling out

Three problems in this codebase that don't have obvious solutions and produced small design decisions worth naming for anyone reviewing the technical work.

### 1. Normalizing two leverage axes so a weighting slider actually blends them

MapMoves has a slider that weights presidential leverage vs. state-legislative leverage. First cut used raw closeness (`100 / sqrt(margin_pct)`) for presidential and raw competitive-district share (`comp_leg / total_leg × 500`) for state-leg. Result: presidential leverage capped at 100 for the razor-thin states, state-leg leverage topped out around 39 — meaning at 0% presidential weight the highest score was 39, at 100% it was 100. The slider felt one-sided and the bar visualization was inconsistent across positions.

Fix: normalize both axes against the dataset's own maximum (`Math.max(...STATES.map(rawFn))`) so both scales hit 0–100. The slider now blends genuinely comparable numbers, and the bar widths make sense at any slider position. See [`MapMoves.svelte:79–95`](src/lib/components/sections/MapMoves.svelte).

A related trap: the first version passed `combinedScore(s)` from inside a `$: ranked = ...` reactive block, reading `weightPres` from the outer scope. Svelte 4's compiler only tracks variables that appear literally in the reactive expression — it couldn't see `weightPres` inside the function body, so the ranking never updated when the slider moved. Fix: pass `weightPres` in as an argument.

### 2. Per-state projection fit for the drill-in mini-map

The main scrollytelling map uses `d3.geoAlbersUsa().fitExtent(...)` for the whole nation. Reusing that for the per-state drill-in mini-maps produced tiny, off-center state shapes surrounded by empty ocean.

[`StateMiniMap.svelte`](src/lib/components/viz/StateMiniMap.svelte) instead creates a per-state `d3.geoMercator().fitSize([W, H], stateCounties)` — projecting each state independently into a 320×220 viewBox. Honest tradeoff: Mercator distorts tall states (TX, FL) slightly, but at overview-map size the shapes read correctly. `d3.geoAlbers` with per-state parallels would be more accurate; Mercator was chosen for simplicity given the render size.

The topojson (~10MB) is loaded once, cached in a module-level promise, and shared across all mini-map instances plus the main scrollytelling viz — so opening a mini-map after the main map has scrolled into view is instant.

### 3. County leverage formula — why division, not multiplication

The intuitive formula for "leverage per mover" is `population × (1 - |margin|)` — bigger electorate, closer race, more leverage. But this collapses toward zero as margins approach 50%, and rewards huge lopsided counties (LA County's 65% Democratic margin gives it more "leverage" than Maricopa's 2%).

The formula used is `leverage = total_votes / (1 + |margin_pct|)`. This decays smoothly with margin but never zeros out (capped at 25pt margin above), and puts genuinely competitive large counties at the top rather than small competitive counties or huge lopsided ones. See [`MapMoves.svelte`](src/lib/components/sections/MapMoves.svelte).

### 4. Baseline-preserving margin recomputation in MoversBudget

MoversBudget simulates *"what if N net-new voters chose direction D in state X?"* But the state's `margin_pct` is a percentage of the original 2020 electorate — you can't just add/subtract N from the pct field without rebasing.

The chosen approach: preserve the state's original vote-to-pct ratio (`pctPerVote = margin_pct / margin_votes`), shift `margin_votes` by the allocated movers, then recompute `new_pct = new_margin_votes × pctPerVote`. This drifts slightly at extreme shifts (the electorate itself would grow, changing the denominator), but stays honest at realistic scales and is annotated as such in the code. See the `simulate()` function in [`MoversBudget.svelte`](src/lib/components/sections/MoversBudget.svelte).

### 5. Sticky mobile summary — solving context loss on long allocation UIs

MoversBudget has 9 state cards, each with its own slider, and an impact panel at the bottom. On mobile, the reader can allocate to Card 3 and then wonder *"but what did that do to the EC?"* — the answer is 5 scrolls away.

Fix: a sticky `position: sticky; top: 0` bar that appears at viewports under 900px, sits between the meter and the state grid, and shows the live EC totals plus flip count. It uses `backdrop-filter: blur(6px)` for legibility over both light and dark content, and it only mounts when the containing section is in view (natural behavior of sticky positioning). Discovered by testing the tool on a phone and immediately feeling the context loss — the fix followed the observed problem, not an abstract rule.

### 6. Cross-browser slider thumb sizing + WCAG-compliant touch targets

`accent-color` styles the slider fill but not the thumb size, which varies wildly by browser (~14px on some, ~20px on others). For a piece with 10+ sliders spread across two tools, that inconsistency reads as sloppy.

Both MapMoves and MoversBudget include explicit `::webkit-slider-thumb` and `::-moz-range-thumb` rules that give predictable 22px thumbs everywhere, with a 12% scale-up on hover and a full pattern override under `@media (prefers-reduced-motion: reduce)`. Combined with 44px minimum-height toggle buttons and a `min-height: 36px` reset button on mobile, every interactive element meets WCAG 2.1 AA touch-target guidance.

### 7. Shared data module — single source of truth for the 9 states

MapMoves and MoversBudget both need the same 9 battleground states with the same margin data, EV counts, and legislative-district counts. Duplicating the array inline in each component invites drift: fix a typo in one, forget the other, ship inconsistent numbers.

The fix is a single [`src/lib/data/swingStates.js`](src/lib/data/swingStates.js) module that exports `SWING_STATES`, `BASELINE_D_EV`, `BASELINE_R_EV`, and a `REFERENCES` object with every citation anchor (Census annual interstate movement, Katrina, Maria, 2020 combined swing margin, etc.), each with `value` + `label` + `source` fields. Both components import from it. If a fact changes, one file changes.

---

## Editorial standards

The technical work is only half the piece. The other half is a set of editorial standards enforced at the same rigor as the code — the "orchestration layer" a portfolio piece has to prove exists.

### Voice

Direct, teacher-explaining, numbers-do-the-work. Never academic. Never polemic. The test: if a sentence would survive with the adjective removed, remove it. Every stat is sourced inline with an institution the reviewer recognizes (MIT Election Lab, Census ACS, BLS, Zillow Research, Ballotpedia). No unsourced round numbers.

### Banned vocabulary

Some words editorialize where the data should do the work; others telegraph the piece as partisan or academic when the voice is meant to be direct. This piece never uses any of them:

> wasted · fraud · rigged · stolen · suppressed · shut out · piled up · already decided · already set · structural problem · geographic concentration · intellectual flight · classism · brain drain · inflection point · organically (in political context) · legally defensible · accountable (as policy-speak) · organic undoing

The list is scanned via grep before every substantive copy change. When a banned concept is genuinely load-bearing (e.g., "geographic concentration" in an academic citation) the copy is rewritten in plain language ("how Democratic voters have clustered into safe corners") rather than smuggling the term in.

### Consistent vocabulary across tools

Both interactive tools classify race competitiveness using the same three-tier vocabulary — **Razor thin** (amber), **Competitive** (blue), **Shifting** (gray) — with the same color palette and the same underlying thresholds. A reader learning the vocabulary in MapMoves reads MoversBudget fluently, and vice versa. This isn't a code duplication problem; it's a UX consistency signal.

### Own your rhetorical framings

Where a comparison is illustrative rather than causal — the "216× Georgia" and "146× GA+AZ+WI" hero stats in StatBreaker — the copy names that framing explicitly. The 216× caption ends with *"Those votes couldn't cross state lines — that's precisely what makes geography so important."* The extra sentence costs little and buys the piece's credibility with any trained reviewer.

### Sourced feasibility

Where the piece argues for a remedy, it names the honest scale of the ask. The closer explicitly says *"a meaningful shift in a state-legislative district's math takes thousands of movers, not hundreds"* rather than implying trivial physics. The MoversBudget slider is anchored to real Census ACS 2022 numbers and Katrina/Maria historical precedents, so the reader can't ask "where did that budget come from" — the answer is on-screen and cited.

### Accessibility as a design constraint, not an audit

WCAG 2.1 AA is the minimum. Every focusable element has `focus-visible` outlines, every toggle carries `aria-pressed`, every animation respects `prefers-reduced-motion`, every stat is announced with meaningful text (not just visual). The sensitivity-panel projected values have `role="status"` and `aria-live` where meaningful. Slider thumbs are 22px baseline and toggle buttons are 44px min-height on mobile — hit targets for one-handed thumb use.

### One-thesis discipline

Earlier drafts of this piece ran two theses in parallel: (a) *your vote's ROI* (analytical/data-forward) and (b) *geographic sorting has cultural costs* (reflective/essay). Both were defensible on their own; together they fought for the reader's attention. The piece is now committed to (a). The essay content is preserved in inert component files (`Nobody.svelte`, `HowLinesDrawn.svelte`, `DistrictShopping.svelte`, `LongGame.svelte`, `Hero.svelte`) for future salvage but is not shipped. Cutting is a portfolio skill.

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
| MIT Election Lab | County-level 2020 presidential results · state margins |
| OpenElections | State legislative race margins |
| Ballotpedia | State legislative chamber control · competitive district counts |
| US Census ACS 2022 | Annual interstate migration baseline (MoversBudget anchor) |
| US Census / HUD 2005 | Katrina Houston displacement (MoversBudget reference anchor) |
| US Census 2020 apportionment | Post-2020 Electoral College counts (applies from 2024) |
| U.S. Census ACS | WFH-eligibility by occupation *(Calculator, currently disabled)* |
| Bureau of Labor Statistics (ATUS 2023) | Telework rates *(Calculator, currently disabled)* |
| Zillow Research (ZHVI / ZORI) | Metro home values and rents *(Calculator, currently disabled)* |
| Bureau of Economic Analysis | Regional Price Parities *(Calculator, currently disabled)* |
| Rodden, *Why Cities Lose* (2019) | Intellectual grounding for surplus-vote framing (closer citation) |

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

Single-page site. Full arc lives in [+page.svelte](src/routes/+page.svelte).

```
src/
  app.css                          # Global tokens, scrolly layout, typography
  routes/
    +page.svelte                   # Hero → StatBreaker → scrolly map → State Races
                                   # → MapMoves → MoversBudget → Closer
  lib/
    data/
      swingStates.js               # Shared source of truth: 9 battleground states,
                                   # baseline EC, and reference anchors (Census,
                                   # Katrina, etc.) used by both interactive tools.
    components/
      Scrollytelling.svelte        # Generic sticky-viz + steps shell
      viz/
        SurplusMapViz.svelte       # D3 choropleth, 5 modes, tooltip, annotations
        StateMiniMap.svelte        # Per-state overview map for MapMoves drill-in
      sections/
        StatBreaker.svelte         # 216× / 146× hero stat module
        MapMoves.svelte            # 9-state leverage tool, county drill-in
        MoversBudget.svelte        # Census-anchored what-if allocator: distribute
                                   # a slice of annual interstate movement across
                                   # 9 states, watch the EC recompute live
        Calculator.svelte          # (currently disabled) Metro ranker
data/                              # Source CSVs + processing scripts
static/data/                       # Built TopoJSON + surplus lookup, served at runtime
```

See [content.md](content.md) for the full prose review across every section.
