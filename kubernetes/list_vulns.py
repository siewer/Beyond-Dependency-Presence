import json

with open("vulnerabilities.json", "r", encoding="utf-8") as f:
    data = json.load(f)

vulns = {}
for item in data:
    name = item["Name"]
    loc = item["Location"]
    orig_exp = item["Exploitability"]
    if name not in vulns:
        vulns[name] = {"locations": set(), "original_exploitability": orig_exp}
    vulns[name]["locations"].add(loc)

for k, v in vulns.items():
    print(f"{k}: {', '.join(v['locations'])} - Orig Exp: {v['original_exploitability']}")
