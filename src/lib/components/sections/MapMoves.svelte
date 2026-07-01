<script>
  import { flip } from 'svelte/animate';
  import StateMiniMap from '$lib/components/viz/StateMiniMap.svelte';

  // ── Where the map could move ────────────────────────────────────
  // Interactive: 9 swing states, two-level drill-down.
  // Level 1: states ranked by combined presidential + state-leg leverage.
  // Level 2: counties within the chosen state, ranked by leverage per mover.
  // Safe-state buffer is fixed at ±5 pts — every state currently >5pts in
  // either column stays in that column under any move shown here.

  // ── Curated state dataset ──────────────────────────────────────
  // Sources: MIT Election Lab (2020 pres) · Ballotpedia + OpenElections
  // (state-leg margins) · Census 2020 reapportionment (EV counts in effect
  // from 2024 onward — the relevant cycle for any move planned before 2031).
  // margin_votes: positive = Dem won by this many; negative = GOP won.
  const STATES = [
    { code: 'GA', name: 'Georgia',        ev: 16, margin_votes:   11779, margin_pct:  0.24, comp_leg: 9,  total_leg: 236 },
    { code: 'AZ', name: 'Arizona',        ev: 11, margin_votes:   10457, margin_pct:  0.31, comp_leg: 7,  total_leg:  90 },
    { code: 'WI', name: 'Wisconsin',      ev: 10, margin_votes:   20682, margin_pct:  0.63, comp_leg: 10, total_leg: 132 },
    { code: 'PA', name: 'Pennsylvania',   ev: 19, margin_votes:   80555, margin_pct:  1.17, comp_leg: 12, total_leg: 253 },
    { code: 'MI', name: 'Michigan',       ev: 15, margin_votes:  154188, margin_pct:  2.78, comp_leg: 8,  total_leg: 148 },
    { code: 'NC', name: 'North Carolina', ev: 16, margin_votes:  -74481, margin_pct: -1.34, comp_leg: 6,  total_leg: 170 },
    { code: 'NV', name: 'Nevada',         ev:  6, margin_votes:   33596, margin_pct:  2.39, comp_leg: 4,  total_leg:  63 },
    { code: 'FL', name: 'Florida',        ev: 30, margin_votes: -371686, margin_pct: -3.36, comp_leg: 8,  total_leg: 160 },
    { code: 'TX', name: 'Texas',          ev: 40, margin_votes: -631221, margin_pct: -5.58, comp_leg: 14, total_leg: 181 },
  ];

  // ── Controls ───────────────────────────────────────────────────
  let direction = 'D';        // 'D' = shift toward Democratic, 'R' = toward Republican
  let weightPres = 60;        // 0–100 — presidential weight in combined score
  let expandedCode = null;    // state code currently drilled into
  let countyCache = {};       // stateCode → top counties
  let hoveredFips = null;     // county fips highlighted from card hover
  let shifts = {};            // stateCode → thousands of net-new movers (sensitivity slider)

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

  // ── Sensitivity model ──────────────────────────────────────────
  // Simulate N thousand net-new movers into a state, toward the
  // chosen direction. Preserves the state's vote-to-pct ratio from
  // the 2020 baseline; drifts slightly at extreme shifts because the
  // new voters change the electorate size, acceptable at MVP scale.
  function simulate(s, dir, shiftK) {
    const shiftVotes = shiftK * 1000;
    const netChange = dir === 'D' ? shiftVotes : -shiftVotes;
    const newMargin = s.margin_votes + netChange;
    const pctPerVote = s.margin_pct / s.margin_votes;
    const newPct = newMargin * pctPerVote;
    return {
      newMargin,
      newPct,
      newTier: stateTier(newPct),
      newParty: newPct > 0 ? 'D' : 'R',
      flipped: Math.sign(newMargin) !== Math.sign(s.margin_votes),
    };
  }
  // Slider max: 2× the state's current margin, capped at 500K movers
  // (a realistic upper bound for a 4-year civic relocation campaign),
  // floored at 20K so even razor-thin states have slider granularity.
  function shiftMax(s) {
    return Math.max(20, Math.min(500, Math.ceil(Math.abs(s.margin_votes) * 2 / 1000)));
  }

  // ── Reactive: ranked list ──────────────────────────────────────
  $: ranked = [...STATES]
    .map(s => ({
      ...s,
      score: combinedScore(s, weightPres),
      shiftVotes: votesToShift(s, direction),
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
        const need = direction === 'D'
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
      if (shifts[code] === undefined) shifts[code] = 0;
      loadCounties(code);
    }
  }

  // ── Reactivity: re-compute county "need" when direction flips ──
  $: if (expandedCode && countyCache[expandedCode]) {
    countyCache[expandedCode] = countyCache[expandedCode].map(c => ({
      ...c,
      need: direction === 'D'
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
          class:active={direction === 'D'}
          aria-pressed={direction === 'D'}
          on:click={() => direction = 'D'}
        >Democratic</button>
        <button
          class="toggle-btn"
          class:active={direction === 'R'}
          aria-pressed={direction === 'R'}
          on:click={() => direction = 'R'}
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
              <span class="shift-label">net votes to flip toward {direction === 'D' ? 'D' : 'R'}</span>
            {:else}
              <span class="shift-num mono shift-already">already {direction}</span>
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
              {@const shiftK = shifts[s.code] || 0}
              {@const sim = simulate(s, direction, shiftK)}
              {@const smax = shiftMax(s)}
              {@const axisMin = -8}
              {@const axisMax = 8}
              {@const axisPos = (pct) => Math.max(0, Math.min(100, ((pct - axisMin) / (axisMax - axisMin)) * 100))}
              {@const baselinePos = axisPos(s.margin_pct)}
              {@const projPos = axisPos(sim.newPct)}
              {@const projOffscale = sim.newPct < axisMin || sim.newPct > axisMax}

              <!-- Sensitivity panel — model the piece's own remedy -->
              <div class="sim-panel" aria-label="Relocation sensitivity for {s.name}">
                <div class="sim-header">
                  <span class="mono sim-label">What if</span>
                  <span class="sim-subtitle">
                    Simulate net-new movers into {s.name} voting
                    <span class="sim-dir">{direction === 'D' ? 'Democratic' : 'Republican'}</span>.
                    Watch how the margin shifts.
                  </span>
                </div>

                <!-- Live margin axis — visible proof the tool is reactive -->
                <div class="sim-axis" aria-hidden="true">
                  <div class="axis-labels-top mono">
                    <span>Republican</span>
                    <span>Tied</span>
                    <span>Democratic</span>
                  </div>
                  <div class="axis-track">
                    <div class="axis-half axis-r"></div>
                    <div class="axis-half axis-d"></div>
                    <div class="axis-center"></div>
                    <div class="axis-marker axis-baseline" style="left: {baselinePos}%">
                      <span class="marker-dot"></span>
                      <span class="marker-tag mono">2020</span>
                    </div>
                    <div class="axis-marker axis-projected" class:offscale={projOffscale} style="left: {projPos}%">
                      <span class="marker-dot proj"></span>
                      <span class="marker-label mono">
                        {sim.newParty}+{Math.abs(sim.newPct).toFixed(1)}
                      </span>
                    </div>
                  </div>
                  <div class="axis-scale mono">
                    <span>R+8</span>
                    <span>R+4</span>
                    <span>0</span>
                    <span>D+4</span>
                    <span>D+8</span>
                  </div>
                </div>

                <div class="sim-slider-wrap">
                  <input
                    type="range"
                    min="0"
                    max={smax}
                    step="1"
                    bind:value={shifts[s.code]}
                    class="sim-slider"
                    aria-valuetext="{fmt(shiftK * 1000)} movers"
                  />
                  <div class="sim-scale mono">
                    <span>0</span>
                    <span class="sim-current">{fmt(shiftK * 1000)} movers</span>
                    <span>{fmt(smax * 1000)}</span>
                  </div>
                </div>

                <div class="sim-readout">
                  <div class="sim-col">
                    <span class="sim-col-label mono">2020 result</span>
                    <span class="sim-value lean-{s.lean.party} mono">{s.lean.label}</span>
                    <span class="tier-pill mono tier-{s.tier.key}">{s.tier.label}</span>
                  </div>
                  <div class="sim-arrow mono" aria-hidden="true">→</div>
                  <div class="sim-col">
                    <span class="sim-col-label mono">Projected</span>
                    <span class="sim-value lean-{sim.newParty} mono">
                      {sim.newParty} +{Math.abs(sim.newPct).toFixed(2)} pts
                    </span>
                    <span class="tier-pill mono tier-{sim.newTier.key}">{sim.newTier.label}</span>
                  </div>
                </div>

                {#if sim.flipped}
                  <div class="sim-flipped mono" role="status">
                    ✓ Flipped — {s.name} projects to {sim.newParty === 'D' ? 'Democratic' : 'Republican'}
                  </div>
                {/if}
              </div>

              <p class="drill-intro">
                Top counties in {s.name} ranked by leverage per mover —
                largest electorates × closest current margins. Hover a
                card to see where the county sits in the state. The
                "votes to flip" column shows the net shift it would need
                to swing toward {direction === 'D' ? 'Democratic' : 'Republican'}.
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
                            <span class="cstat-label">to flip {direction}</span>
                          {:else}
                            <span class="cstat-num mono cstat-already">already {direction}</span>
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

  /* ── Sensitivity panel ────────────────────────────────────── */
  .sim-panel {
    background: #fff;
    border: 2px solid var(--color-competitive);
    border-radius: 3px;
    padding: 1.5rem;
    margin: 1.25rem 0 1.75rem;
  }
  .sim-header {
    display: flex;
    align-items: baseline;
    gap: 0.75rem;
    flex-wrap: wrap;
    margin-bottom: 1.25rem;
  }
  .sim-label {
    font-size: 0.6875rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--color-competitive);
    font-weight: 600;
    flex-shrink: 0;
  }
  .sim-subtitle {
    font-size: 0.9375rem;
    color: var(--color-text-muted);
    line-height: 1.55;
  }
  .sim-dir { font-weight: 600; color: var(--color-text); }

  /* ── Live margin axis ─────────────────────────────────────── */
  .sim-axis {
    margin: 0 0 2rem;
    padding: 2rem 0.5rem 0;
  }
  .axis-labels-top {
    display: flex;
    justify-content: space-between;
    font-size: 0.625rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: var(--color-text-muted);
    margin-bottom: 0.625rem;
  }
  .axis-labels-top span:first-child { color: #b91c1c; }
  .axis-labels-top span:last-child  { color: #1d4ed8; }
  .axis-track {
    position: relative;
    height: 42px;
    display: flex;
    border-radius: 3px;
    overflow: visible;
  }
  .axis-half {
    flex: 1;
    height: 100%;
  }
  .axis-r {
    background: linear-gradient(to left, rgba(220, 38, 38, 0.06), rgba(220, 38, 38, 0.22));
    border-radius: 3px 0 0 3px;
  }
  .axis-d {
    background: linear-gradient(to right, rgba(37, 99, 235, 0.06), rgba(37, 99, 235, 0.22));
    border-radius: 0 3px 3px 0;
  }
  .axis-center {
    position: absolute;
    left: 50%;
    top: -4px;
    bottom: -4px;
    width: 1px;
    background: #4b5563;
    transform: translateX(-0.5px);
  }

  .axis-marker {
    position: absolute;
    top: 50%;
    transform: translate(-50%, -50%);
    display: flex;
    flex-direction: column;
    align-items: center;
  }
  .axis-baseline { z-index: 1; }
  .axis-projected {
    z-index: 2;
    transition: left 0.32s cubic-bezier(0.4, 0, 0.2, 1);
  }
  @media (prefers-reduced-motion: reduce) {
    .axis-projected { transition: none; }
  }
  .marker-dot {
    width: 12px;
    height: 12px;
    border-radius: 50%;
    background: #6b7280;
    border: 2px solid #fff;
    box-shadow: 0 1px 3px rgba(0,0,0,0.25);
  }
  .marker-dot.proj {
    background: var(--color-competitive);
    width: 15px;
    height: 15px;
    animation: sim-pulse 2.6s ease-in-out infinite;
  }
  @keyframes sim-pulse {
    0%, 100% { box-shadow: 0 0 0 0 rgba(217, 119, 6, 0.45), 0 1px 3px rgba(0,0,0,0.25); }
    50%      { box-shadow: 0 0 0 10px rgba(217, 119, 6, 0), 0 1px 3px rgba(0,0,0,0.25); }
  }
  .marker-tag {
    position: absolute;
    top: 1.25rem;
    font-size: 0.625rem;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #6b7280;
  }
  .marker-label {
    position: absolute;
    bottom: 1.25rem;
    font-size: 0.75rem;
    color: var(--color-text);
    background: #fff;
    padding: 0.15em 0.5em;
    border-radius: 2px;
    border: 1.5px solid var(--color-competitive);
    white-space: nowrap;
    font-weight: 600;
  }
  .axis-projected.offscale .marker-label::after {
    content: ' →';
    color: var(--color-competitive);
  }
  .axis-scale {
    display: flex;
    justify-content: space-between;
    margin-top: 0.75rem;
    font-size: 0.625rem;
    color: #9ca3af;
  }

  .sim-slider-wrap { margin-bottom: 1.25rem; }
  .sim-slider {
    width: 100%;
    accent-color: var(--color-competitive);
    height: 4px;
  }
  .sim-scale {
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 0.6875rem;
    color: #9ca3af;
    margin-top: 0.625rem;
  }
  .sim-current {
    color: var(--color-text);
    font-size: 0.9375rem;
    font-weight: 500;
    padding: 0.15em 0.6em;
    background: rgba(217, 119, 6, 0.08);
    border-radius: 2px;
  }

  .sim-readout {
    display: grid;
    grid-template-columns: 1fr auto 1fr;
    align-items: center;
    gap: 1.25rem;
    padding: 1.125rem 1.25rem;
    background: #fafaf8;
    border-radius: 3px;
  }
  .sim-col {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
    align-items: flex-start;
  }
  .sim-col-label {
    font-size: 0.625rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: var(--color-text-muted);
  }
  .sim-value {
    display: inline-block;
    font-size: 1.125rem;
    font-weight: 500;
    padding: 0.25em 0.55em;
    border-radius: 2px;
    letter-spacing: -0.01em;
    transition: background 0.2s, color 0.2s;
  }
  .sim-value.lean-D { background: rgba(37, 99, 235, 0.1);  color: #1d4ed8; }
  .sim-value.lean-R { background: rgba(220, 38, 38, 0.1);  color: #b91c1c; }

  .sim-arrow {
    font-size: 1.5rem;
    color: var(--color-competitive);
    align-self: center;
  }
  .sim-flipped {
    margin-top: 1rem;
    padding: 0.75rem 1rem;
    background: #ecfdf5;
    color: #047857;
    border: 1px solid #a7f3d0;
    border-radius: 3px;
    font-size: 0.875rem;
    letter-spacing: 0.02em;
    text-align: center;
    font-weight: 600;
  }

  @media (max-width: 620px) {
    .sim-readout {
      grid-template-columns: 1fr;
      gap: 0.875rem;
    }
    .sim-arrow {
      transform: rotate(90deg);
      justify-self: center;
    }
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
