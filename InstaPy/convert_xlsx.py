import pandas as pd
import sys

file_path = r'c:\Users\majab\OneDrive\Desktop\repo\InstaPy\vulnerabilities_master_filtered_202603232050.xlsx'
try:
    df = pd.read_excel(file_path)
    df.to_csv('vulnerabilities.csv', index=False)
    print("XLSX converted to vulnerabilities.csv")
    print(df.head())
except Exception as e:
    print(f"Error: {e}")
