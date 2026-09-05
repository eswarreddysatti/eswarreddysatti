from pathlib import Path
from PIL import Image, ImageOps
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
src = ROOT / "source-prepped.png"
out = ROOT / "avi-ascii.svg"

RAMP = " .`:-=+*cs#%@"
W, H = 100, 53

if not src.exists():
    raise SystemExit("Run prep_photo.py after adding photo.jpg first.")

img = Image.open(src).convert("L")
img = ImageOps.fit(img, (W, H))
a = np.asarray(img)

svg = [
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 520">',
    '<rect width="100%" height="100%" rx="12" fill="#0d1117"/>',
    '<style>text{font-family:monospace;font-size:12px;fill:#39d353}</style>',
]

for y in range(H):
    line = "".join(
        RAMP[min(len(RAMP)-1, int(v) * len(RAMP) // 256)]
        for v in a[y]
    )
    delay = y * 0.035
    svg.append(
        f'<text x="4" y="{16+y*9}" opacity="0">{line}'
        f'<animate attributeName="opacity" from="0" to="1" '
        f'begin="{delay:.3f}s" dur=".22s" fill="freeze"/></text>'
    )

svg += [
    '<text x="4" y="510" fill="#8b949e">ASCII PORTRAIT</text>',
    '</svg>'
]

out.write_text("\n".join(svg), encoding="utf-8")
print(out)
