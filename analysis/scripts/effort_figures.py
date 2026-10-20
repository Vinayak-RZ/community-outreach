"""Poster figures for the 'Our fieldwork' band: fig9 timeline, fig10 by-the-numbers, fig11 sources-to-findings flow.
All numbers are counted in deliverables/work-log.md. Run with /workspace/tools/analysis-venv/bin/python."""
import pathlib, matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from datetime import date
F = pathlib.Path(__file__).resolve().parents[2] / "analysis/figures"
# Style: near-black ink, ONE muted accent, greys; flat, no legends, lots of white space.
INK, ACC, GREY, LGREY = "#1A1A1A", "#3D7A8C", "#8A8A8A", "#D9D9D9"
NAVY, TEAL, ORANGE, LIGHT = INK, ACC, ACC, "white"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 11})

# fig9 timeline
ev = [(date(2026,8,16),"Group formed",0),(date(2026,8,23),"First meetup + first dog clips (ICC)",1),
      (date(2026,8,27),"Survey v1 built",0),(date(2026,9,17),"CCF volunteer interview",1),
      (date(2026,9,22),"Survey revised, anonymous",0),(date(2026,9,24),"Hospital visit + CCF GMeet (36 min)",1),
      (date(2026,9,25),"MNC guard + student interviews shared",1),(date(2026,10,5),"CMO permission by email",2),
      (date(2026,10,13),"Survey out (199 replies that day)\n+ CMO interview",1),(date(2026,10,14),"Fieldwork night:\n21 recordings",1),
      (date(2026,10,16),"More interviews; 200+ replies",1),(date(2026,10,19),"All media compiled",3),
      (date(2026,10,20),"80 transcripts, coding,\ntriangulation",3)]
col = {0: GREY, 1: ACC, 2: GREY, 3: INK}  # accent = fieldwork days
fig, ax = plt.subplots(figsize=(16, 4.6)); ax.axhline(0, color=LGREY, lw=1, zorder=0)
for i, (d, t, k) in enumerate(ev):
    x = i  # evenly spaced (ordinal) so October events don't collide; real dates are in the labels
    y = 1.0 if i % 2 == 0 else -1.0
    ax.plot([x, x], [0, y * .85], color=col[k], lw=1.2); ax.scatter(x, 0, s=80, color=col[k], zorder=3)
    ax.text(x, y, f"{d.day}/{d.month}\n{t}", ha="center", va="bottom" if y > 0 else "top", fontsize=9, color=NAVY)
ax.text(-.6, -2.0, "Fieldwork days in colour", color=ACC, fontsize=9)
ax.set_ylim(-2.2, 2.2); ax.set_xlim(-.7, len(ev)-.3); ax.set_xticks([]); ax.set_yticks([]); [s.set_visible(False) for s in ax.spines.values()]
ax.set_title("Two months in the field: 16 Aug – 20 Oct 2026", loc="left", color=NAVY, fontsize=14, pad=28)
fig.tight_layout(); fig.savefig(F/"fig9_project_timeline.png", dpi=300); plt.close(fig)

# fig10 by the numbers
tiles = [("211","survey responses\n(199 on 13/10)"),("36","recorded interviews\n(≥37 people)"),("6","stakeholder groups\n+ the CMO"),
         ("3.95 h","of audio/video\n(80 recordings)"),("80","transcripts, each\nwith an English pass"),("6","dated field days\n(file timestamps)"),
         ("72","files on the team Drive"),("566","group-chat messages\nover 33 days"),("27","interview codes,\n36-row coded dataset")]
fig, ax = plt.subplots(figsize=(10, 7.5)); ax.set_xlim(0, 3); ax.set_ylim(0, 3); ax.axis("off")
for i, (n, l) in enumerate(tiles):
    x, y = i % 3, 2 - i // 3
    ax.plot([x+.08, x+.92], [y+.9, y+.9], color=LGREY, lw=.8)
    ax.text(x+.08, y+.6, n, ha="left", va="center", fontsize=30, weight="bold", color=ACC if i in (0, 1) else INK)
    ax.text(x+.08, y+.3, l, ha="left", va="center", fontsize=10.5, color=GREY)
ax.set_title("Our fieldwork by the numbers", color=INK, fontsize=15, loc="left", x=.03)
fig.tight_layout(); fig.savefig(F/"fig10_by_the_numbers.png", dpi=300); plt.close(fig)

# fig11 sources -> findings, links = the evidence matrix in analysis/synthesis.md
src = ["Survey (n=211)", "Students (18 interviews)", "Guards (5)", "Mess, shop, cleaning staff (4)", "CCF (3) + GMeet", "Feeders (2), faculty (1)", "CMO notes"]
fnd = ["F1  Space, not presence", "F2  Dogs inside hostels", "F3  Night chases, few routes", "F4  A few packs + outside dogs",
       "F5  Feeding zones fail", "F6  Awareness gap", "F7  No facts on record"]
M = {0: [0, 1, 2, 3, 4, 5], 1: [0, 1, 2, 3], 2: [0, 1, 2, 4], 3: [1, 2, 4, 5], 4: [0, 1, 2, 3, 4, 5], 5: [0, 1, 4], 6: [1, 2, 4, 6]}
fig, ax = plt.subplots(figsize=(12, 6.5)); ax.set_xlim(0, 12); ax.set_ylim(-.8, 7.8); ax.axis("off")
ys = [7 - i for i in range(7)]
for y, t in zip(ys, src): ax.text(3.6, y, t, ha="right", va="center", color=INK, fontsize=11)
for i, (y, t) in enumerate(zip(ys, fnd)):
    ax.text(8.4, y, t, ha="left", va="center", color=ACC, fontsize=11)
    ax.text(11.9, y, f"{len(M[i])}/7", ha="right", va="center", color=GREY, fontsize=10)
    for j in M[i]: ax.plot([3.8, 8.2], [ys[j], y], color=ACC, alpha=.35, lw=1.1)
for x, t, h in [(3.6, "SOURCES", "right"), (8.4, "FINDINGS", "left"), (11.9, "SOURCES AGREEING", "right")]:
    ax.text(x, 7.7, t, ha=h, fontsize=9, color=GREY)
ax.text(0, -.6, "Method: survey cross-tabs; 80 recordings transcribed + translated (Whisper); 36 interviews coded with 27 codes; triangulated.", fontsize=9, color=GREY)
fig.tight_layout(); fig.savefig(F/"fig11_sources_to_findings.png", dpi=300); plt.close(fig)
