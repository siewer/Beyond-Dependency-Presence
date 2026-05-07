import json

with open('c:/Users/majab/OneDrive/Desktop/repo/axios/package-lock.json', 'r') as f:
    lock = json.load(f)

packages = lock.get('packages', {})

vulnerable_pkgs = [
    "braces", "tough-cookie", "dicer", "got", "request", "semver-regex", 
    "ajv", "form-data", "http-cache-semantics", "qs", "babel-traverse", 
    "micromatch", "multer", "cross-spawn", "tar", "elliptic", "serialize-javascript"
]

production_deps = ["follow-redirects", "form-data", "proxy-from-env"]

# Build a graph of dependencies
# In package-lock.json v3, 'packages' has all info.
routes = []

for pkg_path, pkg_info in packages.items():
    pkg_name = pkg_path.split('node_modules/')[-1]
    if pkg_name in vulnerable_pkgs:
        # Check if it's a dev dependency
        is_dev = pkg_info.get('dev', False)
        routes.append({"name": pkg_name, "path": pkg_path, "dev": is_dev})

print(json.dumps(routes, indent=2))
