import pandas as pd
import json

file_path = r'c:\Users\majab\OneDrive\Desktop\repo\AdGuardHome\vulnerabilities_master_filtered_202603312132.xlsx'
df = pd.read_excel(file_path)
print(df.to_json(orient='records'))
