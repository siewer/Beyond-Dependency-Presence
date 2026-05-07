import re

packages = ["jinja2", "urllib3", "filelock", "idna", "virtualenv", "wheel"]
results = {}

with open('uv.lock', 'r') as f:
    content = f.read()
    for pkg in packages:
        pattern = rf'\[\[package\]\]\nname = "{pkg}"\nversion = "([^"]+)"'
        match = re.search(pattern, content, re.MULTILINE)
        if match:
            results[pkg] = match.group(1)

print(results)
