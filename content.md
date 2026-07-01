# Content Review — Where It Counts

Single-page site. ROI thesis. All user-facing prose in scroll order,
with the source file linked next to each section so edits land in
the right place.

---

## 1. Hero
*Inline at [+page.svelte](src/routes/+page.svelte)*

> **A data journalism project**
>
> # Make it count
>
>     In 2020, 76 million votes were cast in places where the outcome
      where the margin was not in question. Because of geography.
      Here's what the data says about where yours would actually matter,
      and what moving could change. 

    It's one of the most common reasons Americans give for not voting.
      And here's the uncomfortable truth: they're not entirely wrong.
      Not because their vote doesn't count — it does. It's because of
      <em>where they live</em>. Stay with me.

 "My vote doesn't matter." It's one of the most common reasons Americans give for not voting. And while this isn't true, it acknowledges the fact that some  In 2020, 76 million votes were cast in places where the margin was never in question — not thrown out, just cast somewhere geography had settled the result long before anyone showed up. So stay with me: here's what the data says about where your vote would actually move something, and what a move could change.

Here's something nobody tells you: a handful of places decide almost every election. Everywhere else, the outcome's basically locked in before you show up. Which kind of place you live in is the whole game — and politicians figured that out ages ago. It's why they're so picky about their address. Good news: you get to be picky too.
>
> *[CTA: See the data ↓]*

---

## 2. Two Moves + Mechanism note
*Inline at [+page.svelte](src/routes/+page.svelte)*

> **Same instinct, two moves**
>
> # Politicians Have Always Treated Location as Strategy.
>
> Start with the big ones — president, senator, governor. Nobody draws districts for those. What decides them is simpler: over the years, people sorted themselves. We moved for jobs, for weather, for the cost of living, for the vibe — and whole states quietly slid into one column and stayed. That's the engine under all of it. Politicians didn't build it. They just learned to use it two ways.
>
> ### 01 — They pick their spot
> They move to where they can win. A state senate hopeful picks a district that already leans their way. Someone running for Congress rents an apartment in a swing seat. They're not drawing the map — just standing in a good spot on it. Both parties, every level. It's legal, it's out in the open, and once you notice it you can't unsee it.
> **What this affects:** Every race, president to school board. Anywhere location shapes the odds.
>
> ### 02 — They draw the lines
> For races that do have districts, whoever's in power gets a second move. Every ten years they redraw the lines — cramming the other side into a few districts, spreading their own people out to win more. That's gerrymandering. It only works because we've already sorted ourselves; the lines just press harder on it.
> **What this affects:** U.S. House. State house and senate. Anywhere district lines get drawn.
>
> > You've got the same map they do — the same numbers, the same freedom to pack up and move. The only question is whether you ever use it.
>
> **THE COMMON THREAD.**
> So here's the whole thing in one breath: sorting decides the big races, sorting plus map-drawing decides the district ones. Either way it shakes out the same — most votes get cast where the result was never close, and a few get cast where it all comes down to the wire. Whether your vote is *decisive or surplus* comes down to where you live. The rest of this is us showing you that math — and what you'd actually do about it. No yard signs, no doorknocking.

---

## 3. StatBreaker — 216× / 146×
File: [StatBreaker.svelte](src/lib/components/sections/StatBreaker.svelte)

> **What the data actually shows**
>
> California surplus votes, 2020: **2,552,143** vs Georgia's entire margin, 2020: **11,779**
>
> # 216×
> *California's surplus was 216 times Georgia's decisive margin. Those votes couldn't cross state lines — that's precisely what makes geography so decisive.*
>
> ---
>
> # 146×
> *The surplus across nine safe blue states — 6.3M votes — was 146 times the combined margin that decided GA + AZ + WI: 43K votes.*
>
> Three states. 37 electoral votes. Decided by fewer people than fit in a sold-out football stadium.

---

## 4. Scrollytelling map (5 steps)
*Defined in [+page.svelte](src/routes/+page.svelte), rendered through [Scrollytelling.svelte](src/lib/components/Scrollytelling.svelte)*

> **Step 1 (intro):** Each dot on this map is a county. The deeper the color, the more votes accumulated beyond what determined the outcome. Both parties. Every county.
>
> **Step 2 (11.8M blue surplus):** Across safe blue counties nationwide, Democratic votes accumulated 11.8 million beyond what their winners needed. New York City alone: 1.3 million. LA County: 897,000. Cook County: 565,000.
>
> **Step 3 (8.6M red surplus):** Republican surplus votes totaled 8.6 million — real, but smaller. The biggest single surplus GOP county had 57,000 votes beyond the margin. LA County's Democratic surplus is 15× larger.
>
> **Step 4 (76M total):** Combined, 76 million votes — nearly half of all votes cast in 2020 — went to places where the margin was not in question. They were counted. But the result in those places was settled before they were cast. Because of geography.
>
> **Step 5 (zoom to AZ/GA/WI):** Meanwhile, three swing states that together carried 37 electoral votes were decided by a combined 43,000 votes. Less than a sold-out football stadium. Georgia alone: 11,779 people.

---

## 5. State Races: Even Smaller
*Inline at [+page.svelte](src/routes/+page.svelte)*

> **Zoom out further**
>
> # State races are decided by even fewer people.
>
> Presidential margins get the headlines. State legislative seats are where the floors actually move — and they turn on numbers small enough to fit in a single apartment building.
>
> - **139** — votes decided · WI Assembly · District 73 · 2020
> - **280** — votes decided · GA House · District 35 · 2020
> - **582** — votes decided · WI State Senate · District 32 · 2020
>
> These are the people who draw the maps, set school curricula, decide healthcare access, and control what goes on your ballot. Seven Georgia House districts were decided by fewer than 1,000 votes. Twenty-six Wisconsin Assembly districts by fewer than 5,000.

