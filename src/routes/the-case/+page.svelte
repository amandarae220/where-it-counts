<script>
  import HowLinesDrawn    from '$lib/components/sections/HowLinesDrawn.svelte';
  import DistrictShopping from '$lib/components/sections/DistrictShopping.svelte';
  import Nobody           from '$lib/components/sections/Nobody.svelte';
  import LongGame         from '$lib/components/sections/LongGame.svelte';
  import Calculator       from '$lib/components/sections/Calculator.svelte';
</script>

<div class="page-nav">
  <a href="/" class="back-link mono">← Back</a>
</div>

<main>

  <!-- 1. The defensive move: gerrymandering + geographic sorting -->
  <HowLinesDrawn />

  <!-- 2. The offensive move: candidates pick their districts -->
  <DistrictShopping />

  <!-- 3. The Part Nobody's Talking About -->
  <Nobody />

  <!-- 4. The Long Game -->
  <LongGame />

  <!-- 5. Interactive calculator -->
  <Calculator />

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
  .page-nav {
    position: fixed;
    top: 1.25rem;
    left: 1.5rem;
    z-index: 100;
  }
  .back-link {
    font-size: 0.8125rem;
    letter-spacing: 0.06em;
    color: #6b7280;
    text-decoration: none;
    background: rgba(17, 17, 16, 0.85);
    padding: 0.375rem 0.75rem;
    border-radius: 3px;
    backdrop-filter: blur(4px);
    transition: color 0.12s;
  }
  .back-link:hover { color: #d97706; }

  .site-footer {
    padding: 3rem 0;
    background: var(--color-bg-dark);
    border-top: 1px solid #1f2937;
  }
</style>
