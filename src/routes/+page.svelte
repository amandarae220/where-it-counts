<script>
  import StatBreaker   from '$lib/components/sections/StatBreaker.svelte';
  import Scrollytelling   from '$lib/components/Scrollytelling.svelte';
  import SurplusMapViz    from '$lib/components/viz/SurplusMapViz.svelte';

  const surplusSteps = [
    {
      mode: 'intro',
      text: 'Each dot on this map is a county. The deeper the color, the more votes accumulated beyond what determined the outcome. Both parties. Every county.',
    },
    {
      mode: 'surplus-blue',
      stat: '11.8M',
      statLabel: 'Democratic surplus votes',
      text: 'Across safe blue counties nationwide, Democratic votes accumulated 11.8 million beyond what their winners needed. New York City alone: 1.3 million. LA County: 897,000. Cook County: 565,000.',
    },
    {
      mode: 'surplus-red',
      stat: '8.6M',
      statLabel: 'Republican surplus votes',
      text: 'Republican surplus votes totaled 8.6 million — real, but smaller. The biggest single surplus GOP county had 57,000 votes beyond the margin. LA County\'s Democratic surplus is 15× larger.',
    },
    {
      mode: 'total-surplus',
      stat: '76M',
      statLabel: 'Votes cast outside the decisive margin',
      text: 'Combined, 76 million votes — nearly half of all votes cast in 2020 — went to places where the margin was not in question. They were counted. But the result in those places was settled before they were cast. Because of geography.',
    },
    {
      mode: 'zoom-swing',
      text: 'Meanwhile, three swing states that together carried 37 electoral votes were decided by a combined 43,000 votes. Less than a sold-out football stadium. Georgia alone: 11,779 people.',
    },
  ];
</script>

<main>

  <!-- Hero -->
  <section class="hero">
    <div class="hero-inner prose">
      <p class="kicker mono">A data journalism project</p>
      <h1>Where It&nbsp;Counts</h1>
      <p class="deck">
        For decades, politicians have used geography as a strategic tool —
        drawing maps to protect themselves and picking districts where they
        can win. Voters can make the same move. Most just don't know it yet.
      </p>
      <a href="#the-data" class="cta">See the data <span aria-hidden="true">↓</span></a>
    </div>
  </section>

  <!-- Three jaw-drop numbers -->
  <!--section class="numbers">
    <div class="numbers-inner container">
      <div class="num-block">
        <span class="num mono">76M</span>
        <span class="num-label">votes cast in 2020 where the margin wasn't in question</span>
      </div>
      <div class="num-divider" aria-hidden="true"></div>
      <div class="num-block">
        <span class="num mono text-comp">11,779</span>
        <span class="num-label">votes decided Georgia's entire presidential race</span>
      </div>
      <div class="num-divider" aria-hidden="true"></div>
      <div class="num-block">
        <span class="num mono text-dem">216×</span>
        <span class="num-label">California's surplus over Georgia's deciding margin</span>
      </div>
    </div>
  </section-->

  <!-- Two moves -->
  <section class="two-moves section">
    <div class="prose">
      <p class="eyebrow mono">Two moves. Same instinct.</p>
      <h2>Politicians Have Been Playing This Game for Decades.</h2>
      <div class="divider"></div>

      <div class="moves-grid">
        <div class="move">
          <span class="move-num mono">01</span>
          <h3>They draw the map</h3>
          <p>
            After every Census, the party in power redraws district lines to
            concentrate opponents and spread out their own voters. It locks in
            outcomes that protect careers regardless of how people feel.
            That's gerrymandering — and it's been working for forty years.
          </p>
        </div>
        <div class="move">
          <span class="move-num mono">02</span>
          <h3>They pick their spot on it</h3>
          <p>
            Before gerrymandering is even relevant, candidates scout precincts,
            study registration trends, and choose where to run. A state senate
            candidate moves to a better district. A congressional hopeful picks
            an apartment in a swing seat. Both parties. Every level of office.
            It's not a secret. It's just strategy.
          </p>
        </div>
      </div>

      <div class="pull-quote">
        <p>
          Voters have access to the same map, the same data, and the same
          freedom to move. The question is whether they start using them
          the same way.
        </p>
      </div>
    </div>
  </section>

  <!-- ── What the data actually shows ──────────────────────────── -->
  <div id="the-data">
    <StatBreaker />

    <Scrollytelling
      Viz={SurplusMapViz}
      steps={surplusSteps}
      offset={0.5}
    />

    <!-- State Races: Even Smaller -->
    <section class="section state-leg">
      <div class="prose">
        <p class="eyebrow mono">Zoom out further</p>
        <h2>State races are decided by even fewer people.</h2>
        <div class="divider"></div>
        <p class="state-lede">
          Presidential margins get the headlines. State legislative seats are
          where the floors actually move — and they turn on numbers small
          enough to fit in a single apartment building.
        </p>
        <div class="leg-stats">
          <div class="leg-stat">
            <span class="leg-num mono text-comp">139</span>
            <span class="leg-meta">votes decided</span>
            <span class="leg-where mono">WI Assembly · District 73 · 2020</span>
          </div>
          <div class="leg-stat">
            <span class="leg-num mono text-dem">280</span>
            <span class="leg-meta">votes decided</span>
            <span class="leg-where mono">GA House · District 35 · 2020</span>
          </div>
          <div class="leg-stat">
            <span class="leg-num mono">582</span>
            <span class="leg-meta">votes decided</span>
            <span class="leg-where mono">WI State Senate · District 32 · 2020</span>
          </div>
        </div>
        <p class="state-tail">
          These are the people who draw the maps, set school curricula,
          decide healthcare access, and control what goes on your ballot.
          Seven Georgia House districts were decided by fewer than 1,000 votes.
          Twenty-six Wisconsin Assembly districts by fewer than 5,000.
        </p>
      </div>
    </section>
  </div>

  <!-- Bridge CTA -->
  <section class="bridge">
    <div class="prose">
      <p class="bridge-hed">That's the problem. Here's the opportunity.</p>
      <p class="bridge-sub">
        The same math that explains why your vote doesn't move the needle
        where you live also points to exactly where it would.
      </p>
      <a href="/the-case" class="cta">See where your vote would count <span aria-hidden="true">→</span></a>
    </div>
  </section>

  <!-- Footer -->
  <footer class="site-footer">
    <div class="prose">
      <p class="mono text-muted" style="font-size:0.8125rem;">
        All data public and free. Sources: MIT Election Lab · U.S. Census ACS ·
        Bureau of Labor Statistics · Zillow Research · OpenElections · Ballotpedia ·
        Bureau of Economic Analysis.
      </p>
    </div>
  </footer>

