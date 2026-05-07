import re
import os

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
                matches = re.findall(r'\*.*' + re.escape(cve) + r'.*', content)
                results[cve].extend(matches)

for cve, matches in results.items():
    if matches:
        print(f"--- {cve} ---")
        for m in matches:
            print(m)
