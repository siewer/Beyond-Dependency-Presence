import pandas as pd
import json

file_path = r"c:\Users\majab\OneDrive\Desktop\repo\cryptii\vulnerabilities_main_filtered_202603272054.xlsx"
df = pd.read_excel(file_path)

# Print the columns to see what we have
print(df.columns.tolist())

# Convert to a list of dicts for easier processing
data = df.to_dict(orient='records')
for row in data:
    print(row)
