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

libs = ['@sailshq/nedb', '@sailshq/binary-search-tree', 'mocha', 'flat-cache', 'assertion-error-formatter', 'browserify-sign', 'create-ecdh', '@diplodoc/transform', 'markdownlint']
for lib in libs:
    print(f"Parents of {lib}:")
    cp = find_parent('client/package-lock.json', lib)
    if cp:
        for p in cp: print(f"  Client: {p}")
    sp = find_parent('server/package-lock.json', lib)
    if sp:
        for p in sp: print(f"  Server: {p}")
