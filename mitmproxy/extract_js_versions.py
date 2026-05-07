import json

with open('c:/Users/majab/OneDrive/Desktop/repo/mitmproxy/web/package-lock.json', 'r') as f:
    data = json.load(f)

targets = ["braces", "micromatch", "minimatch", "ajv", "js-yaml", "rollup", "once", "lodash", "bootstrap"]
results = {}

def find_versions(packages):
    for name, pkg in packages.items():
        # Remove "node_modules/" prefix if exists
        clean_name = name.split("node_modules/")[-1]
        if clean_name in targets:
            results.setdefault(clean_name, set()).add(pkg.get("version"))

find_versions(data.get("packages", {}))

for name, versions in results.items():
    print(f"{name}: {list(versions)}")
