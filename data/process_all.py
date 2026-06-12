"""
Full data proof of concept — Where It Counts
Combines:
  - County-level 2020 election surplus (tonmcg/GitHub mirror of county results)
  - Zillow ZHVI + ZORI for metro cost-of-living comparison (April 2026)
  - State-level surplus from surplus_calc.py

Outputs: proof_of_concept.json
"""

import csv, json

ZHVI_LATEST = "2026-04-30"
ZORI_LATEST = "2026-04-30"

# --- 1. COUNTY SURPLUS -------------------------------------------------

county_rows = []
with open("data/county_pres_2020.csv") as f:
    for row in csv.DictReader(f):
        dem   = int(row["votes_dem"])
        gop   = int(row["votes_gop"])
        total = int(row["total_votes"])
        if total == 0:
            continue
        min_to_win   = total / 2 + 1
        winner       = "dem" if dem > gop else "gop"
        winner_votes = max(dem, gop)
        loser_votes  = min(dem, gop)
        surplus      = winner_votes - min_to_win
        county_rows.append({
            "state":    row["state_name"],
            "fips":     row["county_fips"],
            "county":   row["county_name"],
            "dem":      dem,
            "gop":      gop,
            "total":    total,
            "winner":   winner,
            "surplus":  int(surplus),
            "loser_wasted": int(loser_votes),
            "margin":   abs(dem - gop),
            "margin_pct": round(abs(float(row["per_point_diff"])) * 100, 2),
        })

total_dem_surplus = sum(r["surplus"] for r in county_rows if r["winner"] == "dem")
total_gop_surplus = sum(r["surplus"] for r in county_rows if r["winner"] == "gop")
total_all_wasted  = sum(r["surplus"] + r["loser_wasted"] for r in county_rows)

# Top 10 most wasteful counties for each party
top_dem_waste = sorted([r for r in county_rows if r["winner"] == "dem"],
                        key=lambda x: x["surplus"], reverse=True)[:10]
top_gop_waste = sorted([r for r in county_rows if r["winner"] == "gop"],
                        key=lambda x: x["surplus"], reverse=True)[:10]

# Closest counties — the real battlegrounds
closest = sorted(county_rows, key=lambda x: x["margin"])[:20]

print("=" * 65)
print("COUNTY-LEVEL SURPLUS — TOP DEM WASTE")
print("=" * 65)
for r in top_dem_waste:
    print(f"  {r['county']}, {r['state']:<20} surplus: {r['surplus']:>8,}")

print()
print("=" * 65)
print("COUNTY-LEVEL SURPLUS — TOP GOP WASTE")
print("=" * 65)
for r in top_gop_waste:
    print(f"  {r['county']}, {r['state']:<20} surplus: {r['surplus']:>8,}")

print()
print("=" * 65)
print("CLOSEST COUNTIES — decided by the fewest votes")
print("=" * 65)
for r in closest[:10]:
    print(f"  {r['county']}, {r['state']:<20} margin: {r['margin']:>6,}  ({r['winner'].upper()})")

print()
print(f"Total Dem county surplus nationwide:  {total_dem_surplus:>10,}")
print(f"Total GOP county surplus nationwide:  {total_gop_surplus:>10,}")
print(f"Total wasted votes nationwide:        {total_all_wasted:>10,}")


# --- 2. COST OF LIVING -------------------------------------------------

name_fixes = {
    "Los Angeles, CA": "Los Angeles-Long Beach-Anaheim, CA",
}

zhvi, zori = {}, {}
with open("data/zhvi_metro.csv") as f:
    for row in csv.DictReader(f):
        n = name_fixes.get(row["RegionName"], row["RegionName"])
        v = row.get(ZHVI_LATEST, "")
        if v: zhvi[n] = int(float(v))

with open("data/zori_metro.csv") as f:
    for row in csv.DictReader(f):
        n = name_fixes.get(row["RegionName"], row["RegionName"])
        v = row.get(ZORI_LATEST, "")
        if v: zori[n] = int(float(v))

