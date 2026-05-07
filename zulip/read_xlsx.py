import pandas as pd
import json

df = pd.read_excel('vulnerabilities_main_filtered_202603242241.xlsx')
data = df.to_dict(orient='records')
print(json.dumps(data, indent=2))
