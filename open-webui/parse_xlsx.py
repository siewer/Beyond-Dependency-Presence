import pandas as pd
import json

file_path = "vulnerabilities_main_filtered_202603222155.xlsx"
df = pd.read_excel(file_path)

vulnerabilities = []
for index, row in df.iterrows():
    vuln = {
        "Vulnerability": str(row.get("Vulnerability", "")),
        "Location": str(row.get("Location", "")),
        "Original_exploitability": str(row.get("Exploitability", "")),
        "Description": str(row.get("Description", "")) if "Description" in df.columns else "",
        "CVE": str(row.get("CVE", "")) if "CVE" in df.columns else ""
    }
    vulnerabilities.append(vuln)

with open("vulns_extracted.json", "w", encoding="utf-8") as f:
    json.dump(vulnerabilities, f, indent=2)

print(f"Extracted {len(vulnerabilities)} vulnerabilities.")
