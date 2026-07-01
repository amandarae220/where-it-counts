<script>
  // All data embedded — MIT Election Lab 2020, Zillow ZORI/ZHVI 2024–25, BLS ATUS 2023

  const origins = [
    { id: 'nyc',      label: 'New York City, NY',         rent: 3406 },
    { id: 'sf',       label: 'San Francisco Bay Area, CA', rent: 3073 },
    { id: 'la',       label: 'Los Angeles, CA',            rent: 2817 },
    { id: 'boston',   label: 'Boston, MA',                 rent: 3000 },
    { id: 'miami',    label: 'Miami, FL',                  rent: 2300 },
    { id: 'seattle',  label: 'Seattle, WA',                rent: 2400 },
    { id: 'dc',       label: 'Washington, D.C.',           rent: 2350 },
    { id: 'chicago',  label: 'Chicago, IL',                rent: 2100 },
    { id: 'denver',   label: 'Denver, CO',                 rent: 1950 },
    { id: 'portland', label: 'Portland, OR',               rent: 1850 },
    { id: 'minneapolis', label: 'Minneapolis, MN',         rent: 1700 },
    { id: 'austin',   label: 'Austin, TX',                 rent: 1750 },
    { id: 'dallas',   label: 'Dallas, TX',                 rent: 1700 },
    { id: 'slc',      label: 'Salt Lake City, UT',         rent: 1550 },
  ];

  // BLS ATUS 2023: share of employed who worked from home
  const jobCategories = [
    { id: 'computer',   label: 'Tech / Software',       wfhRate: 71 },
    { id: 'management', label: 'Management / Business', wfhRate: 62 },
    { id: 'legal',      label: 'Legal / Finance',       wfhRate: 54 },
    { id: 'arts',       label: 'Creative / Media',      wfhRate: 47 },
    { id: 'education',  label: 'Education / Research',  wfhRate: 38 },
    { id: 'healthcare', label: 'Healthcare',            wfhRate: 11 },
    { id: 'trades',     label: 'Trades / Labor',        wfhRate: 4  },
  ];

  // Competitive destination metros
  // stateMargin: 2020 presidential margin at state level (positive = Dem win)
  // legMargin: representative competitive district margin in that metro area
  // medianHome: Zillow ZHVI approximate 2024–25
  const destinations = [
    {
      id: 'atlanta',
      label: 'Atlanta suburbs',
      sublabel: 'Cobb & Gwinnett County, GA',
      rent: 1620,
      medianHome: 340000,
      stateMargin: 0.23,
      stateWinner: 'dem',
      legMargin: 280,
      legNote: 'GA House Dist. 35, 2020',
      localMargin: 410,
      trend: 'razor',
      trendNote: 'Georgia decided by 11,779 votes in 2020',
      blurb: 'Cobb and Gwinnett counties flipped presidential in 2020 for the first time in a generation. State legislative races here are decided by hundreds of votes — and they control who draws the next map in 2031.',
    },
    {
      id: 'phoenix',
      label: 'Phoenix suburbs',
      sublabel: 'Maricopa County, AZ',
      rent: 1700,
      medianHome: 375000,
      stateMargin: 0.31,
      stateWinner: 'dem',
      legMargin: 1800,
      legNote: 'avg. competitive district, 2020',
      localMargin: 650,
      trend: 'razor',
      trendNote: 'Arizona decided by 10,457 votes in 2020',
      blurb: 'Maricopa County has more registered voters than 15 entire states. Competitive at every level — school board, state legislature, U.S. Senate — and still moving.',
    },
    {
      id: 'milwaukee',
      label: 'Milwaukee metro',
      sublabel: 'Southeastern Wisconsin',
      rent: 1407,
      medianHome: 245000,
      stateMargin: 0.63,
      stateWinner: 'dem',
      legMargin: 582,
      legNote: 'WI Senate Dist. 32, 2020',
      localMargin: 210,
      trend: 'razor',
      trendNote: 'Wisconsin decided by 20,682 votes in 2020',
      blurb: 'One of the most affordable metros among genuinely competitive swing regions. WI Senate District 32 was decided by 582 votes. The suburbs here are where statewide elections turn.',
    },
    {
      id: 'raleigh',
      label: 'Raleigh–Durham',
      sublabel: 'Research Triangle, NC',
      rent: 1491,
      medianHome: 330000,
      stateMargin: -1.3,
      stateWinner: 'rep',
      legMargin: 1200,
      legNote: 'avg. competitive district, 2020',
      localMargin: 520,
      trend: 'competitive',
      trendNote: 'NC has been within 2 points for 3 consecutive presidential cycles',
      blurb: 'North Carolina keeps getting closer. The Research Triangle is one of the fastest-growing metros in the country and a place where the numbers are genuinely moving — at the presidential level and all the way down the ballot.',
    },
    {
      id: 'charlotte',
      label: 'Charlotte metro',
      sublabel: 'Mecklenburg & suburban counties, NC',
      rent: 1500,
      medianHome: 305000,
      stateMargin: -1.3,
      stateWinner: 'rep',
      legMargin: 1500,
      legNote: 'avg. competitive district, 2020',
      localMargin: 600,
      trend: 'competitive',
      trendNote: 'Charlotte\'s inner suburbs have shifted noticeably since 2016',
      blurb: 'The inner suburbs have moved. Competitive congressional and state legislative races run through this region every cycle, and the trend line is still moving.',
    },
    {
      id: 'columbus',
      label: 'Columbus metro',
      sublabel: 'Franklin County, OH',
      rent: 1515,
      medianHome: 330000,
      stateMargin: -8.1,
      stateWinner: 'rep',
      legMargin: 1200,
      legNote: 'avg. competitive district',
      localMargin: 380,
      trend: 'shifting',
      trendNote: 'Ohio leans red statewide; state leg and congressional races remain competitive',
      blurb: 'Ohio isn\'t a swing state at the presidential level — but Columbus\'s state legislative and congressional districts are among the most competitive in the Midwest. Those are the races that set policy and draw the lines.',
    },
    {
      id: 'pittsburgh',
      label: 'Pittsburgh metro',
      sublabel: 'Southwestern Pennsylvania',
      rent: 1250,
      medianHome: 195000,
      stateMargin: 1.2,
      stateWinner: 'dem',
      legMargin: 2100,
      legNote: 'avg. competitive district, 2020',
      localMargin: 480,
      trend: 'competitive',
      trendNote: 'Pennsylvania decided by 80,555 votes in 2020',
      blurb: 'The most affordable metro on this list with real swing dynamics. Pennsylvania state legislative races run through the suburbs here, and the congressional seats have flipped multiple times since 2018.',
    },
    {
      id: 'lasvegas',
      label: 'Las Vegas metro',
      sublabel: 'Clark County, NV',
      rent: 1600,
      medianHome: 350000,
      stateMargin: 2.4,
      stateWinner: 'dem',
      legMargin: 2200,
      legNote: 'avg. competitive district, 2020',
      localMargin: 700,
      trend: 'competitive',
      trendNote: 'Nevada decided by under 35,000 votes in 2016 and 2020',
      blurb: 'Clark County decides Nevada — full stop. Competitive from school board races up to Senate, and the margin is narrow enough that a concentrated shift in one suburb can change statewide outcomes.',
    },
    {
      id: 'richmond',
      label: 'Richmond metro',
      sublabel: 'Central Virginia',
      rent: 1500,
      medianHome: 320000,
      stateMargin: 10.1,
      stateWinner: 'dem',
      legMargin: 1900,
      legNote: 'avg. competitive district, 2020',
      localMargin: 520,
      trend: 'shifting',
      trendNote: 'VA presidential race is now safe blue; state legislature is where it matters',
      blurb: 'Virginia isn\'t a swing state at the presidential level anymore — but the General Assembly races here are genuinely close, and those are the people who draw the maps and set education policy.',
    },
  ];

  let selectedOriginId = 'nyc';
  let selectedJobId = 'computer';
  let budget = 2500;
  let priority = 'balanced';

  $: origin = origins.find(o => o.id === selectedOriginId);
  $: job = jobCategories.find(j => j.id === selectedJobId);

  function legScore(margin) {
    if (margin < 300)  return 5;
    if (margin < 700)  return 4;
    if (margin < 1500) return 3;
    if (margin < 3000) return 2;
    return 1;
  }
  function presScore(margin) {
    const abs = Math.abs(margin);
    if (abs < 0.5)  return 5;
    if (abs < 1.5)  return 4;
    if (abs < 3)    return 3;
    if (abs < 7)    return 2;
    return 1;
  }

  $: results = destinations
    .map(d => {
      const savings     = origin.rent - d.rent;
      const annualSavings = savings * 12;
      const downPayment = d.medianHome * 0.20;
      const yearsToDown = savings > 0 ? Math.round((downPayment / annualSavings) * 10) / 10 : null;
      const ls          = legScore(d.legMargin);
      const ps          = presScore(d.stateMargin);
      const impactScore = ls * 0.7 + ps * 0.3;
      const savingsScore = Math.min(5, Math.max(0, savings / 400));
      const sortScore   = priority === 'savings' ? savingsScore
        : priority === 'impact' ? impactScore
        : (savingsScore * 0.5 + impactScore * 0.5);
      return { ...d, savings, annualSavings, yearsToDown, ls, ps, impactScore, savingsScore, sortScore };
    })
    .filter(d => d.rent <= budget)
    .sort((a, b) => b.sortScore - a.sortScore);

  function fmtK(n) {
    return n >= 1000 ? `$${Math.round(n / 1000)}K` : `$${n}`;
  }
  function dots(score, max = 5) {
    return Array.from({ length: max }, (_, i) => i < Math.round(score));
  }
  function absMarginLabel(margin) {
    const abs = Math.abs(margin).toFixed(1);
    return `${abs}pt ${margin >= 0 ? 'Dem' : 'Rep'}`;
  }
