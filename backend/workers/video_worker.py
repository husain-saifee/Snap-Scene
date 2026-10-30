import os
import shutil
import subprocess
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]

RIFE_EXE = BASE_DIR / "backend/rife/rife-ncnn-vulkan.exe"
SCENE_DIR = BASE_DIR / "backend/static/previews"
FRAME_DIR = BASE_DIR / "backend/static/rife_frames"
VIDEO_DIR = BASE_DIR / "backend/static/videos"

# Resolve FFmpeg from environment variable or system PATH
FFMPEG = os.getenv("FFMPEG_PATH") or shutil.which("ffmpeg") or "ffmpeg"

FPS = 10           
MODEL = "rife-anime"


def interpolate():
    FRAME_DIR.mkdir(parents=True, exist_ok=True)
    VIDEO_DIR.mkdir(parents=True, exist_ok=True)

    for f in FRAME_DIR.glob("*"):
        try:
            f.unlink()
        except OSError:
            pass

    scenes = sorted(SCENE_DIR.glob("*.png"))
    print("🖼 Scenes found:", [s.name for s in scenes])

    if len(scenes) < 2:
        raise RuntimeError("Need at least 2 scene images in backend/static/previews to interpolate")

    print(f"🎞 Running RIFE Neural Interpolation (Model: {MODEL})")

    if not RIFE_EXE.exists():
        print(f"⚠️ RIFE binary not found at {RIFE_EXE}. Skipping neural interpolation.")
        return

    subprocess.run([
        str(RIFE_EXE),
        "-i", str(SCENE_DIR),
        "-o", str(FRAME_DIR),
        "-m", MODEL,
        "-g", "-1"     
    ], check=True)

    print("✅ RIFE interpolation complete")


def build_video():
    output = VIDEO_DIR / "output.mp4"

    print(f"🎬 Compiling video using {FFMPEG} -> {output}")
    subprocess.run([
        str(FFMPEG),
        "-y",
        "-framerate", str(FPS),
        "-i", str(FRAME_DIR / "%08d.png"),
        "-vf", "setpts=10.0*PTS",
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        str(output)
    ], check=True)

    print("✅ Video created successfully:", output)


if __name__ == "__main__":
    interpolate()
    build_video()
