# /// script
# requires-python = ">=3.11"
# dependencies = ["igraph"]
# ///
"""Build assets/airports/{airports,routes}.csv, the one dataset of this module.

OurAirports gives each airport its continent and country; OpenFlights gives the
routes. They are joined on the IATA code. The network is undirected, has no
self-loops, and keeps only the giant connected component.

    uv run tools/build_assets.py            # downloads, then writes assets/airports/

Run once by the author; the two CSVs are committed so students download nothing.
OurAirports is public domain. OpenFlights is under the Open Database License
(ODbL), so the notebook credits it. Its routes date from 2014.
"""
import csv
import io
import urllib.request
from pathlib import Path

import igraph as ig

OURAIRPORTS = "https://davidmegginson.github.io/ourairports-data/airports.csv"
OPENFLIGHTS = "https://raw.githubusercontent.com/jpatokal/openflights/master/data/routes.dat"
OUT = Path(__file__).resolve().parent.parent / "assets" / "airports"


def fetch(url: str) -> str:
    with urllib.request.urlopen(url, timeout=60) as r:
        return r.read().decode("utf-8")


def main() -> None:
    airports = {}
    for r in csv.DictReader(io.StringIO(fetch(OURAIRPORTS))):
        if r["iata_code"]:
            airports[r["iata_code"]] = r
    pairs = set()
    for row in csv.reader(io.StringIO(fetch(OPENFLIGHTS))):
        a, b = row[2], row[4]  # source and destination IATA
        if a != b and a in airports and b in airports:
            pairs.add(tuple(sorted((a, b))))
    codes = sorted({c for p in pairs for c in p})
    index = {c: i for i, c in enumerate(codes)}
    g = ig.Graph(n=len(codes), edges=[(index[a], index[b]) for a, b in pairs])
    # The membership of the biggest component. (`.giant()` returns a renumbered
    # subgraph, so its indices cannot be compared with the original ones.)
    parts = g.connected_components()
    biggest = max(range(len(parts)), key=lambda i: len(parts[i]))
    in_giant = set(parts[biggest])
    keep = [c for c in codes if index[c] in in_giant]
    kept = set(keep)

    OUT.mkdir(parents=True, exist_ok=True)
    with open(OUT / "airports.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["iata", "name", "continent", "country", "lat", "lon"])
        for c in keep:
            a = airports[c]
            w.writerow([c, a["name"], a["continent"], a["iso_country"],
                        round(float(a["latitude_deg"]), 4), round(float(a["longitude_deg"]), 4)])
    with open(OUT / "routes.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["src", "dst"])
        for a, b in sorted(pairs):
            if a in kept and b in kept:
                w.writerow([a, b])
    print(f"{len(keep)} airports, {sum(1 for a, b in pairs if a in kept and b in kept)} routes")


if __name__ == "__main__":
    main()
