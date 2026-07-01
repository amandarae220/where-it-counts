<script>
  import { flip } from 'svelte/animate';
  import StateMiniMap from '$lib/components/viz/StateMiniMap.svelte';
  import { SWING_STATES as STATES } from '$lib/data/swingStates.js';
  import { direction } from '$lib/stores/direction.js';

  // ── Where the map could move ────────────────────────────────────
  // Interactive: 9 swing states, two-level drill-down.
  // Level 1: states ranked by combined presidential + state-leg leverage.
  // Level 2: counties within the chosen state, ranked by leverage per mover.
  // Safe-state buffer is fixed at ±5 pts — every state currently >5pts in
  // either column stays in that column under any move shown here.
  //
  // The "what happens if you actually move people" sensitivity model
  // lives in a separate component (MoversBudget) so each tool does one
  // job cleanly.

  // ── Controls ───────────────────────────────────────────────────
  // `direction` is a shared store — see $lib/stores/direction.js.
  // Toggling here also updates MoversBudget's direction, so scrolling
  // between the two tools preserves the reader's chosen framing.
  let weightPres = 60;        // 0–100 — presidential weight in combined score
  let expandedCode = null;    // state code currently drilled into
  let countyCache = {};       // stateCode → top counties
  let hoveredFips = null;     // county fips highlighted from card hover

  // ── Scoring ────────────────────────────────────────────────────
  // Both leverage axes are normalized to 0–100 against the most-leveraged
  // state in the dataset, so the slider blends two genuinely comparable
  // scales. Without normalization, leg leverage tops out near 39 while
  // pres tops out at 100 — the slider would feel one-sided.
  const _presRaw = (s) => 100 / Math.sqrt(Math.abs(s.margin_pct) + 0.1);
  const _legRaw  = (s) => s.comp_leg / s.total_leg;
  const _maxPres = Math.max(...STATES.map(_presRaw));
  const _maxLeg  = Math.max(...STATES.map(_legRaw));

  function presLeverage(s) { return (_presRaw(s) / _maxPres) * 100; }
  function legLeverage(s)  { return (_legRaw(s)  / _maxLeg)  * 100; }

  function combinedScore(s, weightPct) {
    const w = weightPct / 100;
    return w * presLeverage(s) + (1 - w) * legLeverage(s);
  }

  // Votes needed to shift state's presidential outcome in chosen direction.
  // If state already leans that way, returns 0 (already there) — but we
  // still surface its leg leverage.
  function votesToShift(s, dir) {
    if (dir === 'D') {
      return s.margin_votes < 0 ? Math.abs(s.margin_votes) + 1 : 0;
    }
    return s.margin_votes > 0 ? s.margin_votes + 1 : 0;
  }

  function currentLean(s) {
    if (s.margin_votes > 0) return { party: 'D', label: `D +${s.margin_pct.toFixed(2)} pts` };
    return { party: 'R', label: `R +${Math.abs(s.margin_pct).toFixed(2)} pts` };
  }

  // Competitiveness labels — same vocabulary as the destination Calculator
  // (Razor thin / Competitive / Shifting) so the piece reads consistently.
  // State thresholds tuned to the 9-state dataset; county thresholds wider
  // because a 5-pt county margin is still very much in play.
  function stateTier(marginPct) {
    const m = Math.abs(marginPct);
    if (m < 1)  return { key: 'razor',       label: 'Razor thin'  };
    if (m < 3)  return { key: 'competitive', label: 'Competitive' };
    return        { key: 'shifting',    label: 'Shifting'    };
  }
  function countyTier(marginPct) {
    const m = Math.abs(marginPct);
    if (m < 2)  return { key: 'razor',       label: 'Razor thin'  };
    if (m < 8)  return { key: 'competitive', label: 'Competitive' };
    return        { key: 'shifting',    label: 'Shifting'    };
  }

  // ── Reactive: ranked list ──────────────────────────────────────
  $: ranked = [...STATES]
    .map(s => ({
      ...s,
      score: combinedScore(s, weightPres),
      shiftVotes: votesToShift(s, $direction),
      lean: currentLean(s),
      tier: stateTier(s.margin_pct),
    }))
    .sort((a, b) => b.score - a.score);

  // ── Level 2: county data on demand ─────────────────────────────
  async function loadCounties(code) {
    if (countyCache[code]) return;
    const all = await fetch('/data/counties-surplus.json').then(r => r.json());
    // Per-county leverage: large population + close margin = most votes
    // moved per new resident. Filter out anything already >25pt lean
    // (a single mover changes nothing meaningful there).
    const counties = all
      .filter(c => c.state === code)
      .filter(c => Math.abs(c.margin_pct) < 25)
      .map(c => {
        const leverage = c.total / (1 + Math.abs(c.margin_pct));
        const need = $direction === 'D'
          ? (c.winner === 'gop' ? Math.ceil(Math.abs(c.dem - c.gop) / 2) + 1 : 0)
          : (c.winner === 'dem' ? Math.ceil(Math.abs(c.dem - c.gop) / 2) + 1 : 0);
        return { ...c, leverage, need };
      })
      .sort((a, b) => b.leverage - a.leverage)
      .slice(0, 6);
    countyCache = { ...countyCache, [code]: counties };
  }

  function toggleExpand(code) {
    if (expandedCode === code) {
      expandedCode = null;
    } else {
      expandedCode = code;
      loadCounties(code);
    }
  }

  // ── Reactivity: re-compute county "need" when direction flips ──
  $: if (expandedCode && countyCache[expandedCode]) {
    countyCache[expandedCode] = countyCache[expandedCode].map(c => ({
      ...c,
      need: $direction === 'D'
        ? (c.winner === 'gop' ? Math.ceil(Math.abs(c.dem - c.gop) / 2) + 1 : 0)
        : (c.winner === 'dem' ? Math.ceil(Math.abs(c.dem - c.gop) / 2) + 1 : 0),
    }));
  }

  function fmt(n) { return n.toLocaleString(); }
