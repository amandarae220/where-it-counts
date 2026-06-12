<script>
  import { onMount } from 'svelte';

  export let step = 0;
  export let steps = [];
  $: mode = steps[step]?.mode ?? 'intro';

  let container;
  let initialized = false;

  // Tooltip state — updated by D3 mouse events
  let tooltip = { visible: false, x: 0, y: 0, data: null };

  // Dynamic import refs — set in boot() for SSR safety
  let d3, topo;

  // Data
  const countyData = new Map(); // fips → {winner, surplus, margin_pct}
  let allFeatures = [];   // county GeoJSON features
  let stateFeatures = []; // state GeoJSON features (for centroids)

  // D3 DOM handles
  let gZoom, gCounties, gBorders;
  let pathGen;

  // Color scales (set after data loads with real domains)
  let demScale, gopScale;

  const W = 960, H = 580;
  const SWING = new Set(['04', '13', '55']); // AZ, GA, WI

  // ── Color helpers ────────────────────────────────────────────

  function countyFill(id) {
    const c = countyData.get(id);
    if (!c) return '#1a1a18';
    if (c.margin_pct < 2) return '#d97706'; // amber — genuinely competitive
    return c.winner === 'dem' ? demScale(c.surplus) : gopScale(c.surplus);
  }

  function styleFor(id, currentMode) {
    const c = countyData.get(id);
    if (!c) return { fill: '#1a1a18', opacity: 0.4 };
    const isSwing = SWING.has(id.slice(0, 2));

    switch (currentMode) {
      case 'surplus-blue':
        return c.winner === 'dem'
          ? { fill: countyFill(id), opacity: 0.95 }
          : { fill: '#111110', opacity: 0.15 };

      case 'surplus-red':
        return c.winner === 'gop'
          ? { fill: countyFill(id), opacity: 0.95 }
          : { fill: '#111110', opacity: 0.15 };

      case 'zoom-swing':
        return isSwing
          ? { fill: countyFill(id), opacity: 1.0 }
          : { fill: '#111110', opacity: 0.10 };

      default: // intro + total-surplus — full choropleth
        return { fill: countyFill(id), opacity: 0.88 };
    }
  }

  // ── Boot ─────────────────────────────────────────────────────

  async function boot() {
    [d3, topo] = await Promise.all([
      import('d3'),
      import('topojson-client'),
    ]);

    const [topoData, surplusArr] = await Promise.all([
      d3.json('/data/counties-10m.json'),
      d3.json('/data/counties-surplus.json'),
    ]);

    // Build lookup map
    surplusArr.forEach(c => countyData.set(c.fips, c));

    // Color scales — sqrt-ish compression handles LA County's outlier surplus
    const maxDem = d3.max(surplusArr.filter(c => c.winner === 'dem'), c => c.surplus);
    const maxGop = d3.max(surplusArr.filter(c => c.winner === 'gop'), c => c.surplus);
    demScale = d3.scalePow().exponent(0.35).domain([0, maxDem]).range(['#93c5fd', '#1d4ed8']);
    gopScale = d3.scalePow().exponent(0.35).domain([0, maxGop]).range(['#fca5a5', '#b91c1c']);

    // Projection fitted to the nation boundary
    const nation = topo.feature(topoData, topoData.objects.nation);
    const projection = d3.geoAlbersUsa().fitExtent([[20, 20], [W - 20, H - 20]], nation);
    pathGen = d3.geoPath().projection(projection);

    // ── SVG skeleton ──────────────────────────────────────────
    const svg = d3.select(container)
      .append('svg')
      .attr('viewBox', `0 0 ${W} ${H}`)
      .attr('preserveAspectRatio', 'xMidYMid meet')
      .style('width', '100%')
      .style('height', '100%');

    svg.append('rect').attr('width', W).attr('height', H).attr('fill', '#111110');

    gZoom = svg.append('g').attr('class', 'zoom-g');

    // ── Counties ──────────────────────────────────────────────
    const countiesFeature = topo.feature(topoData, topoData.objects.counties);
    allFeatures = countiesFeature.features;

    const statesFeature = topo.feature(topoData, topoData.objects.states);
    stateFeatures = statesFeature.features;

    gCounties = gZoom.append('g');
    gCounties.selectAll('path')
      .data(allFeatures)
      .join('path')
        .attr('d', pathGen)
        .attr('fill', d => countyFill(d.id))
        .attr('opacity', 0.88)
        .attr('stroke', '#111110')
        .attr('stroke-width', 0.25)
        .style('cursor', 'crosshair')
        .on('mousemove', (event, d) => {
          const c = countyData.get(d.id);
          if (!c) return;
          const rect = container.getBoundingClientRect();
          let x = event.clientX - rect.left + 16;
          let y = event.clientY - rect.top - 70;
          // Flip horizontally if tooltip would clip right edge
          if (x + 224 > rect.width)  x = event.clientX - rect.left - 240;
          // Flip vertically if tooltip would clip top edge
          if (y < 8) y = event.clientY - rect.top + 20;
          tooltip = { visible: true, x, y, data: c };
        })
        .on('mouseleave', () => { tooltip = { ...tooltip, visible: false }; });

    // ── State borders ─────────────────────────────────────────
    const statesMesh = topo.mesh(topoData, topoData.objects.states, (a, b) => a !== b);
    gBorders = gZoom.append('path')
      .datum(statesMesh)
      .attr('d', pathGen)
      .attr('fill', 'none')
      .attr('stroke', '#374151')
      .attr('stroke-width', 0.75);

    // ── Legend ────────────────────────────────────────────────
    const legend = svg.append('g').attr('transform', `translate(16, ${H - 58})`);
    [
      { color: '#1d4ed8', label: 'Dem surplus' },
      { color: '#b91c1c', label: 'Rep surplus' },
      { color: '#d97706', label: '<2pt margin'  },
    ].forEach(({ color, label }, i) => {
      const row = legend.append('g').attr('transform', `translate(0, ${i * 18})`);
      row.append('rect').attr('width', 10).attr('height', 10).attr('y', -2).attr('rx', 2).attr('fill', color);
      row.append('text')
        .attr('x', 15)
        .attr('font-family', 'Inter, sans-serif')
        .attr('font-size', '11px')
        .attr('fill', '#4b5563')
        .text(label);
    });

    initialized = true;
    // Reactive block fires on next tick — no need to call updateViz here
  }

  // ── Viz update ───────────────────────────────────────────────

  function updateViz(currentMode) {
    if (!initialized || !gCounties) return;

    gCounties.selectAll('path')
      .transition().duration(650).ease(d3.easeCubicOut)
      .attr('fill',    d => styleFor(d.id, currentMode).fill)
      .attr('opacity', d => styleFor(d.id, currentMode).opacity);

    if (currentMode === 'zoom-swing') {
      zoomToSwing();
    } else {
      // Reset zoom + borders
      gZoom.transition().duration(800).ease(d3.easeCubicOut)
        .attr('transform', 'translate(0,0) scale(1)');
      gBorders.transition().duration(800).attr('stroke-width', 0.75);
      gCounties.selectAll('path').transition().duration(800).attr('stroke-width', 0.25);
      d3.select(container).selectAll('.swing-label').remove();
    }
  }

  function zoomToSwing() {
    const swingFeats = allFeatures.filter(f => SWING.has(f.id.slice(0, 2)));
    const [[x0, y0], [x1, y1]] = pathGen.bounds({ type: 'FeatureCollection', features: swingFeats });
    const scale = Math.min(W / (x1 - x0), H / (y1 - y0)) * 0.70;
    const cx = (x0 + x1) / 2;
    const cy = (y0 + y1) / 2;
    const tx = W / 2 - scale * cx;
    const ty = H / 2 - scale * cy;

    gZoom.transition().duration(900).ease(d3.easeCubicInOut)
      .attr('transform', `translate(${tx},${ty}) scale(${scale})`);

    // Scale down borders/strokes so they stay visually thin
    gBorders.transition().duration(900).attr('stroke-width', 0.75 / scale);
    gCounties.selectAll('path').transition().duration(900).attr('stroke-width', 0.25 / scale);

    addSwingLabels(scale, tx, ty);
  }

  function addSwingLabels(scale, tx, ty) {
    d3.select(container).selectAll('.swing-label').remove();
    const svg = d3.select(container).select('svg');

    const info = {
      '04': { name: 'Arizona',   margin: '10,457' },
      '13': { name: 'Georgia',   margin: '11,779' },
      '55': { name: 'Wisconsin', margin: '20,682' },
    };

    Object.entries(info).forEach(([prefix, { name, margin }]) => {
      const feat = stateFeatures.find(f => f.id === prefix);
      if (!feat) return;

      const [cx, cy] = pathGen.centroid(feat);
      if (isNaN(cx) || isNaN(cy)) return;

      // State centroid in screen space
      const sx = cx * scale + tx;
      const sy = cy * scale + ty;

      // Label anchor — pushed to the margin outside the state geography
      let lx, ly, anchor;
      if (prefix === '04') {        // Arizona → left margin
        lx = 16;
        ly = Math.max(70, Math.min(H - 70, sy));
        anchor = 'start';
      } else if (prefix === '13') { // Georgia → right margin
        lx = W - 16;
        ly = Math.max(70, Math.min(H - 70, sy));
        anchor = 'end';
      } else {                      // Wisconsin → top margin
        lx = Math.max(90, Math.min(W - 90, sx));
        ly = 52;
        anchor = 'middle';
      }

      const g = svg.append('g')
        .attr('class', 'swing-label')
        .attr('pointer-events', 'none');

      // Dashed leader line from centroid to label
      g.append('line')
        .attr('x1', sx).attr('y1', sy)
        .attr('x2', lx).attr('y2', ly)
        .attr('stroke', '#4b5563')
        .attr('stroke-width', 1)
        .attr('stroke-dasharray', '4,3');

      // Anchor dot at the centroid — marks the exact spot
      g.append('circle')
        .attr('cx', sx).attr('cy', sy)
        .attr('r', 4)
        .attr('fill', '#d97706')
        .attr('stroke', '#111110')
        .attr('stroke-width', 1.5);

      // Label text at the edge
      const label = g.append('g').attr('transform', `translate(${lx},${ly})`);

      if (prefix === '55') {
        // Wisconsin: label above the line terminus
        label.append('text')
          .attr('text-anchor', anchor).attr('y', -18)
          .attr('font-family', 'Inter, sans-serif')
          .attr('font-size', '11px').attr('fill', '#9ca3af')
          .text(name);
        label.append('text')
          .attr('text-anchor', anchor).attr('y', -4)
          .attr('font-family', '"JetBrains Mono", monospace')
          .attr('font-size', '13px').attr('font-weight', '500')
          .attr('fill', '#d97706')
          .text(`${margin} votes`);
      } else {
        // AZ / GA: two lines centered on the line terminus
        label.append('text')
          .attr('text-anchor', anchor).attr('y', -8)
          .attr('font-family', 'Inter, sans-serif')
          .attr('font-size', '11px').attr('fill', '#9ca3af')
          .text(name);
        label.append('text')
          .attr('text-anchor', anchor).attr('y', 7)
          .attr('font-family', '"JetBrains Mono", monospace')
          .attr('font-size', '13px').attr('font-weight', '500')
          .attr('fill', '#d97706')
          .text(`${margin} votes`);
      }
    });
  }

  // ── Lifecycle ────────────────────────────────────────────────

  onMount(() => {
    boot().catch(console.error);
    return () => { if (container) container.innerHTML = ''; };
  });

  $: if (initialized) updateViz(mode);
