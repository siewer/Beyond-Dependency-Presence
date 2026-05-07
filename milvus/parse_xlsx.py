import pandas as pd
import json
import sys

file_path = 'vulnerabilities_master_filtered_202603302025.xlsx'
try:
    df = pd.read_excel(file_path)
    data = df.to_dict(orient='records')
    with open('vulnerabilities.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)
    print("Success")
except Exception as e:
    print(f"Error: {e}", file=sys.stderr)
    sys.exit(1)
