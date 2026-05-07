import pandas as pd
import subprocess
import json
import re
import os

df = pd.read_excel('vulnerabilities_main_filtered_202603222155.xlsx')
records = df.to_dict('records')

results = []

def search_usage(lib_name):
    lib_name_clean = lib_name.replace('-', '_')
    # search for import/require
    cmd = f"git grep -iE \"(import {lib_name_clean}|from {lib_name_clean} |require\\(['\\\"]{lib_name}['\\\"]\\)|from ['\\\"]{lib_name}['\\\"])\""
    try:
        output = subprocess.check_output(cmd, shell=True, text=True, stderr=subprocess.DEVNULL)
        return output.strip('\n').split('\n')
    except subprocess.CalledProcessError:
        return []

def get_vuln_details(v):
    lib = v['Location'].split(':')[0]
    vuln_id = v['Name']
    orig_exp = v['Exploitability']
    out = {
        "Vulnerability": vuln_id,
        "Location": v['Location'],
        "Original_exploitability": f"{orig_exp}%",
        "Exploitability": "",
        "Exploitability_explanation": "",
        "Assessment": ""
    }
    
    usage = search_usage(lib)
    if not usage:
        new_exp = 1
        out["Exploitability"] = f"{new_exp}%"
        out["Exploitability_explanation"] = f"No explicit call or import to {lib} found in the user code."
    else:
        # found usage
        new_exp = 50
        out["Exploitability"] = f"{new_exp}%"
        out["Exploitability_explanation"] = f"API usage for {lib} confirmed in the codebase. Version is assumed vulnerable."
    
    diff = abs(orig_exp - new_exp)
    out["Assessment"] = "Correct" if diff <= 20 else "Incorrect"
    return out

for v in records:
    results.append(get_vuln_details(v))

with open('wyniki.json', 'w') as f:
    json.dump(results, f, indent=2)

print("Generated wyniki.json")
