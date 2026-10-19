# Survey analysis — "Condition of Dogs in campus" (group 23)

**Data:** `source/survey/survey-responses.csv` (de-identified export of Vrinda's responses sheet, read 19/10/2026). Question wording and options are in `source/survey/data-dictionary.md`.
**Method:** every figure below is computed from the sheet by `analysis/scripts/survey_stats.py` and `survey_code_and_charts.py`. Percentages use all 211 respondents unless another base is given, and are rounded to 1 dp. Free-text coding is described in §6. "Row N" means the row in the original Google Sheet (row 1 is the header), which is the `sheet_row` column in the CSV.
**Charts:** `analysis/figures/fig1–fig6*.png`, 200 dpi, for the poster.

## 1. Response count and timing
- **n = 211** responses (Google Form, 13/10/2026 10:51 to 17/10/2026 22:05, sheet time).
- 199 (94.3%) arrived on 13/10, the day the form was circulated to all groups [chat 12–13/10]. After that: 8 on 14/10, 1 on 15/10, 2 on 16/10, 1 on 17/10.
- 210 responses had come in by 16/10, which matches the "200+" reported in the chat [chat 16/10].

## 2. Who answered
- **Role:** Student 209 (99.1%), Faculty 1, Non-teaching staff 1. The survey speaks for **students only**. Guards, mess and canteen staff, feeders and residents are covered only by the interviews.
- **Department** (from email domain; 191 had an email):

  | Dept | n | Dept | n |
  |---|---|---|---|
  | me | 27 | ce | 8 |
  | ee | 27 | mfs, es, ma | 7 each |
  | ece | 23 | bt, hs | 6 each |
  | ph | 23 | mt | 4 |
  | cs | 17 | cy | 3 |
  | ch | 8 | hre, dm, wr, ms | 1 each |
  | personal email | 14 | no email | 20 |

- **Not collected:** bhawan, gender, year of study, and whether the person has been bitten. None of these can be broken down.

## 3. Distribution of each question

**Q: Experience with campus dogs** (fig1)
| Answer | n | % |
|---|---|---|
| Mostly negative | 110 | 52.1 |
| Mostly positive | 46 | 21.8 |
| Both positive and negative | 33 | 15.6 |
| Neutral / Rarely interact | 22 | 10.4 |

**Q: Problems personally experienced** (multi-select; fig2)
| Problem | n | % of 211 |
|---|---|---|
| Dogs entering hostels/buildings | 143 | 67.8 |
| Feeling unsafe or being chased | 129 | 61.1 |
| Noise or dog fights | 125 | 59.2 |
| Hygiene/waste | 114 | 54.0 |
| No significant problems | 31 | 14.7 |

- Number of the four problems ticked: 0 → 29, 1 → 32, 2 → 37, 3 → 47, **all four → 66 (31.3%)**.

**Q: Strongest reason dogs have a place on campus** (optional, 210 answered; fig6)
| Answer | n | % |
|---|---|---|
| They deserve humane treatment | 59 | 28.0 |
| They can coexist with humans | 55 | 26.1 |
| Caring for animals is our responsibility | 44 | 20.9 |
| They are part of campus life | 29 | 13.7 |
| They provide companionship | 23 | 10.9 |
| (blank, row 208) | 1 | 0.5 |

**Q: Where should the boundary lie?** (fig3)

"Other" answers are recoded; see the data dictionary.
| Answer | n | % |
|---|---|---|
| Restricted from hostels/buildings | 75 | 35.5 |
| Restricted to designated areas | 54 | 25.6 |
| Allowed only if vaccinated/sterilized | 52 | 24.6 |
| Free movement across campus | 17 | 8.1 |
| Remove from campus (**typed in "Other"**: not an option on the form) | 7 | 3.3 |
| Other: restriction-type text | 3 | 1.4 |
| Other: unclear | 3 | 1.4 |

**Q: Aware of organised sterilisation or the CCF committee?** No 149 (70.6%), Yes 62 (29.4%).

**Q: How much of a problem are campus dogs?** (1 = No problem, 5 = Serious problem)
| Rating | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|
| n | 35 | 22 | 24 | 56 | 74 |
| % | 16.6 | 10.4 | 11.4 | 26.5 | 35.1 |

- Mean 3.53 and median 4.
- 130 respondents (61.6%) rated 4–5; 57 (27.0%) rated 1–2.

**Q: Fair solution (free text):** answered by 98 of 211 (46.4%). See §6.

## 4. Key cross-tabs

**4.1 Being chased drives the problem rating** (fig4)
| | n | rated 4–5 | mean rating |
|---|---|---|---|
| Ticked "Feeling unsafe or being chased" | 129 | 112 (86.8%) | 4.36 |
| Did not tick it | 82 | 18 (22.0%) | 2.22 |

- Those who felt unsafe or chased chose "Restricted to designated areas" far more often: 45/129 (34.9%), against 9/82 (11.0%) of the rest.
- All 7 people who wrote in "remove" were in the chased group.

**4.2 Experience vs boundary: restriction, not removal, is the majority view on both sides**
| Experience | n | Hostels | Designated areas | Vaccinated/sterilised only | Free movement | Remove (typed) | Other |
|---|---|---|---|---|---|---|---|
| Mostly negative | 110 | 32 | 40 | 22 | 5 | 7 | 4 |
| Both | 33 | 21 | 6 | 5 | 0 | 0 | 1 |
| Neutral | 22 | 8 | 5 | 9 | 0 | 0 | 0 |
| Mostly positive | 46 | 14 | 3 | 16 | 12 | 0 | 1 |
| **All** | 211 | 75 | 54 | 52 | 17 | 7 | 6 |

- **181/211 (85.8%)** chose one of the three managed-coexistence options (hostels, designated areas, vaccinated/sterilised only).
- Among *mostly negative* respondents, 94/110 (85.5%) chose one of those three; 7 (6.4%) typed in removal.
- Among *mostly positive* respondents, 33/46 (71.7%) still chose a restriction or vaccination condition; only 12 (26.1%) chose free movement.
- Caveat: the form gave no removal option, so the closed question **undercounts** support for removal. See §6 and §7.

**4.3 Experience vs problem rating**
- Mean rating:
  - mostly negative 4.47 (101/110 = 91.8% rated 4–5)
  - both 3.82
  - neutral 3.00
  - mostly positive 1.33 (44/46 = 95.7% rated 1–2)
- Opinion is **polarised**: the two biggest groups sit at opposite ends of the scale.

**4.4 Problems by experience** (counts)
| Experience | n | Hostels | Unsafe/chased | Noise/fights | Hygiene | None |
|---|---|---|---|---|---|---|
| Mostly negative | 110 | 92 | 98 | 82 | 75 | 0 |
| Both | 33 | 25 | 20 | 24 | 19 | 0 |
| Neutral | 22 | 16 | 8 | 14 | 8 | 3 |
| Mostly positive | 46 | 10 | 3 | 5 | 12 | 28 |

- Even among mostly-positive respondents, 10 report dogs entering hostels and 12 report hygiene problems.

**4.5 Dogs in hostels → keep them out of hostels**
- Among people who ticked "Dogs entering hostels/buildings", 63/143 (44.1%) chose "Restricted from hostels/buildings", against 12/68 (17.6%) of the rest.

**4.6 Awareness of CCF / sterilisation** (fig5)
| Experience | Aware |
|---|---|
| Mostly negative | 29/110 (26.4%) |
| Both | 11/33 (33.3%) |
| Neutral | 2/22 (9.1%) |
| Mostly positive | 20/46 (43.5%) |
| **All** | **62/211 (29.4%)** |

- Mean problem rating: aware 3.32, not aware 3.62.
- About 7 in 10 respondents don't know that sterilisation or CCF exists. This gap fits the awareness-poster idea [chat 15–16/10] and the CCF claim that almost all female dogs are neutered [CCF-Meet, unverified].

**4.7 Reason dogs belong, among the mostly negative**
- The forced-choice "reason dogs have a place" question was answered by all 110 mostly-negative respondents.
- Most picked "deserve humane treatment" (39/110, 35.5%).
- Read this as the question making everyone pick a pro-dog reason, **not** as their support for dogs (see §7).

## 5. Topics the survey did *not* ask directly
- **Bites:** no question. Bite and chase evidence in the survey comes only from the "Feeling unsafe or being chased" tick (129) and free text (§6).
- **Support for sterilisation:** no direct question. The proxies are the boundary choice "Allowed only if vaccinated/sterilized" (52, 24.6%) and free-text mentions (12).
- **Feeding zones:** no question; free-text mentions only (§6).
- **Problems dogs face** (food, injury, mistreatment): not asked. Vinayak's 21/9 draft had this question [chat 21/9], but the final form doesn't. This side has to come from the CCF and feeder interviews.

## 6. Free-text themes ("What would a fair solution look like…", 98 answers)

**6.1 Stance on removal** (hand-coded by one coder; row lists are in the data dictionary)
| Stance | n | % of 98 |
|---|---|---|
| No removal proposed | 67 | 68.4 |
| Remove all/most dogs (sole proposal) | 16 | 16.3 |
| Remove as one option / "ideally" | 10 | 10.2 |
| Remove only aggressive dogs/packs | 5 | 5.1 |

- 26 of 98 written answers (26.5%) propose removing all or most dogs at least as an option. All 16 sole-removal answers came from *mostly negative* respondents: 16 of the 55 mostly-negative respondents who wrote something (29.1%).

**6.2 Keyword-coded mentions** (case-insensitive regex in `survey_stats.py`. These are exact match counts, but keyword matching is crude: e.g. "feeding" also matches the joke in row 83.)
| Theme | answers | % of 98 |
|---|---|---|
| Keep out of hostels/buildings (hostel, bhawan, room, mess, canteen, building) | 38 | 38.8 |
| Designated areas / shelter / park | 26 | 26.5 |
| Vaccination | 23 | 23.5 |
| Feeding zones / regular feeding | 16 | 16.3 |
| Hygiene / waste / garbage | 16 | 16.3 |
| Sterilisation / neutering | 12 | 12.2 |
| Mentions being chased / bitten | 11 | 11.2 |
| Reduce numbers / overpopulation | 8 | 8.2 |
| Guards / security / hotline | 7 | 7.1 |
| Awareness / training / workshop | 6 | 6.1 |
| Tech (app, collar, tracking) | 2 | 2.0 |

**Places named in free text:**
- MNC (rows 28, 31, 193), Govind (31, 110, 148), Rajiv/RJB (31, 96, 148)
- Kasturba/KB (28, 193), MAC (31, 193), Himalaya (31, 68)
- Thomson lane (28), LBS ground (104), LHC (179), hospital (193)
- "Night" comes up in 9 answers.
- These overlap with the CCF hotspots (MNC, Kasturba, MAC, the road to Thomson) [CCF-Meet].

**Short verbatim examples:**
- Restriction: "Keep dogs inside campus but keep them strictly outside hostels and buildings , especially mess" (row 24)
- Hotspots: "Avoid dog groups/territories near choked places like Himalaya, MnC-govind corner, MAC-RJB road etc" (row 31)
- Hygiene: "i can't use the washroom in peace in my own bhawan because these dogs eat the used sanitary pads." (row 68)
- Waste fix that worked: "Once the dustbin were place at a height, dogs stopped entering our Bhawan." (row 112)
- Feeding zones: "feeding zones need to be seriously enforced" (row 118)
- Against removal: "throwing them out of the campus will be really inhumane" (row 179)
- Second-hand bites: "3 of my friends we bitten by dogs on campus without any reason" (row 74). This is unverified.
- Guards: "how the hell are there 0 guards on basically the entire path" (row 148)
- Removal: "Just remove dogs from the campus." (row 196)
- Awareness: "Conduct workshop for IITR junta to teach them that they can easily co exist with dogs." (row 122)

Row 193 claims a recent death on campus was caused by dogs. It is **unverified** and must not go on the poster unless it's checked against a record.

## 7. Data quality issues
1. **Leading or forced items.**
   - The boundary question has **no removal option**, so removal support only shows up through "Other" (7) and free text (26/98).
   - The "strongest reason dogs have a place" item assumes they do, and offers no "they don't" option.
   - The responses sheet is titled "Removal of dogs from campus", though the live form is "Condition of Dogs in campus".
2. **Sample.** 99.1% students, self-selected through WhatsApp groups, 94.3% on one day.
   - This isn't a random sample of campus residents, so present it as "211 respondents", not "campus opinion".
   - Department mix is uneven: me, ee, ece and ph make up 100 of 211.
3. **No demographics.** Bhawan, gender and year weren't asked, so no hostel-level or gender breakdown is possible, though both matter for the "afraid side".
4. **Personal data.**
   - The form was meant to be anonymous after 22/9 [chat 22/9], but the sheet holds **191 email addresses**. The first 20 responses (rows 2–21) have none, which suggests email collection was switched on after them.
   - Emails are kept only on the box. The repo copy holds only a department code.
   - One free-text answer gave a room number (row 83, redacted).
5. **Contradictions.** 2 respondents ticked "No significant problems" together with a problem (rows 75, 206).
6. **Joke or off-topic answers** in free text, e.g. rows 21, 76, 83, 211 (row 211 names a team member). They're kept in the data but don't change any count except where noted.
7. **Duplicates.** All 191 emails are unique.
   - 11 responses (rows 45, 46, 77, 120, 136, 151, 168, 173, 184, 198, 205) have the same closed answers and blank free text as an earlier one. That's plausible for a short form, and with no IDs on rows 2–21 they can't be confirmed as duplicates.
   - Nothing was removed.
8. **Coding.** The removal stance and Other recodes are one coder's judgement; a second coder should check them before the viva. Keyword themes are approximate.

## 8. Poster-ready headline lines (each traceable above)
- "211 people answered; 52.1% describe their experience with campus dogs as mostly negative, 21.8% as mostly positive."
- "68% have had dogs enter their hostel or building; 61% have felt unsafe or been chased."
- "86% chose managed coexistence (out of hostels, designated areas, or vaccinated/sterilised only); 8% want free movement."
- "Of those who felt unsafe or chased, 87% rate dogs a 4–5 problem, against 22% of the rest."
- "71% didn't know about campus sterilisation or the CCF."
