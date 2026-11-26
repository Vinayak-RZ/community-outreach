# Transcripts

Interview transcripts from the media pipeline (`pipeline/`) go here, one folder per recording:

```
transcripts/<recording-name>/
  <name>.txt      timestamped lines
  <name>.srt      subtitles
  <name>.json     segments, word timings, model, detected language + confidence
  <name>.en.*     English translation (when run with --translate)
```

- Real names appear in the transcripts. They stay off the poster and out of the written deliverables, unless written consent covers publishing a name. The analysis uses interview codes.
- Transcripts are machine-made (Whisper). Check names, numbers and key lines against the audio before quoting them. An English file (`.en.*`) is a translation, not the speaker's words.
- **No audio or video in git.** Raw recordings stay outside the repository. Face-blurred videos are published as [GitHub Release](https://github.com/Vinayak-RZ/community-outreach/releases) assets, with a note here or in `evidence/` naming the release and asset.
