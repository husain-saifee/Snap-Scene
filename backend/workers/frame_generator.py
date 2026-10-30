import base64
import os
from pathlib import Path
import time
import requests
from dotenv import load_dotenv

load_dotenv()

# ---------------- CONFIG ---------------- #
BASE_DIR = Path(__file__).resolve().parents[2]
API_KEY = os.getenv("AIML_API_KEY", "")
BASE_URL = os.getenv("AIML_BASE_URL", "https://api.aimlapi.com/v2")

IMAGE_PATH = BASE_DIR / "backend" / "static" / "previews" / "scene_1.png"
# ---------------------------------------- #


def encode_image(image_path: Path) -> str:
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def generate_video(image_path: Path = IMAGE_PATH, prompt: str = "A character in motion"):
    if not API_KEY:
        raise ValueError("AIML_API_KEY environment variable is not set")

    if not image_path.exists():
        raise FileNotFoundError(f"Source preview image not found: {image_path}")

    base64_image = encode_image(image_path)
    image_data_url = f"data:image/png;base64,{base64_image}"

    url = f"{BASE_URL}/generate/video/bytedance/generation"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "bytedance/seedance-1-0-lite-i2v",
        "prompt": prompt,
        "image": image_data_url,
        "duration": 5
    }

    response = requests.post(url, json=payload, headers=headers)
    if response.status_code >= 400:
        print("Error from API:", response.text)
        return None

    return response.json()


def get_video(gen_id: str):
    url = f"{BASE_URL}/generate/video/bytedance/generation"
    headers = {
        "Authorization": f"Bearer {API_KEY}"
    }
    params = {"generation_id": gen_id}
    response = requests.get(url, params=params, headers=headers)
    return response.json()


def main():
    if not API_KEY:
        print("AIML_API_KEY is not set in environment or .env. Skipping cloud I2V generation.")
        return

    gen_response = generate_video()
    if not gen_response:
        return

    gen_id = gen_response.get("id")
    print("Generation ID:", gen_id)

    start_time = time.time()
    timeout = 600

    while time.time() - start_time < timeout:
        result = get_video(gen_id)
        status = result.get("status")
        print("Status:", status)

        if status in {"queued", "waiting", "active", "generating"}:
            time.sleep(10)
        else:
            print("Done:", result)
            return

    print("Timeout reached waiting for generation.")


if __name__ == "__main__":
    main()
