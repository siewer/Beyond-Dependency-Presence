import pandas as pd
import json

file_path = "vulnerabilities_master_filtered_202603282034.xlsx"
df = pd.read_excel(file_path)

# Fill NaN with empty string
df = df.fillna("")

data = df.to_dict(orient="records")
with open("vulnerabilities.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
print("Done")
