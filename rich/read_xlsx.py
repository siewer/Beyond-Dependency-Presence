import pandas as pd
import json

try:
    df = pd.read_excel('vulnerabilities_master_filtered_202603231956.xlsx')
    # replace NaN with None
    df = df.where(pd.notnull(df), None)
    
    records = df.to_dict(orient='records')
    with open('vulnerabilities.json', 'w', encoding='utf-8') as f:
        json.dump(records, f, indent=2)
except Exception as e:
    print(f"Error: {e}")
