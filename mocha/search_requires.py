import os
import json

def search_requires():
    pkgs = ['ajv', 'bn.js', 'elliptic', 'socket.io-parser', 'flatted', 'lodash', 'rollup', 'diff', 'h3', 'devalue', 'svgo']
    results = {p: [] for p in pkgs}
    
    for root, dirs, files in os.walk('.'):
        if 'node_modules' in dirs:
            dirs.remove('node_modules')
        if '.git' in dirs:
            dirs.remove('.git')
            
        for file in files:
            if file.endswith('.js') or file.endswith('.ts'):
                path = os.path.join(root, file)
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        for p in pkgs:
                            if f'require("{p}")' in content or f"require('{p}')" in content or f'import "{p}"' in content or f'from "{p}"' in content or f"from '{p}'" in content:
                                results[p].append(path)
                except:
                    pass
    return results

if __name__ == '__main__':
    res = search_requires()
    print(json.dumps(res, indent=2))
