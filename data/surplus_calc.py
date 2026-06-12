"""
Surplus vote calculator — 2020 presidential election
Source: FEC certified results (https://www.fec.gov/introduction-campaign-finance/election-results-and-voting-information/)

Core concept: once a state's winner is decided, every vote above the minimum
needed to win is "surplus" — it adds nothing to the Electoral College outcome.
This applies symmetrically to both parties.

Surplus = winner_votes - (total_votes / 2 + 1)
"""

import json

# 2020 presidential certified results by state
# Source: FEC / state certified results
# Format: state, biden, trump, total_ev, ev_winner
RESULTS_2020 = [
    # Safe blue states (Biden wins by large margin)
    {"state": "California",      "biden": 11110250, "trump": 6005961,  "total_ev": 54, "biden_ev": 54},
    {"state": "New York",        "biden": 5244886,  "trump": 3251997,  "total_ev": 29, "biden_ev": 29},
    {"state": "Illinois",        "biden": 3471915,  "trump": 2446891,  "total_ev": 20, "biden_ev": 20},
    {"state": "Massachusetts",   "biden": 2382202,  "trump": 1167202,  "total_ev": 11, "biden_ev": 11},
    {"state": "Washington",      "biden": 2369612,  "trump": 1584651,  "total_ev": 12, "biden_ev": 12},
    {"state": "Maryland",        "biden": 1985023,  "trump": 976414,   "total_ev": 10, "biden_ev": 10},
    {"state": "New Jersey",      "biden": 2608400,  "trump": 1883313,  "total_ev": 14, "biden_ev": 14},
    {"state": "Connecticut",     "biden": 1080831,  "trump": 714717,   "total_ev": 7,  "biden_ev": 7},
    {"state": "Oregon",          "biden": 1340383,  "trump": 958448,   "total_ev": 7,  "biden_ev": 7},
    # Safe red states (Trump wins by large margin)
    {"state": "Wyoming",         "biden": 73491,    "trump": 193559,   "total_ev": 3,  "biden_ev": 0},
    {"state": "West Virginia",   "biden": 235984,   "trump": 545382,   "total_ev": 5,  "biden_ev": 0},
    {"state": "Oklahoma",        "biden": 503890,   "trump": 1020280,  "total_ev": 7,  "biden_ev": 0},
    {"state": "North Dakota",    "biden": 114902,   "trump": 235595,   "total_ev": 3,  "biden_ev": 0},
    {"state": "South Dakota",    "biden": 150471,   "trump": 261043,   "total_ev": 3,  "biden_ev": 0},
    {"state": "Kentucky",        "biden": 772474,   "trump": 1326646,  "total_ev": 8,  "biden_ev": 0},
    {"state": "Alabama",         "biden": 849648,   "trump": 1441170,  "total_ev": 9,  "biden_ev": 0},
    {"state": "Tennessee",       "biden": 1143711,  "trump": 1852475,  "total_ev": 11, "biden_ev": 0},
    {"state": "Arkansas",        "biden": 423932,   "trump": 760647,   "total_ev": 6,  "biden_ev": 0},
    {"state": "Idaho",           "biden": 287021,   "trump": 554119,   "total_ev": 4,  "biden_ev": 0},
    # Swing states — the ones where margins actually decided things
    {"state": "Georgia",         "biden": 2473633,  "trump": 2461854,  "total_ev": 16, "biden_ev": 16},
    {"state": "Arizona",         "biden": 1672143,  "trump": 1661686,  "total_ev": 11, "biden_ev": 11},
    {"state": "Wisconsin",       "biden": 1630866,  "trump": 1610184,  "total_ev": 10, "biden_ev": 10},
    {"state": "Pennsylvania",    "biden": 3458229,  "trump": 3377674,  "total_ev": 20, "biden_ev": 20},
    {"state": "Nevada",          "biden": 703486,   "trump": 669890,   "total_ev": 6,  "biden_ev": 6},
    {"state": "Michigan",        "biden": 2804040,  "trump": 2649852,  "total_ev": 16, "biden_ev": 16},
    {"state": "North Carolina",  "biden": 2684292,  "trump": 2758775,  "total_ev": 15, "biden_ev": 0},
    {"state": "Florida",         "biden": 5297045,  "trump": 5668731,  "total_ev": 30, "biden_ev": 0},
    {"state": "Texas",           "biden": 5259126,  "trump": 5890347,  "total_ev": 40, "biden_ev": 0},
]

def calculate_surplus(biden, trump):
    total = biden + trump  # simplified: excludes third party for cleaner math
    min_to_win = total / 2 + 1
    winner = "biden" if biden > trump else "trump"
    winner_votes = biden if winner == "biden" else trump
    loser_votes = trump if winner == "biden" else biden
    surplus = winner_votes - min_to_win
    margin = abs(biden - trump)
    margin_pct = (margin / total) * 100
    return {
        "winner": winner,
        "margin": int(margin),
        "margin_pct": round(margin_pct, 2),
        "surplus": int(surplus),
        "loser_wasted": int(loser_votes),  # all loser votes are wasted
        "total_wasted": int(surplus + loser_votes),
    }

results = []
for r in RESULTS_2020:
    calc = calculate_surplus(r["biden"], r["trump"])
    results.append({**r, **calc})

