import requests
import time
from pathlib import Path
import base64

# ---------------- CONFIG ---------------- #
API_KEY = "<aiml_d3387aa2-cf08-4a50-b630-c815c1c27759>"
BASE_URL = "https://api.aimlapi.com/v2"

IMAGE_PATH = Path(
    r"C:\Users\KIIT\Documents\ai-video-generator\backend\static\previews\scene_1.png"
)

# ---------------------------------------- #

# Read and encode image
with open(IMAGE_PATH, "rb") as f:
    base64_image = base64.b64encode(f.read()).decode("utf-8")

# Proper data URL
image_data_url = f"data:image/png;base64,{base64_image}"


def generate_video():
    url = f"{BASE_URL}/generate/video/bytedance/generation"
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "bytedance/seedance-1-0-lite-i2v",
        "prompt": "Mona Lisa puts on glasses with her hands.",
        "image": image_data_url,   # ✅ correct
        "duration": 5
    }

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code >= 400:
        print("Error:", response.text)
        return None

    return response.json()


def get_video(gen_id):
    url = f"{BASE_URL}/generate/video/bytedance/generation"

    headers = {
        "Authorization": f"Bearer {API_KEY}"
    }

    params = {
        "generation_id": gen_id
    }

    response = requests.get(url, params=params, headers=headers)
    return response.json()


def main():
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

    print("Timeout reached")


if __name__ == "__main__":
    main()
