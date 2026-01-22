import subprocess
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]

RIFE_EXE = BASE_DIR / "backend/rife/rife-ncnn-vulkan.exe"
SCENE_DIR = BASE_DIR / "backend/static/previews"
FRAME_DIR = BASE_DIR / "backend/static/rife_frames"
VIDEO_DIR = BASE_DIR / "backend/static/videos"

FFMPEG = r"C:\Users\KIIT\Downloads\ffmpeg-2026-01-22-git-4561fc5e48-full_build\ffmpeg-2026-01-22-git-4561fc5e48-full_build\bin\ffmpeg.exe"

FPS = 10           # 👈 slow = smooth anime
MODEL = "rife-anime"

def interpolate():
    FRAME_DIR.mkdir(parents=True, exist_ok=True)
    VIDEO_DIR.mkdir(parents=True, exist_ok=True)

    for f in FRAME_DIR.glob("*"):
        f.unlink()

    scenes = sorted(SCENE_DIR.glob("*.png"))
    print("🖼 Scenes:", [s.name for s in scenes])

    if len(scenes) < 2:
        raise RuntimeError("Need at least 2 images")

    print("🎞 Running RIFE (ANIME, CPU ONLY)")

    subprocess.run([
        str(RIFE_EXE),
        "-i", str(SCENE_DIR),
        "-o", str(FRAME_DIR),
        "-m", MODEL,
        "-g", "-1"      # CPU only
    ], check=True)

    print("✅ RIFE interpolation complete")


def build_video():
    output = VIDEO_DIR / "output.mp4"

    subprocess.run([
        FFMPEG,
        "-y",
        "-framerate", str(FPS),
        "-i", str(FRAME_DIR / "%08d.png"),
        "-vf", "setpts=10.0*PTS",
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        str(output)
    ], check=True)

    print("🎬 Video created:", output)


if __name__ == "__main__":
    interpolate()
    build_video()




