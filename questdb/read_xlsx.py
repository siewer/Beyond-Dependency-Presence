import pandas as pd
import json

file_path = r"c:\Users\majab\OneDrive\Desktop\repo\questdb\vulnerabilities_master_filtered_202603221652.xlsx"
df = pd.read_excel(file_path)
df = df.fillna("")
print("---START JSON---")
print(df.to_json(orient='records', indent=2))
print("---END JSON---")
