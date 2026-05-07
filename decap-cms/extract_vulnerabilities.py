import pandas as pd
import json
import os

file_path = r'c:\Users\majab\OneDrive\Desktop\repo\decap-cms\vulnerabilities_main_filtered_202604102033.xlsx'
output_path = r'c:\Users\majab\OneDrive\Desktop\repo\decap-cms\vulnerabilities.json'

try:
    df = pd.read_excel(file_path)
    # Convert dataframe to list of dicts
    data = df.to_dict(orient='records')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Successfully extracted {len(data)} vulnerabilities to {output_path}")
except Exception as e:
    print(f"Error: {e}")
