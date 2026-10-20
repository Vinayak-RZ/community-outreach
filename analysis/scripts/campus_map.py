"""fig12 base map and fig13 hotspot draft. Geometry © OpenStreetMap contributors (ODbL 1.0)."""
import json, csv, collections, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from pathlib import Path
R = Path(__file__).resolve().parents[1].parent
plt.rcParams["font.family"] = ["Inter", "DejaVu Sans"]
INK, ACC, G1, G2, G3 = "#1A1A1A", "#3D7A8C", "#6B6B6B", "#BDBDBD", "#EDEDED"
L = json.load(open(R/"analysis/data/osm/layers.json"))
X0, X1, Y0, Y1 = 77.8875, 77.9035, 29.8595, 29.8735
# Place positions: OSM feature centroid, Nominatim (OSM) lookup, or midpoint of two OSM features. None = not in OSM.
POS = {
 "Himalaya Bhawan": (29.86113, 77.89610, "OSM (Nominatim)"), "Architecture dept": (29.86354, 77.89922, "OSM"),
 "Govind Bhawan (towards Chemistry)": (29.86240, 77.89515, "midpoint Govind Bhawan–Chemistry (OSM)"),
 "Govind Bhawan": (29.86203, 77.89447, "OSM"), "Jawahar Bhawan": (29.86397, 77.90042, "OSM"),
 "Kasturba Bhawan": (29.86728, 77.90077, "OSM"), "Sarojini Bhawan": (29.86496, 77.90019, "OSM"),
 "Hospital": (29.86182, 77.89300, "OSM (Institute Hospital)"), "SAC": (29.86650, 77.89969, "OSM"),
 "Library": (29.86532, 77.89486, "OSM"), "Main gate": (29.86543, 77.88935, "OSM"),
 "Rajiv Bhawan": (29.86979, 77.89502, "OSM (Nominatim)"), "Radhakrishnan Bhawan": (29.87127, 77.89595, "OSM (Nominatim)"),
 "Ravindra Bhawan": (29.86538, 77.89247, "OSM (canteen node)"), "Cautley Bhawan": (29.87057, 77.89681, "OSM"),
 "Rajendra Bhawan": (29.87101, 77.89411, "OSM"), "Ganga Bhawan": (29.87169, 77.89437, "OSM"),
 "Mandir": (29.86835, 77.89780, "OSM (Saraswati Mandir, uncertain which mandir)"), "LBS ground": (29.86714, 77.89552, "OSM"),
 "ICC": None, "MAC": None, "MNC": None, "Vivekananda Bhawan": None, "Badminton hall": None, "Robocon lab": None,
 "Gate 7": None, "Gate 5": None, "Boundary wall/railing": None, "Mess / canteen": None, "Feeding zone (unnamed)": None,
 "Thomson": None, "Aravali": None,
}
def base(ax):
    for f in L["green"]: ax.add_patch(Polygon(f["pts"], closed=True, fc="#F4F4F4", ec="none", zorder=0))
    for f in L["roads"]:
        xs, ys = zip(*f["pts"]); hw = f["tags"].get("highway", "")
        ax.plot(xs, ys, color=G2 if hw in ("service", "track") else "#A8A8A8", lw=0.5 if hw in ("service", "track") else 1.1, zorder=1, solid_capstyle="round")
    for f in L["buildings"]: ax.add_patch(Polygon(f["pts"], closed=True, fc=G3, ec="#D6D6D6", lw=0.3, zorder=2))
    ax.set_xlim(X0, X1); ax.set_ylim(Y0, Y1); ax.set_aspect(1 / 0.8676); ax.axis("off")
    ax.text(X1, Y0 + 0.0001, "Map data © OpenStreetMap contributors (ODbL)", ha="right", va="bottom", fontsize=6, color=G1)
LABELS = ["Himalaya Bhawan", "Architecture dept", "Govind Bhawan", "Jawahar Bhawan", "Kasturba Bhawan", "Sarojini Bhawan", "Hospital", "SAC",
          "Library", "Main gate", "Rajiv Bhawan", "Radhakrishnan Bhawan", "Ravindra Bhawan", "Cautley Bhawan", "Rajendra Bhawan", "LBS ground"]
fig, ax = plt.subplots(figsize=(8, 7.5)); base(ax)
for k in LABELS:
    la, lo, _ = POS[k]; ax.plot(lo, la, "o", ms=2.5, color=INK, zorder=3)
    ax.text(lo + 0.00015, la + 0.00012, k.replace(" Bhawan", ""), fontsize=7, color=INK, zorder=4)
