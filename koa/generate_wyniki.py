import json

original_vulnerabilities = [
    {"Name": "CVE-2026-26996", "Exploitability": 0, "Location": "minimatch:9.0.5"},
    {"Name": "CVE-2026-32141", "Exploitability": 0, "Location": "flatted:3.3.3"},
    {"Name": "CVE-2025-64756", "Exploitability": 50, "Location": "glob:10.4.5"},
    {"Name": "CVE-2025-69873", "Exploitability": 0, "Location": "ajv:6.12.6"},
    {"Name": "CVE-2025-5889", "Exploitability": 0, "Location": "brace-expansion:1.1.11"},
    {"Name": "CVE-2026-33228", "Exploitability": 0, "Location": "flatted:3.3.3"},
    {"Name": "CVE-2026-27903", "Exploitability": 0, "Location": "minimatch:3.1.2"},
    {"Name": "CVE-2026-27903", "Exploitability": 0, "Location": "minimatch:9.0.5"},
    {"Name": "CVE-2026-27904", "Exploitability": 0, "Location": "minimatch:3.1.2"},
    {"Name": "CVE-2026-27904", "Exploitability": 0, "Location": "minimatch:9.0.5"},
    {"Name": "CVE-2025-5889", "Exploitability": 1, "Location": "brace-expansion:2.0.1"},
    {"Name": "CVE-2026-26996", "Exploitability": 0, "Location": "minimatch:3.1.2"}
]

explanation = "Vulnerable API is not called in any active code path. The library is exclusively used as a devDependency (e.g., by 'standard' or 'c8') and is not reachable by the core 'koa' framework. No usage found in lib/ directory."

results = []
for v in original_vulnerabilities:
    original_exploitability = v["Exploitability"]
    new_exploitability = 1
    
    # Correct if difference is less than or equal to 20%
    # But wait, original is percentage. 0 -> 1 is 1% difference. 50 -> 1 is 49% difference.
    is_correct = "Correct" if abs(original_exploitability - new_exploitability) <= 20 else "Incorrect"
    
    results.append({
        "Vulnerability": v["Name"],
        "Location": v["Location"],
        "Original_exploitability": f"{original_exploitability}%",
        "Exploitability": f"{new_exploitability}%",
        "Exploitability_explanation:": explanation,
        "Assessment": is_correct
    })

with open("wyniki.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)
