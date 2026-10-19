#!/usr/bin/env python3
"""Process new media: inbox/ -> raw/ (read-only originals) -> transcripts/ + blurred/.

Idempotent: files are tracked by SHA-256 in manifest.csv. A file already in the
manifest is never re-added; finished stages (transcript / blur) are skipped, and
failed or interrupted ones are retried on the next run. Duplicates dropped into
inbox/ are moved to inbox/_duplicates/ untouched.
"""
import argparse, csv, hashlib, json, os, shutil, subprocess, sys, time
from datetime import datetime

ROOT = os.environ.get("MEDIA_ROOT", "/workspace/library/acads/community-outreach/media")
PIPE = os.path.dirname(os.path.abspath(__file__))
FIELDS = ["file", "sha256", "audio_md5", "date_added", "type", "duration_s", "language", "transcript_path",
          "translation_path", "blurred_path", "status", "notes"]
AUDIO_EXT = {".mp3", ".m4a", ".wav", ".ogg", ".opus", ".aac", ".flac", ".amr", ".wma", ".3gp"}
VIDEO_EXT = {".mp4", ".mov", ".mkv", ".webm", ".avi", ".m4v", ".3gp", ".mts"}
IMAGE_EXT = {".jpg", ".jpeg", ".png", ".webp", ".heic"}
D = lambda *p: os.path.join(ROOT, *p)


def log(msg):
    line = f"{datetime.now():%Y-%m-%d %H:%M:%S} {msg}"
    print(line, flush=True)
    with open(D("logs", "process-inbox.log"), "a") as f:
        f.write(line + "\n")


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def load_manifest():
    if not os.path.exists(D("manifest.csv")):
        return []
    with open(D("manifest.csv"), newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def save_manifest(rows):
    tmp = D("manifest.csv.tmp")
    with open(tmp, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS); w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in FIELDS})
    os.replace(tmp, D("manifest.csv"))


def media_type(path):
    ext = os.path.splitext(path)[1].lower()
    if ext in IMAGE_EXT:
        return "image", ""
    try:
        info = json.loads(subprocess.run(["ffprobe", "-v", "error", "-print_format", "json", "-show_streams",
                                          "-show_format", path], capture_output=True, text=True, check=True).stdout)
    except subprocess.CalledProcessError:
        return "other", ""
    dur = info.get("format", {}).get("duration", "")
    dur = f"{float(dur):.1f}" if dur else ""
    st = info.get("streams", [])
    real_video = [s for s in st if s["codec_type"] == "video" and not s.get("disposition", {}).get("attached_pic")]
    if real_video and float(dur or 0) > 0.5:
        return "video", dur
    if any(s["codec_type"] == "audio" for s in st):
        return "audio", dur
    return "other", dur


def audio_md5(path):
    """MD5 of the decoded audio track: catches re-exports/forwards of the same recording
    whose container bytes (timestamps etc.) differ."""
    p = subprocess.run(["ffmpeg", "-nostdin", "-loglevel", "error", "-i", path, "-map", "0:a:0", "-f", "md5", "-"],
                       capture_output=True, text=True)
    return p.stdout.strip().removeprefix("MD5=") if p.returncode == 0 else ""


def unique_raw_name(name):
    dst = D("raw", name)
    if not os.path.exists(dst):
        return name
    stem, ext = os.path.splitext(name)
    return f"{stem}__{datetime.now():%Y%m%d-%H%M%S}{ext}"


def run(cmd, logname):
    with open(D("logs", logname), "a") as lf:
        lf.write(f"\n=== {datetime.now():%Y-%m-%d %H:%M:%S} {' '.join(cmd)}\n"); lf.flush()
        p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=lf, text=True)
    if p.returncode:
        raise RuntimeError(f"exit {p.returncode}, see logs/{logname}")
    return json.loads(p.stdout.strip().splitlines()[-1])


def ingest(rows, dry):
    known = {r["sha256"]: r for r in rows}
    for r in rows:  # backfill audio fingerprints for rows from older manifests
        if not r.get("audio_md5") and r["type"] in ("audio", "video") and not r["status"].startswith("duplicate"):
            r["audio_md5"] = audio_md5(D("raw", r["file"]))
    by_audio = {r["audio_md5"]: r for r in rows if r.get("audio_md5") and not r["status"].startswith("duplicate")}
    for name in sorted(os.listdir(D("inbox"))):
        src = D("inbox", name)
        if name.startswith(".") or name.startswith("_") or not os.path.isfile(src):
            continue
        h = sha256(src)
        if h in known:
            log(f"duplicate of {known[h]['file']}: {name} -> inbox/_duplicates/")
            if not dry:
                os.makedirs(D("inbox", "_duplicates"), exist_ok=True)
                shutil.move(src, D("inbox", "_duplicates", name))
            continue
        mtype, dur = media_type(src)
        amd5 = audio_md5(src) if mtype in ("audio", "video") else ""
        if amd5 and amd5 in by_audio and mtype == "audio":
            orig = by_audio[amd5]
            log(f"same audio as {orig['file']}: {name} -> inbox/_duplicates/ (reusing its transcript)")
            if not dry:
                os.makedirs(D("inbox", "_duplicates"), exist_ok=True)
                shutil.move(src, D("inbox", "_duplicates", name))
                rows.append({"file": "_duplicates/" + name, "sha256": h, "audio_md5": amd5,
                             "date_added": datetime.now().strftime("%Y-%m-%d %H:%M"), "type": mtype, "duration_s": dur,
                             "language": orig.get("language", ""), "transcript_path": orig.get("transcript_path", ""),
                             "translation_path": orig.get("translation_path", ""),
                             "status": f"duplicate of {orig['file']}", "notes": "identical decoded audio; not reprocessed"})
                known[h] = rows[-1]; save_manifest(rows)
            continue
        rname = unique_raw_name(name)
        log(f"ingest {name} -> raw/{rname} ({mtype}, {dur or '?'} s)")
        if dry:
            continue
        shutil.move(src, D("raw", rname))
        os.chmod(D("raw", rname), 0o444)  # originals are never modified
        r = {"file": rname, "sha256": h, "date_added": datetime.now().strftime("%Y-%m-%d %H:%M"),
             "audio_md5": amd5, "type": mtype, "duration_s": dur, "status": "pending"}
        rows.append(r); known[h] = r
        if amd5:
            by_audio[amd5] = r
        save_manifest(rows)