ax.set_title("IIT Roorkee campus (base)", loc="left", fontsize=11, color=INK, fontweight="bold")
for ext in ("png", "svg"): fig.savefig(R/f"analysis/figures/fig12_campus_basemap.{ext}", dpi=300, bbox_inches="tight", facecolor="white")
plt.close(fig)
# Hotspots
rows = list(csv.DictReader(open(R/"analysis/data/places.csv")))
ISS = ["chasing", "bite", "dogs in hostel", "feeding zone", "boundary gap", "garbage", "noise", "puppies", "shelter or care"]
COL = {"chasing": ACC, "bite": ACC, "dogs in hostel": INK, "feeding zone": "#8FB8C4"}
cnt = collections.defaultdict(collections.Counter); night = collections.Counter(); inter = set(); team = set(); total = collections.Counter()
for r in rows:
    p = r["place"]
    if r["mention_type"] == "hotspot (team)": team.add(p); continue
    if r["mention_type"] == "interview location": inter.add(p); continue
    if r["source"].startswith("WhatsApp"): continue  # team logistics chat: not evidence of dog issues at a place
    total[p] += 1
    for t in r["mention_type"].split(";"):
        if t in ISS: cnt[p][t] += 1
    if r["time_of_day"]: night[p] += 1
if "Govind Bhawan (towards Chemistry)" in team: pass
fig, ax = plt.subplots(figsize=(8, 7.5)); base(ax)
out = []
for p, v in POS.items():
    if not v: continue
    la, lo, how = v; n = total[p] + (total["Govind Bhawan"] if p == "Govind Bhawan (towards Chemistry)" else 0)
    if p == "Govind Bhawan": continue
    dom = cnt[p].most_common(1)[0][0] if cnt[p] else ""
    if n: ax.scatter(lo, la, s=18 + n * 22, color=COL.get(dom, G1), alpha=0.75, lw=0, zorder=5)
    if p in team: ax.scatter(lo, la, s=18 + max(n, 4) * 22 + 120, facecolor="none", edgecolor=ACC, lw=1.4, zorder=6)
    if p in inter: ax.plot(lo, la, "o", ms=2.6, color="white", mec=INK, mew=0.6, zorder=7)
    if n or p in team:
        lab = p.replace(" Bhawan", "").replace(" (towards Chemistry)", "–Chemistry") + (f" {n}" if n else "")
        if night[p]: lab += f"\nnight: {night[p]}"
        ax.text(lo + 0.0004, la - 0.0001, lab, fontsize=7, color=INK, zorder=8, va="center")
    out.append([p, la, lo, how, n, dom, night[p], "yes" if p in team else "", "yes" if p in inter else ""])
y = Y1 - 0.0004
for txt, c in [("chasing / bite", ACC), ("dogs in hostel", INK), ("feeding", "#8FB8C4"), ("other", G1)]:
    ax.scatter(X0 + 0.0004, y, s=40, color=c, alpha=0.75, lw=0); ax.text(X0 + 0.0009, y, txt, fontsize=7, va="center", color=INK); y -= 0.0005
ax.scatter(X0 + 0.0004, y, s=60, facecolor="none", edgecolor=ACC, lw=1.4); ax.text(X0 + 0.0009, y, "team-confirmed hotspot (20 Oct)", fontsize=7, va="center"); y -= 0.0005
ax.text(X0 + 0.0002, y, "Not placed (no OSM match): MAC, MNC, gate 7, gate 5, wall gaps,\nbadminton hall, Robocon lab, Vivekananda", fontsize=6.5, color=G1, va="top")
ax.set_title("Where people mentioned dog problems (DRAFT, circle size = mentions)", loc="left", fontsize=10, color=INK, fontweight="bold")
fig.savefig(R/"analysis/figures/fig13_hotspot_map_draft.png", dpi=300, bbox_inches="tight", facecolor="white")
fig.savefig(R/"analysis/figures/fig13_hotspot_map_draft.svg", bbox_inches="tight", facecolor="white")
with open(R/"analysis/data/places-osm-match.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(["place", "lat", "lon", "position_from", "issue_mentions_excl_chat", "dominant_issue", "night_mentions", "team_hotspot", "interviewed_here"])
    w.writerows(out); w.writerows([[p, "", "", "not in OSM", total[p], (cnt[p].most_common(1) or [("",)])[0][0], night[p], "yes" if p in team else "", "yes" if p in inter else ""] for p, v in POS.items() if not v])
print(sorted(((r[4], r[0]) for r in out), reverse=True)[:12]); print("unplaced", {p: total[p] for p, v in POS.items() if not v})
