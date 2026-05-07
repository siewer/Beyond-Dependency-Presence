import pandas as pd
import json

df = pd.read_excel('vulnerabilities_master_filtered_202604032235.xlsx')
vulnerabilities = []
for index, row in df.iterrows():
    vulnerabilities.append({
        "Index": index,
        "Severity": str(row['Severity']),
        "Name": str(row['Name']),
        "Status": str(row['Status']),
        "Exploitability": float(row['Exploitability']),
        "Location": str(row['Location'])
    })

with open('vulnerabilities.json', 'w') as f:
    json.dump(vulnerabilities, f, indent=2)
