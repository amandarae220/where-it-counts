// Unit tests for the simulation module. These functions are the
// mathematical core of MoversBudget and the tier classifiers used by
// both interactive tools — worth testing so they don't drift silently.
//
// Framework-free by design (no DOM, no Svelte imports), which is
// why extracting simulate() out of the component paid off. Run with:
//   npm test          # watch mode
//   npm run test:ci   # single run, CI-friendly

import { describe, it, expect } from 'vitest';
import { simulate, stateTier, countyTier } from './simulation.js';

// Fixtures matching real state values from swingStates.js so the tests
// stay defensible against the numbers the piece publicly cites.
const GA = { margin_votes:   11779, margin_pct:  0.24 };  // razor-thin D
const NC = { margin_votes:  -74481, margin_pct: -1.34 };  // competitive R
const TX = { margin_votes: -631221, margin_pct: -5.58 };  // shifting R

describe('simulate()', () => {
  it('preserves the state at zero movers', () => {
    const r = simulate(GA, 'D', 0);
    expect(r.newMargin).toBe(11779);
    expect(r.newPct).toBeCloseTo(0.24, 2);
    expect(r.newParty).toBe('D');
    expect(r.origParty).toBe('D');
    expect(r.flipped).toBe(false);
  });

  it('flips a currently-R state when D allocation exceeds its margin', () => {
    const r = simulate(NC, 'D', 100_000);
    expect(r.newMargin).toBe(25_519);      // -74,481 + 100,000
    expect(r.newParty).toBe('D');
    expect(r.origParty).toBe('R');
    expect(r.flipped).toBe(true);
  });

  it('does NOT flip when D allocation is below the R margin', () => {
    const r = simulate(NC, 'D', 50_000);
    expect(r.newMargin).toBe(-24_481);     // -74,481 + 50,000
    expect(r.newParty).toBe('R');
    expect(r.flipped).toBe(false);
  });

  it('expands the D cushion when allocating D into an already-D state', () => {
    const r = simulate(GA, 'D', 20_000);
    expect(r.newMargin).toBeGreaterThan(GA.margin_votes);
    expect(r.newParty).toBe('D');
    expect(r.flipped).toBe(false);
  });

  it('flips a currently-D state when R allocation exceeds the D margin', () => {
    const r = simulate(GA, 'R', 15_000);
    expect(r.newMargin).toBe(-3_221);      // 11,779 - 15,000
    expect(r.newParty).toBe('R');
    expect(r.origParty).toBe('D');
    expect(r.flipped).toBe(true);
  });

  it('preserves the vote-to-pct ratio in the projected margin percentage', () => {
    // Doubling the raw margin should double the percentage margin.
    // GA at rest: 11,779 votes ≈ 0.24 pts.
    // After +11,779 D movers: 23,558 votes ≈ 0.48 pts.
    const r = simulate(GA, 'D', 11_779);
    expect(r.newPct).toBeCloseTo(0.48, 2);
  });

  it('handles the "meaningful shift takes thousands, not hundreds" claim honestly', () => {
    // TX at R+5.58 (631K votes) — even a 100K reallocation barely dents it.
    const r = simulate(TX, 'D', 100_000);
    expect(r.newParty).toBe('R');
    expect(r.flipped).toBe(false);
    // Margin narrows but stays comfortably R
    expect(Math.abs(r.newPct)).toBeGreaterThan(4);
  });
});

describe('stateTier()', () => {
  it('classifies under 1 pt as razor thin', () => {
    expect(stateTier(0.24).key).toBe('razor');
    expect(stateTier(-0.5).key).toBe('razor');
    expect(stateTier(0.99).key).toBe('razor');
  });

  it('classifies 1–3 pts as competitive', () => {
    expect(stateTier(1.0).key).toBe('competitive');
    expect(stateTier(2.5).key).toBe('competitive');
    expect(stateTier(-2.99).key).toBe('competitive');
  });

  it('classifies 3 pts and above as shifting', () => {
    expect(stateTier(3.0).key).toBe('shifting');
    expect(stateTier(-5.58).key).toBe('shifting');
    expect(stateTier(15).key).toBe('shifting');
  });

  it('treats R and D margins symmetrically (absolute value)', () => {
    expect(stateTier(0.5).key).toBe(stateTier(-0.5).key);
    expect(stateTier(2).key).toBe(stateTier(-2).key);
    expect(stateTier(4).key).toBe(stateTier(-4).key);
  });

  it('returns both a key and a human label', () => {
    const t = stateTier(0.24);
    expect(t).toHaveProperty('key');
    expect(t).toHaveProperty('label');
    expect(t.label).toBe('Razor thin');
  });
});

describe('countyTier()', () => {
  it('uses wider thresholds than stateTier — 5 pts is still competitive at county level', () => {
    expect(countyTier(5).key).toBe('competitive');
    expect(stateTier(5).key).toBe('shifting');
  });

  it('classifies under 2 pts as razor thin', () => {
    expect(countyTier(1.9).key).toBe('razor');
    expect(countyTier(-0.5).key).toBe('razor');
  });

  it('classifies 2–8 pts as competitive', () => {
    expect(countyTier(2).key).toBe('competitive');
    expect(countyTier(7.9).key).toBe('competitive');
    expect(countyTier(-5).key).toBe('competitive');
  });

  it('classifies 8 pts and above as shifting', () => {
    expect(countyTier(8).key).toBe('shifting');
    expect(countyTier(20).key).toBe('shifting');
    expect(countyTier(-15).key).toBe('shifting');
  });
});
