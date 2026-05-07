import json
import re

with open('c:/Users/majab/OneDrive/Desktop/repo/axios/package-lock.json', 'r') as f:
    lock = json.load(f)

packages = lock.get('packages', {})

vulnerable_pkgs = [
    "braces", "tough-cookie", "dicer", "got", "request", "semver-regex", 
    "ajv", "form-data", "http-cache-semantics", "qs", "babel-traverse", 
    "micromatch", "multer", "cross-spawn", "tar", "elliptic", "serialize-javascript"
]

version_quotes = {}

for pkg_name in vulnerable_pkgs:
    found = []
    # Match node_modules/pkg_name
    pattern = re.compile(f"(^|/)node_modules/{re.escape(pkg_name)}$")
    for path, info in packages.items():
        if pattern.search(path):
            found.append(f'"{path}": {{"version": "{info.get("version")}"}}')
    if found:
        version_quotes[pkg_name] = found
    else:
        version_quotes[pkg_name] = ["VERSION_SEARCH_COMPLETE: No entry for this package found in package-lock.json"]

print(json.dumps(version_quotes, indent=2))
