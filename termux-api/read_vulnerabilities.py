import pandas as pd
import json
import os

def convert_xlsx_to_json(xlsx_path, json_path):
    try:
        df = pd.read_excel(xlsx_path)
        # Convert to list of dicts
        data = df.to_dict(orient='records')
        with open(json_path, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"Successfully converted {xlsx_path} to {json_path}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    xlsx_file = "vulnerabilities_master_filtered_202604022132.xlsx"
    target_json = "vulnerabilities.json"
    convert_xlsx_to_json(xlsx_file, target_json)
