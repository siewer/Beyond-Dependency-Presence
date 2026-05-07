import pandas as pd
import json

df = pd.read_excel('vulnerabilities_main_filtered_202603232012.xlsx')
data = df.to_dict(orient='records')

with open('vulnerabilities.json', 'w') as f:
    json.dump(data, f, indent=2)

print("Converted XLSX to vulnerabilities.json")
