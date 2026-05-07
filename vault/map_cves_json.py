import re
import os
import json

repo_path = r'c:\Users\majab\OneDrive\Desktop\repo\vault'
csv_path = os.path.join(repo_path, 'vulnerabilities.csv')

with open(csv_path, 'r') as f:
    lines = f.readlines()
    cves = [line.split(',')[1] for line in lines[1:] if line.strip()]

changelog_files = [f for f in os.listdir(repo_path) if f.startswith('CHANGELOG') and f.endswith('.md')]

results = {}
for cve in cves:
    results[cve] = []
    for cf in changelog_files:
        cf_path = os.path.join(repo_path, cf)
        with open(cf_path, 'r', encoding='utf-8') as f:
            content = f.read()
            if cve in content:
                # Find the sentence/bullet point containing the CVE
                # Look for lines starting with * or - and containing the CVE
                matches = re.findall(r'^[*-]\s+.*' + re.escape(cve) + r'.*', content, re.MULTILINE)
                results[cve].extend([m.strip() for m in matches])

with open(os.path.join(repo_path, 'cve_map.json'), 'w') as f:
    json.dump(results, f, indent=2)

print("Mapped", len([k for k, v in results.items() if v]), "CVEs out of", len(cves))
