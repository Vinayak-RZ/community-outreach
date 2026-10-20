# A3 poster plan: "Campus dogs: two sides of one street" (group 23)

_Draft of 20/10/2026 (Acads), for the team to edit. Every number on it has to trace back to `analysis/`. No team selfies, no faces, and no names of interviewees or officials [course ethics, slides 20–21]._

## Headline message
**"Not 'dogs or no dogs': out of our rooms, fed in the right places, kept inside a sealed boundary."**
Sub-line: *211 survey respondents, 36 recorded interviews with students, guards, mess staff, CCF and feeders. 86% want managed coexistence, and only 8% want free movement.*

## Layout (A3 portrait, 297 × 420 mm, 3 columns, 10 mm margins)
| Zone | Holds | Figures / data |
|---|---|---|
| **Header** (full width, ~45 mm) | Title, headline, course, group, Topic 3. Small "how we know": 211 survey · 36 interviews · 3.45 h recorded · CMO · CCF | — |
| **"Our fieldwork" band** (full width under the header, ~70 mm) | Makes the effort visible at a glance: the by-the-numbers row (211 · 36 · 6 groups · 3.95 h · 80 transcripts · 6 field days), the timeline, and a small sources→findings diagram on the right | `fig10_by_the_numbers.png` (as one row of numbers), `fig9_project_timeline.png`, `fig11_sources_to_findings.png` |
| **Col 1: The question and who we heard** | The course question "What happens when it's not safe to walk in a campus?", our two-sides framing, and the method in 4 lines | `fig8_stakeholder_reach.png` (new) |
| **Col 1: The afraid side** | Dogs in hostels at 68%, chased or unsafe at 61%. Chased → 87% call it a serious problem. Night routes | `fig2_problems.png`, `fig4_rating_by_chased.png` |
| **Col 2: Two sides, one street** (centre, biggest) | What each group raises: students (rooms, fear), guards (bites, chasing, outside dogs), staff (hygiene), CCF (feeding and the boundary) | `fig7_theme_by_stakeholder.png` (new), `fig1_experience.png` |
| **Col 2: Where they agree** | The boundary question at 86% managed coexistence, alongside the interview solutions (zones, out of hostels, sterilise) | `fig3_boundary.png` |
| **Col 2: Hotspot map** | Campus sketch with the named hotspots (MAC–Rajiv road, MNC–Govind, SAC, Mandir, gate 7 and the Himalaya-side gaps) | **New, needs the field walk** (KPI action 4). If it isn't done, use a schematic map labelled "places named by respondents" |
| **Col 3: What we couldn't verify** | The sterilisation conflict (CCF says all ~90 females are neutered, guards say litters keep coming); no hospital data; survey limitations. Honesty about these scores marks (slide 15) | `fig5_awareness_by_experience.png` (71% unaware of CCF) |
| **Col 3: The coexistence proposal** | R1–R7 from `analysis/synthesis.md`, each with the office that acts | Icon list, no chart |
| **Col 3: KPI strip** | The 5-row KPI table, with achieved figures against targets | From `deliverables/kpi-table.md` |
| **Footer** | Survey caveats (leading items; 94% on 13/10; students only), data and ethics note, QR code to the evidence folder (private link shown only to evaluators) | — |

Charts in `analysis/figures`: fig1–fig6 (survey, 200 dpi, old palette); fig7–fig8 (`analysis/scripts/interview_coding.py`) and fig9–fig11 (`analysis/scripts/effort_figures.py`), all 300 dpi in the poster style.

## Style spec (Vinayak, 20/10): minimal, designed by a person
- **White space first.** 15 mm outer margins, 8 mm gutters, one 12-column grid; everything aligns to it. Leave about 30% of the sheet empty.
- **Colour.** Near-black text `#1A1A1A`, **one** muted accent `#3D7A8C` (only for the key number or bar in each figure), and greys `#4D4D4D`, `#8A8A8A`, `#D9D9D9`. No other colours.
- **Type.** One clean sans (Inter in Figma; the charts use DejaVu Sans, so re-export them in Inter if you want an exact match). Three sizes only: title 72 pt, section heads 28 pt, body 14–16 pt.
- **Charts.** Flat. No gradients, shadows, 3D, emoji, clip-art icons or AI imagery. Minimal gridlines, values labelled directly, no legends where a direct label works. Left-aligned titles.
- **Photos.** At most 2–3 real, geotagged field photos, faces blurred, no team selfies.
- **Consistency.** The same accent means the same thing everywhere ("our data / the key figure"). Same rounding (1 dp for percentages, with denominators).

The figures fig7–fig11 already follow this; fig1–fig6 (survey) use the older palette and should be re-rendered in the accent and greys before printing.

## Software
| Tool | A3 print + PDF | Pros | Cons |
|---|---|---|---|
| **Figma** (recommended) | A frame at 297 × 420 mm (1191 × 1684 px at 72 ppi; scale on export), vector PDF export | The whole team edits live. Precise grids and auto-layout. Charts drop in as PNG or SVG. Vinayak has the Figma plugin, so an agent can help lay it out | PDF export is RGB, so do one test print at the print shop. Fonts need care |
| Canva | A3 preset, "PDF Print" export | Fastest for non-designers, with templates | Templates look generic, and the team-selfie poster style is a known way to lose marks. Fine control is limited, and some features are paid |
| PowerPoint | Custom 29.7 × 42 cm slide, Save as PDF | Everyone has it and knows it. Works offline | Clumsy grids. Large images bloat the file. Easy to end up with a crowded slide |
| LaTeX / tikzposter | `a3paper`, vector PDF | Reproducible, crisp text, figures included from `analysis/figures` | Slow to iterate, and only one or two people on the team can edit it. Hard to make look designed |

**Recommendation: Figma.** It gives the best print-ready control, lets the team edit together, and the plugin means the layout can be drafted for you. **Fallback: PowerPoint** if the team wants something everyone can edit offline the night before. Export the final as PDF/X-quality at 100% scale, and print one A3 proof before the review.

## Checklist before printing
- Every number traces back to `analysis/` (mark each with its source in the Figma comments).
- No faces, names, room numbers or emails. Blur any photo with a person in it (blurring was dropped from the pipeline, so do it by hand for the few poster images).
- Any quote on the poster has been checked by ear and is covered by consent.
- Check font sizes at A3: body ≥ 14 pt, headings ≥ 28 pt.

## Figma draft (20/10/2026)
- File: [EEC 399 Group 23 – Campus Dogs Poster](https://www.figma.com/design/17JnrRFCdZtaPkjD30PSb5) (Vinayak's team drafts), frame "A3 Poster – 297×420 mm @300dpi" (3508 × 4961 px, node 1:410).
- Preview: [`poster-preview.png`](poster-preview.png). Draft PDF: [`poster-draft.pdf`](poster-draft.pdf) is a 300 dpi raster made from the preview, because the Figma tools here can't export PDF. For printing, export a vector PDF from Figma (File → Export frames to PDF).
- To check before printing: the text inside fig9 and fig11 is small at A3, so re-render those with larger labels. Body text is 40 px (about 10 pt), smaller than the 14 pt in the spec, because of how much content there is.
