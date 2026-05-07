import pandas as pd
import json

file_path = "vulnerabilities_master_filtered_202604011928.xlsx"
df = pd.read_excel(file_path)
data = df.to_dict(orient="records")

with open("vulnerabilities.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2)
