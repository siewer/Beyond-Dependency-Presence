import json

with open('vulnerabilities.json', 'r') as f:
    vulnerabilities = json.load(f)

unique_cves = {}
for v in vulnerabilities:
    name = v['Name']
    location = v['Location']
    if name not in unique_cves:
        unique_cves[name] = []
    unique_cves[name].append(v)

print(f"Total unique CVEs/GHSAs: {len(unique_cves)}")
for name, entries in unique_cves.items():
    locations = [e['Location'] for e in entries]
    print(f"{name}: {len(entries)} occurrences in {locations}")
