<!-- The offensive move: candidates scout and pick their districts -->
<!--section class="section district-shopping">
  <div class="prose">
    <p class="eyebrow mono">The other move politicians make</p>
    <h2>They Don't Just Draw the Map. They Pick Their Spot on It.</h2>
    <div class="divider"></div>

    <p>
      Gerrymandering is the defensive play — protect the seat you already
      have. But before that's even relevant, there's an offensive one:
      candidates research the map and choose where to run.
    </p>
    <p>
      A state senate candidate moves across the county to a district with a
      better registration advantage. A congressional hopeful picks an
      apartment in a swing seat instead of the safe one next door. Both
      parties. Every level of office. They pull precinct data, look at
      turnout trends, find a place where the math works in their favor —
      and they establish residency.
    </p>

    <div class="pull-quote">
      <p>
        It's not cheating. It's not even unusual. It's just strategy —
        treating geography as a variable to optimize, not a fixed fact
        to accept.
      </p>
    </div>

    <p>
      Voters have access to the same data. The same map. The same math.
      The difference is that candidates have been thinking this way for
      decades, and most voters haven't started yet.
    </p>

    <div class="pull-quote">
      <p>
        Voters have access to the same map, the same data, and the same
        freedom to move. The question is whether they start using them
        the same way.
      </p>
    </div>

    <div class="compare-block">
      <div class="compare-col">
        <span class="compare-label mono">What a candidate asks</span>
        <p class="compare-text">
          Where is the margin close enough that my presence changes
          the outcome?
        </p>
      </div>
      <div class="compare-divider" aria-hidden="true"></div>
      <div class="compare-col">
        <span class="compare-label mono">What a voter can ask</span>
        <p class="compare-text">
          Where is the margin close enough that my vote — and the votes
          of people who move with me — changes the outcome?
        </p>
      </div>
    </div>

    <p>
      The question this piece tries to answer is what happens when regular
      people start asking the second question.
    </p>
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
          <span class="move-num mono">Gerrymandering</span>
          <h3>The defensive move</h3>
          <p>
            <!--After every Census, the party in power redraws district lines to
            concentrate opponents and spread out their own voters. It locks in
            outcomes that protect careers regardless of how people feel.
            That's gerrymandering — and it's been working for forty years.-->
            Gerrymandering is the defensive play — protect the seat you already
      have. But before that's even relevant, there's an offensive one:
      candidates research the map and choose where to run.
          </p>
        </div>
        <div class="move">
          <span class="move-num mono">Relocation</span>
          <h3>The offensive move</h3>
          <p>
            <!--Before gerrymandering is even relevant, candidates scout precincts,
            study registration trends, and choose where to run. A state senate
            candidate moves to a better district. A congressional hopeful picks
            an apartment in a swing seat. Both parties. Every level of office.
            It's not a secret. It's just strategy.-->
                  A state senate candidate moves across the county to a district with a
      better registration advantage. A congressional hopeful picks an
      apartment in a swing seat instead of the safe one next door. Both
      parties. Every level of office. They pull precinct data, look at
      turnout trends, find a place where the math works in their favor —
      and they establish residency.
          </p>
        </div>
      </div>

      <div>
        <p>
        Cue gerrymandering. For forty years, politicians have been drawing their own district maps.
        They sorted red voters and blue voters into separate corners, locking
        in election outcomes that favor them and protect their path to becoming
        a career politician. And it worked. 
        </p>
        <p>
        But gerrymandering didn't create the problem from scratch — it amplified one that was already happening. Cities got more liberal. Rural areas got more conservative. Not because
        of any grand plan, the sorting happened on its own. Gerrymandering
        looked at that sorting and drew it into law.
        </p>
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

<style>
  .district-shopping { padding: 8rem 0; background: var(--color-bg); }
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

  .compare-block {
    display: grid;
    grid-template-columns: 1fr auto 1fr;
    gap: 2rem;
    align-items: start;
    background: var(--color-bg-dark);
    color: var(--color-text-light);
    padding: 2rem;
    margin: 2.5rem 0;
    border-radius: 2px;
  }
  .compare-col { display: flex; flex-direction: column; gap: 0.75rem; }
  .compare-label {
    font-size: 0.6875rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #6b7280;
  }
  .compare-text {
    font-size: 1rem;
    color: #d1d5db;
    line-height: 1.6;
    margin: 0;
    max-width: 100%;
  }
  .compare-divider {
    width: 1px;
    background: #374151;
    align-self: stretch;
    margin: 0.25rem 0;
  }

  @media (max-width: 600px) {
    .compare-block {
      grid-template-columns: 1fr;
    }
    .compare-divider {
      width: 100%;
      height: 1px;
    }
  }
</style>
