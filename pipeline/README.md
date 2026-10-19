# Media pipeline (transcription + face blurring)

Turns interview audio/video for the EEC 399 campus-dogs project into timestamped
transcripts (Hindi / English / mixed) and face-blurred copies of the videos.

Runs on the shared box. Media lives in `/workspace/library/acads/community-outreach/media/`
and **is never committed to git**. Transcripts can go into the private Illusion repo under
`transcripts/`; blurred videos go to GitHub Releases.

## Folders (`$MEDIA_ROOT`)

| Folder | What |
|---|---|
| `inbox/` | Drop new files here (audio, video, photos). Duplicates get moved to `inbox/_duplicates/`. |
| `raw/` | Originals, moved from inbox and made read-only. Never edited. |
| `transcripts/<name>/` | `<name>.txt` (timestamped lines), `.srt` (subtitles), `.json` (segments + word timings + model/language info), and `.en.*` when translated. |
| `blurred/` | `<name>.blurred.mp4` (audio kept, metadata stripped) or `<name>.blurred.jpg`. |
| `logs/` | `process-inbox.log`, `transcribe.log`, `blur.log`. |
| `manifest.csv` | One row per file: file, sha256, date_added, type, duration_s, language (with detection confidence), transcript_path, translation_path, blurred_path, status, notes. |

## Usage

```bash
cd /workspace/library/acads/community-outreach/pipeline

# Everything new in inbox/: ingest -> transcribe (audio+video) -> blur (video+photos)
./process-inbox                       # auto-detect language
./process-inbox --translate           # also write English translations (.en.*)
./process-inbox -l hi --translate     # force Hindi (use when auto-detect picks wrong)
./process-inbox --initial-prompt "IIT Roorkee, campus dogs, mess, hostel, guard"   # vocabulary hint
./process-inbox --dry-run             # show what would be ingested
./process-inbox --only FILE.mp4 --force   # redo one file
./process-inbox --no-blur / --no-transcribe

# Queue a redo with a forced language, picked up after the current queue (no new process needed):
# add "FILE<TAB>LANG" lines to media/logs/requeue.tsv. Only a catch-all run (no --files-from/--only,
# not --no-transcribe) redoes them; old outputs are copied to logs/requeue-backup/ first, and a file
# is skipped once its transcript was made with that forced language.

# Single files
./transcribe interview.m4a -o /tmp/out [-l hi] [--translate] [-m medium] [-v]
./blur in.mp4 out.mp4 [--backend auto|egoblur|yunet] [--threshold 0.5] [--scale 1.4]
./blur photo.jpg photo.blurred.jpg
```

Re-running is safe: files are tracked by SHA-256, finished steps are skipped,
failed steps (`status = error: ...`) are retried next run. Only one
`process-inbox` runs at a time (lock file in `logs/`).

## Transcription

- faster-whisper 1.2.1 (CTranslate2 4.8.3), CPU only (no GPU on the box).
- Transcribe model: **large-v3-turbo, float32**. About 3.5x faster than real time
  (2 min of audio takes about 35 s, plus about 10 s to load the model). It gave clean Devanagari on a Hindi/Hinglish test.
- Translation: Whisper's built-in speech-to-English using **medium, float32** (turbo
  can't translate). This is a second pass, so expect roughly double the time. English
  audio is copied rather than "translated", because Whisper garbles English-to-English.
- **Do not use int8** on this box. On this Xeon (AMX/AVX-512), CTranslate2's int8 path
  produced garbage, mostly in Hindi. full large-v3 in float32 needs more than 10 GB to load,
  and the shared box OOM-killed it. Override with `WHISPER_MODEL` / `WHISPER_COMPUTE`
  if the hardware changes (on a GPU use large-v3 with float16).
- Hindi speech comes out in Devanagari. English words said mid-sentence often come out
  transliterated ("स्टूडेंट्स", "कंप्लेंट"). Check names and numbers against the audio
  before quoting.

## Face blurring

- `blur.py` streams frames through ffmpeg at a constant frame rate, detects faces on every frame
  (`--detect-every`), and also blurs the boxes from the last 3 detections (`--hold`)
  to cover single-frame misses. Each box is enlarged 1.4x and gets an elliptical pixelate+blur.
  The video is re-encoded as H.264 and the original audio copied back in as AAC.
- Backends:
  - `egoblur`: Meta EgoBlur Gen2 face model (preferred). Installed in its own venv
    (`egoblur` 2.0.1, torch 2.9.1 CPU). It needs the weights file at
    `$EGOBLUR_FACE_MODEL` (`/workspace/tools/models/egoblur/ego_blur_face_gen2.jit`).
    **Weights aren't downloaded yet.** Meta only distributes them through an email form at
    https://www.projectaria.com/tools/egoblur ("Download EgoBlur Gen 1 and Gen 2").
    Submitting it means agreeing to the model license and to receive emails.
    Unzip the face model so it ends up at that path, and `auto` picks it up.
    On CPU expect about 1.5 s per frame, so a 10-minute 30 fps video is about 7.5 h. Use
    `--detect-every 2-3` to speed it up, at some risk.
  - `yunet`: OpenCV YuNet (official opencv_zoo model, MIT). Interim fallback, about 25-30 fps
    at 720p. Fine for frontal and three-quarter faces, weaker on small, profile, or occluded faces.
  - `auto` (default): egoblur if its weights exist, otherwise yunet.
- **Always spot-check blurred output by eye before publishing.** Lower `--threshold`
  to blur more aggressively. False positives (e.g. a clock face) are harmless.
- Photos: blurred copies lose EXIF (including geotags) on purpose. The geotagged
  original stays in `raw/` as evidence.

## Setup / rebuild

`./setup.sh` reinstalls everything into `/workspace/tools` (venvs, EgoBlur repo,
YuNet model, Whisper models). Paths and models are set in `config.sh` and can be changed with env vars.

## Tested

19 Oct 2026, end-to-end via `process-inbox --translate`:
- Video: 20 s, 720p cut (from 0:30) of *Interview on extreme weather with physical geographer
  Hannah Cloke – The Royal Society*, CC BY 3.0, The Royal Society, via Wikimedia Commons
  (https://commons.wikimedia.org/wiki/File:Interview_on_extreme_weather_with_physical_geographer_Hannah_Cloke_%E2%80%93_The_Royal_Society.webm).
  Language detected en (1.00), transcript accurate, both faces blurred, audio kept.
- Audio: 17 s Hinglish sentence synthesised with Google TTS (gTTS) for the test.
  Detected hi (0.96), transcript verbatim in Devanagari, English translation correct.
- Re-run skipped both files, and a duplicate drop went to `_duplicates/`. Test rows were then
  removed from the manifest.
