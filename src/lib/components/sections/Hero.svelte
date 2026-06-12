<section class="hero">
  <div class="hero-inner prose">
    <p class="hero-kicker mono text-muted">A data journalism project</p>
    <h1>Where It&nbsp;Counts</h1>
    <p class="hero-deck">
      In 2020, 76 million votes were cast in places where the outcome
      where the margin was not in question. Because of geography.
      Here's what the data says about where yours would actually matter,
      and what moving could change.
    </p>
    <div class="hero-scroll-hint" aria-hidden="true">
      <span>scroll</span>
      <svg width="16" height="24" viewBox="0 0 16 24" fill="none">
        <path d="M8 4v16M2 14l6 6 6-6" stroke="currentColor" stroke-width="1.5"
              stroke-linecap="round" stroke-linejoin="round"/>
      </svg>
    </div>
  </div>
</section>

<style>
  .hero {
    min-height: 100svh;
    display: flex;
    align-items: center;
    background: var(--color-bg-dark);
    color: var(--color-text-light);
    padding: 4rem 0;
  }
  .hero-inner { padding-top: 6rem; }

  .hero-kicker {
    font-size: 0.8125rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: var(--color-competitive);
    margin-bottom: 1.25rem;
    max-width: 100%;
  }

  h1 {
    color: var(--color-text-light);
    margin-bottom: 1.5rem;
  }

  .hero-deck {
    font-size: clamp(1.125rem, 2.5vw, 1.375rem);
    color: #9ca3af;
    line-height: 1.6;
    max-width: 560px;
    margin-bottom: 3rem;
  }

  .hero-scroll-hint {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-size: 0.8125rem;
    color: #6b7280;
    letter-spacing: 0.1em;
    text-transform: uppercase;
  }
</style>
