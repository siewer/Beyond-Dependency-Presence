import pandas as pd

file_path = r'c:\Users\majab\OneDrive\Desktop\repo\vault\vulnerabilities_main_filtered_202603212056.xlsx'
df = pd.read_excel(file_path, sheet_name='Filtered')
pd.set_option('display.max_columns', None)
pd.set_option('display.max_colwidth', None)
print(df.to_string())
