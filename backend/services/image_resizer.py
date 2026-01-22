

from PIL import Image
from .canvas import CANVAS_HEIGHT

# Relative base sizes (percent of canvas height)
BASE_HEIGHT_RATIO = {
    "character": 0.40,   # ~288px on 720p
    "object": 0.20,      # ~144px
    "smallprop": 0.10    # ~72px
}

def resize_image(image_path: str, element_type: str, scale: float = 1.0) -> Image.Image:
    """
    Auto-resize image relative to canvas height.

    Args:
        image_path (str): Path to image file
        element_type (str): character | object | smallprop
        scale (float): 0.6 - 1.3

    Returns:
        PIL.Image
    """

    img = Image.open(image_path).convert("RGBA")

    base_height = int(CANVAS_HEIGHT * BASE_HEIGHT_RATIO[element_type])
    target_height = int(base_height * scale)

    aspect_ratio = img.width / img.height
    target_width = int(target_height * aspect_ratio)

    return img.resize((target_width, target_height), Image.LANCZOS)
