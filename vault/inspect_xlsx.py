import pandas as pd

file_path = r'c:\Users\majab\OneDrive\Desktop\repo\vault\vulnerabilities_main_filtered_202603212056.xlsx'
df = pd.read_excel(file_path)
print("Columns:", df.columns.tolist())
print("\ndf head:\n", df.head())
