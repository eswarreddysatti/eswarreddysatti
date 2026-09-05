from pathlib import Path
import json
import re
import requests
from bs4 import BeautifulSoup

USER = "eswarreddysatti"
ROOT = Path(__file__).resolve().parents[1]

url = f"https://github.com/users/{USER}/contributions"
r = requests.get(
    url,
    headers={"User-Agent": "Mozilla/5.0"},
    timeout=30,
)
r.raise_for_status()

soup = BeautifulSoup(r.text, "html.parser")
days = []

for td in soup.select("td.ContributionCalendar-day"):
    date = td.get("data-date")
    level = int(td.get("data-level") or 0)
    cell_id = td.get("id")

    count = 0

    if cell_id:
        tooltip = soup.find("tool-tip", attrs={"for": cell_id})

        if tooltip:
            text = tooltip.get_text(" ", strip=True)
            match = re.search(
                r"(\d[\d,]*)\s+contributions?",
                text,
                re.IGNORECASE,
            )

            if match:
                count = int(match.group(1).replace(",", ""))

    days.append({
        "date": date,
        "count": count,
        "level": level,
    })

if not days:
    raise RuntimeError("No GitHub contribution cells found.")

total = sum(d["count"] for d in days)

current_streak = 0
for d in reversed(days):
    if d["count"] > 0:
        current_streak += 1
    else:
        break

longest_streak = 0
run = 0

for d in days:
    if d["count"] > 0:
        run += 1
        longest_streak = max(longest_streak, run)
    else:
        run = 0

best_day = max(days, key=lambda d: d["count"])

payload = {
    "username": USER,
    "total": total,
    "current_streak": current_streak,
    "longest_streak": longest_streak,
    "best_day": best_day,
    "days": days,
}

out = ROOT / "data/contributions.json"
out.write_text(json.dumps(payload, indent=2), encoding="utf-8")

print(
    f"Fetched {len(days)} days; "
    f"total={total}; "
    f"current_streak={current_streak}; "
    f"longest_streak={longest_streak}"
)
