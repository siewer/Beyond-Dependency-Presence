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

mapping = {}

for pkg_name in vulnerable_pkgs:
    found = []
    # Match node_modules/pkg_name OR node_modules/.../node_modules/pkg_name
    pattern = re.compile(f"(^|/)node_modules/{re.escape(pkg_name)}$")
    for path, info in packages.items():
        if pattern.search(path):
            found.append({"path": path, "version": info.get('version'), "dev": info.get('dev', False)})
    mapping[pkg_name] = found

print(json.dumps(mapping, indent=2))
