import openpyxl
import json

def excel_to_json(excel_file, json_file):
    # Load the workbook
    workbook = openpyxl.load_workbook(excel_file, data_only=True)
    
    # Select the active worksheet
    sheet = workbook.active
    
    # Get column headers
    headers = [cell.value for cell in sheet[1]]
    
    # Iterate over the rows
    data = []
    for row in sheet.iter_rows(min_row=2, values_only=True):
        row_data = dict(zip(headers, row))
        data.append(row_data)
        
    # Write data to JSON file
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    excel_to_json('vulnerabilities_develop_filtered_202603312025.xlsx', 'vulns.json')
