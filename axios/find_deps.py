import json
import sys

def find_in_lockfile(data):
    results = {
        "ajv": "5.5.2",
        "http-cache-semantics": "3.8.1",
        "semver-regex": "2.0.0",
        "babel-traverse": "6.26.0",
        "multer": "1.4.4"
    }
    found = {k: False for k in results}

    def walk_v1(deps):
        for name, info in deps.items():
            if name in results and info.get('version') == results[name]:
                found[name] = True
            if 'dependencies' in info:
                walk_v1(info['dependencies'])

    def walk_v2_v3(packages):
        for path, info in packages.items():
            # path is like "node_modules/ajv"
            parts = path.split('/')
            name = parts[-1]
            if name in results and info.get('version') == results[name]:
                found[name] = True

    if 'packages' in data:
        walk_v2_v3(data['packages'])
    if 'dependencies' in data:
        walk_v1(data['dependencies'])
    
    return found

try:
    with open('package-lock.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        found = find_in_lockfile(data)
        for name, status in found.items():
            print(f"{name}: {status}")
except Exception as e:
    print(f"Error: {e}")
