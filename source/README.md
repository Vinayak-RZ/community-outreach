# source/ — raw team material (INTERNAL, private repo)

Raw group-chat export and shared files from the project team. Contains real names of classmates and interviewees: keep internal, and anonymise in analysis/deliverables (see AGENTS.md rule 4).

| Path | What it is |
|---|---|
| `whatsapp/` | WhatsApp group "comm outreach" library (16/8–19/10/2026). Start with `whatsapp/INDEX.md`. Includes the course PPTX and its extracted text. |
| `drive-inventory.csv` | All 72 files in the team Drive folder `1RwPyoukOcCx7umyHtwqF9Zhilzpci8-V` (flat, no subfolders): name, id, mime, size, created/modified (UTC), owner, category, download_status. |
| `media-metadata.csv` | Per downloaded media file: duration, embedded creation time (IST), GPS. |
| `drive/comm outreach/` | Docs and photos from Drive: `ccf gmeet transcript.pdf`, 4 × `20261013_*.jpg`, `comm1/2.jpeg`, 2 × HEIC. |
| `ccf-gmeet-transcript.txt` | Text of the CCF Google Meet transcript PDF (Tactiq auto-transcript, 24/9). |
| `gandagi.md` | Vinayak's Google Doc "Gandagi" (24/9), verbatim. |

Project brief: `../project-brief.md`.

## Audio and video: GitHub release `source-media-v1`
https://github.com/Vinayak-RZ/Illusion/releases/tag/source-media-v1
Zips are uncompressed (stored), and paths inside them are `comm outreach/<original Drive filename>`. Checksums are in `SHA256SUMS.txt`.

| Asset | Files | Size | Contents |
|---|---|---|---|
| `audio-interviews.zip` | 28 | 113 MB | All Drive audio (m4a/opus): Agrim, Archi dept ma'am, Cautley Bhawan ×2, Chayan, Indian Institute of Technology ×3, Jawahar bhawan guard, Jawahar rishit, Mac balu, Mac guard, Malishka pt1/pt2, Mnc guard, Neh Road 2/3/4, ROBOCON, Sarojini bhawan guard, Sarojni Canteen, Uttkarsh, VK canteen bhaiya, Voice 261013_122210 / 261014_223912 / 261014_230515, Wasif, AUD-20261015-WA0000.opus |
| `video-2026-08-23-meetup.zip` | 10 | 417 MB | IMG_0570, IMG_5259, 5260, 5261, 5263, 5264, 5265, 5266, 5267, 5269 (.MOV; 23/8 meetup, mostly geotagged) |
| `video-other.zip` | 13 | 281 MB | 20261013_120605.mp4, 20261014_225642/230442/232749/234047/234618.mp4, IMG_9397.MOV, IMG_9400.MOV, VID-20261016-WA0012.mp4, ccf bhavagna interview.mp4, comm.mp4, comm3.mp4, comm4.mp4 |
| `SHA256SUMS.txt` | — | — | sha256 of the three zips |

## Not yet fetched: 12 videos, 7.6 GB (still only on Drive)
These can't be fetched from the box yet. The connector's limits are 100 MB (DownloadFile) and 10 MB (download_file_content). The files are shared only with the iitr.ac.in domain, so an unauthenticated download redirects to Google sign-in.
Recording 2026-09-25 163540.mp4 (3.05 GB; split into parts under 2 GB when added), IMG_5268.MOV (950 MB), IMG_9409.MOV (569 MB), IMG_9408.MOV (506 MB), IMG_0576.MOV (461 MB), IMG_9402.MOV (442 MB), IMG_9395.MOV (393 MB), IMG_9401.MOV (380 MB), IMG_9404.MOV (317 MB), IMG_9405.MOV (301 MB), 20261013_120723.mp4 (131 MB), VID-20261016-WA0018.mp4 (109 MB).
