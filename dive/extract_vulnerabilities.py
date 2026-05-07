import pandas as pd
import json

file_path = r"c:\Users\majab\OneDrive\Desktop\repo\dive\vulnerabilities_main_filtered_202603301849.xlsx"
df = pd.read_excel(file_path)

# Convert to list of dictionaries
data = df.to_dict(orient='records')

# Save as JSON for easier reading in the next steps
with open('vulnerabilities.json', 'w') as f:
    json.dump(data, f, indent=2, default=str)

print(f"Extracted {len(data)} vulnerabilities to vulnerabilities.json")