</main>

<style>
  /* ── Hero ──────────────────────────────────────────────────── */
  .hero {
    min-height: 100svh;
    display: flex;
    align-items: center;
    background: var(--color-bg-dark);
    color: var(--color-text-light);
    padding: 4rem 0;
  }
  .hero-inner { padding-top: 4rem; }

  .kicker {
    font-size: 0.8125rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: var(--color-competitive);
    margin-bottom: 1.25rem;
    max-width: 100%;
  }
  h1 { color: var(--color-text-light); margin-bottom: 1.5rem; }

  .deck {
    font-size: clamp(1.125rem, 2.5vw, 1.375rem);
    color: #9ca3af;
    line-height: 1.6;
    max-width: 540px;
    margin-bottom: 2.5rem;
  }

  /* ── CTA ───────────────────────────────────────────────────── */
  .cta {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    background: var(--color-competitive);
    color: #fff;
    font-family: var(--font-mono);
    font-size: 0.9375rem;
    letter-spacing: 0.04em;
    padding: 0.875rem 1.75rem;
    border-radius: 3px;
    text-decoration: none;
    transition: background 0.15s;
  }
  .cta:hover { background: #b45309; }
  .cta:focus-visible {
    outline: 2px solid var(--color-competitive);
    outline-offset: 3px;
  }

  /* ── Numbers strip ─────────────────────────────────────────── */
  .numbers {
    background: var(--color-bg-dark);
    border-top: 1px solid #1f2937;
    padding: 4rem 0;
  }
  .numbers-inner {
    display: flex;
    align-items: flex-start;
    flex-wrap: wrap;
  }
  .num-block {
    flex: 1;
    min-width: 200px;
    display: flex;
    flex-direction: column;
    gap: 0.625rem;
    padding: 0 2.5rem;
  }
  .num-block:first-child { padding-left: 0; }
  .num-block:last-child  { padding-right: 0; }
  .num {
    font-size: clamp(2.5rem, 6vw, 4rem);
    font-weight: 500;
    letter-spacing: -0.03em;
    line-height: 1;
    color: #fff;
  }
  .num-label {
    font-size: 0.875rem;
    color: #6b7280;
    line-height: 1.45;
    max-width: 220px;
  }
  .num-divider {
    width: 1px;
    background: #1f2937;
    align-self: stretch;
    flex-shrink: 0;
    margin: 0.5rem 0;
  }

  @media (max-width: 640px) {
    .numbers-inner { flex-direction: column; gap: 2.5rem; }
    .num-block { padding: 0; min-width: unset; }
    .num-divider { display: none; }
  }

  /* ── Two moves ─────────────────────────────────────────────── */
  .two-moves { padding: 7rem 0; }
  .eyebrow {
    font-size: 0.75rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--color-competitive);
    margin-bottom: 1rem;
    max-width: 100%;
  }
  h2 { margin-bottom: 1rem; }
  p  { margin-bottom: 1.25rem; }

  .moves-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 2.5rem;
    margin: 2.5rem 0;
  }
  .move {
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
    padding: 1.75rem;
    border: 1px solid #e5e7eb;
    border-radius: 2px;
    background: #f9fafb;
  }
  .move-num {
    font-size: 0.75rem;
    letter-spacing: 0.1em;
    color: var(--color-competitive);
  }
  .move h3 { font-size: 1.125rem; margin: 0; }
  .move p {
    font-size: 0.9375rem;
    color: var(--color-text-muted);
    line-height: 1.65;
    margin: 0;
  }

  @media (max-width: 600px) {
    .moves-grid { grid-template-columns: 1fr; }
  }

  .pull-quote {
    border-left: 3px solid var(--color-competitive);
    margin: 2.5rem 0;
    padding: 1rem 1.5rem;
    background: #f9fafb;
  }
  .pull-quote p {
    font-family: var(--font-serif);
    font-size: 1.1875rem;
    line-height: 1.6;
    color: var(--color-text);
    margin: 0;
  }

  /* ── State leg ─────────────────────────────────────────────── */
  .state-leg {
    padding: 7rem 0;
    background: var(--color-bg-dark);
    color: var(--color-text-light);
  }
  .state-leg h2 { color: var(--color-text-light); max-width: 720px; }
  .state-leg .divider { background: #1f2937; }
  .state-lede,
  .state-tail {
    color: #9ca3af;
    font-size: 1.0625rem;
    line-height: 1.65;
  }
  .leg-stats {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1.25rem;
    margin: 3rem 0;
  }
  .leg-stat {
    display: flex;
    flex-direction: column;
    gap: 0.4rem;
    padding: 1.75rem 1.5rem;
    border: 1px solid #1f2937;
    border-radius: 3px;
    background: rgba(255, 255, 255, 0.015);
  }
  .leg-num {
    font-size: clamp(3rem, 8vw, 5rem);
    font-weight: 500;
    line-height: 0.9;
    letter-spacing: -0.03em;
  }
  .leg-meta {
    font-size: 0.8125rem;
    color: #9ca3af;
    margin-top: 0.25rem;
  }
  .leg-where {
    font-size: 0.6875rem;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #4b5563;
    margin-top: 0.25rem;
  }

  @media (max-width: 780px) {
    .leg-stats { grid-template-columns: 1fr; gap: 1rem; }
  }

  /* ── Bridge CTA ────────────────────────────────────────────── */
  .bridge {
    padding: 7rem 0;
    background: var(--color-bg-dark);
    color: var(--color-text-light);
  }
  .bridge-hed {
    font-family: var(--font-serif);
    font-size: clamp(1.5rem, 3.5vw, 2.25rem);
    font-weight: 700;
    color: var(--color-text-light);
    line-height: 1.2;
    margin-bottom: 1rem;
    max-width: var(--max-prose);
  }
  .bridge-sub {
    font-size: 1.0625rem;
    color: #9ca3af;
    line-height: 1.65;
    margin-bottom: 2rem;
    max-width: 520px;
  }

  /* ── Footer ────────────────────────────────────────────────── */
  .site-footer {
    padding: 3rem 0;
    background: var(--color-bg-dark);
    border-top: 1px solid #1f2937;
  }
</style>
