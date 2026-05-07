import pandas as pd
import json

file_path = r'c:\Users\majab\OneDrive\Desktop\repo\spring-authorization-server\vulnerabilities_main_filtered_202604092110.xlsx'
df = pd.read_excel(file_path)
data = df.to_dict(orient='records')

with open('vulnerabilities.json', 'w') as f:
    json.dump(data, f, indent=2)

print(f"Successfully converted {len(data)} vulnerabilities to vulnerabilities.json")
