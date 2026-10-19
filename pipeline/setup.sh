#!/usr/bin/env bash
# Rebuild the pipeline's tools on a fresh box. Safe to re-run.
set -euo pipefail
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"; source "$DIR/config.sh"
command -v ffmpeg >/dev/null || { echo "install ffmpeg first (apt-get install ffmpeg)"; exit 1; }
mkdir -p "$TOOLS_ROOT/models/egoblur"
cd "$TOOLS_ROOT"
[ -d "$WHISPER_VENV" ] || uv venv --python 3.11 "$WHISPER_VENV"
VIRTUAL_ENV="$WHISPER_VENV" uv pip install "faster-whisper==1.2.1"
[ -d "$EGOBLUR_VENV" ] || uv venv --python 3.12 "$EGOBLUR_VENV"
VIRTUAL_ENV="$EGOBLUR_VENV" uv pip install "egoblur==2.0.1" \
  --extra-index-url https://download.pytorch.org/whl/cpu --index-strategy unsafe-best-match
[ -d "$EGOBLUR_REPO" ] || git clone https://github.com/facebookresearch/EgoBlur.git "$EGOBLUR_REPO"
[ -f "$YUNET_MODEL" ] || curl -fsSL -o "$YUNET_MODEL" \
  https://github.com/opencv/opencv_zoo/raw/main/models/face_detection_yunet/face_detection_yunet_2023mar.onnx
"$WHISPER_VENV/bin/python" -c "
from faster_whisper import download_model
for m in ['$WHISPER_MODEL', '$WHISPER_TRANSLATE_MODEL']: print(m, download_model(m))"
mkdir -p "$MEDIA_ROOT"/{inbox,raw,transcripts,blurred,logs}
[ -f "$MEDIA_ROOT/manifest.csv" ] || echo "file,sha256,date_added,type,duration_s,language,transcript_path,translation_path,blurred_path,status,notes" > "$MEDIA_ROOT/manifest.csv"
[ -f "$EGOBLUR_FACE_MODEL" ] && echo "EgoBlur face weights: OK" || echo "EgoBlur face weights MISSING -> blur falls back to YuNet. See README."
