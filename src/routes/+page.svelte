<script>
  import StatBreaker   from '$lib/components/sections/StatBreaker.svelte';
  import Scrollytelling   from '$lib/components/Scrollytelling.svelte';
  import SurplusMapViz    from '$lib/components/viz/SurplusMapViz.svelte';
  import MapMoves         from '$lib/components/sections/MapMoves.svelte';
  // import Calculator       from '$lib/components/sections/Calculator.svelte';

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
        In 2020, 76 million votes were cast in places where the margin
        was never in question. Here's what the data says about where your vote can have the
        most impact, and what moving could change.
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
  <!--section class="two-moves section">
    <div class="prose">
      <p class="eyebrow mono">Same instinct, two moves</p>
      <h2>Politicians Have Always Treated Location as Strategy.</h2>
      <div class="divider"></div>

      <p class="moves-lede">
        Start with the big ones — president, senator, governor. Nobody draws
        districts for those. What decides them is simpler: over the years,
        people sorted themselves. We moved for jobs, for weather, for the
        cost of living, for the vibe — and whole states quietly slid into
        one column and stayed. That's the engine under all of it. Politicians
        didn't build it. They just learned to use it two ways.
      </p>

      <div class="moves-grid">
        <div class="move">
          <span class="move-num mono">01</span>
          <h3>They pick their spot</h3>
          <p>
            They move to where they can win. A state senate hopeful picks a
            district that already leans their way. Someone running for
            Congress rents an apartment in a swing seat. They're not drawing
            the map — just standing in a good spot on it. Both parties, every
            level. It's legal, it's out in the open, and once you notice it
            you can't unsee it.
          </p>
          <div class="move-affects">
            <span class="mono affects-label">What this affects</span>
            <span class="affects-body">
              Every race, president to school board.
              Anywhere location shapes the odds.
            </span>
          </div>
        </div>
        <div class="move">
          <span class="move-num mono">02</span>
          <h3>They draw the lines</h3>
          <p>
            For races that do have districts, whoever's in power gets a
            second move. Every ten years they redraw the lines — cramming the
            other side into a few districts, spreading their own people out to
            win more. That's gerrymandering. It only works because we've
            already sorted ourselves; the lines just press harder on it.
          </p>
          <div class="move-affects">
            <span class="mono affects-label">What this affects</span>
            <span class="affects-body">
              U.S. House. State house and senate.
              Anywhere district lines get drawn.
            </span>
          </div>
        </div>
      </div>

      <div class="pull-quote">
        <p>
          You've got the same map they do — the same numbers, the same
          freedom to pack up and move. The only question is whether you
          ever use it.
        </p>
      </div>

      <p class="mechanism-note">
        <span class="mono note-label">The common thread</span>
        So here's the whole thing in one breath: sorting decides the big
        races, sorting plus map-drawing decides the district ones. Either way
        it shakes out the same — most votes get cast where the result was
        never close, and a few get cast where it all comes down to the wire.
        Whether your vote is <em>decisive or surplus</em> comes down to where
        you live. The rest of this is us showing you that math — and what
        you'd actually do about it. No yard signs, no doorknocking.
      </p>
    </div>
  </section-->

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
        <p class="leg-source mono">Source: OpenElections + Ballotpedia · 2020 official returns</p>
        <p class="state-tail">
          These are the people who draw the maps, set school curricula,
          decide healthcare access, and control what goes on your ballot.
          Seven Georgia House districts were decided by fewer than 1,000 votes.
          Twenty-six Wisconsin Assembly districts by fewer than 5,000.
        </p>
        <p class="state-tail">
          And here's what ties it together: win enough of these seats and
          your party gets to redraw the district lines for the next ten
          years — packing the other side into a few districts, spreading
          your own voters out to win the rest. That's gerrymandering, and it
          starts in races this small. The candidates already know it. Plenty
          of them move into a district that leans their way before they ever
          run — pick the spot, then stand on it. Both parties, every level.
          It's legal, it's out in the open, and it's the same move that's
          available to you.
        </p>
      </div>
    </section>
  </div>

  <!-- Interactive: how the map could move -->
  <MapMoves />

  <!-- Destination calculator — the actionable payoff -->
  <!-- <Calculator /> -->

  <!-- Closer: 2031 timing math + honest scale + academic grounding -->
  <section class="closer">
    <div class="prose">
      <p class="eyebrow mono">The timing</p>
      <h2>The map resets in 2030.</h2>
      <div class="divider"></div>

      <p>
        Every ten years, after the Census, every district in the country
        gets redrawn based on where people actually live. The next count
        is April 2030. The new maps arrive for 2031.
      </p>

      <p>
        A meaningful shift in a state-legislative district's math takes
        thousands of movers, not hundreds. That's the honest scale of
        the ask. This is a long-form civic move, not a stunt — and it's
        the only one where a single household decision reallocates
        political leverage the same way it reallocates real estate
        value.
      </p>

      <p class="cite mono">
        For the intellectual grounding of the surplus-vote framing, see
        Jonathan Rodden, <em>Why Cities Lose</em> (2019), which documents
        how Democratic voters have clustered into safe corners — the
        same pattern this piece visualizes.
      </p>
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

  .moves-lede {
    font-size: 1.0625rem;
    line-height: 1.7;
    color: var(--color-text-muted);
    max-width: var(--max-prose);
  }
  .moves-lede em { font-style: italic; color: var(--color-text); }

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
  .move-affects {
    display: flex;
    flex-direction: column;
    gap: 0.375rem;
    margin-top: 1rem;
    padding-top: 0.875rem;
    border-top: 1px dashed #d1d5db;
  }
  .affects-label {
    font-size: 0.625rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--color-competitive);
  }
  .affects-body {
    font-size: 0.8125rem;
    color: var(--color-text);
    line-height: 1.55;
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

  .mechanism-note {
    margin-top: 2rem;
    padding: 1.25rem 1.5rem;
    background: #fff;
    border: 1px solid #e5e7eb;
    border-left: 3px solid var(--color-competitive);
    border-radius: 2px;
    font-size: 0.9375rem;
    line-height: 1.7;
    color: var(--color-text-muted);
  }
  .note-label {
    display: block;
    font-size: 0.6875rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: var(--color-competitive);
    margin-bottom: 0.5rem;
  }
  .mechanism-note em {
    font-style: italic;
    color: var(--color-text);
    font-weight: 500;
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
  .leg-source {
    font-size: 0.6875rem;
    letter-spacing: 0.04em;
    color: #6b7280;
    margin-top: -1.5rem;
    margin-bottom: 2rem;
  }

  @media (max-width: 780px) {
    .leg-stats { grid-template-columns: 1fr; gap: 1rem; }
  }

  /* ── Closer ────────────────────────────────────────────────── */
  .closer {
    padding: 7rem 0;
    background: var(--color-bg-dark);
    color: var(--color-text-light);
  }
  .closer h2 {
    color: var(--color-text-light);
    margin-bottom: 1rem;
  }
  .closer p {
    color: #d1d5db;
    font-size: 1.0625rem;
    line-height: 1.7;
    margin-bottom: 1.5rem;
    max-width: var(--max-prose);
  }
  .closer .eyebrow {
    color: var(--color-competitive);
  }
  .closer .cite {
    font-size: 0.8125rem;
    color: #6b7280;
    line-height: 1.65;
    padding-top: 1.5rem;
    margin-top: 2rem;
    border-top: 1px solid #1f2937;
  }
  .closer .cite em {
    font-style: italic;
    color: #9ca3af;
  }

  /* ── Footer ────────────────────────────────────────────────── */
  .site-footer {
    padding: 3rem 0;
    background: var(--color-bg-dark);
    border-top: 1px solid #1f2937;
  }
</style>