# --- KEY NUMBERS FOR THE BRIEF ---

print("=" * 65)
print("SURPLUS VOTES — SAFE BLUE STATES (Biden surplus only)")
print("=" * 65)

safe_blue = ["California", "New York", "Illinois", "Massachusetts",
             "Washington", "Maryland", "New Jersey", "Connecticut", "Oregon"]

total_blue_surplus = 0
for r in results:
    if r["state"] in safe_blue:
        total_blue_surplus += r["surplus"]
        print(f"  {r['state']:<18} Biden surplus: {r['surplus']:>10,}  (margin: {r['margin_pct']}%)")

print(f"\n  TOTAL blue-state surplus:    {total_blue_surplus:>10,}")

print()
print("=" * 65)
print("SURPLUS VOTES — SAFE RED STATES (Trump surplus only)")
print("=" * 65)

safe_red = ["Wyoming", "West Virginia", "Oklahoma", "North Dakota",
            "South Dakota", "Kentucky", "Alabama", "Tennessee", "Arkansas", "Idaho"]

total_red_surplus = 0
for r in results:
    if r["state"] in safe_red:
        total_red_surplus += r["surplus"]
        print(f"  {r['state']:<18} Trump surplus: {r['surplus']:>10,}  (margin: {r['margin_pct']}%)")

print(f"\n  TOTAL red-state surplus:     {total_red_surplus:>10,}")

print()
print("=" * 65)
print("SWING STATE MARGINS — where it was actually decided")
print("=" * 65)

swing = ["Georgia", "Arizona", "Wisconsin", "Pennsylvania", "Nevada", "Michigan"]
total_swing_margin = 0
for r in results:
    if r["state"] in swing:
        total_swing_margin += r["margin"]
        winner_label = "Biden" if r["winner"] == "biden" else "Trump"
        print(f"  {r['state']:<18} {winner_label} +{r['margin']:>7,}  ({r['margin_pct']}%)")

print(f"\n  Combined margin across all 6 swing states: {total_swing_margin:>7,}")

print()
print("=" * 65)
print("THE HEADLINE NUMBERS")
print("=" * 65)
closest_3_margin = 11779 + 10457 + 20682  # GA + AZ + WI
print(f"  Blue-state surplus (9 states):        {total_blue_surplus:>10,}")
print(f"  Red-state surplus (10 states):        {total_red_surplus:>10,}")
print(f"  Combined margin GA + AZ + WI:         {closest_3_margin:>10,}")
print(f"  Blue surplus is {total_blue_surplus // closest_3_margin}x the GA+AZ+WI combined margin")
print()
print(f"  CA surplus alone vs GA margin:        {results[0]['surplus']:,} vs 11,779")
print(f"  CA surplus could flip GA {results[0]['surplus'] // 11779}x over")
print()

# --- NYC COUNTY-LEVEL NOTE ---
print("=" * 65)
print("NYC BOROUGH BREAKDOWN (2020) — for the brief's 1.4M claim")
print("=" * 65)
# Source: NYC Board of Elections certified results
nyc_boroughs = [
    {"name": "Manhattan",    "biden": 354504,  "trump": 24100},
    {"name": "Brooklyn",     "biden": 564186,  "trump": 75204},
    {"name": "Queens",       "biden": 441033,  "trump": 116068},
    {"name": "Bronx",        "biden": 250192,  "trump": 31130},
    {"name": "Staten Island","biden": 70210,   "trump": 116580},
]
nyc_biden = sum(b["biden"] for b in nyc_boroughs)
nyc_trump = sum(b["trump"] for b in nyc_boroughs)
nyc_net = nyc_biden - nyc_trump

ny_state = next(r for r in results if r["state"] == "New York")

print(f"  NYC total Biden:              {nyc_biden:>10,}")
print(f"  NYC total Trump:              {nyc_trump:>10,}")
print(f"  NYC net margin (Biden-Trump): {nyc_net:>10,}")
print(f"  NY State Biden surplus:       {ny_state['surplus']:>10,}")
print()
print(f"  NOTE: The brief says '1.4M more votes than NY State needed.'")
print(f"  NYC's net margin alone ({nyc_net:,}) is the more accurate")
print(f"  plain-language version of this — NYC generated a {nyc_net:,}-vote")
print(f"  net advantage while NY only needed {ny_state['margin']:,} to be called.")
print(f"  Recommend updating the brief to use {nyc_net:,} or the state")
print(f"  surplus figure ({ny_state['surplus']:,}) — both are defensible.")

# --- WRITE JSON OUTPUT ---
output = {
    "safe_blue_surplus_total": total_blue_surplus,
    "safe_red_surplus_total": total_red_surplus,
    "swing_state_margins": {
        r["state"]: {"margin": r["margin"], "margin_pct": r["margin_pct"], "winner": r["winner"]}
        for r in results if r["state"] in swing
    },
    "by_state": results,
    "nyc": {
        "boroughs": nyc_boroughs,
        "net_margin": nyc_net,
        "biden_total": nyc_biden,
        "trump_total": nyc_trump,
    }
}

with open("/Users/manders/where-it-counts/data/surplus_2020.json", "w") as f:
    json.dump(output, f, indent=2)

print()
print("✓ Data written to data/surplus_2020.json")
