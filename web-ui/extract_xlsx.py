import pandas as pd
import json

def extract_vulnerabilities(file_path):
    df = pd.read_excel(file_path)
    # Print the columns to understand the structure
    print(f"Columns: {df.columns.tolist()}")
    
    # Store the result in a list of dictionaries
    vulnerabilities = df.to_dict(orient='records')
    
    # Write to a JSON file for easier processing
    with open('vulnerabilities.json', 'w') as f:
        json.dump(vulnerabilities, f, indent=4)
        
if __name__ == "__main__":
    extract_vulnerabilities('vulnerabilities_main_filtered_202603232021.xlsx')
