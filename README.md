# Illusion — EEC 399 Community Outreach

Home for the **EEC 399 Community Outreach** project (Department of Electrical Engineering, IIT Roorkee). The assigned topic is campus dogs ("Two sides of one street"): understanding problems people face from dogs on campus, problems dogs face, and where campus consensus might lie, with an aim toward humane, practical recommendations.

This repository holds course materials, source records, interview notes, evidence, analysis, and final deliverables. Future analysis and inference by agents is also expected to run against this repo.

## Folder map

| Path | Contents |
|------|----------|
| `course/` | Course deck (`.pptx`), extracted text, and overview notes |
| `source/` | Raw group chat exports and shared files from the team |
| `interviews/` | Interview notes |
| `transcripts/` | Machine transcripts (Whisper) of interview audio/video, one folder per recording |
| `pipeline/` | Media pipeline scripts: transcription (faster-whisper) and face blurring (EgoBlur / YuNet) |
| `evidence/` | Photos, videos, consent sheets, field diary |
| `analysis/` | Analysis notebooks, dataset summaries, inference artefacts |
| `deliverables/` | Poster, KPI table, and other final submissions |
| `AGENTS.md` | Guidance for agents working in this repo |

## Large files

Binary media and other large files (roughly over 20 MB, or bundled photo/video archives) are **not** committed here. They are published as [GitHub Release](https://github.com/Vinayak-RZ/Illusion/releases) assets. Pointers or short README notes in the relevant folders should name the release and asset when something is published that way.

## Privacy

This repo is **private** (since 19 Oct 2026). Raw material and transcripts can be kept here as they are, with real names. Privacy still matters: keep it inside the team, and use roles or codes instead of interviewee names in anything that leaves the team (poster, deliverables) unless consent covers publishing. See `AGENTS.md`.
