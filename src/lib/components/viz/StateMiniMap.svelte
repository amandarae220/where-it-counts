<script>
  // Small per-state overview map. Renders all counties of the named state,
  // highlights the top-leverage counties supplied by the parent, and
  // emphasises one county when a card is hovered. Shares the same
  // counties-10m.json the main scrollytelling viz already loads —
  // second fetch hits the browser cache.

  import { SWING_STATE_FIPS as STATE_FIPS } from '$lib/data/swingStates.js';

  export let stateCode;
  export let highlightFips = [];
  export let hoveredFips = null;
  const W = 320, H = 220;

  let counties = [];
  let stateOutlinePath = null;   // rendered on top of counties for visual clarity
  let viewBox = `0 0 ${W} ${H}`;
  let loaded = false;

  // Module-level cache so every mini-map instance shares one load.
  let topoPromise;
  function loadTopo() {
    if (!topoPromise) {
      topoPromise = fetch('/data/counties-10m.json').then(r => r.json());
    }
    return topoPromise;
  }

  $: build(stateCode);

  async function build(code) {
    if (!code) return;
    loaded = false;
    const [d3, topo, topoData] = await Promise.all([
      import('d3'),
      import('topojson-client'),
      loadTopo(),
    ]);
    const allFeatures = topo.feature(topoData, topoData.objects.counties).features;
    const prefix = STATE_FIPS[code];
    const stateCounties = allFeatures.filter(f => String(f.id).startsWith(prefix));

    const projection = d3
      .geoMercator()
      .fitSize([W - 8, H - 8], { type: 'FeatureCollection', features: stateCounties });
    const path = d3.geoPath().projection(projection);

    counties = stateCounties.map(f => ({ id: String(f.id), d: path(f) }));

    // State outline: find the state polygon matching this code and
    // render it as a heavy-stroke overlay so the shape reads clearly
    // against the surrounding whitespace. Uses the same fitted
    // projection so it registers exactly with the counties beneath.
    const stateFeatures = topo.feature(topoData, topoData.objects.states).features;
    const stateFeature = stateFeatures.find(f =>
      String(f.id).padStart(2, '0') === prefix
    );
    stateOutlinePath = stateFeature ? path(stateFeature) : null;

    loaded = true;
  }
</script>

<div class="mini-wrap" aria-label="Map of {stateCode} highlighting top counties">
  {#if !loaded}
    <div class="mini-loading mono">Loading map…</div>
  {/if}
  <svg
    {viewBox}
    class="mini-map"
    class:ready={loaded}
    preserveAspectRatio="xMidYMid meet"
    role="img"
  >
    {#each counties as c (c.id)}
      <path
        d={c.d}
        class:highlight={highlightFips.includes(c.id)}
        class:hover-on={hoveredFips === c.id}
      />
    {/each}
    {#if stateOutlinePath}
      <path class="state-outline" d={stateOutlinePath} />
    {/if}
  </svg>
</div>

<style>
  .mini-wrap {
    position: relative;
    width: 100%;
    min-height: 180px;
    background: #fafaf8;
    border: 1px solid #e5e7eb;
    border-radius: 3px;
    padding: 0.5rem;
  }
  .mini-loading {
    position: absolute;
    inset: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.75rem;
    color: var(--color-text-muted);
  }
  .mini-map {
    display: block;
    width: 100%;
    height: auto;
    opacity: 0;
    transition: opacity 0.2s;
  }
  .mini-map.ready { opacity: 1; }

  path {
    fill: #d1d5db;
    stroke: #fff;
    stroke-width: 0.4;
    transition: fill 0.18s, stroke 0.18s, fill-opacity 0.18s;
  }
  path.highlight {
    fill: var(--color-competitive);
    fill-opacity: 0.55;
  }
  path.hover-on {
    fill: var(--color-competitive);
    fill-opacity: 1;
    stroke: #1a1a1a;
    stroke-width: 0.9;
  }
  /* State outer boundary — heavy stroke rendered on top of county fills
     so the state's shape reads instantly. pointer-events: none keeps
     county hover interactions working through the overlay. */
  path.state-outline {
    fill: none;
    stroke: #1a1a1a;
    stroke-width: 1.4;
    stroke-linejoin: round;
    stroke-linecap: round;
    pointer-events: none;
    transition: none;
  }
</style>
