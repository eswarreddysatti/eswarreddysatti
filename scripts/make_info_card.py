from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
out = ROOT / "info-card.svg"

rows = [
    ("Role", "Systems Operations Analyst"),
    ("Focus", "Cloud Ops / DevOps / Cybersecurity"),
    ("Stack", "AWS · Linux · Splunk · Python · Bash"),
    ("Security", "SIEM · IR · IAM · Detection Engineering"),
    ("Tools", "ServiceNow · PowerShell · Networking"),
    ("Learning", "Azure · Cloud Security · Automation"),
]

svg = [
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 700 430">',
    '<rect width="700" height="430" rx="14" fill="#0d1117" stroke="#30363d"/>',
    '<text x="28" y="42" font-family="monospace" font-size="22" fill="#39d353">eswar@github:~$ neofetch</text>',
]

for i, (k, v) in enumerate(rows):
    y = 92 + i * 52
    svg.append(
        f'<text x="28" y="{y}" font-family="monospace" font-size="16" fill="#8b949e">{k}</text>'
    )
    svg.append(
        f'<text x="160" y="{y}" font-family="monospace" font-size="16" fill="#f0f6fc">{v}</text>'
    )

svg += [
    '<text x="28" y="408" font-family="monospace" font-size="14" fill="#58a6ff">[ production systems • security • automation ]</text>',
    '</svg>',
]

out.write_text("\n".join(svg), encoding="utf-8")
print(out)
