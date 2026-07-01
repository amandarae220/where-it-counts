<script>
  // ── The Movers Budget ─────────────────────────────────────────
  // Allocate a slice of America's annual interstate migration flow
  // across nine battleground states. Watch the electoral college and
  // per-state margins shift live.
  //
  // Anchor 1 (Census ACS): every budget figure the user picks is
  // expressed as a percentage of the ~8M Americans who already move
  // between states each year. No aspirational numbers.
  import {
    SWING_STATES,
    BASELINE_D_EV,
    BASELINE_R_EV,
    REFERENCES,
  } from '$lib/data/swingStates.js';

  // ── Controls ───────────────────────────────────────────────────
  let budgetPct = 5;        // % of US annual interstate flow
  let direction = 'D';      // 'D' or 'R'
  let allocations = {};     // stateCode → absolute movers assigned

  // ── Derived: budget + meter math ───────────────────────────────
  $: budget = Math.round(REFERENCES.annualInterstate.value * budgetPct / 100);
  $: allocatedTotal = SWING_STATES.reduce(
    (sum, s) => sum + (allocations[s.code] || 0), 0
  );
  $: overBudget = allocatedTotal > budget;
  $: budgetUsePct = budget === 0 ? 0 : Math.min(100, Math.round((allocatedTotal / budget) * 100));

  // ── Simulation model ───────────────────────────────────────────
  // Same math the (now-removed) MapMoves sensitivity panel used:
  // shift margin_votes by movers in the chosen direction, then
  // recompute margin_pct proportionally.
  function simulate(state, dir, movers) {
    const netChange = dir === 'D' ? movers : -movers;
    const newMargin = state.margin_votes + netChange;
    const pctPerVote = state.margin_pct / state.margin_votes;
    const newPct = newMargin * pctPerVote;
    const newParty = newMargin > 0 ? 'D' : 'R';
    const origParty = state.margin_votes > 0 ? 'D' : 'R';
    return {
      newMargin,
      newPct,
      newParty,
      origParty,
      flipped: newParty !== origParty,
    };
  }
  function stateTier(pct) {
    const m = Math.abs(pct);
    if (m < 1)  return { key: 'razor',       label: 'Razor thin'  };
    if (m < 3)  return { key: 'competitive', label: 'Competitive' };
    return        { key: 'shifting',    label: 'Shifting'    };
  }

  // ── Derived: per-state results + aggregate EC ──────────────────
  $: simResults = SWING_STATES.map(s => ({
    ...s,
    movers: allocations[s.code] || 0,
    ...simulate(s, direction, allocations[s.code] || 0),
  }));
  $: flippedStates = simResults.filter(r => r.flipped);
  $: ecShift = flippedStates.reduce((acc, r) => {
    return r.newParty === 'D' ? acc + r.ev : acc - r.ev;
  }, 0);
  $: newD = BASELINE_D_EV + ecShift;
  $: newR = BASELINE_R_EV - ecShift;
  $: moversForFlippedStates = flippedStates.reduce((sum, r) => sum + r.movers, 0);
  $: efficiency = ecShift !== 0
    ? Math.round(moversForFlippedStates / Math.abs(ecShift))
    : null;

  // Slider step scales with budget so granularity feels right at both ends.
  $: sliderStep = budget < 100_000 ? 1000 : budget < 500_000 ? 5000 : 10_000;
  $: perStateMax = budget;

  // ── Anchor context strings ─────────────────────────────────────
  $: budgetInKatrinas = (budget / REFERENCES.katrinaHouston.value).toFixed(1);
  $: budgetVsSwingMargin = (budget / REFERENCES.swingMargin2020.value).toFixed(1);

  // ── Format helpers ─────────────────────────────────────────────
  const fmt = (n) => n.toLocaleString();

  function resetAll() { allocations = {}; }
</script>

