# Shared config for the media pipeline. Override any value via environment.
: "${MEDIA_ROOT:=/workspace/library/acads/community-outreach/media}"
: "${TOOLS_ROOT:=/workspace/tools}"
: "${WHISPER_VENV:=$TOOLS_ROOT/whisper-venv}"
: "${EGOBLUR_VENV:=$TOOLS_ROOT/egoblur-venv}"
: "${EGOBLUR_REPO:=$TOOLS_ROOT/EgoBlur}"
: "${HF_HOME:=$TOOLS_ROOT/hf-cache}"                       # faster-whisper model cache
: "${WHISPER_MODEL:=medium}"                                # medium beat turbo on noisy Hindi field audio; one model for both passes
: "${WHISPER_TRANSLATE_MODEL:=medium}"                       # English pass via translate task (accurate); "large-v3-turbo" = fast English-forced decoding (rough)
: "${WHISPER_THREADS:=4}"                                   # fewer threads = less contention on the shared box
: "${WHISPER_COMPUTE:=float32}"                              # int8 is garbled on this CPU; float16 on GPU
: "${EGOBLUR_FACE_MODEL:=$TOOLS_ROOT/models/egoblur/ego_blur_face_gen2.jit}"
: "${YUNET_MODEL:=$TOOLS_ROOT/models/face_detection_yunet_2023mar.onnx}"
export MEDIA_ROOT TOOLS_ROOT WHISPER_VENV EGOBLUR_VENV EGOBLUR_REPO HF_HOME WHISPER_MODEL WHISPER_TRANSLATE_MODEL WHISPER_COMPUTE WHISPER_THREADS EGOBLUR_FACE_MODEL YUNET_MODEL
