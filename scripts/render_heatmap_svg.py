from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
data = json.loads((ROOT / "data/contributions.json").read_text())

days = data.get("days", [])[-371:]
palette = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353"]

cell = 12
gap = 3
left = 40
top = 34
cols = 53
rows = 7
width = left + cols * (cell + gap) + 25
height = top + rows * (cell + gap) + 70

svg = [
    f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}">',
    '<rect width="100%" height="100%" rx="12" fill="#0d1117"/>',
    '<text x="20" y="22" font-family="monospace" font-size="12" fill="#8b949e">CONTRIBUTIONS</text>',
]

for i, d in enumerate(days):
    col = i // 7
    row = i % 7

    x = left + col * (cell + gap)
    y = top + row * (cell + gap)

    level = max(0, min(4, int(d.get("level", 0))))
    delay = i * 0.008

    svg.append(
        f'<rect x="{x}" y="{y}" width="{cell}" height="{cell}" rx="2" '
        f'fill="{palette[level]}" opacity="0">'
        f'<title>{d["date"]}: {d["count"]} contributions</title>'
        f'<animate attributeName="opacity" from="0" to="1" '
        f'begin="{delay:.3f}s" dur=".35s" fill="freeze"/>'
        f'</rect>'
    )

svg += [
    f'<text x="20" y="{height-35}" font-family="monospace" font-size="12" fill="#39d353">total: {data.get("total", 0)}</text>',
    f'<text x="150" y="{height-35}" font-family="monospace" font-size="12" fill="#8b949e">streak: {data.get("current_streak", 0)} · longest: {data.get("longest_streak", 0)}</text>',
    '</svg>',
]

out = ROOT / "contrib-heatmap.svg"
out.write_text("\n".join(svg), encoding="utf-8")
print(out)
