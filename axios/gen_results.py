import pandas as pd
import json
import os

df = pd.read_csv('c:/Users/majab/OneDrive/Desktop/repo/axios/vulnerabilities.csv')

# Scoring model:
# 1. Version (Assuming satisfied) = 25%
# 2. Presence in tree (package-lock.json) = 25%
# 3. Reachability from lib/ = 25%
# 4. Exploitation Context/Difficulty = 25%
#
# Scores:
# 25% satisfied -> 15%
# 50% satisfied -> 35%
# 75% satisfied -> 60%
# 100% satisfied -> 77.5%

# Mapped Presence (from prev script):
in_tree = [
    "braces", "ajv", "form-data", "http-cache-semantics", "qs", 
    "micromatch", "multer", "cross-spawn", "tar", "serialize-javascript"
]
# Reachable from lib/
reachable = ["form-data"]

results = []

for _, row in df.iterrows():
    vuln = row['Name']
    loc = row['Location']
    orig = row['Exploitability']
    pkg = loc.split(':')[0]
    
    # Calculate satisfied constraints
    satisfied_count = 1 # Version always satisfied
    
    explanation = "Assume version is vulnerable. "
    
    if pkg in in_tree:
        satisfied_count += 1
        explanation += "Package exists in dependency tree (dev/transitive). "
    else:
        explanation += "Package not found in current dependency tree. "
        
    if pkg in reachable:
        satisfied_count += 1
        explanation += "Package is directly reachable from Axios library code. "
        # For reachable items, check if exploitation is easy
        if vuln == "CVE-2025-7783": # form-data predictable boundaries
             satisfied_count += 1
             explanation += "Vulnerability has high exploitability (predictable boundaries)."
    
    # Map count to score
    score_map = {1: 15, 2: 35, 3: 60, 4: 77.5}
    recal = score_map.get(satisfied_count, 15)
    
    # Assessment (20% absolute tolerance)
    diff = abs(orig - recal)
    assessment = "Correct" if diff <= 20 else "Incorrect"
    
    results.append({
        "Vulnerability": vuln,
        "Location": loc,
        "Original_exploitability": orig,
        "Exploitability": recal,
        "Exploitability_explanation": explanation.strip(),
        "Assessment": assessment
    })

# Save results
output_path = 'c:/Users/majab/OneDrive/Desktop/repo/axios/wyniki.json'
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(results, f, indent=2)

print(f"Generated {len(results)} entries in {output_path}")
