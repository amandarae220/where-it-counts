"""
State legislative margin calculator
Processes OpenElections precinct/ward data into district-level margins.
Shows how small the winning margins are in state legislature races —
the "few hundred votes" argument for the brief.
"""

import csv, json
from collections import defaultdict

def process_state(filepath, state_abbr, office_filter, vote_col,
                  candidate_col="candidate", district_col="district",
                  party_col="party"):
    """Aggregate precinct/ward rows into district totals, return margins."""
    districts = defaultdict(lambda: defaultdict(int))

    with open(filepath) as f:
        for row in csv.DictReader(f):
            if row.get("office","").strip() not in office_filter:
                continue
            district = row.get(district_col,"").strip()
            candidate = row.get(candidate_col,"").strip()
            party = row.get(party_col,"").strip().upper()
            try:
                votes = int(row.get(vote_col, 0) or 0)
            except ValueError:
                continue
            if not district or not candidate or votes == 0:
                continue
            # Key by party bucket: DEM / REP / OTHER
            if party in ("DEM","DEMOCRATIC","D"):
                bucket = "DEM"
            elif party in ("REP","REPUBLICAN","R"):
                bucket = "REP"
            else:
                bucket = "OTHER"
            districts[district][bucket] += votes

    results = []
    for district, totals in districts.items():
        dem = totals.get("DEM", 0)
        rep = totals.get("REP", 0)
        total = dem + rep + totals.get("OTHER", 0)
        if total == 0 or (dem == 0 and rep == 0):
            continue
        margin = abs(dem - rep)
        winner = "DEM" if dem > rep else "REP"
        margin_pct = round(margin / total * 100, 2) if total else 0
        results.append({
            "state": state_abbr,
            "district": district,
            "dem": dem,
            "rep": rep,
            "total": total,
            "winner": winner,
            "margin": margin,
            "margin_pct": margin_pct,
            "competitive": margin < 5000,
        })

    return sorted(results, key=lambda x: x["margin"])


# --- GA State House ----------------------------------------------------
ga_house = process_state(
    "/Users/manders/where-it-counts/data/openelec_ga_2020.csv",
    state_abbr="GA",
    office_filter={"State House"},
    vote_col=None,   # GA uses split vote columns — handle below
    candidate_col="candidate",
    district_col="district",
    party_col="party",
)

# GA has election_day_votes, advanced_votes, absentee_by_mail_votes, provisional_votes
# Re-process GA with summed vote columns
ga_districts = defaultdict(lambda: defaultdict(int))
with open("/Users/manders/where-it-counts/data/openelec_ga_2020.csv") as f:
    for row in csv.DictReader(f):
        if row.get("office","").strip() != "State House":
            continue
        district = row.get("district","").strip()
        party = row.get("party","").strip().upper()
        candidate = row.get("candidate","").strip()
        if not district or not candidate:
            continue
        try:
            votes = (int(row.get("election_day_votes") or 0) +
                     int(row.get("advanced_votes") or 0) +
                     int(row.get("absentee_by_mail_votes") or 0) +
                     int(row.get("provisional_votes") or 0))
        except (ValueError, KeyError):
            continue
        bucket = "DEM" if "DEM" in party else ("REP" if "REP" in party else "OTHER")
        ga_districts[district][bucket] += votes

ga_house = []
for district, totals in ga_districts.items():
    dem = totals.get("DEM", 0)
    rep = totals.get("REP", 0)
    total = dem + rep + totals.get("OTHER", 0)
    if dem == 0 and rep == 0:
        continue
    margin = abs(dem - rep)
    winner = "DEM" if dem > rep else "REP"
    margin_pct = round(margin / total * 100, 2) if total else 0
    ga_house.append({
        "state": "GA", "district": district,
        "dem": dem, "rep": rep, "total": total,
        "winner": winner, "margin": margin, "margin_pct": margin_pct,
    })
ga_house.sort(key=lambda x: x["margin"])

# --- WI State Assembly ------------------------------------------------
wi_assembly = process_state(
    "/Users/manders/where-it-counts/data/openelec_wi_2020.csv",
    state_abbr="WI",
    office_filter={"State Assembly"},
    vote_col="votes",
    candidate_col="candidate",
    district_col="district",
    party_col="party",
)

# --- WI State Senate ---------------------------------------------------
wi_senate = process_state(
    "/Users/manders/where-it-counts/data/openelec_wi_2020.csv",
    state_abbr="WI",
    office_filter={"State Senate"},
    vote_col="votes",
    candidate_col="candidate",
    district_col="district",
    party_col="party",
)

# --- GA State Senate ---------------------------------------------------
ga_senate_districts = defaultdict(lambda: defaultdict(int))
with open("/Users/manders/where-it-counts/data/openelec_ga_2020.csv") as f:
    for row in csv.DictReader(f):
        if row.get("office","").strip() != "State Senate":
            continue
        district = row.get("district","").strip()
        party = row.get("party","").strip().upper()
        candidate = row.get("candidate","").strip()
        if not district or not candidate:
            continue
        try:
            votes = (int(row.get("election_day_votes") or 0) +
                     int(row.get("advanced_votes") or 0) +
                     int(row.get("absentee_by_mail_votes") or 0) +
                     int(row.get("provisional_votes") or 0))
        except (ValueError, KeyError):
            continue
        bucket = "DEM" if "DEM" in party else ("REP" if "REP" in party else "OTHER")
        ga_senate_districts[district][bucket] += votes

