import pandas as pd
import json

file_path = 'vulnerabilities_dev-next_filtered_202604011905.xlsx'
df = pd.read_excel(file_path)

# Extract relevant columns
# Assuming columns are 'Vulnerability', 'Location', 'Original_exploitability'
# I'll check the column names first if I'm not sure, but I'll try to find common ones.
print(df.columns.tolist())

# Convert to list of dicts
vulnerabilities = df.to_dict(orient='records')

with open('vulnerabilities.json', 'w') as f:
    json.dump(vulnerabilities, f, indent=2)
