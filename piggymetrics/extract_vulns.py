import pandas as pd
import json

file_path = 'vulnerabilities_master_filtered_202604092027.xlsx'
df = pd.read_excel(file_path)

# Convert to a list of dictionaries
vulnerabilities = df.to_dict(orient='records')

with open('vulnerabilities.json', 'w') as f:
    json.dump(vulnerabilities, f, indent=2)
