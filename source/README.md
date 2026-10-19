# source/ — raw team material (INTERNAL, private repo)

Raw group-chat export and shared files from the project team. Contains real names of classmates and interviewees: keep internal, and anonymise in analysis/deliverables (see AGENTS.md rule 4).

| Path | What it is |
|---|---|
| `whatsapp/` | WhatsApp group "comm outreach" library (16/8–19/10/2026). Start with `whatsapp/INDEX.md`. Includes the course PPTX and its extracted text. |
| `whatsapp-comm-kaam/` | Second WhatsApp group "Comm Kaam" (forwarded media + guards' field notes). |
| `drive-inventory.csv` | All 72 files in the team Drive folder `1RwPyoukOcCx7umyHtwqF9Zhilzpci8-V` (flat, no subfolders): name, id, mime, size, created/modified (UTC), owner, category, download_status. |
| `media-metadata.csv` | Per downloaded media file: duration, embedded creation time (IST), GPS. |
| `drive/comm outreach/` | Docs and photos from Drive: `ccf gmeet transcript.pdf`, 4 × `20261013_*.jpg`, `comm1/2.jpeg`, 2 × HEIC. |
| `ccf-gmeet-transcript.txt` | Text of the CCF Google Meet transcript PDF (Tactiq auto-transcript, 24/9). |
| `gandagi.md` | Vinayak's Google Doc "Gandagi" (24/9), verbatim. |
| `survey/` | Anonymised survey export and analysis inputs. |

Project brief: `../project-brief.md`.

## Audio and video: GitHub release `source-media-v1`
https://github.com/Vinayak-RZ/community-outreach/releases/tag/source-media-v1
Zips are uncompressed (stored), and paths inside them are `comm outreach/<original Drive filename>`. Checksums are in `SHA256SUMS.txt`.

| Asset | Files | Size | Contents |
|---|---|---|---|
| `audio-interviews.zip` | 28 | 113 MB | All Drive audio (m4a/opus) |
| `video-2026-08-23-meetup.zip` | 10 | 417 MB | IMG_0570, IMG_5259–5267, 5269 (.MOV) |
| `video-other.zip` | 13 | 281 MB | Smaller mp4/MOV interviews already processed |
| `SHA256SUMS.txt` | — | — | sha256 of the three zips |

## Large Drive videos: GitHub release `raw-drive-videos-v1`
https://github.com/Vinayak-RZ/community-outreach/releases/tag/raw-drive-videos-v1

Uploaded from Vinayak's laptop (Asia/Calcutta 2026-10-19). All 12 previously pending Drive videos are now on the box under `source/drive-large/` (not in git; too large). Staged for the pipeline worker at `media/staging-large/` (see that folder's `STAGING.md`). Do not put them in the inbox.

| Asset | Size | Contents |
|---|---|---|
| `drive-download-20261019T101529Z-1-002.zip` | 1.61 GB | IMG_5268.MOV, IMG_9408.MOV, plus smaller already-held videos |
| `drive-download-20261019T101529Z-1-003.zip` | 1.46 GB | IMG_9401.MOV, IMG_9402.MOV, IMG_9409.MOV, plus smaller already-held videos |
| `drive-download-20261019T101529Z-1-004.zip` | 0.80 GB | IMG_9404.MOV, IMG_9405.MOV, VID-20261016-WA0018.mp4, plus smaller already-held videos |
| `drive-download-20261019T101529Z-1-005.zip` | 1.04 GB | 20261013_120723.mp4, IMG_0576.MOV, IMG_9395.MOV, plus smaller already-held videos |
| `recording-2026-09-25.mp4.part1` + `.part2` | 1.50 + 1.38 GB | Rejoined on the box as `Recording 2026-09-25 163540.mp4` (2.90 GB, 36.4 min; ffprobe ok) |

### Newly obtained (12 pending → received; 1.43 hours total)

| File | Duration | Size |
|---|---:|---:|
| `Recording 2026-09-25 163540.mp4` | 36.4 min | 2.90 GB |
| `IMG_5268.MOV` | 9.8 min | 906 MB |
| `VID-20261016-WA0018.mp4` | 9.6 min | 104 MB |
| `IMG_9409.MOV` | 4.8 min | 543 MB |
| `IMG_9408.MOV` | 4.3 min | 482 MB |
| `IMG_9402.MOV` | 3.8 min | 422 MB |
| `IMG_0576.MOV` | 3.7 min | 440 MB |
| `IMG_9395.MOV` | 3.3 min | 375 MB |
| `IMG_9401.MOV` | 3.2 min | 362 MB |
| `IMG_9404.MOV` | 2.7 min | 302 MB |
| `IMG_9405.MOV` | 2.6 min | 287 MB |
| `20261013_120723.mp4` | 1.7 min | 125 MB |

Twenty-two other files inside the zips are sha256 duplicates of media already in `media/manifest.csv` / `source-media-v1` and were not restaged.

### Still missing from Drive
None of the 12 previously pending videos. Photos and audio were already complete.