</script>

<section class="map-moves" aria-labelledby="map-moves-h">

  <div class="prose">
    <p class="eyebrow mono">The interactive</p>
    <h2 id="map-moves-h">How the map could move.</h2>
    <div class="divider"></div>
    <p class="lede">
      Pick a direction. Set what stays safe. The tool ranks nine 2024
      battleground states by combined presidential and state-legislative
      leverage, then drills into the counties inside each one where a
      single move would count twice.
    </p>
  </div>

  <!-- Controls -->
  <div class="controls">
    <div class="control-group">
      <span class="control-label mono">Shift the map toward</span>
      <div class="toggle" role="radiogroup" aria-label="Direction">
        <button
          class="toggle-btn"
          class:active={$direction === 'D'}
          aria-pressed={$direction === 'D'}
          on:click={() => $direction = 'D'}
        >Democratic</button>
        <button
          class="toggle-btn"
          class:active={$direction === 'R'}
          aria-pressed={$direction === 'R'}
          on:click={() => $direction = 'R'}
        >Republican</button>
      </div>
      <p class="toggle-hint mono">
        Rankings stay the same — closeness is symmetric.
        Direction sets what the flip and sensitivity numbers mean.
      </p>
    </div>

    <div class="control-group">
      <label class="control-label mono" for="weight-slider">
        Presidential vs. state-leg weight
      </label>
      <div class="slider-row">
        <span class="slider-end">State-leg</span>
        <input
          id="weight-slider"
          type="range"
          min="0"
          max="100"
          step="5"
          bind:value={weightPres}
          aria-valuetext="{weightPres}% presidential, {100 - weightPres}% state-leg"
        />
        <span class="slider-end">Presidential</span>
      </div>
      <span class="slider-readout mono">{weightPres}% / {100 - weightPres}%</span>
    </div>

    <div class="buffer-badge">
      <span class="buffer-dot" aria-hidden="true"></span>
      <span class="buffer-text">
        Holding all states currently &gt;±5 pts in their column.
        At realistic relocation volumes, every safe state stays safe.
      </span>
    </div>
  </div>

  <!-- Level 1: state ranking -->
  <ol class="state-list" aria-label="States ranked by leverage">
    {#each ranked as s (s.code)}
      <li class="state-row" class:expanded={expandedCode === s.code} animate:flip={{ duration: 350 }}>
        <button class="state-head" on:click={() => toggleExpand(s.code)} aria-expanded={expandedCode === s.code}>
          <span class="state-rank mono">{ranked.indexOf(s) + 1}</span>

          <span class="state-id">
            <span class="state-name-row">
              <span class="state-name">{s.name}</span>
              <span class="tier-pill mono tier-{s.tier.key}">{s.tier.label}</span>
            </span>
            <span class="state-meta mono">
              <span class="lean lean-{s.lean.party}">{s.lean.label}</span>
              <span class="sep">·</span>
              <span>{s.ev} EV</span>
              <span class="sep">·</span>
              <span>{s.comp_leg} competitive leg districts</span>
            </span>
          </span>

          <span class="state-shift">
            {#if s.shiftVotes > 0}
              <span class="shift-num mono">{fmt(s.shiftVotes)}</span>
              <span class="shift-label">net votes to flip toward {$direction === 'D' ? 'D' : 'R'}</span>
            {:else}
              <span class="shift-num mono shift-already">already {$direction}</span>
              <span class="shift-label">leg districts still in play</span>
            {/if}
          </span>

          <span class="state-score" aria-label="Combined leverage score">
            <span class="score-bar" style="width: {Math.min(100, s.score)}%"></span>
            <span class="score-num mono">{Math.round(s.score)}</span>
          </span>

          <span class="state-chevron" aria-hidden="true">
            {expandedCode === s.code ? '−' : '+'}
          </span>
        </button>

        {#if expandedCode === s.code}
          <div class="state-body">
            {#if !countyCache[s.code]}
              <p class="loading mono">Loading counties…</p>
            {:else}
              <p class="drill-intro">
                Top counties in {s.name} ranked by leverage per mover —
                largest electorates × closest current margins. Hover a
                card to see where the county sits in the state. The
                "votes to flip" column shows the net shift it would need
                to swing toward {$direction === 'D' ? 'Democratic' : 'Republican'}.
              </p>
              <div class="drill-layout">
                <div class="drill-map">
                  <StateMiniMap
                    stateCode={s.code}
                    highlightFips={countyCache[s.code].map(c => c.fips)}
                    {hoveredFips}
                  />
                  <p class="drill-map-key mono">
                    <span class="key-dot" aria-hidden="true"></span>
                    Top {countyCache[s.code].length} counties by leverage
                  </p>
                </div>

                <div class="county-grid">
                  {#each countyCache[s.code] as c}
                    {@const ct = countyTier(c.margin_pct)}
                    <div
                      class="county-card"
                      class:hovered={hoveredFips === c.fips}
                      on:mouseenter={() => hoveredFips = c.fips}
                      on:mouseleave={() => hoveredFips = null}
                      on:focusin={() => hoveredFips = c.fips}
                      on:focusout={() => hoveredFips = null}
                      role="group"
                      tabindex="0"
                    >
                      <div class="county-head">
                        <span class="county-name">{c.county}</span>
                        <span class="county-lean lean-{c.winner === 'dem' ? 'D' : 'R'} mono">
                          {c.winner === 'dem' ? 'D' : 'R'} +{c.margin_pct.toFixed(1)}
                        </span>
                      </div>
                      <span class="tier-pill mono tier-{ct.key} county-tier">{ct.label}</span>
                      <div class="county-stats">
                        <div class="cstat">
                          <span class="cstat-num mono">{fmt(c.total)}</span>
                          <span class="cstat-label">2020 votes cast</span>
                        </div>
                        <div class="cstat">
                          {#if c.need > 0}
                            <span class="cstat-num mono cstat-need">{fmt(c.need)}</span>
                            <span class="cstat-label">to flip {$direction}</span>
                          {:else}
                            <span class="cstat-num mono cstat-already">already {$direction}</span>
                            <span class="cstat-label">expand the cushion</span>
                          {/if}
                        </div>
                      </div>
                    </div>
                  {/each}
                </div>
              </div>
            {/if}
          </div>
        {/if}
      </li>
    {/each}
  </ol>

  <p class="method mono">
    <span class="method-label">Method in plain English:</span>
    counties where more people voted <em>and</em> the 2020 margin was
    closer score higher — those are the places where a single mover
    changes the largest amount of political math per person. States
    are scored the same way, with a boost for how many of that state's
    legislative seats are currently competitive.
  </p>
  <p class="method mono method-formal">
    Formal: presidential leverage scaled by closeness of 2020 margin;
    state-leg leverage scaled by share of chamber seats currently within
    5 points. Combined per the weight slider above. County leverage =
    total votes cast ÷ (1 + |margin %|). Sources: MIT Election Lab ·
    OpenElections · Ballotpedia · Census 2020 reapportionment.
  </p>

</section>

<style>
  .map-moves {
    background: var(--color-bg);
    color: var(--color-text);
    padding: 7rem 1.5rem;
  }

  .eyebrow {
    font-size: 0.75rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--color-competitive);
    margin-bottom: 1rem;
  }
  .lede {
    font-size: 1.0625rem;
    color: var(--color-text-muted);
    line-height: 1.65;
    margin-top: 1.5rem;
  }

  /* ── Controls ─────────────────────────────────────────────── */
  .controls {
    max-width: var(--max-wide);
    margin: 3rem auto 2.5rem;
    display: grid;
    grid-template-columns: auto 1fr;
    gap: 2rem;
    padding: 1.75rem;
    background: #fff;
    border: 1px solid #e5e7eb;
    border-radius: 4px;
  }
  .control-group {
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
  }
  .control-label {
    font-size: 0.6875rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #6b7280;
  }

  .toggle {
    display: inline-flex;
    background: #f3f4f6;
    border-radius: 3px;
    padding: 3px;
    width: fit-content;
  }
  .toggle-btn {
    background: transparent;
    border: 0;
    font-family: var(--font-mono);
    font-size: 0.8125rem;
    letter-spacing: 0.04em;
    padding: 0.5rem 1rem;
    cursor: pointer;
    color: var(--color-text-muted);
    border-radius: 2px;
    transition: background 0.12s, color 0.12s;
  }
  .toggle-btn.active { background: #fff; color: var(--color-text); box-shadow: 0 1px 2px rgba(0,0,0,0.06); }
  .toggle-btn:focus-visible { outline: 2px solid var(--color-competitive); outline-offset: 2px; }

  .toggle-hint {
    margin: 0;
    font-size: 0.6875rem;
    color: #9ca3af;
    line-height: 1.5;
    max-width: 280px;
  }

  .slider-row {
    display: flex;
    align-items: center;
    gap: 0.75rem;
  }
  .slider-row input[type=range] {
    flex: 1;
    accent-color: var(--color-competitive);
  }

  /* Consistent slider thumb size across the piece (matches MoversBudget).
     22px thumb reads well on touch without dominating desktop. */
  input[type=range] {
    -webkit-appearance: none;
    appearance: none;
    background: transparent;
  }
  input[type=range]::-webkit-slider-runnable-track {
    height: 4px;
    background: #e5e7eb;
    border-radius: 2px;
  }
  input[type=range]::-webkit-slider-thumb {
    -webkit-appearance: none;
    appearance: none;
    width: 22px;
    height: 22px;
    border-radius: 50%;
    background: var(--color-competitive);
    border: 2px solid #fff;
    box-shadow: 0 1px 3px rgba(0,0,0,0.15);
    cursor: pointer;
    margin-top: -9px;
    transition: transform 0.12s;
  }
  input[type=range]::-webkit-slider-thumb:hover  { transform: scale(1.12); }
  input[type=range]::-webkit-slider-thumb:active { transform: scale(1.2); }
  input[type=range]::-moz-range-track {
    height: 4px;
    background: #e5e7eb;
    border-radius: 2px;
  }
  input[type=range]::-moz-range-thumb {
    width: 22px;
    height: 22px;
    border-radius: 50%;
    background: var(--color-competitive);
    border: 2px solid #fff;
    box-shadow: 0 1px 3px rgba(0,0,0,0.15);
    cursor: pointer;
  }
  @media (prefers-reduced-motion: reduce) {
    input[type=range]::-webkit-slider-thumb { transition: none; }
    input[type=range]::-webkit-slider-thumb:hover,
    input[type=range]::-webkit-slider-thumb:active { transform: none; }
  }
  .slider-end {
    font-size: 0.6875rem;
    letter-spacing: 0.06em;
    color: #9ca3af;
    text-transform: uppercase;
  }
  .slider-readout {
    font-size: 0.75rem;
    color: var(--color-text-muted);
    margin-top: 0.25rem;
  }

  .buffer-badge {
    grid-column: 1 / -1;
    display: flex;
    align-items: flex-start;
    gap: 0.625rem;
    padding-top: 1rem;
    border-top: 1px solid #f3f4f6;
  }
  .buffer-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: var(--color-competitive);
    flex-shrink: 0;
    margin-top: 0.4rem;
  }
  .buffer-text {
    font-size: 0.8125rem;
    color: var(--color-text-muted);
    line-height: 1.55;
  }

  /* ── State list ───────────────────────────────────────────── */
  .state-list {
    list-style: none;
    max-width: var(--max-wide);
    margin: 0 auto;
    padding: 0;
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
  }
  .state-row {
    background: #fff;
    border: 1px solid #e5e7eb;
    border-radius: 3px;
    overflow: hidden;
    transition: border-color 0.15s, box-shadow 0.15s;
  }
  .state-row.expanded {
    border-color: var(--color-competitive);
    box-shadow: 0 2px 8px rgba(217, 119, 6, 0.08);
  }

  .state-head {
    display: grid;
    grid-template-columns: 2rem 1fr 14rem 8rem 1.5rem;
    align-items: center;
    gap: 1.25rem;
    width: 100%;
    background: transparent;
    border: 0;
    text-align: left;
    padding: 1.125rem 1.25rem;
    cursor: pointer;
    color: inherit;
  }
  .state-head:hover { background: #fafaf8; }
  .state-head:focus-visible { outline: 2px solid var(--color-competitive); outline-offset: -2px; }

  .state-rank {
    font-size: 0.875rem;
    color: #9ca3af;
  }
  .state-name-row {
    display: flex;
    align-items: center;
    gap: 0.625rem;
    flex-wrap: wrap;
  }
  .state-name {
    font-family: var(--font-serif);
    font-size: 1.25rem;
    font-weight: 700;
    line-height: 1.2;
  }

  /* Competitiveness pills — same vocabulary + palette as Calculator */
  .tier-pill {
    font-size: 0.625rem;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    padding: 0.2em 0.55em;
    border-radius: 2px;
    font-weight: 600;
    line-height: 1.4;
    white-space: nowrap;
  }
  .tier-razor       { background: #fef3c7; color: #92400e; }
  .tier-competitive { background: #dbeafe; color: #1e40af; }
  .tier-shifting    { background: #f3f4f6; color: #4b5563; }
  .county-tier { align-self: flex-start; margin-top: -0.25rem; }
  .state-meta {
    font-size: 0.75rem;
    color: var(--color-text-muted);
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    gap: 0.5rem;
    margin-top: 0.25rem;
  }
  .sep { color: #d1d5db; }
  .lean {
    font-weight: 600;
    padding: 0.1em 0.4em;
    border-radius: 2px;
  }
  .lean-D { background: rgba(37, 99, 235, 0.08);  color: #1d4ed8; }
  .lean-R { background: rgba(220, 38, 38, 0.08);  color: #b91c1c; }

  .state-shift {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
  }
  .shift-num {
    font-size: 1.375rem;
    font-weight: 500;
    color: var(--color-text);
    line-height: 1;
    letter-spacing: -0.02em;
  }
  .shift-num.shift-already {
    font-size: 0.875rem;
    color: #9ca3af;
    font-weight: 400;
  }
  .shift-label {
    font-size: 0.6875rem;
    color: var(--color-text-muted);
    text-transform: uppercase;
    letter-spacing: 0.06em;
    margin-top: 0.25rem;
  }

  .state-score {
    position: relative;
    height: 22px;
    background: #f3f4f6;
    border-radius: 2px;
    display: flex;
    align-items: center;
    overflow: hidden;
  }
  .score-bar {
    position: absolute;
    inset: 0 auto 0 0;
    background: var(--color-competitive);
    opacity: 0.18;
    border-right: 1.5px solid var(--color-competitive);
    transition: width 0.35s cubic-bezier(0.4, 0, 0.2, 1);
  }
  @media (prefers-reduced-motion: reduce) {
    .score-bar { transition: none; }
  }
  .score-num {
    position: relative;
    font-size: 0.75rem;
    margin-left: 0.5rem;
    color: var(--color-text);
  }

  .state-chevron {
    font-family: var(--font-mono);
    font-size: 1.125rem;
    color: var(--color-competitive);
    text-align: center;
  }

  /* ── Level 2: counties ────────────────────────────────────── */
  .state-body {
    padding: 0 1.25rem 1.5rem;
    border-top: 1px solid #f3f4f6;
  }

  .loading {
    font-size: 0.8125rem;
    color: var(--color-text-muted);
    padding: 1rem 0;
  }
  .drill-intro {
    font-size: 0.875rem;
    color: var(--color-text-muted);
    line-height: 1.6;
    margin: 1rem 0 1.25rem;
    max-width: 720px;
  }
  .drill-layout {
    display: grid;
    grid-template-columns: 300px 1fr;
    gap: 1.5rem;
    align-items: start;
  }
  .drill-map {
    position: sticky;
    top: 1rem;
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
  }
  .drill-map-key {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-size: 0.6875rem;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    color: var(--color-text-muted);
    margin: 0;
  }
  .key-dot {
    width: 9px;
    height: 9px;
    border-radius: 2px;
    background: var(--color-competitive);
    opacity: 0.55;
  }

  .county-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
    gap: 0.75rem;
  }
  .county-card {
    background: #fafaf8;
    border: 1px solid #e5e7eb;
    border-radius: 3px;
    padding: 0.875rem 1rem;
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
    cursor: default;
    transition: border-color 0.15s, background 0.15s, transform 0.15s;
  }
  .county-card:hover,
  .county-card.hovered,
  .county-card:focus-within {
    border-color: var(--color-competitive);
    background: #fff;
    transform: translateY(-1px);
  }
  .county-card:focus-visible {
    outline: 2px solid var(--color-competitive);
    outline-offset: 2px;
  }
  .county-head {
    display: flex;
    align-items: baseline;
    justify-content: space-between;
    gap: 0.5rem;
  }
  .county-name {
    font-size: 0.9375rem;
    font-weight: 600;
    color: var(--color-text);
    line-height: 1.25;
  }
  .county-lean {
    font-size: 0.6875rem;
    padding: 0.15em 0.5em;
    border-radius: 2px;
    flex-shrink: 0;
  }
  .county-stats {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 0.5rem;
    border-top: 1px solid #ececec;
    padding-top: 0.625rem;
  }
  .cstat { display: flex; flex-direction: column; }
  .cstat-num {
    font-size: 1.0625rem;
    color: var(--color-text);
    line-height: 1;
  }
  .cstat-need { color: var(--color-competitive); }
  .cstat-already { font-size: 0.75rem; color: #9ca3af; }
  .cstat-label {
    font-size: 0.625rem;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: var(--color-text-muted);
    margin-top: 0.25rem;
  }

  /* ── Method footnote ──────────────────────────────────────── */
  .method {
    max-width: var(--max-wide);
    margin: 2rem auto 0;
    font-size: 0.8125rem;
    color: var(--color-text-muted);
    line-height: 1.65;
  }
  .method-label {
    font-weight: 600;
    color: var(--color-text);
    letter-spacing: 0.02em;
  }
  .method em { font-style: italic; color: var(--color-text); font-weight: 500; }
  .method-formal {
    font-size: 0.75rem;
    color: #9ca3af;
    margin-top: 0.5rem;
    padding-top: 1rem;
    border-top: 1px solid #f3f4f6;
  }

  /* ── Mobile ───────────────────────────────────────────────── */
  @media (max-width: 820px) {
    .map-moves { padding: 4rem 1rem; }
    .controls { grid-template-columns: 1fr; gap: 1.5rem; padding: 1.25rem; }
    .drill-layout { grid-template-columns: 1fr; gap: 1rem; }
    .drill-map { position: static; max-width: 360px; margin: 0 auto; }
    .state-head {
      grid-template-columns: 1.5rem 1fr 1.25rem;
      grid-template-areas:
        "rank  name    chev"
        ".     shift   shift"
        ".     score   score";
      row-gap: 0.625rem;
      padding: 1rem;
    }
    .state-rank { grid-area: rank; }
    .state-id { grid-area: name; }
    .state-shift { grid-area: shift; flex-direction: row; align-items: baseline; gap: 0.5rem; }
    .shift-label { margin-top: 0; }
    .state-score { grid-area: score; }
    .state-chevron { grid-area: chev; }
  }
</style>
