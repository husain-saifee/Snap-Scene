import json
import os
from video.image_resizer import resize_image

ASSETS_PATH = "backend/assets"

def process_images():
    with open("backend/workers/image_gen.json", "r") as f:
        scene_data = json.load(f)

    for char in scene_data["characters"]:
        image_path = os.path.join(
            ASSETS_PATH,
            "characters",
            char["image"]
        )

        resized_img = resize_image(
            image_path=image_path,
            resize_to=char["resolution_resize"]
        )

        print("Resized image to:", resized_img.size)


if __name__ == "__main__":
    process_images()
