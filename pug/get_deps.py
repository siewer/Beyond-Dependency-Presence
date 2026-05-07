import os
import json

deps = {}
for root, dirs, files in os.walk('packages'):
    if 'package.json' in files:
        try:
            with open(os.path.join(root, 'package.json'), 'r', encoding='utf-8') as f:
                pj = json.load(f)
                deps[pj['name']] = pj.get('dependencies', {})
        except Exception as e:
            pass

print(json.dumps(deps, indent=2))
