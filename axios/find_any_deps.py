import json
import sys

def find_any_version(data):
    results = [
        "ajv",
        "http-cache-semantics",
        "semver-regex",
        "babel-traverse",
        "multer"
    ]
    found = {k: set() for k in results}

    def walk_v1(deps):
        for name, info in deps.items():
            if name in results:
                found[name].add(info.get('version'))
            if 'dependencies' in info:
                walk_v1(info['dependencies'])

    def walk_v2_v3(packages):
        for path, info in packages.items():
            parts = path.split('/')
            name = parts[-1]
            if name in results:
                found[name].add(info.get('version'))

    if 'packages' in data:
        walk_v2_v3(data['packages'])
    if 'dependencies' in data:
        walk_v1(data['dependencies'])
    
    return found

try:
    with open('package-lock.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        found = find_any_version(data)
        for name, versions in found.items():
            print(f"{name}: {', '.join(filter(None, versions)) or 'None'}")
except Exception as e:
    print(f"Error: {e}")
