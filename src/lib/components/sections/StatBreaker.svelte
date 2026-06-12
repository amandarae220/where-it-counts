<section class="stat-breaker" aria-label="Key data comparison">

  <p class="eyebrow mono">What the data actually shows</p>

  <!-- Scale comparison: CA surplus vs GA margin -->
  <div class="comparison">
    <div class="comparison-col surplus-col">
      <span class="comp-label mono">California surplus votes, 2020</span>
      <span class="comp-number dem">2,552,143</span>
      <div class="comp-bar-wrap">
        <div class="comp-bar dem full" aria-hidden="true"></div>
      </div>
    </div>

    <div class="comparison-divider" aria-hidden="true">vs</div>

    <div class="comparison-col margin-col">
      <span class="comp-label mono">Georgia's entire margin, 2020</span>
      <span class="comp-number comp">11,779</span>
      <div class="comp-bar-wrap">
        <!-- 11,779 / 2,552,143 ≈ 0.46% of the bar -->
        <div class="comp-bar comp slim" aria-hidden="true"></div>
      </div>
    </div>
  </div>

  <!-- The multiplier — the hero number -->
  <div class="multiplier-block">
    <span class="multiplier-number mono">216<span class="multiplier-x">×</span></span>
    <p class="multiplier-caption">
      California's surplus alone could have flipped Georgia
      two hundred and sixteen times over.
    </p>
  </div>

  <hr class="stat-rule" aria-hidden="true" />

  <!-- 9 blue states vs 3 swing states -->
  <div class="versus-block">
    <div class="versus-side">
      <span class="versus-number mono dem">6.3M</span>
      <span class="versus-label">surplus votes<br/>across 9 safe blue states</span>
    </div>

    <div class="versus-middle" aria-hidden="true">
      <span class="versus-x mono">146×</span>
      <span class="versus-descriptor">larger</span>
    </div>

    <div class="versus-side right">
      <span class="versus-number mono comp">43K</span>
      <span class="versus-label">combined margin<br/>GA + AZ + WI</span>
    </div>
  </div>

  <p class="footnote mono">
    Three states. 37 electoral votes. Decided by fewer people than fit in a sold-out football stadium.
  </p>

</section>

<style>
  .stat-breaker {
    background: var(--color-bg-dark);
    color: var(--color-text-light);
    padding: 6rem 2rem;
    text-align: center;
  }

  /* Eyebrow label */
  .eyebrow {
    font-size: 0.75rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #6b7280;
    margin-bottom: 4rem;
  }

  /* ── Scale comparison ──────────────────────────────── */
  .comparison {
    display: flex;
    align-items: flex-start;
    justify-content: center;
    gap: 1.5rem;
    max-width: 860px;
    margin: 0 auto 4rem;
    flex-wrap: wrap;
  }

  .comparison-col {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    flex: 1;
    min-width: 220px;
    max-width: 380px;
  }
  .margin-col { align-items: flex-start; }

  .comp-label {
    font-size: 0.75rem;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    color: #6b7280;
    margin-bottom: 0.5rem;
    line-height: 1.4;
    text-align: left;
  }

  .comp-number {
    font-family: var(--font-mono);
    font-size: clamp(2rem, 5vw, 3.25rem);
    font-weight: 500;
    letter-spacing: -0.02em;
    line-height: 1;
    margin-bottom: 0.75rem;
  }

  .comp-bar-wrap {
    width: 100%;
    height: 6px;
    background: #1f2937;
    border-radius: 3px;
    overflow: hidden;
  }
  .comp-bar {
    height: 100%;
    border-radius: 3px;
  }
  .comp-bar.full  { width: 100%; }
  .comp-bar.slim  { width: 0.46%; min-width: 2px; }
  .comp-bar.dem   { background: var(--color-dem); }
  .comp-bar.comp  { background: var(--color-competitive); }

  .comparison-divider {
    font-family: var(--font-mono);
    font-size: 1rem;
    color: #4b5563;
    padding-top: 3.25rem;
    flex-shrink: 0;
    align-self: center;
  }

  /* Number colors */
  .dem  { color: var(--color-dem); }
  .comp { color: var(--color-competitive); }

  /* ── Multiplier hero ────────────────────────────────── */
  .multiplier-block {
    margin: 0 auto 4rem;
    max-width: 600px;
  }

  .multiplier-number {
    display: block;
    font-size: clamp(5rem, 18vw, 10rem);
    font-weight: 500;
    line-height: 0.9;
    letter-spacing: -0.04em;
    color: #fff;
  }
  .multiplier-x {
    font-size: 0.45em;
    color: var(--color-competitive);
    vertical-align: super;
  }

  .multiplier-caption {
    font-size: clamp(1rem, 2.5vw, 1.25rem);
    color: #9ca3af;
    line-height: 1.5;
    margin-top: 1.25rem;
    max-width: 440px;
    margin-left: auto;
    margin-right: auto;
  }

  /* ── Divider rule ───────────────────────────────────── */
  .stat-rule {
    border: none;
    border-top: 1px solid #1f2937;
    max-width: 560px;
    margin: 0 auto 4rem;
  }

  /* ── Versus block ───────────────────────────────────── */
  .versus-block {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 2rem;
    max-width: 700px;
    margin: 0 auto 2rem;
    flex-wrap: wrap;
  }

  .versus-side {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    min-width: 160px;
  }
  .versus-side.right { align-items: flex-start; }

  .versus-number {
    font-size: clamp(2.5rem, 7vw, 4rem);
    font-weight: 500;
    letter-spacing: -0.03em;
    line-height: 1;
    margin-bottom: 0.4rem;
  }
  .versus-label {
    font-size: 0.8125rem;
    color: #6b7280;
    line-height: 1.45;
    text-align: left;
  }

  .versus-middle {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 0.25rem;
    padding: 0 0.5rem;
  }
  .versus-x {
    font-size: clamp(1.75rem, 5vw, 2.75rem);
    color: #fff;
    font-weight: 500;
    letter-spacing: -0.02em;
  }
  .versus-descriptor {
    font-size: 0.75rem;
    color: #4b5563;
    text-transform: uppercase;
    letter-spacing: 0.1em;
  }

  /* ── Footnote ───────────────────────────────────────── */
  .footnote {
    font-size: 0.8125rem;
    color: #4b5563;
    max-width: 480px;
    margin: 0 auto;
    line-height: 1.6;
  }

  /* ── Responsive ─────────────────────────────────────── */
  @media (max-width: 600px) {
    .comparison { flex-direction: column; align-items: stretch; }
    .comparison-divider { align-self: flex-start; padding-top: 0; }
    .versus-block { flex-direction: column; align-items: flex-start; }
    .versus-side.right { align-items: flex-start; }
  }
</style>