</script>

<section class="calculator" aria-label="Interactive relocation impact calculator">

  <div class="calc-intro prose">
    <p class="eyebrow mono">What would it mean for you?</p>
    <h2>Run your own numbers</h2>
    <p>
      The same clustering that produces the surplus-vote pattern also
      produces the cost-of-living pattern: NYC median rent is $3,406/mo;
      Columbus is $1,515. That's roughly $23,000 a year. Nine metros
      below sit at the intersection of measurably competitive politics
      and materially lower cost of living. Set your origin, your work
      type, and your budget — the tool ranks them for you.
    </p>
  </div>

  <!-- ── Controls ──────────────────────────────────────────────── -->
  <div class="controls-panel" role="group" aria-label="Calculator inputs">
    <div class="controls-inner">

      <div class="control-block">
        <label for="origin-select" class="control-label mono">Where are you now?</label>
        <div class="select-wrap">
          <select id="origin-select" bind:value={selectedOriginId} class="control-select">
            {#each origins as o}
              <option value={o.id}>{o.label} &nbsp;·&nbsp; ${o.rent.toLocaleString()}/mo</option>
            {/each}
          </select>
        </div>
      </div>

      <div class="control-block">
        <span class="control-label mono">What do you do?</span>
        <div class="job-pills" role="group" aria-label="Job category">
          {#each jobCategories as j}
            <button
              class="job-pill"
              class:active={selectedJobId === j.id}
              on:click={() => selectedJobId = j.id}
              aria-pressed={selectedJobId === j.id}
            >
              <span class="pill-name">{j.label}</span>
              <span class="pill-wfh mono">{j.wfhRate}% remote-eligible</span>
            </button>
          {/each}
        </div>
        {#if job && job.wfhRate < 30}
          <p class="wfh-caution mono">
            Only {job.wfhRate}% of {job.label.toLowerCase()} roles are remote-eligible —
            factor in local employers when weighing destinations.
          </p>
        {/if}
      </div>

      <div class="control-block">
        <label for="budget-slider" class="control-label mono">
          Monthly rent budget: <span class="budget-val">${budget.toLocaleString()}</span>
        </label>
        <input
          id="budget-slider"
          type="range"
          min="1000"
          max="4000"
          step="50"
          bind:value={budget}
          class="budget-slider"
          aria-valuetext="${budget.toLocaleString()} per month"
        />
        <div class="slider-ends mono">
          <span>$1,000</span>
          <span>$4,000</span>
        </div>
      </div>

      <div class="control-block">
        <span class="control-label mono">Sort results by</span>
        <div class="sort-tabs" role="group" aria-label="Sort order">
          <button class:active={priority === 'savings'} on:click={() => priority = 'savings'} aria-pressed={priority === 'savings'}>Monthly savings</button>
          <button class:active={priority === 'impact'}  on:click={() => priority = 'impact'}  aria-pressed={priority === 'impact'}>Civic impact</button>
          <button class:active={priority === 'balanced'} on:click={() => priority = 'balanced'} aria-pressed={priority === 'balanced'}>Both</button>
        </div>
      </div>

    </div>
  </div>

  <!-- ── Results ───────────────────────────────────────────────── -->
  <div class="results-area">
    {#if results.length === 0}
      <div class="no-results prose">
        <p class="mono">
          No destinations fit a ${budget.toLocaleString()}/mo budget.
          Slide the budget up to see options.
        </p>
      </div>
    {:else}
      <p class="results-meta mono">
        {results.length} destination{results.length === 1 ? '' : 's'} within your ${budget.toLocaleString()}/mo budget
        {#if origin}· currently paying ${origin.rent.toLocaleString()}/mo in {origin.label.split(',')[0]}{/if}
      </p>

      <div class="results-grid">
        {#each results as dest, i}
          <article class="result-card" class:card-best={i === 0} aria-label="{dest.label} results">
            {#if i === 0}
              <div class="best-badge mono" aria-hidden="true">Top match</div>
            {/if}

            <div class="card-head">
              <div class="card-location">
                <span class="card-city">{dest.label}</span>
                <span class="card-sublabel mono">{dest.sublabel}</span>
              </div>
              <span class="trend-pill mono trend-{dest.trend}" aria-label="Competitiveness: {dest.trend}">
                {#if dest.trend === 'razor'}Razor thin{:else if dest.trend === 'competitive'}Competitive{:else}Shifting{/if}
              </span>
            </div>

            <!-- Savings -->
            <div class="savings-block">
              {#if dest.savings > 0}
                <span class="savings-num pos mono" aria-label="Save ${dest.savings.toLocaleString()} per month">
                  +${dest.savings.toLocaleString()}<span class="unit">/mo</span>
                </span>
                <span class="savings-annual mono">${dest.annualSavings.toLocaleString()} saved per year</span>
              {:else if dest.savings < 0}
                <span class="savings-num neg mono" aria-label="${Math.abs(dest.savings).toLocaleString()} more per month">
                  ${Math.abs(dest.savings).toLocaleString()}<span class="unit">/mo more</span>
                </span>
              {:else}
                <span class="savings-num mono">Same as now</span>
              {/if}
            </div>

            <!-- Down payment -->
            {#if dest.yearsToDown !== null && dest.savings > 0}
              <div class="down-payment">
                <span class="dp-years mono">{dest.yearsToDown}yr</span>
                <span class="dp-desc">
                  to a 20% down payment on a {fmtK(dest.medianHome)} median home —
                  banking only the rent difference
                </span>
              </div>
            {/if}

            <!-- Impact dots -->
            <div class="impact-section">
              <div class="impact-row" aria-label="State legislature impact: {dest.ls} out of 5">
                <span class="impact-label">State legislature</span>
                <div class="impact-dots" aria-hidden="true">
                  {#each dots(dest.ls) as filled}
                    <span class="dot" class:dot-on={filled}></span>
                  {/each}
                </div>
                <span class="impact-data mono">{dest.legMargin.toLocaleString()} votes · {dest.legNote}</span>
              </div>
              <div class="impact-row" aria-label="Presidential impact: {dest.ps} out of 5">
                <span class="impact-label">Presidential (state)</span>
                <div class="impact-dots" aria-hidden="true">
                  {#each dots(dest.ps) as filled}
                    <span class="dot" class:dot-on={filled}></span>
                  {/each}
                </div>
                <span class="impact-data mono">{absMarginLabel(dest.stateMargin)} · 2020</span>
              </div>
            </div>

            <p class="card-blurb">{dest.blurb}</p>
            <p class="card-trend-note mono">{dest.trendNote}</p>
          </article>
        {/each}
      </div>
    {/if}

    <p class="data-note mono">
      Election data: MIT Election Lab 2020. Rent: Zillow ZORI 2024–25.
      Home prices: Zillow ZHVI 2024–25. Remote-eligibility: BLS ATUS 2023.
      State legislative margins: OpenElections + MIT Election Lab.
    </p>
  </div>

</section>

<style>
  /* ── Section wrapper ─────────────────────────────────────────── */
  .calculator {
    background: var(--color-bg);
    padding-bottom: 6rem;
  }

  .calc-intro {
    padding: 6rem 1.5rem 3rem;
    max-width: var(--max-prose);
    margin: 0 auto;
  }
  .eyebrow {
    font-size: 0.75rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--color-text-muted);
    margin-bottom: 1rem;
  }
  .calc-intro h2 { margin-bottom: 1rem; }
  .calc-intro p  { color: var(--color-text-muted); }

  /* ── Controls panel ──────────────────────────────────────────── */
  .controls-panel {
    background: #f3f4f6;
    padding: 3rem 1.5rem;
  }
  .controls-inner {
    max-width: var(--max-wide);
    margin: 0 auto;
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 2.5rem 3rem;
  }
  .control-block {
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
  }
  .control-label {
    font-size: 0.75rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #4b5563;
  }
  .budget-val {
    color: var(--color-competitive);
    letter-spacing: 0;
  }

  /* Select */
  .select-wrap {
    position: relative;
  }
  .select-wrap::after {
    content: '▾';
    position: absolute;
    right: 1rem;
    top: 50%;
    transform: translateY(-50%);
    color: #9ca3af;
    pointer-events: none;
    font-size: 0.875rem;
  }
  .control-select {
    width: 100%;
    appearance: none;
    background: #fff;
    color: var(--color-text);
    border: 1px solid #d1d5db;
    border-radius: 4px;
    padding: 0.75rem 2.5rem 0.75rem 1rem;
    font-family: var(--font-sans);
    font-size: 0.9375rem;
    cursor: pointer;
    line-height: 1.4;
  }
  .control-select:focus {
    outline: 2px solid var(--color-competitive);
    outline-offset: 2px;
  }

  /* Job pills */
  .job-pills {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
  }
  .job-pill {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    padding: 0.5rem 0.875rem;
    border: 1px solid #d1d5db;
    border-radius: 4px;
    background: #fff;
    color: #374151;
    cursor: pointer;
    font-size: 0.875rem;
    line-height: 1.3;
    transition: background 0.12s, border-color 0.12s, color 0.12s;
  }
  .job-pill:focus-visible {
    outline: 2px solid var(--color-competitive);
    outline-offset: 2px;
  }
  .job-pill.active {
    background: var(--color-dem);
    border-color: var(--color-dem);
    color: #fff;
  }
  .pill-name { font-weight: 500; }
  .pill-wfh {
    font-size: 0.6875rem;
    color: #9ca3af;
    margin-top: 0.125rem;
  }
  .job-pill.active .pill-wfh { color: rgba(255,255,255,0.65); }

  .wfh-caution {
    font-size: 0.8125rem;
    color: #6b7280;
    line-height: 1.5;
  }

  /* Budget slider */
  .budget-slider {
    -webkit-appearance: none;
    appearance: none;
    width: 100%;
    height: 4px;
    background: #d1d5db;
    border-radius: 2px;
    outline: none;
    cursor: pointer;
  }
  .budget-slider::-webkit-slider-thumb {
    -webkit-appearance: none;
    width: 22px;
    height: 22px;
    border-radius: 50%;
    background: var(--color-competitive);
    cursor: pointer;
    box-shadow: 0 0 0 3px rgba(217,119,6,0.25);
    transition: box-shadow 0.12s;
  }
  .budget-slider::-moz-range-thumb {
    width: 22px;
    height: 22px;
    border-radius: 50%;
    background: var(--color-competitive);
    border: none;
    cursor: pointer;
  }
  .budget-slider:focus-visible::-webkit-slider-thumb {
    box-shadow: 0 0 0 4px rgba(217,119,6,0.4);
  }
  .slider-ends {
    display: flex;
    justify-content: space-between;
    font-size: 0.6875rem;
    color: #4b5563;
    margin-top: 0.25rem;
  }

  /* Sort tabs */
  .sort-tabs {
    display: flex;
    border: 1px solid #d1d5db;
    border-radius: 4px;
    overflow: hidden;
    align-self: flex-start;
    background: #fff;
  }
  .sort-tabs button {
    flex: 1;
    padding: 0.5625rem 1rem;
    background: transparent;
    border: none;
    border-right: 1px solid #d1d5db;
    color: #6b7280;
    cursor: pointer;
    font-size: 0.875rem;
    font-family: var(--font-sans);
    white-space: nowrap;
    transition: background 0.12s, color 0.12s;
  }
  .sort-tabs button:last-child { border-right: none; }
  .sort-tabs button.active {
    background: var(--color-competitive);
    color: #fff;
  }
  .sort-tabs button:focus-visible {
    outline: 2px solid var(--color-competitive);
    outline-offset: -2px;
  }

  /* ── Results area ────────────────────────────────────────────── */
  .results-area {
    padding: 3rem 1.5rem 0;
    max-width: var(--max-wide);
    margin: 0 auto;
  }
  .results-meta {
    font-size: 0.8125rem;
    color: var(--color-text-muted);
    margin-bottom: 2rem;
    letter-spacing: 0.02em;
  }
  .no-results p {
    color: var(--color-text-muted);
    font-size: 0.9375rem;
    padding: 3rem 0;
  }

  /* Results grid */
  .results-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 1.25rem;
  }

  /* Cards */
  .result-card {
    background: #fff;
    border: 1px solid #e5e7eb;
    border-radius: 8px;
    padding: 1.5rem;
    position: relative;
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }
  .card-best {
    border-color: var(--color-competitive);
    border-width: 2px;
  }
  .best-badge {
    position: absolute;
    top: -1px;
    right: 1rem;
    background: var(--color-competitive);
    color: #fff;
    font-size: 0.6875rem;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    padding: 0.25rem 0.625rem;
    border-radius: 0 0 4px 4px;
  }

  /* Card header */
  .card-head {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    gap: 0.75rem;
  }
  .card-location { display: flex; flex-direction: column; gap: 0.125rem; }
  .card-city {
    font-family: var(--font-serif);
    font-size: 1.125rem;
    font-weight: 700;
    color: var(--color-text);
    line-height: 1.2;
  }
  .card-sublabel {
    font-size: 0.6875rem;
    color: var(--color-text-muted);
    letter-spacing: 0.04em;
  }

  /* Trend pill */
  .trend-pill {
    font-size: 0.6875rem;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    padding: 0.25rem 0.5rem;
    border-radius: 3px;
    white-space: nowrap;
    flex-shrink: 0;
  }
  .trend-razor      { background: #fef3c7; color: #92400e; }
  .trend-competitive { background: #dbeafe; color: #1e40af; }
  .trend-shifting   { background: #f3f4f6; color: #4b5563; }

  /* Savings */
  .savings-block {
    display: flex;
    flex-direction: column;
    gap: 0.125rem;
  }
  .savings-num {
    font-size: clamp(1.75rem, 4vw, 2.25rem);
    font-weight: 500;
    letter-spacing: -0.02em;
    line-height: 1;
  }
  .savings-num.pos  { color: #16a34a; }
  .savings-num.neg  { color: var(--color-rep); }
  .unit { font-size: 0.55em; font-weight: 400; color: inherit; opacity: 0.75; }
  .savings-annual { font-size: 0.8125rem; color: var(--color-text-muted); }

  /* Down payment */
  .down-payment {
    display: flex;
    align-items: baseline;
    gap: 0.5rem;
    background: #f0fdf4;
    border-radius: 4px;
    padding: 0.625rem 0.875rem;
  }
  .dp-years {
    font-size: 1.5rem;
    font-weight: 500;
    color: #16a34a;
    letter-spacing: -0.02em;
    white-space: nowrap;
  }
  .dp-desc {
    font-size: 0.8125rem;
    color: #166534;
    line-height: 1.4;
  }

  /* Impact dots */
  .impact-section {
    display: flex;
    flex-direction: column;
    gap: 0.625rem;
    border-top: 1px solid #f3f4f6;
    padding-top: 1rem;
  }
  .impact-row {
    display: grid;
    grid-template-columns: 8rem auto 1fr;
    align-items: center;
    gap: 0.625rem;
  }
  .impact-label {
    font-size: 0.75rem;
    color: var(--color-text-muted);
    white-space: nowrap;
  }
  .impact-dots {
    display: flex;
    gap: 3px;
  }
  .dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: #e5e7eb;
    flex-shrink: 0;
  }
  .dot.dot-on { background: var(--color-competitive); }
  .impact-data {
    font-size: 0.6875rem;
    color: #6b7280;
    letter-spacing: 0.02em;
    text-align: right;
  }

  /* Card text */
  .card-blurb {
    font-size: 0.875rem;
    color: var(--color-text-muted);
    line-height: 1.55;
    max-width: 100%;
    margin: 0;
  }
  .card-trend-note {
    font-size: 0.6875rem;
    letter-spacing: 0.04em;
    color: #9ca3af;
    margin: 0;
    border-top: 1px solid #f3f4f6;
    padding-top: 0.625rem;
  }

  /* Data footnote */
  .data-note {
    margin-top: 3rem;
    font-size: 0.75rem;
    color: #9ca3af;
    letter-spacing: 0.02em;
    line-height: 1.6;
    max-width: 100%;
  }

  /* ── Responsive ──────────────────────────────────────────────── */
  @media (max-width: 700px) {
    .controls-inner {
      grid-template-columns: 1fr;
      gap: 2rem;
    }
    .results-grid {
      grid-template-columns: 1fr;
    }
    .impact-row {
      grid-template-columns: 7rem auto 1fr;
      gap: 0.375rem;
    }
    .sort-tabs button {
      font-size: 0.8125rem;
      padding: 0.5rem 0.5rem;
    }
  }
</style>