metros = {
    "New York, NY":                          {"type": "blue",  "state": "NY"},
    "Los Angeles-Long Beach-Anaheim, CA":    {"type": "blue",  "state": "CA"},
    "San Francisco, CA":                     {"type": "blue",  "state": "CA"},
    "Boston, MA":                            {"type": "blue",  "state": "MA"},
    "Seattle, WA":                           {"type": "blue",  "state": "WA"},
    "Chicago, IL":                           {"type": "blue",  "state": "IL"},
    "Washington, DC":                        {"type": "blue",  "state": "MD"},
    "Atlanta, GA":                           {"type": "swing", "state": "GA"},
    "Phoenix, AZ":                           {"type": "swing", "state": "AZ"},
    "Milwaukee, WI":                         {"type": "swing", "state": "WI"},
    "Philadelphia, PA":                      {"type": "swing", "state": "PA"},
    "Las Vegas, NV":                         {"type": "swing", "state": "NV"},
    "Detroit, MI":                           {"type": "swing", "state": "MI"},
    "Raleigh, NC":                           {"type": "swing", "state": "NC"},
    "Charlotte, NC":                         {"type": "swing", "state": "NC"},
    "Columbus, OH":                          {"type": "swing", "state": "OH"},
    "Nashville, TN":                         {"type": "red",   "state": "TN"},
    "Austin, TX":                            {"type": "red",   "state": "TX"},
}

metro_data = []
for name, info in metros.items():
    hv   = zhvi.get(name, 0)
    rent = zori.get(name, 0)
    metro_data.append({
        "metro": name, **info,
        "home_value": hv,
        "monthly_rent": rent,
    })

# Key comparisons for the brief
print()
print("=" * 65)
print("RENT SAVINGS: moving from blue → competitive metros")
print("=" * 65)
blue_metros = [(m["metro"], m["monthly_rent"]) for m in metro_data
               if m["type"] == "blue" and m["monthly_rent"]]
dest_metros = [(m["metro"], m["monthly_rent"]) for m in metro_data
               if m["type"] in ("swing","red") and m["monthly_rent"]]

for origin, o_rent in sorted(blue_metros, key=lambda x: -x[1]):
    for dest, d_rent in sorted(dest_metros, key=lambda x: x[1])[:3]:
        monthly_save = o_rent - d_rent
        annual_save  = monthly_save * 12
        if monthly_save > 0:
            print(f"  {origin.split(',')[0]:<12} → {dest.split(',')[0]:<12}  "
                  f"saves ${monthly_save:,}/mo  (${annual_save:,}/yr)")
    print()

# --- 3. WRITE COMBINED JSON -------------------------------------------

state_surplus = {
    "CA": 2552143, "NY": 996443, "IL": 512511,
    "MA": 607499,  "WA": 392479, "MD": 504303,
    "NJ": 362542,  "CT": 183056, "OR": 190966,
}

output = {
    "generated": "2026-06-12",
    "sources": {
        "election": "MIT Election Lab via tonmcg/GitHub (county 2020)",
        "housing": f"Zillow Research ZHVI + ZORI ({ZHVI_LATEST})",
    },
    "national_summary": {
        "total_dem_county_surplus": total_dem_surplus,
        "total_gop_county_surplus": total_gop_surplus,
        "total_wasted_votes": total_all_wasted,
        "blue_state_surplus_9_states": 6301942,
        "red_state_surplus_10_states": 1817685,
        "ga_az_wi_combined_margin": 42918,
        "multiplier_blue_surplus_vs_swing_margin": 146,
    },
    "top_wasted_dem": [
        {"county": r["county"], "state": r["state"],
         "surplus": r["surplus"], "margin_pct": r["margin_pct"]}
        for r in top_dem_waste
    ],
    "top_wasted_gop": [
        {"county": r["county"], "state": r["state"],
         "surplus": r["surplus"], "margin_pct": r["margin_pct"]}
        for r in top_gop_waste
    ],
    "closest_counties": [
        {"county": r["county"], "state": r["state"],
         "margin": r["margin"], "winner": r["winner"]}
        for r in closest
    ],
    "metros": metro_data,
    "counties": county_rows,
}

with open("data/proof_of_concept.json", "w") as f:
    json.dump(output, f, indent=2)

print("=" * 65)
print(f"✓ Wrote data/proof_of_concept.json")
print(f"  {len(county_rows):,} counties | {len(metro_data)} metros")
