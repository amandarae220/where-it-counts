<script>
  import Hero        from '$lib/components/sections/Hero.svelte';
  import Rigged      from '$lib/components/sections/Rigged.svelte';
  import Nobody      from '$lib/components/sections/Nobody.svelte';
  import LongGame    from '$lib/components/sections/LongGame.svelte';
  import Scrollytelling from '$lib/components/Scrollytelling.svelte';
  import SurplusMapViz  from '$lib/components/viz/SurplusMapViz.svelte';
  import StatBreaker    from '$lib/components/sections/StatBreaker.svelte';
  import Calculator     from '$lib/components/sections/Calculator.svelte';

  // Steps for the hero scrollytelling sequence — "What the Data Actually Shows"
  const surplusSteps = [
    {
      mode: 'intro',
      text: 'Each dot on this map is a county. The deeper the color, the more votes piled up beyond what the winner needed. Both parties. Every county.',
    },
    {
      mode: 'surplus-blue',
      stat: '11.8M',
      statLabel: 'Democratic surplus votes',
      text: 'Across safe blue counties nationwide, Democratic votes piled up 11.8 million beyond what their winners needed. New York City alone: 1.3 million. LA County: 897,000. Cook County: 565,000.',
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
      statLabel: 'Votes cast where the outcome was already set',
      text: 'Combined, 76 million votes — nearly half of all votes cast in 2020 — went to places where the outcome was already decided. They showed up. They got counted. The result was already set before they arrived. Because of geography.',
    },
    {
      mode: 'zoom-swing',
      text: 'Meanwhile, three swing states that together carried 37 electoral votes were decided by a combined 43,000 votes. Less than a sold-out football stadium. Georgia alone: 11,779 people.',
    },
  ];
</script>

<main>
  <!-- 1. Hero -->
  <Hero />

  <!-- 2. Narrative: Geographic sorting + gerrymandering -->
  <Rigged />

  <!-- 3. Data infographic + Scrollytelling: The Data -->
  <StatBreaker />

  <div id="the-data">
    <Scrollytelling
      Viz={SurplusMapViz}
      steps={surplusSteps}
      offset={0.5}
    />
  </div>

  <!-- 4. State Legislative callout -->
  <section class="section state-leg">
    <div class="prose">
      <h2>State Leg Races: Even Smaller</h2>
      <div class="divider"></div>
      <p>
        Presidential margins get the headlines. State legislative races are
        where the floors actually move.
      </p>
      <div class="leg-stats">
        <div class="leg-stat">
          <span class="stat text-dem">280</span>
          <span class="stat-label">votes — GA House District 35, 2020</span>
        </div>
        <div class="leg-stat">
          <span class="stat text-comp">139</span>
          <span class="stat-label">votes — WI Assembly District 73, 2020</span>
        </div>
        <div class="leg-stat">
          <span class="stat" style="color:#6b7280;">582</span>
          <span class="stat-label">votes — WI State Senate District 32, 2020</span>
        </div>
      </div>
      <p>
        These are state senate and state house races — the people who draw
        the maps, set your school curriculum, decide Medicaid expansion, and
        determine what ends up on your ballot.
      </p>
      <p>
        7 Georgia House districts were decided by fewer than 1,000 votes.
        26 Wisconsin Assembly districts by fewer than 5,000. These aren't
        edge cases — they're the norm in competitive areas.
      </p>
    </div>
  </section>

  <!-- 5. The Part Nobody's Talking About -->
  <Nobody />

  <!-- 6. The Long Game -->
  <LongGame />

  <!-- 7. Interactive calculator -->
  <Calculator />

  <!-- 8. Footer / data sources -->
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
  /* State leg section */
  .state-leg {
    padding: 6rem 0;
    background: #f9fafb;
  }
  h2 { margin-bottom: 1rem; }
  p  { margin-bottom: 1.25rem; }

  .leg-stats {
    display: flex;
    flex-wrap: wrap;
    gap: 2rem;
    margin: 2.5rem 0;
  }
  .leg-stat {
    display: flex;
    flex-direction: column;
  }
  .leg-stat .stat { font-size: clamp(2rem, 5vw, 3rem); }

  /* Footer */
  .site-footer {
    padding: 3rem 0;
    background: var(--color-bg-dark);
    border-top: 1px solid #1f2937;
  }
</style>
