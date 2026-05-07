import pandas as pd
import json

try:
    df = pd.read_excel('vulnerabilities_master_filtered_202603301930.xlsx')
    # Filter the columns we need: Vulnerability, Location, Exploitability
    # The prompt mentions: Vulnerability, Location, Original_exploitability
    # Let's see what columns are available.
    data = df.to_dict(orient='records')
    print(json.dumps(data, indent=2))
except Exception as e:
    print(f"Error: {e}")