</script>

<div class="viz-wrap" bind:this={container}>
  {#if tooltip.visible && tooltip.data}
    <div
      class="tt"
      style="left:{tooltip.x}px; top:{tooltip.y}px"
      aria-hidden="true"
    >
      <div class="tt-head">
        <span class="tt-county">{tooltip.data.county}</span>
        <span class="tt-state mono">{tooltip.data.state}</span>
      </div>

      <div class="tt-badge" class:tt-dem={tooltip.data.winner === 'dem'} class:tt-gop={tooltip.data.winner === 'gop'}>
        {tooltip.data.winner === 'dem' ? 'Biden +' : 'Trump +'}{tooltip.data.margin_pct.toFixed(1)}%
      </div>

      <div class="tt-grid">
        <span class="tt-label">Biden</span>
        <span class="tt-val mono tt-dem-num">{tooltip.data.dem.toLocaleString()}</span>
        <span class="tt-label">Trump</span>
        <span class="tt-val mono tt-gop-num">{tooltip.data.gop.toLocaleString()}</span>
        <span class="tt-label">Total</span>
        <span class="tt-val mono">{tooltip.data.total.toLocaleString()}</span>
        <span class="tt-label">Surplus</span>
        <span class="tt-val mono tt-surplus">{tooltip.data.surplus.toLocaleString()}</span>
      </div>
    </div>
  {/if}
</div>

<style>
  .viz-wrap {
    width: 100%;
    height: 100%;
    position: relative;
  }

  /* ── Tooltip ──────────────────────────────────────────────── */
  .tt {
    position: absolute;
    pointer-events: none;
    background: rgba(15, 15, 14, 0.96);
    border: 1px solid #374151;
    border-radius: 6px;
    padding: 0.75rem 1rem;
    width: 210px;
    z-index: 10;
    backdrop-filter: blur(4px);
    box-shadow: 0 4px 20px rgba(0,0,0,0.5);
  }

  .tt-head {
    display: flex;
    align-items: baseline;
    justify-content: space-between;
    gap: 0.5rem;
    margin-bottom: 0.5rem;
  }
  .tt-county {
    font-size: 0.875rem;
    font-weight: 600;
    color: #f9fafb;
    line-height: 1.3;
  }
  .tt-state {
    font-size: 0.6875rem;
    color: #6b7280;
    letter-spacing: 0.06em;
    flex-shrink: 0;
  }

  .tt-badge {
    display: inline-block;
    font-family: var(--font-mono);
    font-size: 0.6875rem;
    font-weight: 600;
    letter-spacing: 0.05em;
    padding: 0.2rem 0.5rem;
    border-radius: 3px;
    margin-bottom: 0.625rem;
  }
  .tt-dem { background: rgba(37, 99, 235, 0.2); color: #93c5fd; }
  .tt-gop { background: rgba(220, 38, 38, 0.2); color: #fca5a5; }

  .tt-grid {
    display: grid;
    grid-template-columns: auto 1fr;
    row-gap: 0.25rem;
    column-gap: 0.75rem;
    align-items: baseline;
  }
  .tt-label {
    font-size: 0.6875rem;
    color: #6b7280;
    text-transform: uppercase;
    letter-spacing: 0.06em;
  }
  .tt-val {
    font-size: 0.8125rem;
    color: #e5e7eb;
    text-align: right;
  }
  .tt-dem-num { color: #93c5fd; }
  .tt-gop-num { color: #fca5a5; }
  .tt-surplus  { color: #d97706; }
</style>
