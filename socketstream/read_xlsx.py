import pandas as pd
import json

df = pd.read_excel('vulnerabilities_develop_filtered_202603271936.xlsx')
data = df.to_dict(orient='records')

with open('vulnerabilities.json', 'w') as f:
    json.dump(data, f, indent=2)

print("SUCCESS: vulnerabilities.json created")
