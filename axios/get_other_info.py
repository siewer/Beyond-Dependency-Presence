import json

with open('c:/Users/majab/OneDrive/Desktop/repo/axios/package-lock.json', 'r') as f:
    lock = json.load(f)

packages = lock.get('packages', {})

for path, info in packages.items():
    if path.endswith('node_modules/follow-redirects') or path.endswith('node_modules/proxy-from-env'):
        print(json.dumps({path: info}, indent=2))
