import pandas as pd
import json

try:
    df = pd.read_excel('vulnerabilities_master_filtered_202603221627.xlsx')
    records = df.to_dict(orient='records')
    with open('vulnerabilities_extracted.json', 'w', encoding='utf-8') as f:
        json.dump(records, f, indent=2, default=str)
except Exception as e:
    print(f"Error: {e}")