def process(r, args):
    raw = D("raw", r["file"]); stem = os.path.splitext(r["file"])[0]
    notes, errors = [], []
    if r["type"] in ("audio", "video") and not args.no_transcribe:
        tdir = D("transcripts", stem); tjson = os.path.join(tdir, stem + ".json")
        need_tr = args.translate and not os.path.exists(os.path.join(tdir, stem + ".en.json"))
        if not os.path.exists(tjson) or need_tr or args.force:
            cmd = [os.path.join(PIPE, "transcribe"), raw, "-o", tdir, "--stem", stem]
            if args.language: cmd += ["-l", args.language]
            if args.translate: cmd.append("--translate")
            if os.path.exists(tjson) and not args.force: cmd.append("--reuse-transcript")
            if args.model: cmd += ["-m", args.model]
            if args.initial_prompt: cmd += ["--initial-prompt", args.initial_prompt]
            log(f"transcribe {r['file']}")
            try:
                out = run(cmd, "transcribe.log")
                notes.append(f"transcribed in {out['processing_s']}s")
            except Exception as e:
                errors.append(f"transcribe: {e}")
        if os.path.exists(tjson):
            with open(tjson, encoding="utf-8") as f:
                meta = json.load(f)
            r["language"] = f"{meta['language']}" + ("" if meta.get("language_forced") else f" ({meta['language_probability']:.2f})")
            r["transcript_path"] = os.path.relpath(tjson, ROOT)
            en = os.path.join(tdir, stem + ".en.json")
            r["translation_path"] = os.path.relpath(en, ROOT) if os.path.exists(en) else ""
    if r["type"] in ("video", "image") and not args.no_blur:
        out_path = D("blurred", stem + (".blurred.mp4" if r["type"] == "video" else ".blurred" + os.path.splitext(r["file"])[1].lower()))
        if not os.path.exists(out_path) or args.force:
            cmd = [os.path.join(PIPE, "blur"), raw, out_path, "--backend", args.blur_backend]
            log(f"blur {r['file']}")
            try:
                out = run(cmd, "blur.log")
                notes.append(f"blur={out['backend']}")
            except Exception as e:
                errors.append(f"blur: {e}")
        if os.path.exists(out_path):
            r["blurred_path"] = os.path.relpath(out_path, ROOT)
    if r["type"] == "other":
        r["status"] = "skipped (unsupported type)"
    elif errors:
        r["status"] = "error: " + "; ".join(errors)
    else:
        missing = []
        if r["type"] in ("audio", "video") and not r.get("transcript_path"): missing.append("transcript")
        if r["type"] in ("video", "image") and not r.get("blurred_path"): missing.append("blur")
        r["status"] = "partial (no " + ", ".join(missing) + ")" if missing else "done"
    if notes or errors:
        r["notes"] = "; ".join(notes + errors)
    log(f"{r['file']}: {r['status']}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("-l", "--language", help="force language for new transcripts (hi, en, ...); default auto")
    ap.add_argument("--translate", action="store_true", help="also make English translations")
    ap.add_argument("-m", "--model", help="Whisper model (default $WHISPER_MODEL = large-v3-turbo)")
    ap.add_argument("--initial-prompt", help="vocabulary/context hint passed to Whisper")
    ap.add_argument("--blur-backend", default="auto", choices=["auto", "egoblur", "yunet"])
    ap.add_argument("--no-blur", action="store_true"); ap.add_argument("--no-transcribe", action="store_true")
    ap.add_argument("--only", help="process only this raw filename")
    ap.add_argument("--force", action="store_true", help="redo stages even if outputs exist")
    ap.add_argument("--dry-run", action="store_true", help="show what would be ingested; change nothing")
    args = ap.parse_args()
    for d in ("inbox", "raw", "transcripts", "blurred", "logs"):
        os.makedirs(D(d), exist_ok=True)
    rows = load_manifest()
    ingest(rows, args.dry_run)
    if args.dry_run:
        return
    todo = [r for r in rows if not r["status"].startswith("duplicate") and (r["status"] != "done" or args.force or args.translate and not r.get("translation_path")
                                and r["type"] in ("audio", "video")) and (not args.only or r["file"] == args.only)]
    # Transcripts first: interview audio, then long videos (>=60 s), then short clips.
    def prio(r):
        d = float(r.get("duration_s") or 0)
        return (0 if r["type"] == "audio" else 1 if r["type"] == "video" and d >= 60 else 2, d)
    todo.sort(key=prio)
    if not todo:
        log("nothing to do"); return
    for r in todo:
        process(r, args)
        save_manifest(rows)


if __name__ == "__main__":
    main()
