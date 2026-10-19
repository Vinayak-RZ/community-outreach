# Survey data dictionary — "Condition of Dogs in campus" (Google Form)

- **Responses sheet:** "Removal of dogs from campus (Responses)", owned by Vrinda Gupta, Drive id `1ZWFgR2P-y6Hr0ne9CB-hOdIdsSk9A65466EfbjXwQ5k`. Exported read-only on 19/10/2026: 1 tab ("Form Responses 1"), 211 responses, 10 columns.
- **Form:** https://forms.gle/njHLxCJCfrVBztiw8 (live title "Condition of Dogs in campus"). Option lists, required flags and scale labels below were read from the public form page on 19/10/2026. The form may have been edited since responses were collected.
- **Files in this folder:**
  - `survey-responses.csv` / `.xlsx`: **de-identified** export.
    - The `Email Address` column is replaced by `dept_from_email`, the part of the address before `.iitr.ac.in` (e.g. `ee`, `me`). Non-IITR addresses become `(personal email)` and blanks become `(no email)`.
    - One free-text answer that gave a room number (sheet row 83) is redacted.
    - `sheet_row` = the row number in the original Google Sheet, where row 1 is the header.
    - Two `[coded]` columns hold the analysts' coding (see below).
  - The full export, emails included, stays only on the box at `/workspace/library/acads/community-outreach/source/survey/` and isn't committed.

| # | Column (exact question text) | Type | Required | Options |
|---|---|---|---|---|
| 0 | Timestamp | auto (sheet time) | — | 2026-10-13 10:51 to 2026-10-17 22:05 |
| 1 | Email Address | auto-collected | — | 191 filled, 20 blank. The blanks are the first 20 responses (rows 2–21, 13/10 10:51–10:58), so collection was apparently switched on after them. **Not in the repo copy.** |
| 2 | I am a | single choice + Other | yes | Student / Faculty / Non-teaching staff / Other (text) |
| 3 | How would you describe your experience with campus dogs? | single choice | yes | Mostly positive / Mostly negative / Both positive and negative / Neutral / Rarely interact |
| 4 | What problems have you personally experienced because of campus dogs? | checkboxes (multi-select), stored comma-joined | yes | Dogs entering hostels/buildings / Feeling unsafe or being chased / Noise or dog fights / Hygiene/waste / No significant problems |
| 5 | What is the strongest reason you believe dogs have a place in the campus community? | single choice | no | They deserve humane treatment / They are part of campus life / They provide companionship / Caring for animals is our responsibility / They can coexist with humans. There is no "they don't" option. |
| 6 | Where should the boundary between dogs and student spaces lie? | single choice + Other | yes | Free movement across campus / Restricted from hostels/buildings / Restricted to designated areas / Allowed only if vaccinated/sterilized / Other (text). **"Remove from campus" is not an option**: the 2 responses with that exact text were typed into Other. |
| 7 | Are you aware of any organized sterilization or the CCF committee in campus? | single choice | yes | Yes / No |
| 8 | On a scale of 1–5, how much of a problem do you consider campus dogs to currently be? | linear scale 1–5 | yes | 1 = "No problem", 5 = "Serious problem" |
| 9 | What would a fair solution look like for both students and dogs? | paragraph (free text) | no | 98 of 211 answered |

## Coded columns (added by Acads, 19/10/2026)
- `[coded] boundary_recoded`: Q6 with the 11 "Other" texts sorted into *Remove from campus (free text)* (rows 51, 93, 196, 197, 201), *Restriction (free text)* (13, 37, 125) or *Unclear* (80, 83, 112). The two typed "Remove from campus" answers keep that label.
- `[coded] text_removal_stance`: Q9, hand-coded for the 98 written answers.
  - *remove all/most (sole proposal)*: rows 12, 13, 17, 25, 38, 51, 57, 72, 84, 93, 159, 162, 193, 196, 197, 210
  - *remove as one option / ideal*: 20, 23, 27, 58, 60, 69, 143, 146, 156, 186
  - *remove only aggressive dogs/packs*: 31, 80, 96, 127, 138
  - *no removal proposed*: everything else

  This is one coder's judgement and should be checked by a second team member.
