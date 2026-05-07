import json
import re
import os

# Load original vulnerabilities
with open('vulnerabilities.json', 'r') as f:
    vulnerabilities = json.load(f)

# Rules summary:
# API not used in src: 0.01 (1%)
# Library/Vendor code only: Max 0.10 (10%) - We'll use 1% for non-imported, 5% for imported but not confirmed vulnerable helpers.

results = []

for v in vulnerabilities:
    name = v['Name']
    location = v['Location']
    original_exploitability = v['Exploitability']
    
    # We already checked that none of the vulnerable libraries are imported in src/
    # EXCEPT for @babel/runtime which is a direct dependency.
    
    if "@babel/runtime" in location:
        # @babel/runtime is used. No evidence of vulnerable helper usage.
        probability = 5.0 
        status = "uncertain" # Status uncertain when usage present but reachability not fully proven
        exploitable = "Maybe"
        explanation = "Library usage found (@babel/runtime). No evidence of specific vulnerable helper call in User Code. Version assumed vulnerable as per instructions."
    else:
        # All other libraries (tar, ejs, json5, loader-utils, ssri, etc.) are NOT imported in src/
        probability = 1.0
        status = "not_confirmed"
        exploitable = False
        explanation = "Vulnerable API is not called in any active code path. Searched src/ for imports/requires and found no evidence of usage. Library is a transitive or dev dependency not reachable from runtime code."

    # Assessment: Correct if difference <= 20
    assessment = "Correct" if abs(original_exploitability - probability) <= 20 else "Incorrect"
    
    results.append({
        "Vulnerability": name,
        "Location": location,
        "Original_exploitability": original_exploitability,
        "Exploitability": probability,
        "Exploitability_explanation": explanation,
        "Assessment": assessment
    })

# Write wyniki.json
with open('wyniki.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

print(f"Generated wyniki.json with {len(results)} entries.")
