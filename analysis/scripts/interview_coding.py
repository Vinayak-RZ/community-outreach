"""Build the interview frequency tables and charts from analysis/data/interview-codes.csv.
Usage: python analysis/scripts/interview_coding.py  (writes analysis/figures/fig7*, fig8*, and analysis/data/theme-by-group.csv). Needs matplotlib (box venv: /workspace/tools/analysis-venv)."""
import csv, collections, pathlib
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
INK, ACC, GREY = "#1A1A1A", "#3D7A8C", "#8A8A8A"
plt.rcParams.update({"font.family": "DejaVu Sans", "axes.spines.top": False, "axes.spines.right": False, "axes.edgecolor": GREY, "text.color": INK})
R = pathlib.Path(__file__).resolve().parents[2]
rows = list(csv.DictReader(open(R/"analysis/data/interview-codes.csv", encoding="utf-8")))
THEMES = {"People's problems": "P-", "Dogs' problems": "D-", "Causes": "C-", "Solutions": "S-"}
GROUPS = ["Student", "Guard", "Mess/shop staff", "CCF", "Feeder/caretaker", "Faculty", "Unclear"]
by_group = collections.Counter(r["group"] for r in rows)
code_group = collections.defaultdict(collections.Counter)
for r in rows:
    for c in filter(None, r["codes"].split(";")):
        code_group[c][r["group"]] += 1
codes = sorted(code_group, key=lambda c: (c[0], -sum(code_group[c].values())))
with open(R/"analysis/data/theme-by-group.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(["code", "total"] + GROUPS)
    for c in codes: w.writerow([c, sum(code_group[c].values())] + [code_group[c][g] for g in GROUPS])
print("| Code | Total | " + " | ".join(f"{g} (n={by_group[g]})" for g in GROUPS) + " |")
print("|---|---|" + "---|" * len(GROUPS))
for c in codes: print(f"| {c} | {sum(code_group[c].values())} | " + " | ".join(str(code_group[c][g] or "") for g in GROUPS) + " |")
st = collections.defaultdict(list)
for r in rows: st[r["group"]].append(int(r["stance"]))
print("\nStance by group:", {g: (len(v), round(sum(v)/len(v), 2)) for g, v in st.items()})
print("Reliability:", collections.Counter(r["reliability"] for r in rows))
# fig7: share of interviews in each group raising key codes (direct labels on the top row, no legend)
key = ["P-HOSTEL", "P-BITE", "P-CHASE", "P-HYG", "C-FEED", "C-BOUND", "S-OUT", "S-ZONE", "S-STER", "S-REDUCE"]
lab = {"P-HOSTEL": "Dogs in hostels", "P-BITE": "Bite mentioned", "P-CHASE": "Chased", "P-HYG": "Hygiene / waste",
       "C-FEED": "Feeding outside zones", "C-BOUND": "Boundary gaps, outside dogs", "S-OUT": "Keep out of hostels",
       "S-ZONE": "Designated / feeding zones", "S-STER": "Sterilise / vaccinate", "S-REDUCE": "Reduce numbers / remove"}
gs = ["Student", "Guard", "Mess/shop staff", "CCF"]; shades = [ACC, "#4D4D4D", "#9A9A9A", "#CCCCCC"]
fig, ax = plt.subplots(figsize=(11, 6.5)); wd = 0.2
for i, g in enumerate(gs):
    ax.barh([k + i*wd for k in range(len(key))], [100*code_group[c][g]/by_group[g] for c in key], wd, color=shades[i])
x0 = .22
for i, g in enumerate(gs):
    t = fig.text(x0, .905, f"\u25A0 {g} (n={by_group[g]})", color=shades[i] if i < 3 else "#9A9A9A", fontsize=10)
    x0 += .17
ax.set_yticks([k + 1.5*wd for k in range(len(key))]); ax.set_yticklabels([lab[c] for c in key]); ax.invert_yaxis()
ax.set_xlim(0, 100); ax.set_xlabel("% of interviews in the group that raise it", color=GREY); ax.tick_params(colors=INK, length=0)
fig.suptitle("What each group raises (36 coded interviews)", x=.02, ha="left", fontsize=14)
fig.tight_layout(rect=(0, 0, 1, .9)); fig.savefig(R/"analysis/figures/fig7_theme_by_stakeholder.png", dpi=300)
# fig8: reach, value-labelled, single accent
fig, ax = plt.subplots(figsize=(9, 4.5))
g2 = [g for g in GROUPS if by_group[g]]
ax.barh(g2, [by_group[g] for g in g2], color=[ACC] + ["#9A9A9A"]*(len(g2)-1)); ax.invert_yaxis()
for i, g in enumerate(g2): ax.text(by_group[g] + .3, i, by_group[g], va="center", color=INK)
ax.set_xticks([]); ax.spines["bottom"].set_visible(False); ax.tick_params(length=0)
fig.suptitle(f"Who we spoke to on record: {len(rows)} interviews", x=.02, ha="left", fontsize=14)
ax.set_title("plus 211 survey responses and the CMO (notes only)", loc="left", color=GREY, fontsize=10)
fig.tight_layout(); fig.savefig(R/"analysis/figures/fig8_stakeholder_reach.png", dpi=300)
