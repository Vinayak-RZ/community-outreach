#!/usr/bin/env python3
"""Blur faces in a video (audio kept) or image.

Backends:
  egoblur  Meta EgoBlur Gen2 face model (preferred; needs the official weights file,
           see README). ~1.5 s/frame on this CPU box.
  yunet    OpenCV YuNet face detector (interim fallback; fast, less robust for
           small/profile/occluded faces). Always check the output by eye.
  auto     egoblur if its weights file exists, else yunet (default).

Video is decoded with ffmpeg at constant frame rate, faces detected (every frame by
default), blurred with an elliptical mask, re-encoded as H.264, and the original
audio track is copied back in. Frames are streamed, so long videos don't fill RAM.
"""
import argparse, json, os, shutil, subprocess, sys, time
import cv2
import numpy as np

IMAGE_EXT = {".jpg", ".jpeg", ".png", ".webp", ".bmp", ".heic"}


def probe(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-print_format", "json", "-show_streams", "-show_format", path],
                         capture_output=True, text=True, check=True).stdout
    return json.loads(out)


class EgoBlurBackend:
    name = "egoblur-gen2"

    def __init__(self, model_path, threshold, device):
        import torch  # noqa
        from gen2.script.predictor import ClassID, EgoblurDetector, PATCH_INSTANCES_FIELDS
        from gen2.script.constants import RESIZE_MIN_GEN2, RESIZE_MAX_GEN2, FACE_THRESHOLDS_GEN2
        from gen2.script.detectron2.export.torchscript_patch import patch_instances
        self.torch = torch
        self._patch = patch_instances(fields=PATCH_INSTANCES_FIELDS); self._patch.__enter__()
        if device == "auto":
            device = "cuda" if torch.cuda.is_available() else "cpu"
        self.device = device
        self.det = EgoblurDetector(model_path=model_path, device=device, detection_class=ClassID.FACE,
                                   score_threshold=threshold if threshold is not None else FACE_THRESHOLDS_GEN2["camera-rgb"],
                                   nms_iou_threshold=0.3,
                                   resize_aug={"min_size_test": RESIZE_MIN_GEN2, "max_size_test": RESIZE_MAX_GEN2})

    def detect(self, bgr):
        t = self.torch.from_numpy(np.ascontiguousarray(np.transpose(bgr, (2, 0, 1)))).to(self.device)
        with self.torch.no_grad():
            res = self.det.run(t)
        return [list(map(float, b[:4])) for b in (res[0] if res else [])]


class YuNetBackend:
    name = "opencv-yunet"

    def __init__(self, model_path, threshold):
        self.model_path, self.th = model_path, threshold if threshold is not None else 0.6
        self.det, self.size = None, None

    def detect(self, bgr):
        h, w = bgr.shape[:2]
        # Upscale small frames / downscale huge ones so YuNet sees faces at a useful size.
        scale = 1280.0 / max(h, w)
        img = cv2.resize(bgr, (int(w * scale), int(h * scale))) if abs(scale - 1) > 0.05 else bgr
        size = (img.shape[1], img.shape[0])
        if self.det is None:
            self.det = cv2.FaceDetectorYN.create(self.model_path, "", size, self.th, 0.3, 5000)
        if size != self.size:
            self.det.setInputSize(size); self.size = size
        _, faces = self.det.detect(img)
        if faces is None:
            return []
        return [[f[0] / scale, f[1] / scale, (f[0] + f[2]) / scale, (f[1] + f[3]) / scale] for f in faces]


