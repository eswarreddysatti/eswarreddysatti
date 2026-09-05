from pathlib import Path
from PIL import Image, ImageOps, ImageEnhance
import cv2
import numpy as np
from rembg import remove

ROOT = Path(__file__).resolve().parents[1]
src = ROOT / "photo.jpg"
out = ROOT / "source-prepped.png"

if not src.exists():
    raise SystemExit("Add photo.jpg to the repository root first.")

img = Image.open(src).convert("RGB")
img = remove(img).convert("RGBA")

bg = Image.new("RGBA", img.size, "white")
bg.alpha_composite(img)
img = bg.convert("RGB")

arr = np.array(img)
lab = cv2.cvtColor(arr, cv2.COLOR_RGB2LAB)
l, a, b = cv2.split(lab)
l = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8)).apply(l)
arr = cv2.cvtColor(cv2.merge((l, a, b)), cv2.COLOR_LAB2RGB)

img = Image.fromarray(arr)
img = ImageOps.fit(img, (1000, 1000), method=Image.Resampling.LANCZOS)
img = ImageEnhance.Contrast(img).enhance(1.15)
img.save(out)

print(out)
