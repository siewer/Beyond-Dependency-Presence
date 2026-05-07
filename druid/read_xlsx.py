import pandas as pd
import json

file_path = r"c:\Users\majab\OneDrive\Desktop\repo\druid\vulnerabilities_master_filtered_202603221724.xlsx"
df = pd.read_excel(file_path)

# Convert to list of dicts
vulnerabilities = df.to_dict(orient='records')

with open('vulnerabilities.json', 'w') as f:
    json.dump(vulnerabilities, f, indent=2)

print(f"Extracted {len(vulnerabilities)} vulnerabilities.")
