import pandas as pd
import json

df = pd.read_excel('vulnerabilities_2.3_filtered_202603281434.xlsx')
data = df.to_dict(orient='records')
print(json.dumps(data, indent=2))
