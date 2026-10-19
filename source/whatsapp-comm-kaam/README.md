# source/whatsapp-comm-kaam/ — "Comm Kaam" WhatsApp group (INTERNAL)

WhatsApp group "Comm Kaam", created by Vinayak on 19/10/2026. He is the only member and forwarded campus-dogs material into it from other chats, so original senders and dates aren't shown. Times are IST, 19/10/2026.

| Path | What |
|---|---|
| `messages.md` | All texts verbatim, plus captions and which media went with which time block |
| `media-log.csv` | One row per media item (P01–P25 photos, V01–V25 videos, A01 audio): file, kind, duration, forwarded time, original date, GPS, caption context, location stated or visible, inside a building?, what it shows, duplicate_of, notes |
| `photos/` | 22 of the 25 photos (3.3 MB). The folder is named photos/, not media/, because the repo .gitignore ignores every media/ directory |

**Not committed:**
- **Three photos**, kept on the box only (`/workspace/library/acads/community-outreach/source/whatsapp-comm-kaam/media/`). They're screenshots showing survey respondents' names or emails, and the repo copy of the survey is de-identified.
  - P17 (`3.46.15 PM.jpeg`)
  - P21 (`3.46.17 PM (1).jpeg`)
  - P23 (`3.46.17 PM.jpeg`)
