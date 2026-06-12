<script>
  import { onMount } from 'svelte';

  /** @type {any} viz component to render in the sticky panel */
  export let Viz;
  /** @type {any[]} array of step objects passed to viz + rendered as step content */
  export let steps = [];
  /** offset 0–1 — how far down viewport triggers step enter */
  export let offset = 0.5;

  let currentStep = 0;
  let scroller;

  onMount(async () => {
    const { default: scrollama } = await import('scrollama');
    scroller = scrollama();
    scroller
      .setup({ step: '.scrolly-step', offset, debug: false })
      .onStepEnter(({ index }) => { currentStep = index; });

    const onResize = () => scroller.resize();
    window.addEventListener('resize', onResize);

    return () => {
      scroller.destroy();
      window.removeEventListener('resize', onResize);
    };
  });
</script>

<div class="scrolly">
  <!-- Sticky viz panel -->
  <div class="scrolly-sticky" aria-hidden="true">
    {#if Viz}
      <svelte:component this={Viz} step={currentStep} {steps} />
    {/if}
  </div>

  <!-- Narrative steps -->
  <div class="scrolly-steps">
    {#each steps as step, i}
      <div class="scrolly-step step" data-step={i}>
        <div class="step-content">
          {#if step.stat}
            <div class="stat">{step.stat}</div>
            {#if step.statLabel}
              <div class="stat-label">{step.statLabel}</div>
            {/if}
            <div class="divider"></div>
          {/if}
          <p>{@html step.text}</p>
        </div>
      </div>
    {/each}
  </div>
</div>
