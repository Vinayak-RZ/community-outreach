"""Build the interview frequency tables and charts from analysis/data/interview-codes.csv.
Usage: python analysis/scripts/interview_coding.py  (writes analysis/figures/fig7*, fig8*, and analysis/data/theme-by-group.csv). Needs matplotlib (box venv: /workspace/tools/analysis-venv)."""
import csv, collections, pathlib
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
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
# fig7: share of interviews in each group mentioning key codes
key = ["P-HOSTEL", "P-BITE", "P-CHASE", "P-HYG", "C-FEED", "C-BOUND", "S-OUT", "S-ZONE", "S-STER", "S-REDUCE"]
lab = {"P-HOSTEL": "Dogs in hostels", "P-BITE": "Bite (self/known)", "P-CHASE": "Chased", "P-HYG": "Hygiene/waste",
       "C-FEED": "Feeding outside zones", "C-BOUND": "Boundary gaps/outside dogs", "S-OUT": "Keep out of hostels",
       "S-ZONE": "Designated/feeding zones", "S-STER": "Sterilise/vaccinate", "S-REDUCE": "Reduce numbers/remove"}
gs = ["Student", "Guard", "Mess/shop staff", "CCF"]
fig, ax = plt.subplots(figsize=(12, 5.5)); wd = 0.2
for i, g in enumerate(gs):
    ax.barh([k + i*wd for k in range(len(key))], [100*code_group[c][g]/by_group[g] for c in key], wd, label=f"{g} (n={by_group[g]})")
ax.set_yticks([k + 1.5*wd for k in range(len(key))]); ax.set_yticklabels([lab[c] for c in key]); ax.invert_yaxis()
ax.set_xlabel("% of interviews in the group that raise it"); ax.legend(loc="upper left", bbox_to_anchor=(1.01, 1))
ax.set_title(f"What each group raises ({len(rows)} coded interviews, machine transcripts)")
fig.tight_layout(); fig.savefig(R/"analysis/figures/fig7_theme_by_stakeholder.png", dpi=200)
# fig8: reach
fig, ax = plt.subplots(figsize=(8, 4.5))
g2 = [g for g in GROUPS if by_group[g]]
ax.bar(g2, [by_group[g] for g in g2], color="#4C72B0")
for i, g in enumerate(g2): ax.text(i, by_group[g] + .3, by_group[g], ha="center")
ax.set_ylabel("Recorded interviews (distinct)"); plt.xticks(rotation=20, ha="right")
ax.set_title(f"Who we spoke to on record: {len(rows)} interviews + 211 survey responses + CMO (notes)")
fig.tight_layout(); fig.savefig(R/"analysis/figures/fig8_stakeholder_reach.png", dpi=200)