<section class="movers-budget" aria-labelledby="mb-title">

  <div class="prose">
    <p class="eyebrow mono">The what-if</p>
    <h2 id="mb-title">If people moved strategically.</h2>
    <div class="divider"></div>
    <p class="lede">
      About <strong>8 million Americans</strong> move between states
      every year (Census ACS 2022). Redirect a slice of that flow —
      toward one direction, across the nine battleground states — and
      watch what changes. Every number below is a fraction of what
      already happens.
    </p>
  </div>

  <!-- ── Budget + direction controls ─────────────────────────── -->
  <div class="controls">
    <div class="ctrl-block ctrl-budget">
      <span class="ctrl-label mono">Total budget</span>
      <div class="budget-value">
        <span class="budget-num mono">{fmt(budget)}</span>
        <span class="budget-unit mono">relocations</span>
      </div>
      <input
        type="range"
        min="0.5"
        max="25"
        step="0.5"
        bind:value={budgetPct}
        class="budget-slider"
        aria-label="Percentage of US annual interstate movement to allocate"
      />
      <div class="budget-scale mono">
        <span>0.5%</span>
        <span class="budget-scale-current">{budgetPct}% of US annual interstate flow (8M)</span>
        <span>25%</span>
      </div>
      <ul class="budget-anchors mono">
        <li>
          <span class="anchor-num">{budgetInKatrinas}×</span>
          Katrina's Houston displacement (~250K, 2005)
        </li>
        <li>
          <span class="anchor-num">{budgetVsSwingMargin}×</span>
          the combined 2020 margin that decided GA + AZ + WI (43K)
        </li>
      </ul>
    </div>

    <div class="ctrl-block ctrl-direction">
      <span class="ctrl-label mono">Direction</span>
      <div class="toggle" role="radiogroup" aria-label="Allocation direction">
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
        Every mover you allocate is a net-new vote for the direction
        selected above.
      </p>
    </div>
  </div>

  <!-- ── Budget meter ────────────────────────────────────────── -->
  <div class="meter" class:over={overBudget}>
    <div class="meter-header">
      <span class="mono meter-label">Allocated</span>
      <span class="mono meter-count">
        {fmt(allocatedTotal)} of {fmt(budget)}
        <span class="meter-pct">({budgetUsePct}%)</span>
      </span>
      <button
        type="button"
        class="reset-btn mono"
        on:click={resetAll}
        disabled={allocatedTotal === 0}
      >Reset all</button>
    </div>
    <div class="meter-bar-wrap" aria-hidden="true">
      <div class="meter-bar" style="width: {budgetUsePct}%"></div>
    </div>
    {#if overBudget}
      <p class="meter-warning mono" role="alert">
        Over budget by {fmt(allocatedTotal - budget)}.
        Reduce a slider or expand the budget above.
      </p>
    {/if}
  </div>

  <!-- ── State allocation grid ───────────────────────────────── -->
  <div class="state-grid">
    {#each simResults as r (r.code)}
      {@const tierNow  = stateTier(r.margin_pct)}
      {@const tierProj = stateTier(r.newPct)}
      <div class="alloc-card" class:flipped={r.flipped}>
        <div class="alloc-head">
          <div class="alloc-title">
            <span class="alloc-name">{r.name}</span>
            <span class="alloc-ev mono">{r.ev} EV</span>
          </div>
          <div class="alloc-current mono">
            Now:
            <span class="lean-{r.origParty}">
              {r.origParty}&thinsp;+{Math.abs(r.margin_pct).toFixed(2)}
            </span>
            <span class="tier-pill mono tier-{tierNow.key}">{tierNow.label}</span>
          </div>
        </div>

        <div class="alloc-slider-wrap">
          <label class="mono alloc-slider-label" for="alloc-{r.code}">
            <span class="alloc-slider-num">{fmt(r.movers)}</span>
            <span class="alloc-slider-sub">movers to {r.name}</span>
          </label>
          <input
            id="alloc-{r.code}"
            type="range"
            min="0"
            max={perStateMax}
            step={sliderStep}
            value={r.movers}
            on:input={(e) => allocations[r.code] = +e.target.value}
            class="alloc-slider"
            aria-valuetext="{fmt(r.movers)} movers to {r.name}"
          />
        </div>

        <div class="alloc-projected">
          <span class="alloc-arrow mono" aria-hidden="true">→</span>
          <span class="alloc-result lean-{r.newParty} mono">
            {r.newParty}&thinsp;+{Math.abs(r.newPct).toFixed(2)}
          </span>
          <span class="tier-pill mono tier-{tierProj.key}">{tierProj.label}</span>
          {#if r.flipped}
            <span class="alloc-flipped mono">Flipped</span>
          {/if}
        </div>
      </div>
    {/each}
  </div>

  <!-- ── Impact panel ────────────────────────────────────────── -->
  <div class="impact">
    <h3 class="impact-title">Your allocation, aggregated</h3>

    <div class="impact-grid">
      <div class="impact-block impact-ec">
        <span class="impact-label mono">Electoral College</span>
        <div class="ec-row">
          <div class="ec-side">
            <span class="ec-num mono lean-D">{newD}</span>
            <span class="ec-delta mono">
              {ecShift > 0 ? `+${ecShift}` : ecShift === 0 ? '±0' : ecShift} vs. baseline
            </span>
          </div>
          <span class="ec-vs mono" aria-hidden="true">vs</span>
          <div class="ec-side">
            <span class="ec-num mono lean-R">{newR}</span>
            <span class="ec-delta mono">
              {-ecShift > 0 ? `+${-ecShift}` : -ecShift === 0 ? '±0' : -ecShift} vs. baseline
            </span>
          </div>
        </div>
        <p class="ec-baseline mono">
          Baseline: 2020 result with post-2020 EV apportionment
          (D&thinsp;{BASELINE_D_EV} · R&thinsp;{BASELINE_R_EV})
        </p>
      </div>

      <div class="impact-block impact-flips">
        <span class="impact-label mono">States flipped</span>
        <div class="flip-count mono">{flippedStates.length}</div>
        {#if flippedStates.length > 0}
          <div class="flip-chips">
            {#each flippedStates as f}
              <span class="flip-chip lean-{f.newParty} mono">
                {f.code} → {f.newParty}
              </span>
            {/each}
          </div>
        {:else}
          <p class="flip-none mono">
            No states have flipped yet. Try pushing a slider above the
            state's current margin.
          </p>
        {/if}
      </div>

      <div class="impact-block impact-efficiency">
        <span class="impact-label mono">Movers per EC vote gained</span>
        {#if efficiency !== null}
          <div class="eff-num mono">{fmt(efficiency)}</div>
          <p class="eff-desc mono">
            averaged across the states that flipped
          </p>
        {:else}
          <div class="eff-num mono eff-idle">—</div>
          <p class="eff-desc mono">no flips yet</p>
        {/if}
      </div>
    </div>
  </div>

  <p class="method mono">
    <span class="method-label">Method:</span>
    state margins shift proportionally to movers allocated, and tiers
    re-classify per the piece's standard thresholds (Razor thin under
    1&thinsp;pt, Competitive 1–3&thinsp;pts, Shifting above 3). Baseline
    EC is the 2020 presidential result recomputed under post-2020 census
    apportionment (applies from 2024). Only the nine battleground states
    are modeled — the other 41 hold their 2020 outcomes.
    <span class="method-label">Sources:</span>
    MIT Election Lab · US Census ACS 2022 (interstate migration) ·
    US Census / HUD 2005 (Katrina reference).
  </p>

</section>

<style>
  .movers-budget {
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
  .lede strong { color: var(--color-text); font-weight: 600; }

  /* ── Controls ─────────────────────────────────────────────── */
  .controls {
    max-width: var(--max-wide);
    margin: 3rem auto 2rem;
    display: grid;
    grid-template-columns: 2fr 1fr;
    gap: 2rem;
    padding: 1.75rem;
    background: #fff;
    border: 1px solid #e5e7eb;
    border-radius: 4px;
  }
  .ctrl-block { display: flex; flex-direction: column; gap: 0.75rem; }
  .ctrl-label {
    font-size: 0.6875rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #6b7280;
  }

  .budget-value {
    display: flex;
    align-items: baseline;
    gap: 0.5rem;
    margin: 0.25rem 0 0.5rem;
  }
  .budget-num {
    font-size: clamp(1.75rem, 4vw, 2.5rem);
    font-weight: 500;
    color: var(--color-text);
    letter-spacing: -0.02em;
    line-height: 1;
  }
  .budget-unit {
    font-size: 0.75rem;
    color: var(--color-text-muted);
    letter-spacing: 0.05em;
    text-transform: uppercase;
  }
  .budget-slider {
    width: 100%;
    accent-color: var(--color-competitive);
    height: 4px;
  }
  .budget-scale {
    display: flex;
    justify-content: space-between;
    font-size: 0.6875rem;
    color: #9ca3af;
  }
  .budget-scale-current {
    color: var(--color-text);
    font-weight: 500;
    padding: 0.1em 0.5em;
    background: rgba(217, 119, 6, 0.08);
    border-radius: 2px;
  }
  .budget-anchors {
    list-style: none;
    padding: 0.75rem 0 0;
    margin: 0.5rem 0 0;
    border-top: 1px dashed #e5e7eb;
    display: flex;
    flex-direction: column;
    gap: 0.375rem;
    font-size: 0.75rem;
    color: var(--color-text-muted);
  }
  .anchor-num {
    color: var(--color-competitive);
    font-weight: 600;
    margin-right: 0.35em;
  }

  /* Direction toggle — matches MapMoves */
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
  .toggle-btn.active {
    background: #fff;
    color: var(--color-text);
    box-shadow: 0 1px 2px rgba(0,0,0,0.06);
  }
  .toggle-btn:focus-visible {
    outline: 2px solid var(--color-competitive);
    outline-offset: 2px;
  }
  .toggle-hint {
    margin: 0;
    font-size: 0.6875rem;
    color: #9ca3af;
    line-height: 1.5;
  }

  /* ── Budget meter ─────────────────────────────────────────── */
  .meter {
    max-width: var(--max-wide);
    margin: 0 auto 2rem;
    padding: 1rem 1.25rem;
    background: #fafaf8;
    border-radius: 3px;
    border: 1px solid #e5e7eb;
    transition: border-color 0.2s, background 0.2s;
  }
  .meter.over {
    border-color: #dc2626;
    background: #fef2f2;
  }
  .meter-header {
    display: flex;
    align-items: center;
    gap: 1rem;
    flex-wrap: wrap;
  }
  .meter-label {
    font-size: 0.6875rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #6b7280;
    flex-shrink: 0;
  }
  .meter-count {
    font-size: 0.9375rem;
    color: var(--color-text);
    flex: 1;
  }
  .meter-pct { color: var(--color-text-muted); }
  .reset-btn {
    background: transparent;
    border: 1px solid #d1d5db;
    font-family: var(--font-mono);
    font-size: 0.6875rem;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    color: var(--color-text-muted);
    padding: 0.4rem 0.75rem;
    border-radius: 2px;
    cursor: pointer;
    transition: color 0.15s, border-color 0.15s;
  }
  .reset-btn:hover:not(:disabled) {
    color: var(--color-text);
    border-color: #9ca3af;
  }
  .reset-btn:disabled { opacity: 0.4; cursor: not-allowed; }
  .reset-btn:focus-visible {
    outline: 2px solid var(--color-competitive);
    outline-offset: 2px;
  }
  .meter-bar-wrap {
    height: 8px;
    background: #e5e7eb;
    border-radius: 4px;
    overflow: hidden;
    margin-top: 0.625rem;
  }
  .meter-bar {
    height: 100%;
    background: var(--color-competitive);
    border-radius: 4px;
    transition: width 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  }
  .meter.over .meter-bar { background: #dc2626; }
  .meter-warning {
    margin: 0.75rem 0 0;
    padding: 0.5rem 0.75rem;
    background: rgba(220, 38, 38, 0.08);
    border-radius: 2px;
    font-size: 0.75rem;
    color: #b91c1c;
  }
  @media (prefers-reduced-motion: reduce) {
    .meter-bar { transition: none; }
  }

  /* ── State grid ───────────────────────────────────────────── */
  .state-grid {
    max-width: var(--max-wide);
    margin: 0 auto 3rem;
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1rem;
  }
  .alloc-card {
    padding: 1.125rem 1.25rem;
    background: #fff;
    border: 1px solid #e5e7eb;
    border-radius: 3px;
    display: flex;
    flex-direction: column;
    gap: 1rem;
    transition: border-color 0.2s, box-shadow 0.2s;
  }
  .alloc-card.flipped {
    border-color: var(--color-competitive);
    box-shadow: 0 2px 8px rgba(217, 119, 6, 0.15);
  }
  .alloc-title {
    display: flex;
    align-items: baseline;
    justify-content: space-between;
    gap: 0.5rem;
  }
  .alloc-name {
    font-family: var(--font-serif);
    font-size: 1.125rem;
    font-weight: 700;
    line-height: 1.15;
  }
  .alloc-ev {
    font-size: 0.6875rem;
    letter-spacing: 0.05em;
    color: var(--color-text-muted);
  }
  .alloc-current {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-size: 0.75rem;
    color: var(--color-text-muted);
    margin-top: 0.375rem;
    flex-wrap: wrap;
  }

  .lean-D { color: #1d4ed8; }
  .lean-R { color: #b91c1c; }

  /* Tier pills — same palette as Calculator + MapMoves */
  .tier-pill {
    font-size: 0.625rem;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    padding: 0.15em 0.4em;
    border-radius: 2px;
    font-weight: 600;
    white-space: nowrap;
  }
  .tier-razor       { background: #fef3c7; color: #92400e; }
  .tier-competitive { background: #dbeafe; color: #1e40af; }
  .tier-shifting    { background: #f3f4f6; color: #4b5563; }

  .alloc-slider-wrap { display: flex; flex-direction: column; gap: 0.5rem; }
  .alloc-slider-label {
    font-size: 0.8125rem;
    color: var(--color-text);
    display: flex;
    align-items: baseline;
    gap: 0.4rem;
  }
  .alloc-slider-num { font-weight: 500; font-size: 1rem; }
  .alloc-slider-sub {
    font-size: 0.6875rem;
    color: var(--color-text-muted);
    letter-spacing: 0.02em;
  }
  .alloc-slider {
    width: 100%;
    accent-color: var(--color-competitive);
    height: 4px;
  }

  .alloc-projected {
    display: flex;
    align-items: center;
    flex-wrap: wrap;
    gap: 0.5rem;
    padding-top: 0.75rem;
    border-top: 1px solid #f3f4f6;
    font-size: 0.9375rem;
  }
  .alloc-arrow { color: var(--color-competitive); font-size: 1rem; }
  .alloc-result { font-weight: 500; }
  .alloc-flipped {
    color: #047857;
    background: #ecfdf5;
    padding: 0.15em 0.5em;
    border-radius: 2px;
    font-size: 0.6875rem;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    font-weight: 600;
    margin-left: auto;
  }

  /* ── Impact panel ─────────────────────────────────────────── */
  .impact {
    max-width: var(--max-wide);
    margin: 3rem auto 0;
    padding: 2rem;
    background: #fff;
    border: 2px solid var(--color-competitive);
    border-radius: 3px;
  }
  .impact-title {
    font-family: var(--font-serif);
    font-size: clamp(1.375rem, 3vw, 1.75rem);
    font-weight: 700;
    margin: 0 0 1.75rem;
    line-height: 1.2;
  }
  .impact-grid {
    display: grid;
    grid-template-columns: 1.5fr 1fr 1fr;
    gap: 2rem;
  }
  .impact-block { display: flex; flex-direction: column; gap: 0.5rem; }
  .impact-label {
    font-size: 0.625rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: var(--color-text-muted);
    margin-bottom: 0.25rem;
  }

  .ec-row {
    display: flex;
    align-items: flex-start;
    gap: 1.25rem;
  }
  .ec-side { display: flex; flex-direction: column; gap: 0.25rem; }
  .ec-num {
    font-size: clamp(2rem, 5vw, 3rem);
    font-weight: 500;
    line-height: 0.9;
    letter-spacing: -0.03em;
    transition: color 0.2s;
  }
  .ec-delta {
    font-size: 0.75rem;
    color: var(--color-text-muted);
    letter-spacing: 0.02em;
  }
  .ec-vs {
    align-self: center;
    color: #9ca3af;
    font-size: 0.875rem;
    padding-top: 0.5rem;
  }
  .ec-baseline {
    font-size: 0.6875rem;
    color: #9ca3af;
    margin: 0.5rem 0 0;
    padding-top: 0.625rem;
    border-top: 1px solid #f3f4f6;
  }

  .flip-count {
    font-size: clamp(2rem, 5vw, 3rem);
    font-weight: 500;
    color: var(--color-text);
    line-height: 0.9;
    letter-spacing: -0.02em;
  }
  .flip-chips {
    display: flex;
    gap: 0.375rem;
    flex-wrap: wrap;
    margin-top: 0.375rem;
  }
  .flip-chip {
    padding: 0.2em 0.55em;
    border-radius: 2px;
    font-size: 0.6875rem;
    font-weight: 600;
    letter-spacing: 0.04em;
  }
  .flip-chip.lean-D { background: rgba(37, 99, 235, 0.1); color: #1d4ed8; }
  .flip-chip.lean-R { background: rgba(220, 38, 38, 0.1); color: #b91c1c; }
  .flip-none {
    margin: 0;
    font-size: 0.75rem;
    color: var(--color-text-muted);
    line-height: 1.55;
  }

  .eff-num {
    font-size: clamp(1.75rem, 4vw, 2.25rem);
    font-weight: 500;
    color: var(--color-text);
    line-height: 0.95;
    letter-spacing: -0.02em;
  }
  .eff-idle { color: #d1d5db; }
  .eff-desc {
    margin: 0;
    font-size: 0.6875rem;
    color: var(--color-text-muted);
    line-height: 1.5;
  }

  /* ── Method footnote ──────────────────────────────────────── */
  .method {
    max-width: var(--max-wide);
    margin: 2rem auto 0;
    font-size: 0.75rem;
    color: #9ca3af;
    line-height: 1.65;
  }
  .method-label { font-weight: 600; color: var(--color-text-muted); }

  /* ── Responsive ───────────────────────────────────────────── */
  @media (max-width: 900px) {
    .controls { grid-template-columns: 1fr; }
    .state-grid { grid-template-columns: repeat(2, 1fr); }
    .impact-grid { grid-template-columns: 1fr; gap: 2rem; }
  }
  @media (max-width: 600px) {
    .movers-budget { padding: 4rem 1rem; }
    .controls { padding: 1.25rem; }
    .state-grid { grid-template-columns: 1fr; }
    .impact { padding: 1.5rem; }
    .ec-row { flex-direction: column; }
    .ec-vs { align-self: flex-start; padding-top: 0; }
  }
</style>