def blur_boxes(img, boxes, scale):
    if not boxes:
        return img
    h, w = img.shape[:2]
    mask = np.zeros((h, w), np.uint8)
    for x1, y1, x2, y2 in boxes:
        cx, cy, bw, bh = (x1 + x2) / 2, (y1 + y2) / 2, (x2 - x1) * scale, (y2 - y1) * scale
        if bw < 2 or bh < 2:
            continue
        cv2.ellipse(mask, ((cx, cy), (bw, bh), 0), 255, -1)
    if not mask.any():
        return img
    ys, xs = np.where(mask > 0)
    y1, y2, x1, x2 = ys.min(), ys.max() + 1, xs.min(), xs.max() + 1
    roi = img[y1:y2, x1:x2]
    # Heavy pixelate + blur: irreversible enough that faces can't be recognised.
    small = cv2.resize(roi, (max(1, roi.shape[1] // 16), max(1, roi.shape[0] // 16)), interpolation=cv2.INTER_AREA)
    k = max(3, (min(roi.shape[:2]) // 4) | 1)
    blurred = cv2.GaussianBlur(cv2.resize(small, (roi.shape[1], roi.shape[0]), interpolation=cv2.INTER_LINEAR), (k, k), 0)
    m = mask[y1:y2, x1:x2, None] > 0
    out = img.copy(); out[y1:y2, x1:x2] = np.where(m, blurred, roi)
    return out


def make_backend(args):
    choice = args.backend
    if choice == "auto":
        choice = "egoblur" if os.path.isfile(args.egoblur_model) else "yunet"
        if choice == "yunet":
            print(f"note: EgoBlur weights not found at {args.egoblur_model}; using YuNet fallback", file=sys.stderr)
    if choice == "egoblur":
        sys.path.insert(0, os.environ.get("EGOBLUR_REPO", "/workspace/tools/EgoBlur"))
        return EgoBlurBackend(args.egoblur_model, args.threshold, args.device)
    return YuNetBackend(args.yunet_model, args.threshold)


def blur_video(args, be):
    info = probe(args.input)
    v = next(s for s in info["streams"] if s["codec_type"] == "video")
    has_audio = any(s["codec_type"] == "audio" for s in info["streams"])
    num, den = map(int, (v.get("avg_frame_rate") or v["r_frame_rate"]).split("/"))
    fps = num / den if den and num else 25.0
    w, h = int(v["width"]), int(v["height"])
    rot = 0
    for sd in v.get("side_data_list", []):
        rot = int(sd.get("rotation", rot) or rot)
    rot = int(v.get("tags", {}).get("rotate", rot))
    if abs(rot) % 180 == 90:
        w, h = h, w  # ffmpeg autorotates on decode
    dur = float(info["format"].get("duration", 0) or 0)
    total = int(dur * fps) if dur else None

    dec = subprocess.Popen(["ffmpeg", "-nostdin", "-loglevel", "error", "-i", args.input, "-map", "0:v:0",
                            "-vf", f"fps={fps}", "-f", "rawvideo", "-pix_fmt", "bgr24", "-"], stdout=subprocess.PIPE)
    tmp = args.output + ".part.mp4"
    enc_cmd = ["ffmpeg", "-nostdin", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24",
               "-s", f"{w}x{h}", "-r", f"{fps}", "-i", "-", "-i", args.input, "-map", "0:v:0"]
    if has_audio:
        enc_cmd += ["-map", "1:a:0", "-c:a", "aac", "-b:a", "192k"]
    enc_cmd += ["-c:v", "libx264", "-preset", "medium", "-crf", str(args.crf), "-pix_fmt", "yuv420p",
                "-map_metadata", "-1", "-movflags", "+faststart", tmp]
    enc = subprocess.Popen(enc_cmd, stdin=subprocess.PIPE)
    fsize = w * h * 3
    n, faces_frames, max_faces, last, t0 = 0, 0, 0, [], time.time()
    hist = []  # boxes from recent detections, to bridge single-frame misses
    while True:
        buf = dec.stdout.read(fsize)
        if len(buf) < fsize:
            break
        frame = np.frombuffer(buf, np.uint8).reshape(h, w, 3)
        if n % args.detect_every == 0:
            last = be.detect(frame)
            hist = (hist + [last])[-args.hold:]
        boxes = [b for bs in hist for b in bs] if args.hold > 1 else last
        if last:
            faces_frames += 1; max_faces = max(max_faces, len(last))
        enc.stdin.write(blur_boxes(frame, boxes, args.scale).tobytes())
        n += 1
        if n % 100 == 0:
            el = time.time() - t0
            print(f"  {n}/{total or '?'} frames, {n / el:.2f} fps", file=sys.stderr)
    enc.stdin.close(); enc.wait(); dec.wait()
    if enc.returncode or dec.returncode or n == 0:
        raise SystemExit(f"ffmpeg failed (decoder {dec.returncode}, encoder {enc.returncode}, frames {n})")
    os.replace(tmp, args.output)
    return {"frames": n, "fps": round(fps, 3), "frames_with_faces": faces_frames, "max_faces_in_frame": max_faces,
            "audio_kept": has_audio, "processing_s": round(time.time() - t0, 1)}


def blur_image(args, be):
    img = cv2.imread(args.input)
    if img is None:
        raise SystemExit(f"cannot read image {args.input}")
    boxes = be.detect(img)
    cv2.imwrite(args.output, blur_boxes(img, boxes, args.scale))
    return {"faces": len(boxes)}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("input"); ap.add_argument("output")
    ap.add_argument("--backend", choices=["auto", "egoblur", "yunet"], default="auto")
    ap.add_argument("--egoblur-model", default=os.environ.get("EGOBLUR_FACE_MODEL", "/workspace/tools/models/egoblur/ego_blur_face_gen2.jit"))
    ap.add_argument("--yunet-model", default=os.environ.get("YUNET_MODEL", "/workspace/tools/models/face_detection_yunet_2023mar.onnx"))
    ap.add_argument("--threshold", type=float, default=None, help="detection score threshold (lower = blur more)")
    ap.add_argument("--scale", type=float, default=1.4, help="grow each face box by this factor before blurring")
    ap.add_argument("--detect-every", type=int, default=1, help="run detector every N frames (speed vs safety)")
    ap.add_argument("--hold", type=int, default=3, help="also blur boxes from the last N detections (bridges misses)")
    ap.add_argument("--crf", type=int, default=20)
    ap.add_argument("--device", default="auto")
    args = ap.parse_args()
    os.makedirs(os.path.dirname(os.path.abspath(args.output)), exist_ok=True)
    be = make_backend(args)
    is_img = os.path.splitext(args.input)[1].lower() in IMAGE_EXT
    stats = blur_image(args, be) if is_img else blur_video(args, be)
    print(json.dumps({"output": os.path.abspath(args.output), "backend": be.name, **stats}))


if __name__ == "__main__":
    main()
