// Pure simulation helpers shared between MapMoves and MoversBudget.
// Keeps the numerical / classification logic out of Svelte components
// so the same math produces the same result no matter which tool
// invokes it. `swingStates.js` holds the DATA; this module holds the
// LOGIC that operates on it.

/**
 * Simulate `movers` net-new votes into a state, toward the chosen
 * direction. Returns the projected margin (both raw votes and pct),
 * the projected winner, and whether the state flipped from its
 * baseline 2020 result.
 *
 * The pct is recomputed from the baseline vote-to-pct ratio rather
 * than re-derived from the shifted electorate — a small honesty
 * shortcut that drifts at extreme shifts (~500K+ into a razor-thin
 * state) but stays accurate at realistic scales. The MoversBudget
 * method note calls this out explicitly.
 *
 * @param {{ margin_votes: number, margin_pct: number }} state
 * @param {'D' | 'R'} direction
 * @param {number} movers  absolute count of net-new movers
 */
export function simulate(state, direction, movers) {
  const netChange = direction === 'D' ? movers : -movers;
  const newMargin = state.margin_votes + netChange;
  const pctPerVote = state.margin_pct / state.margin_votes;
  const newPct = newMargin * pctPerVote;
  const newParty = newMargin > 0 ? 'D' : 'R';
  const origParty = state.margin_votes > 0 ? 'D' : 'R';
  return {
    newMargin,
    newPct,
    newParty,
    origParty,
    flipped: newParty !== origParty,
  };
}

/**
 * Tier classification for state-level races. Thresholds tuned to the
 * 9-state dataset — every razor-thin battleground is under 1pt, the
 * competitive tier covers 1-3pt, and 3pt+ is "shifting" (still in
 * play at a decade horizon, not razor thin today).
 */
export function stateTier(marginPct) {
  const m = Math.abs(marginPct);
  if (m < 1)  return { key: 'razor',       label: 'Razor thin'  };
  if (m < 3)  return { key: 'competitive', label: 'Competitive' };
  return        { key: 'shifting',    label: 'Shifting'    };
}

/**
 * Tier classification for county-level races. Wider thresholds
 * because a 5-pt county margin is still very much in play, whereas
 * a 5-pt state margin isn't.
 */
export function countyTier(marginPct) {
  const m = Math.abs(marginPct);
  if (m < 2)  return { key: 'razor',       label: 'Razor thin'  };
  if (m < 8)  return { key: 'competitive', label: 'Competitive' };
  return        { key: 'shifting',    label: 'Shifting'    };
}
