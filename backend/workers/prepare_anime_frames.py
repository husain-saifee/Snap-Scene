from PIL import Image
from pathlib import Path

SRC = Path("backend/static/previews")

for img in SRC.glob("*.png"):
    im = Image.open(img).convert("RGB")
    im.save(img)
    print("Fixed:", img.name)
