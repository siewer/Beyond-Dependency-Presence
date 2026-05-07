import json

with open("wyniki.json", "r", encoding="utf-8") as f:
    data = json.load(f)

absent = [d for d in data if d["Exploitability"] == 1.0]
print(f"Total Absent (1.0): {len(absent)}")
for d in absent:
    print(f"{d['Vulnerability']} at {d['Location']} - Orig: {d['Original_exploitability']} -> Assessment: {d['Assessment']}")
