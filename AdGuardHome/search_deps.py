import json

file_path = r'c:\Users\majab\OneDrive\Desktop\repo\AdGuardHome\client\package-lock.json'
search_terms = ["node-fetch", "rollup", "qs", "ajv", "vite", "braces", "node-forge", "micromatch", "minimatch", "flatted", "min-document", "d3-color", "serialize-javascript"]

with open(file_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

results = {}
def find_deps(deps):
    for name, info in deps.items():
        if any(term in name for term in search_terms):
            results[name] = info.get('version')
        if 'dependencies' in info:
            find_deps(info['dependencies'])

if 'dependencies' in data:
    find_deps(data['dependencies'])
elif 'packages' in data:
    for name, info in data['packages'].items():
        if any(term in name for term in search_terms):
            results[name] = info.get('version')

print(json.dumps(results, indent=2))
