<!-- The offensive move: candidates scout and pick their districts -->
<section class="section district-shopping">
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
