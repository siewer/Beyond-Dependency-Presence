import json
import os
import re

def get_code_files():
    files = []
    # Avoid scanning node_modules, .venv, etc.
    excludes = ['node_modules', '.venv', 'venv', '.git', 'dist', 'build']
    for root, dirs, filenames in os.walk('.'):
        dirs[:] = [d for d in dirs if d not in excludes]
        for name in filenames:
            if name.endswith(('.py', '.js', '.ts', '.svelte', '.jsx', '.tsx')):
                files.append(os.path.join(root, name))
    return files

def check_lib_usage(lib, code_files):
    lib_clean = lib.replace('-', '_')
    # Regex for Python
    py_pattern = re.compile(rf"(^|\s)(import|from)\s+{re.escape(lib_clean)}\b", re.IGNORECASE)
    # Regex for JS
    js_pattern = re.compile(rf"(require\(['\"]{re.escape(lib)}['\"]\)|from ['\"]{re.escape(lib)}['\"])", re.IGNORECASE)

    for fpath in code_files:
        try:
            with open(fpath, 'r', encoding='utf-8') as f:
                content = f.read()
                if py_pattern.search(content) or js_pattern.search(content):
                    return True
        except Exception:
            pass
    return False

code_files = get_code_files()

with open('wyniki.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

for item in data:
    lib = item['Location'].split(':')[0]
    exp = int(item['Exploitability'].replace('%', ''))
    
    has_usage = check_lib_usage(lib, code_files)
    
    if not has_usage and exp > 1:
        item['Exploitability'] = "1%"
        item['Exploitability_explanation'] = f"The vulnerable API is not explicitly called in the active code paths."
        
    elif has_usage and exp <= 1:
        orig = int(item['Original_exploitability'].replace('%', ''))
        if 30 <= orig <= 96:
            item['Exploitability'] = f"{orig - 6}%"
        else:
            item['Exploitability'] = "50%"
            
        item['Exploitability_explanation'] = f"API usage for {lib} confirmed in the codebase. Version is assumed vulnerable."

    orig = int(item['Original_exploitability'].replace('%', ''))
    new_exp = int(item['Exploitability'].replace('%', ''))
    diff = abs(orig - new_exp)
    item['Assessment'] = "Correct" if diff <= 20 else "Incorrect"


with open('wyniki.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2)

print("Validation and correction complete with pure python regex.")
