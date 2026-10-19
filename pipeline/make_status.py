#!/usr/bin/env python3
"""Refresh the auto-generated Status section of the repo README from media/manifest.csv.

Replaces the text between <!-- status:start --> and <!-- status:end --> in README.md.
Only counts things that can be read from the manifest, the inbox and the repo.
Rule: never commit the status on its own. Run this right before every commit and stage
README.md in that same commit (`--stage` does the `git add`; `pipeline/commit` wraps it all).
"""
import csv, json, os, subprocess, sys
from datetime import datetime, timedelta, timezone

ROOT = os.environ.get("MEDIA_ROOT", "/workspace/library/acads/community-outreach/media")
args = [a for a in sys.argv[1:] if a != "--stage"]
README = args[0] if args else "/workspace/repos/Illusion/README.md"
IST = timezone(timedelta(hours=5, minutes=30))
REL = "https://github.com/Vinayak-RZ/community-outreach/releases/tag/"


def dur(p):
    try:
        return float(json.loads(subprocess.run(["ffprobe", "-v", "error", "-print_format", "json", "-show_format", p],
                                               capture_output=True, text=True).stdout)["format"]["duration"])
    except Exception:
        return 0.0


rows = [r for r in csv.DictReader(open(os.path.join(ROOT, "manifest.csv"), encoding="utf-8"))
        if r["type"] in ("audio", "video") and not r["status"].startswith("duplicate")]
dups = sum(1 for r in csv.DictReader(open(os.path.join(ROOT, "manifest.csv"), encoding="utf-8")) if r["status"].startswith("duplicate"))
items = [(r["type"], float(r["duration_s"] or 0), bool(r["transcript_path"] and os.path.exists(os.path.join(ROOT, r["transcript_path"]))),
          bool(r.get("translation_path") and os.path.exists(os.path.join(ROOT, r["translation_path"]))),
          bool(r.get("blurred_path") and os.path.exists(os.path.join(ROOT, r["blurred_path"])))) for r in rows]
for f in sorted(os.listdir(os.path.join(ROOT, "inbox"))):  # queued, not yet ingested
    p = os.path.join(ROOT, "inbox", f)
    if os.path.isfile(p) and not f.startswith((".", "_")):
        items.append(("video", dur(p), False, False, False))
h = lambda L: sum(x[1] for x in L) / 3600
au = [x for x in items if x[0] == "audio"]; vi = [x for x in items if x[0] == "video"]
tr = [x for x in items if x[2]]; en = [x for x in items if x[3]]; bl = [x for x in vi if x[4]]
now = datetime.now(IST)
block = f"""## Status
_Last updated: {now:%d %b %Y, %H:%M} IST. Numbers are refreshed from the pipeline's `manifest.csv` each time transcripts are pushed._

**Collected**
- Survey: 211 responses (13–17/10), de-identified copy in `source/survey/`.
- Interview audio: {len(au)} recordings, {h(au):.2f} h (the 28 Drive audio files plus the CCF interview, an audio-only `.mp4`). Two Drive files ("Indian Institute of Technology" and "… 2") have identical audio, so that recording is counted twice here.
- Videos: {len(vi)} files, {h(vi):.2f} h (Drive videos, the Comm Kaam WhatsApp videos, and the 12 large Drive videos including the 36-minute recording of 25/9).
- {dups} more files were exact re-sends of recordings already held (same decoded audio) and aren't counted.
- Releases: [`source-media-v1`]({REL}source-media-v1), [`comm-kaam-media-v1`]({REL}comm-kaam-media-v1), [`raw-drive-videos-v1`]({REL}raw-drive-videos-v1).

**Transcribed**: {len(tr)} of {len(items)} recordings ({h(tr):.2f} of {h(items):.2f} h); interview audio {sum(1 for x in au if x[2])} of {len(au)}. English translations: {len(en)}. See [`transcripts/INDEX.md`](transcripts/INDEX.md). Machine transcripts: check against the audio before quoting.

**Analysis**: the survey analysis is in [`analysis/survey-analysis.md`](analysis/survey-analysis.md) (headline results below). Interview coding hasn't started: `interviews/` holds only its README so far.

**In progress**: transcription (with English translations) of the remaining interview audio, then the large Drive videos, then the Comm Kaam and other Drive videos. Face blurring (YuNet) comes after that: {len(bl)} of {len(vi)} videos blurred so far; the blurred-media release isn't published yet.

**Open KPI and evidence gaps**
- No consent sheets, no contact log, and no dated field diary yet (Reach and Depth evidence).
- No hospital or admin data on bites, vaccination or sterilisation (requests sent, no reply).
- Output and Change have no written acknowledgement yet.
"""
s = open(README, encoding="utf-8").read()
a, b = "<!-- status:start -->", "<!-- status:end -->"
if a not in s:
    raise SystemExit("status markers not found in README")
i, j = s.index(a) + len(a), s.index(b)
open(README, "w", encoding="utf-8").write(s[:i] + "\n" + block + s[j:])
if "--stage" in sys.argv:
    subprocess.run(["git", "-C", os.path.dirname(os.path.abspath(README)), "add", os.path.basename(README)], check=True)
print(f"status: {len(tr)}/{len(items)} transcribed")
