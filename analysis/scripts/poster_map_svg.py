"""Simplified campus SVG + hotspot pixel positions for the Figma poster. © OpenStreetMap contributors (ODbL)."""
import json, csv, math
from pathlib import Path
R = Path(__file__).resolve().parents[1].parent
L = json.load(open(R/"analysis/data/osm/layers.json"))
X0, X1, Y0, Y1 = 77.8886, 77.9021, 29.8604, 29.8717
W = 1340; H = round(W * (Y1 - Y0) / ((X1 - X0) * math.cos(math.radians(29.866))))
px = lambda lo, la: (round((lo - X0) / (X1 - X0) * W), round((Y1 - la) / (Y1 - Y0) * H))
inside = lambda pts: any(X0 <= x <= X1 and Y0 <= y <= Y1 for x, y in pts)
d = lambda pts, z="": "M" + "L".join(f"{a},{b}" for a, b in (px(*p) for p in pts)) + z
roads = [f for f in L["roads"] if inside(f["pts"])]
major = " ".join(d(f["pts"]) for f in roads if f["tags"].get("highway") not in ("service", "track"))
minor = " ".join(d(f["pts"]) for f in roads if f["tags"].get("highway") in ("service", "track"))
def big(pts, m=9):
    q = [px(*p) for p in pts]; return max(a for a, _ in q) - min(a for a, _ in q) >= m or max(b for _, b in q) - min(b for _, b in q) >= m
bld = " ".join(d(f["pts"][:-1] if f["pts"][0] == f["pts"][-1] else f["pts"], "Z") for f in L["buildings"] if inside(f["pts"]) and big(f["pts"]))
grn = " ".join(d(f["pts"], "Z") for f in L["green"] if inside(f["pts"]))
svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">'
       f'<path d="{grn}" fill="#F3F3F3"/><path d="{minor}" fill="none" stroke="#DADADA" stroke-width="2"/>'
       f'<path d="{major}" fill="none" stroke="#BDBDBD" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>'
       f'<path d="{bld}" fill="#E6E6E6"/></svg>')
open(R/"analysis/figures/poster_map_base.svg", "w").write(svg)
pts = []
for r in csv.DictReader(open(R/"analysis/data/places-osm-match.csv")):
    if not r["lat"]: continue
    x, y = px(float(r["lon"]), float(r["lat"]))
    if 0 <= x <= W and 0 <= y <= H: pts.append(dict(p=r["place"], x=x, y=y, n=int(r["issue_mentions_excl_chat"]), dom=r["dominant_issue"], night=int(r["night_mentions"]), team=r["team_hotspot"], iv=r["interviewed_here"], approx="approx" in r["position_from"]))
json.dump(dict(W=W, H=H, pts=pts), open("/tmp/mapx_pts.json", "w"))
print(W, H, len(svg), len(pts))
