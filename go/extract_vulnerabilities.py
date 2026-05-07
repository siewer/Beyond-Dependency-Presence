import pandas as pd
import json

file_path = r'c:\Users\majab\OneDrive\Desktop\repo\go\vulnerabilities_master_filtered_202603282156.xlsx'
df = pd.read_excel(file_path)

# Convert to list of dicts
vulnerabilities = df.to_dict(orient='records')

# Save to json in tmp for processing
with open(r'c:\Users\majab\OneDrive\Desktop\repo\go\vulnerabilities.json', 'w') as f:
    json.dump(vulnerabilities, f, indent=2)

print(f"Extracted {len(vulnerabilities)} vulnerabilities.")
