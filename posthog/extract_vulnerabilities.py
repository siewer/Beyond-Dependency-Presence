import pandas as pd
import json

try:
    df = pd.read_excel('vulnerabilities_master_filtered_202603251736.xlsx')
    data = df.to_dict(orient='records')
    with open('vulnerabilities_utf8.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)
    print("Success: vulnerabilities_utf8.json created.")
except Exception as e:
    print(f"Error: {e}")
