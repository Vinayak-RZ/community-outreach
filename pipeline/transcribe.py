#!/usr/bin/env python3
"""Transcribe an audio or video file with faster-whisper.

Writes <out_dir>/<stem>.txt, .srt, .json (segment + word timestamps).
With --translate also writes <stem>.en.txt/.en.srt/.en.json (Whisper's built-in
speech->English translation, done as a second pass on the same audio).
"""
import argparse, json, os, subprocess, sys, tempfile, time
from datetime import datetime, timezone


def ts(t, sep=","):
    ms = int(round(t * 1000)); h, ms = divmod(ms, 3600000); m, ms = divmod(ms, 60000); s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d}{sep}{ms:03d}"


def extract_audio(src, dst):
    # 16 kHz mono WAV is what Whisper consumes internally.
    subprocess.run(["ffmpeg", "-nostdin", "-loglevel", "error", "-y", "-i", src, "-vn",
                    "-ac", "1", "-ar", "16000", "-c:a", "pcm_s16le", dst], check=True)


def run_pass(model, wav, task, args):
    t0 = time.time()
    # "en-decode" = transcribe with language forced to English. On Hindi/Hinglish speech
    # whisper-turbo then writes English, i.e. a rough translation (turbo has no translate task).
    lang = "en" if task == "en-decode" else args.language
    task = "transcribe" if task == "en-decode" else task
    segments, info = model.transcribe(
        # Translation uses greedy decoding (2-3x cheaper on this shared CPU; it's a reading aid, not a quote source).
        wav, task=task, language=lang, beam_size=args.beam_size if task == "transcribe" else 1,
        # Limited temperature fallback + mild repetition penalty: full fallback (6 temps) made
        # noisy field audio 3-5x slower, and temp 0 alone looped ("क्या किस लिए?" x14).
        temperature=[0.0, 0.4], best_of=2, repetition_penalty=1.1,
        vad_filter=not args.no_vad, word_timestamps=True,
        # The vocabulary prompt helps transcription but gets echoed verbatim by the translate task.
        initial_prompt=args.initial_prompt if task == "transcribe" else None,
        condition_on_previous_text=False)
    segs = []
    for s in segments:
        segs.append({"id": s.id, "start": round(s.start, 3), "end": round(s.end, 3), "text": s.text.strip(),
                     "avg_logprob": round(s.avg_logprob, 3), "no_speech_prob": round(s.no_speech_prob, 3),
                     "words": [{"start": round(w.start, 3), "end": round(w.end, 3), "word": w.word,
                                "prob": round(w.probability, 3)} for w in (s.words or [])]})
        if args.verbose:
            print(f"[{ts(s.start, '.')} -> {ts(s.end, '.')}] {s.text.strip()}", file=sys.stderr)
    return segs, info, time.time() - t0


def write_outputs(base, segs, meta):
    with open(base + ".txt", "w", encoding="utf-8") as f:
        for s in segs:
            f.write(f"[{ts(s['start'], '.')[:-4]}] {s['text']}\n")
    with open(base + ".srt", "w", encoding="utf-8") as f:
        for i, s in enumerate(segs, 1):
            f.write(f"{i}\n{ts(s['start'])} --> {ts(s['end'])}\n{s['text']}\n\n")
    with open(base + ".json", "w", encoding="utf-8") as f:
        json.dump({**meta, "segments": segs}, f, ensure_ascii=False, indent=1)


