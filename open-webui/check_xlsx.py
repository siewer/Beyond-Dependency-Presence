import pandas as pd

file_path = "vulnerabilities_main_filtered_202603222155.xlsx"
df = pd.read_excel(file_path)

print("Columns:", df.columns.tolist())
print("First row:", df.iloc[0].to_dict())