- **`ccf gmeet transcript.pdf`**: byte-identical (md5 `ff44cffa…3276`) to `source/drive/comm outreach/ccf gmeet transcript.pdf`, so it's deduplicated. Its text is in `source/ccf-gmeet-transcript.txt`.
- **Videos and audio**: in the GitHub release **`comm-kaam-media-v1`** (https://github.com/Vinayak-RZ/community-outreach/releases/tag/comm-kaam-media-v1). The zips are uncompressed; paths inside are `comm-kaam/<filename>`.

| Asset | Contents | Size |
|---|---|---|
| `comm-kaam-videos.zip` | all 25 `WhatsApp Video …mp4` (V01–V25) | 250 MB |
| `comm-kaam-audio.zip` | `WhatsApp Audio 2026-10-19 at 3.46.11 PM.mp4` (11:33) | 5.8 MB |
| `SHA256SUMS.txt` | checksums | — |

## Duplicates of material we already have
- The 11:33 audio is **byte-identical** to `ccf bhavagna interview.mp4` (the CCF interview of 17/9; file metadata says 17/9 19:10 IST).
- V22 is byte-identical to `comm3.mp4`. V23 is the same clip as `comm.mp4`, re-encoded.
- V13–V18 are WhatsApp re-encodes of `IMG_5269`, `5264`, `5263`, `5261`, `5260` and `5259.MOV` from Drive (the 23/8 meetup, which carry GPS). Durations match to 0.1 s and frames match on inspection.
- V20 (3:45) and V21 (9:27) have the same lengths as Jay's 24/9 "voice notes" of 3:45 and 9:27 [chat 24/9 7:57–7:58 pm]. They're probably the same recordings: night sessions where team members sit with people near a dog, interview-like. Transcribe them before relying on this.

## Evidence value (for the KPI table's Record row)
- **Dogs inside buildings:** 15 items show dogs inside hostels or departments. Photos P01, P02, P04, P05, P06, P07, P09, P10 and P14 show dogs in corridors, a washroom (with a bin tipped over), outside room doors and next to a bed. Videos V02, V03, V04, V05, V19 and V25 show dogs in office or lab rooms, asleep on a chair, on a bed, in a corridor outside rooms, and in a "study room".
- The block captions name **CB 7th floor**, **CB 8th** and **A block 5th floor** ("There is a dog on cb 7th floor", "a block 5th floor", "Cb8th") [messages.md 3:33, 3:46]. They can't be tied to individual files.
- **Weak as course evidence on their own:** WhatsApp removed all EXIF and creation dates, and no item has GPS. The course asks for "geotagged photographs, dated videos only" (deck slide 18). To count, each item needs its original from the person who took it, or a dated statement of where and when it was taken.
- **Faces are visible** in P11, P18–P22, V07 and V20–V21. Blur them before any of these is used outside the team.

## KPI table image (P24, `WhatsApp Image 2026-10-19 at 3.46.18 PM (1).jpeg`): transcription
> **The KPI table every team must think about**
> Five KPIs, one from each row below. Fill the target yourself; the category is fixed.
>
> | Category | What it measures | Example target | Example Evidence |
> |---|---|---|---|
> | Reach | How many people you actually engaged | 25 individuals from the community | Consent sheet + contact log |
> | Depth | Time spent in genuine contact | 40 person-hours of field time | Dated field diary, mentor-initialled |
> | Record | A dataset or artefact that did not exist before | 1 mapped dataset of 6 gates / 40 stalls | Spreadsheet + methodology note |
> | Output | Something handed back to the community or institute | 1 written submission to the concerned office | Acknowledged copy |
> | Change | One concrete thing that shifted | 1 stated commitment or corrected practice | Written or recorded confirmation |

Its caption, forwarded from the main group, reads: "Were thinking of doing some small scale implementation (can be something as simple as putting posters in a specific bhawan on awareness about handling dogs after talking with ccf) / Can be a big differentiating factor for us" [messages.md 3:46; same text in chat 15/10 8:10 pm].

**What it means for our KPI table:**
- This is the deck's slide 16, word for word. Nothing new in the requirements, and the draft in `project-brief.md` already follows it.
- The evidence column is the checklist we have to meet, and we're short on these:
  - **Reach** needs a consent sheet and contact log. Neither exists yet.
  - **Depth** needs a dated field diary *initialled by a mentor*. There's no diary, and no mentor has been identified (course-overview: "[Unclear] who the mentor is").
  - **Record** needs a methodology note. The survey has none yet, and the hotspot map isn't made.
  - **Output** needs an *acknowledged* copy of what we hand over.
  - **Change** needs written or recorded confirmation.

## "Dogs in a group?" poster (P25, `WhatsApp Image 2026-10-19 at 3.46.18 PM.jpeg`): transcription
> IIT ROORKEE | CAMPUS SAFETY
> **Dogs in a group?**
> Give them space. Give yourself time.
> *(illustration: a student with a backpack walking on a campus path, slowing near three dogs on the path ahead; trees and a building behind)*
> **01 DON'T RUN.** Stay calm. Avoid shouting, sudden movements, or staring directly at the dogs.
> **02 DON'T PUSH THROUGH.** Keep your distance. Don't approach, corner, or try to touch the group.
> **03 GIVE YOURSELF AN EXIT.** If safe, slowly move away or take another route. Don't run.
> **IF YOU'RE BITTEN OR SCRATCHED** Wash the wound with soap and running water for 15 minutes. Seek medical care immediately for rabies assessment.
> Stay aware. Keep your distance. Share the campus.

This is the awareness poster Vinayak made on 15/10, meant to go up around MAC with permission [chat 15/10 9:56 pm, 16/10 3:39 am].

**What it means for our KPI table:**
- It's the strongest candidate for **Output** and **Change**. It only counts if it's actually handed back and confirmed: put up in a named place (MAC or one bhawan) with written permission from CCF, the bhawan or the Chief Warden, with dated, geotagged photos of it in place and an acknowledgement in writing.
- On its own it's "spread awareness", which the deck lists as an untestable aim that loses marks (slide 21). Making it testable could mean a short before-and-after check of whether residents know the three steps or about CCF, or a count of guard-reported incidents at the site. 70.6% of survey respondents didn't know about sterilisation or the CCF (`analysis/survey-analysis.md` §3), which gives the baseline.
- The bite first-aid line should be checked against the CMO's advice (13/10 notes) or a health-centre source before printing, so it's evidence-backed.