def translate(model, wav, segs, meta, base, args, device, compute, WhisperModel, result):
    # Keep the source language from pass 1 so the translate pass doesn't re-detect it.
    args.language = args.language or meta["language"]
    if args.language == "en":
        # Whisper's translate task garbles speech that is already English; reuse pass 1.
        tsegs, tel = segs, 0.0
    else:
        if args.translate_model != args.model:
            del model; import gc; gc.collect()  # one model in RAM at a time (shared box)
            model = WhisperModel(args.translate_model, device=device, compute_type=compute, cpu_threads=args.threads)
        tsegs, _, tel = run_pass(model, wav, "en-decode" if args.translate_model.endswith("turbo") else "translate", args)
    write_outputs(base + ".en", tsegs, {**meta, "task": "translate", "target_language": "en",
                                        "processing_s": round(tel, 1),
                                        "model": args.model if args.language == "en" else args.translate_model,
                                        "method": "copy of English transcript" if args.language == "en" else
                                        ("English-forced decoding (rough translation)" if args.translate_model.endswith("turbo")
                                         else "whisper translate task")})
    result["translation"] = base + ".en.json"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("input")
    ap.add_argument("-o", "--out-dir", help="default: alongside input")
    ap.add_argument("--stem", help="output basename (default: input filename without extension)")
    ap.add_argument("-l", "--language", default=None,
                    help="force language code (hi, en, ...). 'auto-hi' = treat as Hindi unless the model is "
                         ">=0.7 sure it's English (Whisper often mislabels Hinglish as English). Default: plain auto")
    ap.add_argument("--translate", action="store_true", help="also produce an English translation (.en.*)")
    ap.add_argument("-m", "--model", default=os.environ.get("WHISPER_MODEL", "medium"))
    ap.add_argument("--translate-model", default=os.environ.get("WHISPER_TRANSLATE_MODEL", "medium"),
                    help="model for the English pass. turbo: English-forced decoding (fast, one model); "
                         "others (e.g. medium): Whisper's translate task")
    ap.add_argument("--device", default="auto", help="auto | cpu | cuda")
    ap.add_argument("--compute-type", default=os.environ.get("WHISPER_COMPUTE", "float32"),
                    help="float32 on this CPU box: int8 output is garbled here (CTranslate2 4.8 + AMX CPU)")
    ap.add_argument("--threads", type=int, default=int(os.environ.get("WHISPER_THREADS", 4)),
                    help="CPU threads (4: using all 8 on the shared box made decoding several times slower)")
    ap.add_argument("--beam-size", type=int, default=5)
    ap.add_argument("--initial-prompt", default=None,
                    help="optional context/vocab hint, e.g. 'IIT Roorkee campus dogs, Hinglish interview'")
    ap.add_argument("--no-vad", action="store_true", help="disable silence filtering")
    ap.add_argument("--reuse-transcript", action="store_true",
                    help="if <stem>.json exists, don't redo pass 1 (only add the translation)")
    ap.add_argument("-v", "--verbose", action="store_true")
    args = ap.parse_args()

    from faster_whisper import WhisperModel
    import ctranslate2, faster_whisper
    device = args.device
    if device == "auto":
        device = "cuda" if ctranslate2.get_cuda_device_count() > 0 else "cpu"
    compute = args.compute_type if device == "cpu" else ("float16" if args.compute_type in ("int8", "float32") else args.compute_type)

    src = os.path.abspath(args.input)
    stem = args.stem or os.path.splitext(os.path.basename(src))[0]
    out_dir = os.path.abspath(args.out_dir or os.path.dirname(src)); os.makedirs(out_dir, exist_ok=True)
    base = os.path.join(out_dir, stem)

    model = WhisperModel(args.model, device=device, compute_type=compute, cpu_threads=args.threads)
    with tempfile.TemporaryDirectory() as td:
        wav = os.path.join(td, "audio.wav"); extract_audio(src, wav)
        if args.reuse_transcript and os.path.exists(base + ".json"):
            with open(base + ".json", encoding="utf-8") as f:
                meta = json.load(f)
            segs = meta.pop("segments")
            args.language = meta["language"]
            result = {"language": meta["language"], "language_probability": meta["language_probability"],
                      "duration_s": meta["duration_s"], "processing_s": 0.0, "transcript": base + ".json"}
            if args.translate:
                translate(model, wav, segs, meta, base, args, device, compute, WhisperModel, result)
            print(json.dumps(result)); return
        detection = None
        if args.language == "auto-hi":
            from faster_whisper.audio import decode_audio
            lg, pr, allp = model.detect_language(decode_audio(wav), language_detection_segments=4)
            detection = {"detected": lg, "probability": round(pr, 3),
                         "top": [[l, round(p, 3)] for l, p in allp[:3]]}
            # medium labels Hindi/Hinglish field audio as hi (0.5-0.99); en >= 0.7 has meant English speech.
            args.language = "en" if (lg == "en" and pr >= 0.7) else "hi"
        segs, info, el = run_pass(model, wav, "transcribe", args)
        meta = {"source_file": os.path.basename(src), "created": datetime.now(timezone.utc).isoformat(),
                "model": args.model, "device": device, "compute_type": compute,
                "faster_whisper": faster_whisper.__version__, "task": "transcribe",
                "language": info.language, "language_probability": round(info.language_probability, 3),
                "language_forced": args.language is not None, "language_policy_detection": detection, "duration_s": round(info.duration, 2),
                "processing_s": round(el, 1), "initial_prompt": args.initial_prompt}
        write_outputs(base, segs, meta)
        result = {"language": info.language, "language_probability": meta["language_probability"],
                  "duration_s": meta["duration_s"], "processing_s": meta["processing_s"],
                  "transcript": base + ".json"}
        if args.translate:
            translate(model, wav, segs, meta, base, args, device, compute, WhisperModel, result)
    print(json.dumps(result))


if __name__ == "__main__":
    main()
