import pandas as pd

file_path = r'c:\Users\majab\OneDrive\Desktop\repo\vault\vulnerabilities_main_filtered_202603212056.xlsx'
xls = pd.ExcelFile(file_path)
print("Sheets:", xls.sheet_names)

for sheet in xls.sheet_names:
    df = pd.read_excel(file_path, sheet_name=sheet)
    print(f"\n--- {sheet} ---")
    print("Columns:", df.columns.tolist())
    print(df.head())
