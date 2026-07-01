// Shared source of truth for the 9 battleground states used across
// MapMoves (ranking + drill-in) and MoversBudget (allocation + impact).
// Extract-to-module avoids the two components drifting out of sync.
//
// Field notes:
// - margin_votes: positive = Biden won by that many, negative = Trump.
// - margin_pct:   same convention as votes; percentage points.
// - ev:           electoral votes under post-2020 census apportionment
//                 (applies to 2024 and 2028 elections).
// - comp_leg:     count of state-legislative districts within a 5-pt
//                 margin in 2020/2022 (state house + senate combined).
// - total_leg:    total seats in the state legislature (house + senate).
//
// Sources: MIT Election Lab (2020 pres) · OpenElections + Ballotpedia
// (state-leg margins) · Census 2020 reapportionment (EV counts).

export const SWING_STATES = [
  { code: 'GA', name: 'Georgia',        ev: 16, margin_votes:   11779, margin_pct:  0.24, comp_leg: 9,  total_leg: 236 },
  { code: 'AZ', name: 'Arizona',        ev: 11, margin_votes:   10457, margin_pct:  0.31, comp_leg: 7,  total_leg:  90 },
  { code: 'WI', name: 'Wisconsin',      ev: 10, margin_votes:   20682, margin_pct:  0.63, comp_leg: 10, total_leg: 132 },
  { code: 'PA', name: 'Pennsylvania',   ev: 19, margin_votes:   80555, margin_pct:  1.17, comp_leg: 12, total_leg: 253 },
  { code: 'MI', name: 'Michigan',       ev: 15, margin_votes:  154188, margin_pct:  2.78, comp_leg: 8,  total_leg: 148 },
  { code: 'NC', name: 'North Carolina', ev: 16, margin_votes:  -74481, margin_pct: -1.34, comp_leg: 6,  total_leg: 170 },
  { code: 'NV', name: 'Nevada',         ev:  6, margin_votes:   33596, margin_pct:  2.39, comp_leg: 4,  total_leg:  63 },
  { code: 'FL', name: 'Florida',        ev: 30, margin_votes: -371686, margin_pct: -3.36, comp_leg: 8,  total_leg: 160 },
  { code: 'TX', name: 'Texas',          ev: 40, margin_votes: -631221, margin_pct: -5.58, comp_leg: 14, total_leg: 181 },
];

// 2020 presidential result recomputed under post-2020 EV apportionment.
// Biden's states lose ~3 EVs net; Trump's gain ~3.
export const BASELINE_D_EV = 303;
export const BASELINE_R_EV = 235;

// Census state FIPS codes for the 9 battleground states. Used by both
// StateMiniMap (per-state drill-in) and AllocationMap (national impact
// visualization) to join simulation results to TopoJSON state features.
export const SWING_STATE_FIPS = {
  GA: '13', AZ: '04', WI: '55', PA: '42', MI: '26',
  NC: '37', NV: '32', FL: '12', TX: '48',
};

// Reference anchors for the Movers Budget tool.
// Every "budget" the user selects gets contextualized against these
// real numbers — not aspirational scenarios.
export const REFERENCES = {
  annualInterstate: {
    value: 8_000_000,
    label: 'US annual interstate movement',
    source: 'Census ACS 2022',
  },
  katrinaHouston: {
    value: 250_000,
    label: "Katrina's Houston displacement",
    source: 'US Census / HUD, 2005',
  },
  mariaFlorida: {
    value: 500_000,
    label: "Post-Maria Puerto Rico → Florida",
    source: 'US Census, 2017–2022',
  },
  gaAnnualNet: {
    value: 127_000,
    label: 'Net movers to Georgia, 2022',
    source: 'Census ACS 2022',
  },
  swingMargin2020: {
    value: 43_000,
    label: 'Combined 2020 margin: GA + AZ + WI',
    source: 'MIT Election Lab',
  },
};