---

## 6. MapMoves — the leverage tool
File: [MapMoves.svelte](src/lib/components/sections/MapMoves.svelte)

> **The interactive**
>
> # How the map could move.
>
> Pick a direction. Set what stays safe. The tool ranks nine 2024 battleground states by combined presidential and state-legislative leverage, then drills into the counties inside each one where a single move would count twice.
>
> *Controls:* Shift the map toward [Democratic | Republican] · Presidential vs. state-leg weight slider · Holding all states currently >±5 pts in their column. At realistic relocation volumes, every safe state stays safe.
>
> *Drill intro (per state):* Top counties in [State] ranked by leverage per mover — largest electorates × closest current margins. Hover a card to see where the county sits in the state. The "votes to flip" column shows the net shift it would need to swing toward [Democratic | Republican].
>
> *Method:* Presidential leverage scaled by closeness of 2020 margin; state-leg leverage scaled by share of chamber seats currently within 5 points. Combined per the weight slider above. County leverage = total votes cast ÷ (1 + |margin %|). Sources: MIT Election Lab · OpenElections · Ballotpedia · Census 2020 reapportionment.

---

## 7. Calculator — Run your own numbers
File: [Calculator.svelte](src/lib/components/sections/Calculator.svelte)

> **What would it mean for you?**
>
> # Run your own numbers
>
> The same clustering that produces the surplus-vote pattern also produces the cost-of-living pattern: NYC median rent is $3,406/mo; Columbus is $1,515. That's roughly $23,000 a year. Nine metros below sit at the intersection of measurably competitive politics and materially lower cost of living. Set your origin, your work type, and your budget — the tool ranks them for you.

*Destination card prose (9 metros):*

| Metro | Blurb | Trend note |
|---|---|---|
| **Atlanta suburbs (Cobb/Gwinnett)** | Cobb and Gwinnett counties flipped presidential in 2020 for the first time in a generation. State legislative races here are decided by hundreds of votes — and they control who draws the next map in 2031. | Georgia decided by 11,779 votes in 2020 |
| **Phoenix suburbs (Maricopa)** | Maricopa County has more registered voters than 15 entire states. Competitive at every level — school board, state legislature, U.S. Senate — and still moving. | Arizona decided by 10,457 votes in 2020 |
| **Milwaukee metro** | One of the most affordable metros among genuinely competitive swing regions. WI Senate District 32 was decided by 582 votes. The suburbs here are where statewide elections turn. | Wisconsin decided by 20,682 votes in 2020 |
| **Raleigh–Durham** | North Carolina keeps getting closer. The Research Triangle is one of the fastest-growing metros in the country and a place where the numbers are genuinely moving — at the presidential level and all the way down the ballot. | NC has been within 2 points for 3 consecutive presidential cycles |
| **Charlotte metro** | The inner suburbs have moved. Competitive congressional and state legislative races run through this region every cycle, and the trend line is still moving. | Charlotte's inner suburbs have shifted noticeably since 2016 |
| **Columbus metro** | Ohio isn't a swing state at the presidential level — but Columbus's state legislative and congressional districts are among the most competitive in the Midwest. Those are the races that set policy and draw the lines. | Ohio leans red statewide; state leg and congressional races remain competitive |
| **Pittsburgh metro** | The most affordable metro on this list with real swing dynamics. Pennsylvania state legislative races run through the suburbs here, and the congressional seats have flipped multiple times since 2018. | Pennsylvania decided by 80,555 votes in 2020 |
| **Las Vegas metro** | Clark County decides Nevada — full stop. Competitive from school board races up to Senate, and the margin is narrow enough that a concentrated shift in one suburb can change statewide outcomes. | Nevada decided by under 35,000 votes in 2016 and 2020 |
| **Richmond metro** | Virginia isn't a swing state at the presidential level anymore — but the General Assembly races here are genuinely close, and those are the people who draw the maps and set education policy. | VA presidential race is now safe blue; state legislature is where it matters |

---

## 8. Closer — The map resets in 2030
*Inline at [+page.svelte](src/routes/+page.svelte)*

> **The timing**
>
> # The map resets in 2030.
>
> Every ten years, after the Census, every district in the country gets redrawn based on where people actually live. The next count is April 2030. The new maps arrive for 2031.
>
> A meaningful shift in a state-legislative district's math takes thousands of movers, not hundreds. That's the honest scale of the ask. This is a long-form civic move, not a stunt — and it's the only one where a single household decision reallocates political leverage the same way it reallocates real estate value.
>
> *For the intellectual grounding of the surplus-vote framing, see Jonathan Rodden,* Why Cities Lose *(2019), which documents the geographic concentration of Democratic votes that produces the pattern this piece visualizes.*

---

## 9. Footer
*Inline at [+page.svelte](src/routes/+page.svelte)*

> All data public and free. Sources: MIT Election Lab · U.S. Census ACS · Bureau of Labor Statistics · Zillow Research · OpenElections · Ballotpedia · Bureau of Economic Analysis.

---

# Inert component files (no longer imported)

The following sections lived on the deleted `/the-case` route and are
no longer part of the piece. Files still exist on disk; delete when
convenient:

- [Hero.svelte](src/lib/components/sections/Hero.svelte) *(was unused already)*
- [HowLinesDrawn.svelte](src/lib/components/sections/HowLinesDrawn.svelte)
- [DistrictShopping.svelte](src/lib/components/sections/DistrictShopping.svelte)
- [Nobody.svelte](src/lib/components/sections/Nobody.svelte)
- [LongGame.svelte](src/lib/components/sections/LongGame.svelte) *(the 2031 timing beat was rewritten inline as the new closer)*
