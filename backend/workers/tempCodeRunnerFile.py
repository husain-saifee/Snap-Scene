
def interpolate_scenes():
    FRAME_DIR.mkdir(parents=True, exist_ok=True)
    FINAL_DIR.mkdir(parents=True, exist_ok=True)

    scenes = sorted(SCENE_DIR.glob("*.png"))

    if len(scenes) < 2:
        raise ValueError("❌ Need at least 2 scene images")

    frame_counter = 0