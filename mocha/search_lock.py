import json
import os

def find_pkgs(lock_file):
    pkgs = ['devalue', 'flatted', 'ajv', 'bn.js', 'elliptic', 'h3', 'socket.io-parser', 'rollup', 'svgo', 'diff', 'minimatch', 'serialize-javascript', 'lodash']
    found = {p: [] for p in pkgs}
    
    with open(lock_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    packages = data.get('packages', {})
    for path, info in packages.items():
        for p in pkgs:
            if path == f'node_modules/{p}' or path.endswith(f'/node_modules/{p}'):
                found[p].append({'path': path, 'version': info.get('version')})
                
    return found

if __name__ == '__main__':
    result = find_pkgs('package-lock.json')
    print(json.dumps(result, indent=2))
