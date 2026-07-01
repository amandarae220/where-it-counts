<script>
  // National allocation choropleth for MoversBudget's impact panel.
  //
  // Renders all 50 states; the 9 battleground states color-code by their
  // projected margin (D-blue ↔ R-red gradient, saturation scales with
  // margin distance from zero). Non-swing states stay neutral. Any state
  // that has flipped from its 2020 result gets an amber outer stroke —
  // the visual "look what changed" moment MoversBudget was missing.
  //
  // The topojson is loaded via a module-level promise so the second and
  // subsequent viz components (SurplusMapViz, StateMiniMap) hit the same
  // in-memory cache instead of re-fetching ~10MB.

  import { onMount } from 'svelte';
  import { SWING_STATE_FIPS } from '$lib/data/swingStates.js';

  export let simResults = [];

  const W = 640, H = 400;

  let container;
  let stateFeatures = [];
  let pathByFips = new Map();
  let loaded = false;
  let tooltip = { visible: false, x: 0, y: 0, result: null };

  // Shared topo cache
  let topoPromise;
  function loadTopo() {
    if (!topoPromise) {
      topoPromise = fetch('/data/counties-10m.json').then(r => r.json());
    }
    return topoPromise;
  }

  // Invert the FIPS lookup so we can map from feature id → simulation result.
  $: fipsToResult = new Map(
    simResults.map(r => [SWING_STATE_FIPS[r.code], r])
  );

  onMount(async () => {
    const [d3, topo, topoData] = await Promise.all([
      import('d3'),
      import('topojson-client'),
      loadTopo(),
    ]);

    const states = topo.feature(topoData, topoData.objects.states);
    const projection = d3.geoAlbersUsa()
      .fitSize([W - 12, H - 12], states);
    const pathGen = d3.geoPath().projection(projection);

    stateFeatures = states.features;
    pathByFips = new Map(
      states.features.map(f => [String(f.id).padStart(2, '0'), pathGen(f)])
    );
    loaded = true;
  });

  // Color map: neutral for non-swing, gradient D-blue ↔ R-red for swing
  // states based on their PROJECTED margin. Saturation scales with distance
  // from zero, so a razor-thin state reads pale and a solidly-shifted state
  // reads saturated. Matches the tier vocabulary the piece uses everywhere.
  function fillFor(fips) {
    const r = fipsToResult.get(fips);
    if (!r) return '#e5e7eb';                       // non-swing: neutral grey
    const pct = r.newPct;
    if (pct > 0) {
      // Democratic side: #bfdbfe (light) → #1d4ed8 (deep)
      const t = Math.min(1, pct / 5);
      const R = Math.round(191 - t * 162);
      const G = Math.round(219 - t * 141);
      const B = Math.round(254 - t * 38);
      return `rgb(${R}, ${G}, ${B})`;
    }
    // Republican side: #fecaca (light) → #b91c1c (deep)
    const t = Math.min(1, Math.abs(pct) / 5);
    const R = Math.round(254 - t * 69);
    const G = Math.round(202 - t * 174);
    const B = Math.round(202 - t * 174);
    return `rgb(${R}, ${G}, ${B})`;
  }
  function strokeFor(fips) {
    const r = fipsToResult.get(fips);
    if (r?.flipped) return '#d97706';               // amber for flipped
    if (r) return '#fff';
    return '#d1d5db';
  }
  function strokeWidthFor(fips) {
    const r = fipsToResult.get(fips);
    if (r?.flipped) return 2.2;
    if (r) return 0.85;
    return 0.5;
  }

  // ── Tooltip handlers ────────────────────────────────────────
  function showTooltip(event, fips) {
    const r = fipsToResult.get(fips);
    if (!r) return;
    const rect = container.getBoundingClientRect();
    tooltip = {
      visible: true,
      x: event.clientX - rect.left + 12,
      y: event.clientY - rect.top + 12,
      result: r,
    };
  }
  function hideTooltip() { tooltip = { ...tooltip, visible: false }; }
</script>

