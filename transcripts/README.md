# Transcripts

Interview transcripts from the media pipeline (`pipeline/`) go here, one folder per recording:

```
transcripts/<recording-name>/
  <name>.txt      timestamped lines
  <name>.srt      subtitles
  <name>.json     segments, word timings, model, detected language + confidence
  <name>.en.*     English translation (when run with --translate)
```

- The repo is **private** (since 19 Oct 2026), so transcripts can be committed as produced, with real names left in.
  Privacy still matters. Keep them inside the team. Before any quote reaches the poster, a deliverable or anything shared outside, replace
  names with roles/codes unless written consent covers publishing.
- Transcripts are machine-made (Whisper). Check names, numbers and key quotes against the
  audio before citing them, and mark corrections.
- **No audio or video in git.** Raw recordings stay on the box (`media/raw/`). Face-blurred videos are
  bundled and published as [GitHub Release](https://github.com/Vinayak-RZ/Illusion/releases)
  assets, with a note here or in `evidence/` naming the release and asset.