ga_senate = []
for district, totals in ga_senate_districts.items():
    dem = totals.get("DEM", 0)
    rep = totals.get("REP", 0)
    total = dem + rep + totals.get("OTHER", 0)
    if dem == 0 and rep == 0:
        continue
    margin = abs(dem - rep)
    winner = "DEM" if dem > rep else "REP"
    margin_pct = round(margin / total * 100, 2) if total else 0
    ga_senate.append({
        "state": "GA", "district": district,
        "dem": dem, "rep": rep, "total": total,
        "winner": winner, "margin": margin, "margin_pct": margin_pct,
    })
ga_senate.sort(key=lambda x: x["margin"])

# --- PRINT RESULTS ----------------------------------------------------

def print_closest(races, label, n=10):
    print(f"\n{'='*60}")
    print(f"{label} — {n} closest races")
    print(f"{'='*60}")
    contested = [r for r in races if r["dem"] > 0 and r["rep"] > 0]
    for r in contested[:n]:
        print(f"  District {r['district']:<6}  "
              f"{r['winner']} +{r['margin']:>5,}  "
              f"({r['margin_pct']}%)  "
              f"total: {r['total']:,}")
    if contested:
        margins = [r["margin"] for r in contested]
        under_1k = sum(1 for m in margins if m < 1000)
        under_5k = sum(1 for m in margins if m < 5000)
        print(f"\n  Contested districts: {len(contested)}")
        print(f"  Decided by <1,000 votes: {under_1k}")
        print(f"  Decided by <5,000 votes: {under_5k}")
        print(f"  Median margin: {sorted(margins)[len(margins)//2]:,}")

print_closest(ga_house,   "GA State House 2020")
print_closest(ga_senate,  "GA State Senate 2020")
print_closest(wi_assembly,"WI State Assembly 2020")
print_closest(wi_senate,  "WI State Senate 2020")

# --- REMOTE WORK DATA (BLS ATUS 2023) ---------------------------------
# Source: BLS American Time Use Survey + Census ACS 2022
# "Share of workers in occupation who can work from home"
# Published figures — no API key needed
wfh_by_occupation = [
    {"occupation": "Computer & Mathematical",      "pct_wfh": 71, "source": "BLS ATUS 2023"},
    {"occupation": "Management",                   "pct_wfh": 62, "source": "BLS ATUS 2023"},
    {"occupation": "Business & Financial Ops",     "pct_wfh": 58, "source": "BLS ATUS 2023"},
    {"occupation": "Legal",                        "pct_wfh": 54, "source": "BLS ATUS 2023"},
    {"occupation": "Architecture & Engineering",   "pct_wfh": 47, "source": "BLS ATUS 2023"},
    {"occupation": "Life, Physical & Social Sci",  "pct_wfh": 44, "source": "BLS ATUS 2023"},
    {"occupation": "Arts, Design & Media",         "pct_wfh": 42, "source": "BLS ATUS 2023"},
    {"occupation": "Education & Library",          "pct_wfh": 38, "source": "BLS ATUS 2023"},
    {"occupation": "Sales & Related",              "pct_wfh": 28, "source": "BLS ATUS 2023"},
    {"occupation": "Office & Admin Support",       "pct_wfh": 26, "source": "BLS ATUS 2023"},
    {"occupation": "Healthcare Practitioners",     "pct_wfh": 18, "source": "BLS ATUS 2023"},
    {"occupation": "Community & Social Service",   "pct_wfh": 16, "source": "BLS ATUS 2023"},
    {"occupation": "Service Occupations",          "pct_wfh":  5, "source": "BLS ATUS 2023"},
    {"occupation": "Construction & Extraction",    "pct_wfh":  2, "source": "BLS ATUS 2023"},
    {"occupation": "Transportation & Material",    "pct_wfh":  2, "source": "BLS ATUS 2023"},
    {"occupation": "Production (Manufacturing)",   "pct_wfh":  3, "source": "BLS ATUS 2023"},
]

remote_eligible_share = 0.41  # ~41% of US jobs can be done remotely (BLS 2023)

print(f"\n{'='*60}")
print("REMOTE WORK ELIGIBILITY BY OCCUPATION (BLS ATUS 2023)")
print(f"{'='*60}")
for o in wfh_by_occupation:
    bar = "█" * (o["pct_wfh"] // 5)
    print(f"  {o['occupation']:<35} {o['pct_wfh']:>3}%  {bar}")
print(f"\n  Overall share of jobs that can be done remotely: ~{int(remote_eligible_share*100)}%")

# --- WRITE OUTPUT JSON ------------------------------------------------
output = {
    "state_legislative": {
        "ga_house":   [r for r in ga_house   if r["dem"] > 0 and r["rep"] > 0],
        "ga_senate":  [r for r in ga_senate  if r["dem"] > 0 and r["rep"] > 0],
        "wi_assembly":[r for r in wi_assembly if r["dem"] > 0 and r["rep"] > 0],
        "wi_senate":  [r for r in wi_senate  if r["dem"] > 0 and r["rep"] > 0],
    },
    "remote_work": {
        "by_occupation": wfh_by_occupation,
        "overall_pct_remote_eligible": int(remote_eligible_share * 100),
        "source": "BLS American Time Use Survey 2023",
    }
}

with open("/Users/manders/where-it-counts/data/state_leg_and_wfh.json", "w") as f:
    json.dump(output, f, indent=2)
print(f"\n✓ Wrote data/state_leg_and_wfh.json")
