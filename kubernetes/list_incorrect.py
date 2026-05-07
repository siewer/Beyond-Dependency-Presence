import json

with open("wyniki.json", "r", encoding="utf-8") as f:
    data = json.load(f)

incorrects = [d for d in data if d["Assessment"] == "Incorrect"]

print(f"Total Incorrect: {len(incorrects)}")
for i, d in enumerate(incorrects):
    print(f"{i+1}. {d['Vulnerability']} at {d['Location']} - Orig: {d['Original_exploitability']} -> New: {d['Exploitability']}")
