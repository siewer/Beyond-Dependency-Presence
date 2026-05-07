import json
import os

def find_parent(path, pkg):
    if not os.path.exists(path):
        return None
    try:
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            packages = data.get('packages', {})
            parents = []
            for node_path, info in packages.items():
                if 'dependencies' in info and pkg in info['dependencies']:
                    parents.append(node_path)
            return parents
    except Exception as e:
        return [f"Error: {str(e)}"]

libs = ['fast-xml-parser', 'flatted', 'underscore', 'diff', 'elliptic', 'serialize-javascript', 'markdown-it']
for lib in libs:
    print(f"Parents of {lib} in server:")
    for p in find_parent('server/package-lock.json', lib):
        print(f"  {p}")
    print(f"Parents of {lib} in client:")
    for p in find_parent('client/package-lock.json', lib):
        print(f"  {p}")
