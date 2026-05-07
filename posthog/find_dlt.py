import re

pkg_name = 'dlt'
with open('uv.lock', 'r') as f:
    content = f.read()

packages = content.split('[[package]]')
for pkg in packages:
    if f'name = "{pkg_name}"' in pkg:
        print(pkg)
