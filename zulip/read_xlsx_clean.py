import pandas as pd
import json

df = pd.read_excel('vulnerabilities_main_filtered_202603242241.xlsx')
data = df.to_dict(orient='records')
with open('vulnerabilities_clean.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2)
print("Successfully saved to vulnerabilities_clean.json")
