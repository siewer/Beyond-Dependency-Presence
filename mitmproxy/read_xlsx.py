import pandas as pd
import json

df = pd.read_excel('c:/Users/majab/OneDrive/Desktop/repo/mitmproxy/vulnerabilities_main_filtered_202603232008.xlsx')
print(df.to_json(orient='records'))
