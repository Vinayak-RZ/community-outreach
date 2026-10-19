# Campus dogs: two sides of one street

**EEC 399 Community Outreach · Department of Electrical Engineering, IIT Roorkee · Autumn 2026–27**
Topic 3 · Group 23 · Private repository (internal to the team)

This repo is where the group's fieldwork on campus dogs at IIT Roorkee is compiled: course material, raw sources, survey data, transcripts, analysis and deliverables. Agents and team members work from it. Facts below come from `project-brief.md` and `course/course-overview.md`, which cite their sources.

## Team
Vansh Gautam (team lead, group admin), Vinayak Raizada, Jay D, Vrinda Gupta, Jiya Dubey, Khushi, nandini. Roles and contributions are in `project-brief.md` → "Team and roles".

<!-- status:start -->
## Status
_Last updated: 19 Oct 2026, 22:30 IST. Numbers are refreshed from the pipeline's `manifest.csv` each time transcripts are pushed._

**Collected**
- Survey: 211 responses (13–17/10), de-identified copy in `source/survey/`.
- Interview audio: 29 recordings, 2.07 h (the 28 Drive audio files plus the CCF interview, an audio-only `.mp4`). Two Drive files ("Indian Institute of Technology" and "… 2") have identical audio, so that recording is counted twice here.
- Videos: 51 files, 1.87 h (Drive videos, the Comm Kaam WhatsApp videos, and the 12 large Drive videos including the 36-minute recording of 25/9).
- 3 more files were exact re-sends of recordings already held (same decoded audio) and aren't counted.
- Releases: [`source-media-v1`](https://github.com/Vinayak-RZ/community-outreach/releases/tag/source-media-v1), [`comm-kaam-media-v1`](https://github.com/Vinayak-RZ/community-outreach/releases/tag/comm-kaam-media-v1), [`raw-drive-videos-v1`](https://github.com/Vinayak-RZ/community-outreach/releases/tag/raw-drive-videos-v1).

**Transcribed**: 32 of 80 recordings (3.00 of 3.95 h); interview audio 29 of 29. English translations: 3. See [`transcripts/INDEX.md`](transcripts/INDEX.md). Machine transcripts: check against the audio before quoting.

**Analysis**: the survey analysis is in [`analysis/survey-analysis.md`](analysis/survey-analysis.md) (headline results below). Interview coding hasn't started: `interviews/` holds only its README so far.

**In progress**: transcription (with English translations) of the remaining interview audio, then the large Drive videos, then the Comm Kaam and other Drive videos. Face blurring (YuNet) comes after that: 11 of 51 videos blurred so far; the blurred-media release isn't published yet.

**Open KPI and evidence gaps**
- No consent sheets, no contact log, and no dated field diary yet (Reach and Depth evidence).
- No hospital or admin data on bites, vaccination or sterilisation (requests sent, no reply).
- Output and Change have no written acknowledgement yet.
<!-- status:end -->

## Aim and research questions
The course frames this as *enquiry, not charity*: go into a community on or beside campus, understand the real problem with the people living it, and ask honestly whether technology helps (`course/course-overview.md`, slides 1–2).

For Topic 3 the deck asks: *"What happens when it's not safe to walk in a campus?"* (slide 8). The group's working questions:
1. **The afraid side.** What problems do people face because of campus dogs: bites, chases, dogs in hostels, hygiene, routes avoided after dark?
2. **The dogs' side.** What problems do the dogs face (food, injury, shelter, mistreatment), and who looks after them: CCF, feeders, guards?
3. **Population and territory.** Where are the hotspots, and how many dogs are there?
4. **Facts on record.** Health-centre bite and vaccination figures, sterilisation (ABC) status, existing policy.
5. **Consensus.** Where do both sides agree, and what coexistence proposal would both sides actually sign?

## Method
| Strand | What | Status (19/10/2026) |
|---|---|---|
| Interviews | Guards (gates, bhawans, MAC, MNC), canteen and mess staff, students, faculty, a CCF member, the CMO at the institute hospital | ~40 audio and video files on Drive, ~113 min of audio downloaded. CMO interview 13/10, notes only (recording not allowed). Being transcribed (see Status). |
| CCF meeting | Google Meet with a CCF office-bearer, 24/9: feeding, medical care, sterilisation, shelter, hotspots | Auto-transcript in `source/ccf-gmeet-transcript.txt` |
| Survey | Google Form "Condition of Dogs in campus", 13–17/10 | **211 responses**, analysed in `analysis/survey-analysis.md` |
| Field observation | Fieldwork night 14/10, hostel and campus videos and photos (several GPS-tagged), field notes | Media in release `source-media-v1`; notes in `source/gandagi.md` |
| Records | Emails to the hospital, director and CMO asking for bite, vaccination and sterilisation data | No data received yet |

## Headline survey results (n = 211, 209 students)
From `analysis/survey-analysis.md`:
- 52.1% describe their experience with campus dogs as mostly negative; 21.8% as mostly positive.
- 67.8% have had dogs enter their hostel or building; 61.1% have felt unsafe or been chased.
- 85.8% chose a managed-coexistence boundary (out of hostels, designated areas, or vaccinated/sterilised only); 8.1% chose free movement. Removal wasn't a listed option: 7 typed it in, and 26 of 98 free-text answers propose it.
- 70.6% didn't know about organised sterilisation or the CCF.

## What's in each folder
| Path | Contents |
|---|---|
| `project-brief.md` | **Start here.** Course requirements, team, interviews, findings, the KPI table draft and open tasks, with a source for every fact. |
| `course/` | Course deck (`.pptx`), extracted text, and `course-overview.md` |
| `source/` | Raw inputs. `whatsapp/` (group chat library), `drive-inventory.csv` (all 72 Drive files), `media-metadata.csv` (duration, date, GPS), `drive/` (docs and photos), `survey/` (de-identified responses + data dictionary), CCF transcript, field notes. See `source/README.md`. |
| `transcripts/` | Machine transcripts (Whisper) of interview audio and video, one folder per recording |
| `pipeline/` | Media pipeline scripts (see below) |
| `interviews/` | Interview notes and coded summaries |
| `evidence/` | Consent sheets, field diary, photo and video pointers |
| `analysis/` | `survey-analysis.md`, `figures/` (poster-ready charts), `scripts/` (reproducible analysis) |
| `deliverables/` | Poster, KPI table, other submissions |
| `AGENTS.md` | Rules for agents: cite sources, never invent quotes or numbers, media in Releases, privacy |

## Releases (large media)
Audio, video and other large binaries are **never committed**; `.gitignore` blocks media types. They're published as GitHub Release assets: https://github.com/Vinayak-RZ/community-outreach/releases
- **`source-media-v1`**: the original Drive media, as stored (uncompressed) zips. Paths inside are `comm outreach/<Drive filename>`, with checksums in `SHA256SUMS.txt`.
  - `audio-interviews.zip`: all 28 audio files
  - `video-2026-08-23-meetup.zip`: 10 videos from the 23/8 meetup
  - `video-other.zip`: 13 videos from 13–16/10, the CCF interview and the comm clips
- Twelve large videos (7.6 GB, including the 3.05 GB recording of 25/9) aren't in a release yet, because they couldn't be fetched from Drive. Any asset over 2 GB gets split.
- Face-blurred videos from the pipeline go in their own release, named in `transcripts/` or `evidence/`.

## Media pipeline (brief)
`pipeline/` runs on the team's shared processing machine (see `pipeline/README.md`):
- New media dropped into the inbox is fingerprinted (SHA-256) and stored read-only.
- It's transcribed with faster-whisper, using the `medium` model in float32 on CPU (Hindi, English or mixed, with an English translation). Medium replaced large-v3-turbo: on the noisy Hindi field recordings turbo produced garbled text and sometimes labelled Hindi speech as English, so it output English instead of a transcript. int8 was garbled on this machine, and full large-v3 didn't fit in memory.
- Faces in videos and photos are blurred (EgoBlur / YuNet).
- Everything is logged in `manifest.csv`.
- Transcripts land in `transcripts/`. Machine transcripts must be checked against the audio before quoting.

## Deliverables (final review: "October", exact date not yet announced)
From the course deck, slides 16–19:
1. **A3 poster**: printed, plus a PDF. It's about the community, not the team ("no team-selfie posters").
2. **KPI table**: five rows (Reach, Depth, Record, Output, Change), with the team's targets and achieved figures, each backed by evidence. There's a draft in `project-brief.md`.
3. **Evidence**: geotagged photos, dated videos, interview records, datasets, consent sheets and a dated field diary. "A claim with no evidence is treated as not done."
4. **Group and individual viva**: every member must be able to defend the work and tell the same story.

## Status and next steps
**Done**
- Survey (211 responses) and its analysis
- CCF interview and meeting, CMO interview, guard, canteen and student interviews (~40 recordings)
- Drive inventory and media release

**Next**
1. Transcribe and code the interviews, and de-duplicate them into a contact log (Reach target: 30+ interviews).
2. Consent sheets and a dated field diary with person-hours (Reach and Depth evidence). Neither exists yet.
3. A one-page survey method note, and a second-coder check of the free-text coding (Record).
4. A hotspot map from the GPS-tagged media and named hotspots (Record).
5. Hospital and admin figures on bites, vaccination and sterilisation (still no reply).
6. Output and Change: e.g. an awareness poster at MAC or one bhawan made with CCF, plus a written findings note to the relevant office, each with a written acknowledgement.
7. Fetch the 12 remaining large videos; poster layout; viva prep.

## Privacy
This repo is **private**. `source/` and `transcripts/` contain raw team material with real names, so keep it inside the team. The survey copy here is de-identified: emails were replaced by a department code. On the poster and in any deliverable, use roles or codes instead of interviewee names unless written consent covers publishing them (course ethics rules, slide 20). See `AGENTS.md`.
