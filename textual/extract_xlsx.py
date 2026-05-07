import pandas as pd
import json

def extract_xlsx(file_path, output_path):
    df = pd.read_excel(file_path)
    # Convert all columns to strings to avoid JSON serialization issues
    df = df.astype(str)
    data = df.to_dict(orient='records')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    extract_xlsx(r"c:\Users\majab\OneDrive\Desktop\repo\textual\vulnerabilities_main_filtered_202603242152.xlsx", r"c:\Users\majab\OneDrive\Desktop\repo\textual\vulnerabilities.json")
