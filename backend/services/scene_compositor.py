import os
from PIL import Image
from backend.services.canvas import CANVAS_WIDTH, CANVAS_HEIGHT, CANVAS_SIZE
from backend.services.image_resizer import resize_image


ASSETS_BASE = "backend/assets"

POSITION_MAP = {
    "left": 0.25,
    "center": 0.50,
    "right": 0.75
}

def get_x_position(position_str: str, img_width: int) -> int:
    """Calculates X based on semantic strings (left, center, right)."""
    center_x = int(CANVAS_WIDTH * POSITION_MAP.get(position_str, 0.50))
    return center_x - img_width // 2

def compose_scene(scene_json: dict) -> Image.Image:
    """
    Composes a full scene image from JSON data, handling layered 
    assets and coordinate positioning.
    """

    # 1️⃣ Initialize empty transparent canvas
    canvas = Image.new("RGBA", CANVAS_SIZE, (0, 0, 0, 0))

    # 2️⃣ Background (Always fills the canvas)
    bg_name = scene_json.get("background", {}).get("image")
    if bg_name:
        bg_path = os.path.join(ASSETS_BASE, "backgrounds", bg_name)
        if os.path.exists(bg_path):
            background = Image.open(bg_path).convert("RGBA")
            background = background.resize(CANVAS_SIZE, Image.LANCZOS)
            canvas.paste(background, (0, 0))

    # 3️⃣ Define layers to process: (JSON_KEY, ELEMENT_TYPE, FOLDER)
    layers = [
        ("environment_objects", "object", "objects"),
        ("characters", "character", "characters")
    ]

    for json_key, element_type, folder in layers:
        for item in scene_json.get(json_key, []):
            item_path = os.path.join(ASSETS_BASE, folder, item["image"])
            
            if not os.path.exists(item_path):
                print(f"Warning: Asset not found at {item_path}")
                continue

            # Resize based on your predefined BASE_HEIGHT_RATIO
            img = resize_image(item_path, element_type, item.get("scale", 1.0))

            # 4️⃣ Positioning Logic
            pos = item.get("position")
            
            if isinstance(pos, dict):
                # Handle absolute {x, y} from JSON
                # We subtract half width/height to treat (x,y) as the center point
                x = int(pos["x"] - (img.width // 2))
                y = int(pos["y"] - (img.height // 2))
            else:
                # Handle string "left", "center", etc.
                x = get_x_position(pos, img.width)
                # Default bottom-alignment for character types
                y = CANVAS_HEIGHT - img.height - 20

            # Paste using the image itself as the mask to preserve transparency
            canvas.paste(img, (x, y), img)

    return canvas