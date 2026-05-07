import pandas as pd
df = pd.read_excel('vulnerabilities_master_filtered_202604032235.xlsx')
for index, row in df.iterrows():
    print(f"Index: {index}")
    print(f"Severity: {row['Severity']}")
    print(f"Name: {row['Name']}")
    print(f"Status: {row['Status']}")
    print(f"Exploitability: {row['Exploitability']}")
    print(f"Location: {row['Location']}")
    print("-" * 20)