<div class="alloc-map-wrap" bind:this={container} role="img"
     aria-label="National map of your allocation. Nine battleground states colored by projected outcome; flipped states outlined in amber.">
  {#if !loaded}
    <div class="loading mono">Loading map…</div>
  {/if}

  <svg
    viewBox="0 0 {W} {H}"
    class="alloc-map"
    class:ready={loaded}
    preserveAspectRatio="xMidYMid meet"
  >
    {#if loaded}
      {#each stateFeatures as feat (feat.id)}
        {@const fips = String(feat.id).padStart(2, '0')}
        {@const isSwing = fipsToResult.has(fips)}
        <path
          d={pathByFips.get(fips)}
          fill={fillFor(fips)}
          stroke={strokeFor(fips)}
          stroke-width={strokeWidthFor(fips)}
          class:swing={isSwing}
          on:mousemove={(e) => showTooltip(e, fips)}
          on:mouseleave={hideTooltip}
        />
      {/each}
    {/if}
  </svg>

  {#if tooltip.visible && tooltip.result}
    <div
      class="alloc-tt"
      style="left: {tooltip.x}px; top: {tooltip.y}px"
      aria-hidden="true"
    >
      <div class="tt-name">{tooltip.result.name}</div>
      <div class="tt-grid">
        <span class="tt-label mono">2020</span>
        <span class="tt-val lean-{tooltip.result.origParty}">
          {tooltip.result.origParty}&thinsp;+{Math.abs(tooltip.result.margin_pct).toFixed(2)}
        </span>
        <span class="tt-label mono">Projected</span>
        <span class="tt-val lean-{tooltip.result.newParty}">
          {tooltip.result.newParty}&thinsp;+{Math.abs(tooltip.result.newPct).toFixed(2)}
        </span>
        <span class="tt-label mono">Movers</span>
        <span class="tt-val mono">
          {tooltip.result.movers.toLocaleString()}
        </span>
        <span class="tt-label mono">EV</span>
        <span class="tt-val mono">{tooltip.result.ev}</span>
      </div>
      {#if tooltip.result.flipped}
        <div class="tt-flipped mono">Flipped ✓</div>
      {/if}
    </div>
  {/if}

  <div class="legend mono" aria-hidden="true">
    <div class="legend-scale">
      <span class="legend-swatch legend-r-strong" aria-label="Strong Republican"></span>
      <span class="legend-swatch legend-r-light"  aria-label="Lean Republican"></span>
      <span class="legend-swatch legend-tossup"   aria-label="Toss-up"></span>
      <span class="legend-swatch legend-d-light"  aria-label="Lean Democratic"></span>
      <span class="legend-swatch legend-d-strong" aria-label="Strong Democratic"></span>
    </div>
    <div class="legend-labels">
      <span>Republican</span>
      <span class="legend-mid">Tied</span>
      <span>Democratic</span>
    </div>
    <div class="legend-flipped">
      <span class="legend-flip-box"></span>
      <span>Outline = flipped from 2020</span>
    </div>
  </div>
</div>

<style>
  .alloc-map-wrap {
    position: relative;
    width: 100%;
    max-width: 640px;
    margin: 0 auto;
  }
  .loading {
    position: absolute;
    inset: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    color: var(--color-text-muted);
    font-size: 0.75rem;
    pointer-events: none;
  }
  .alloc-map {
    display: block;
    width: 100%;
    height: auto;
    opacity: 0;
    transition: opacity 0.25s;
  }
  .alloc-map.ready { opacity: 1; }

  path {
    transition: fill 0.32s cubic-bezier(0.4, 0, 0.2, 1),
                stroke 0.25s, stroke-width 0.25s;
  }
  path.swing { cursor: pointer; }
  path.swing:hover { filter: brightness(0.92); }
  @media (prefers-reduced-motion: reduce) {
    path, .alloc-map { transition: none; }
  }

  /* ── Tooltip ──────────────────────────────────────────────── */
  .alloc-tt {
    position: absolute;
    pointer-events: none;
    background: rgba(15, 15, 14, 0.96);
    color: #fff;
    border: 1px solid #374151;
    border-radius: 4px;
    padding: 0.625rem 0.875rem;
    font-size: 0.75rem;
    z-index: 10;
    box-shadow: 0 4px 14px rgba(0,0,0,0.25);
    min-width: 170px;
    backdrop-filter: blur(4px);
  }
  .tt-name {
    font-family: var(--font-serif);
    font-weight: 700;
    font-size: 0.9375rem;
    margin-bottom: 0.5rem;
    color: #f9fafb;
  }
  .tt-grid {
    display: grid;
    grid-template-columns: auto 1fr;
    gap: 0.3rem 0.75rem;
    align-items: baseline;
  }
  .tt-label {
    font-size: 0.6rem;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #9ca3af;
  }
  .tt-val {
    font-size: 0.8125rem;
    text-align: right;
    font-family: var(--font-mono);
    color: #e5e7eb;
  }
  .tt-val.lean-D { color: #93c5fd; }
  .tt-val.lean-R { color: #fca5a5; }
  .tt-flipped {
    margin-top: 0.5rem;
    padding-top: 0.5rem;
    border-top: 1px solid #374151;
    color: #fcd34d;
    font-size: 0.6875rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    text-align: center;
    font-weight: 600;
  }

  /* ── Legend ───────────────────────────────────────────────── */
  .legend {
    margin-top: 1rem;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 0.5rem;
    font-size: 0.6875rem;
    color: var(--color-text-muted);
    letter-spacing: 0.05em;
  }
  .legend-scale {
    display: flex;
    gap: 1px;
    padding: 2px;
    background: #e5e7eb;
    border-radius: 2px;
  }
  .legend-swatch {
    display: block;
    width: 36px;
    height: 8px;
  }
  .legend-r-strong { background: #b91c1c; }
  .legend-r-light  { background: #fecaca; }
  .legend-tossup   { background: #e5e7eb; }
  .legend-d-light  { background: #bfdbfe; }
  .legend-d-strong { background: #1d4ed8; }
  .legend-labels {
    display: flex;
    justify-content: space-between;
    width: 190px;
    font-size: 0.625rem;
    letter-spacing: 0.08em;
    text-transform: uppercase;
  }
  .legend-labels > :first-child { color: #b91c1c; }
  .legend-labels > :last-child  { color: #1d4ed8; }
  .legend-mid { color: #9ca3af; }
  .legend-flipped {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    margin-top: 0.25rem;
    font-size: 0.625rem;
    letter-spacing: 0.06em;
    text-transform: uppercase;
  }
  .legend-flip-box {
    display: inline-block;
    width: 14px;
    height: 10px;
    border: 2px solid #d97706;
    background: rgba(217, 119, 6, 0.15);
    border-radius: 2px;
  }

  /* ── Mobile — legend stacks smaller, tooltip repositions ── */
  @media (max-width: 620px) {
    .legend-scale { padding: 1px; }
    .legend-swatch { width: 28px; height: 7px; }
    .legend-labels { width: 148px; }
    .alloc-tt {
      font-size: 0.6875rem;
      min-width: 140px;
      padding: 0.5rem 0.75rem;
    }
  }
</style>
