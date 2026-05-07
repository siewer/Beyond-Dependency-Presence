import pandas as pd
import json

file_path = r'c:\Users\majab\OneDrive\Desktop\repo\1Panel\vulnerabilities_dev-v2_filtered_202603312055.xlsx'
df = pd.read_excel(file_path)
json_data = df.to_json(orient='records')
print(json_data)
