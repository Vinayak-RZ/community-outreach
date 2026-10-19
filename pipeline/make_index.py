#!/usr/bin/env python3
"""Write transcripts/INDEX.md from manifest.csv, transcript JSONs and hand-written notes.

Notes file (TSV: file, description, quality[, date]) holds the one-line descriptions, written
by a person/agent after reading each transcript. Rows without a note say "not yet reviewed".
"""
import csv, json, os, subprocess, sys, statistics
from collections import Counter
from datetime import datetime, timedelta, timezone

ROOT = os.environ.get("MEDIA_ROOT", "/workspace/library/acads/community-outreach/media")
NOTES = os.environ.get("INDEX_NOTES", os.path.join(ROOT, "logs", "index-notes.tsv"))
OUT = sys.argv[1] if len(sys.argv) > 1 else "/workspace/repos/Illusion/transcripts/INDEX.md"
IST = timezone(timedelta(hours=5, minutes=30))


def created_ist(path):
    try:
        t = json.loads(subprocess.run(["ffprobe", "-v", "error", "-print_format", "json", "-show_entries",
                                       "format_tags=creation_time", path], capture_output=True, text=True).stdout)
        v = t.get("format", {}).get("tags", {}).get("creation_time")
        return datetime.fromisoformat(v.replace("Z", "+00:00")).astimezone(IST).strftime("%d/%m/%Y %H:%M") if v else ""
    except Exception:
        return ""


def fmt_dur(s):
    s = int(float(s or 0)); return f"{s // 60}:{s % 60:02d}"


def auto_quality(j):
    segs = j.get("segments", [])
    if not segs:
        return "no speech found"
    lp = statistics.mean(x["avg_logprob"] for x in segs)
    reps = sum(c - 1 for c in Counter(x["text"] for x in segs if len(x["text"]) > 8).values() if c > 2)
    q = "good" if lp > -0.35 else "fair" if lp > -0.55 else "poor"
    return f"{q} (mean logprob {lp:.2f}" + (f", {reps} repeated lines" if reps else "") + ")"


notes = {}
if os.path.exists(NOTES):
    with open(NOTES, encoding="utf-8") as f:
        for r in csv.DictReader(f, delimiter="\t"):
            notes[r["file"]] = r
rows = list(csv.DictReader(open(os.path.join(ROOT, "manifest.csv"), encoding="utf-8")))
out = ["# Transcripts index", "",
       "Machine transcripts (faster-whisper `medium`, float32, CPU) of the project's interview audio and videos.",
       "Hindi speech is written in Devanagari. `.en.*` files are Whisper's English translation, a reading aid only:",
       "don't quote it as the speaker's words. Check names, numbers and key quotes against the audio before citing.",
       "", "Date is the file's embedded creation time in IST. Many Drive copies only carry their export time "
       "(19/10/2026), which is marked as such. Descriptions are written from the transcript only.", "",
       "| File | Date (IST) | Duration | Language | Who / topic (from transcript) | Quality | Transcript |",
       "|---|---|---|---|---|---|---|"]
total = n = 0
for r in rows:
    if r["type"] not in ("audio", "video"):
        continue
    nt = notes.get(r["file"], {})
    dup = r["status"].startswith("duplicate")
    tp = r.get("transcript_path", "")
    j = {}
    if tp and os.path.exists(os.path.join(ROOT, tp)):
        j = json.load(open(os.path.join(ROOT, tp), encoding="utf-8"))
    if not dup and j:
        total += float(r["duration_s"] or 0); n += 1
    date = nt.get("date") or created_ist(os.path.join(ROOT, "raw", r["file"]) if not dup else os.path.join(ROOT, "inbox", r["file"]))
    if date.startswith("19/10/2026") and not nt.get("date"):
        date += " (export time)"
    lang = ""
    if j:
        det = j.get("language_policy_detection") or {}
        lang = j["language"] + (f" (detector: {det['detected']} {det['probability']:.2f})" if det else "")
    desc = nt.get("description") or ("not yet reviewed" if j else "not transcribed yet")
    if dup:
        desc = f"Duplicate: {r['status']} (identical audio). " + (nt.get("description") or "")
    qual = "; ".join(x for x in [nt.get("quality", ""), auto_quality(j) if j else ""] if x)
    link = ""
    if tp:
        stem = os.path.basename(os.path.dirname(tp))
        link = f"[txt]({stem.replace(' ', '%20')}/{stem.replace(' ', '%20')}.txt)"
        if r.get("translation_path"):
            link += f" · [en]({stem.replace(' ', '%20')}/{stem.replace(' ', '%20')}.en.txt)"
    out.append(f"| {os.path.basename(r['file'])} | {date} | {fmt_dur(r['duration_s'])} | {lang} | {desc} | {qual} | {link} |")
out += ["", f"Transcribed so far: {n} recordings, {total / 3600:.2f} h (duplicates not counted).",
        f"Generated {datetime.now(IST):%d/%m/%Y %H:%M} IST by `pipeline/make_index.py`.", ""]
os.makedirs(os.path.dirname(OUT), exist_ok=True)
open(OUT, "w", encoding="utf-8").write("\n".join(out))
print(OUT, n, round(total / 3600, 2))
