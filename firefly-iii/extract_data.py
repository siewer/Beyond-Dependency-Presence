import pandas as pd
import json

df = pd.read_excel('vulnerabilities_main_filtered_202603281515.xlsx')
data = df.to_dict(orient='records')
with open('vulnerabilities.json', 'w') as f:
    json.dump(data, f, indent=2)
print("Data extracted to vulnerabilities.json")
