import re
import json

packages = [
    'lodash', 'minimist', 'json5', 'tough-cookie', 'hoek', 'qs', 'json-schema', 
    'pug-code-gen', 'markdown-it', 'decode-uri-component', 'semver', 'ws', 
    'merge', 'y18n', 'minimatch', 'tmpl', 'request', 'hosted-git-info', 'ajv', 
    'node-notifier', 'hawk', '@babel/traverse', '@babel/helpers', 'yargs-parser', 
    'micromatch', 'cross-spawn', 'debug', 'word-wrap', 'js-yaml', 'brace-expansion', 
    'pug', 'path-parse', 'braces', 'form-data', 'ansi-regex'
]

with open('yarn.lock', 'r', encoding='utf-8') as f:
    content = f.read()

blocks = content.split('\n\n')
child_to_parents = {}

for block in blocks:
    lines = block.strip().split('\n')
    if not lines:
        continue
    header = lines[0]
    deps = []
    in_deps = False
    for line in lines:
        if line.strip() == 'dependencies:':
            in_deps = True
            continue
        if in_deps:
            if line.startswith('    ') and not line.startswith('      '):
                m = re.match(r'^\s+(\"?.*?\"?)\s+\"(.*)\"', line)
                if m:
                    deps.append(m.group(1).replace('"', ''))
            elif not line.startswith('    '):
                in_deps = False
    
    pkg_headers = [h.strip().replace('"', '') for h in header.split(',')]
    for pkg_at_ver in pkg_headers:
        pkg_name = pkg_at_ver.split('@')[0]
        for d in deps:
            d_name = d.split('@')[0]
            if d_name not in child_to_parents:
                child_to_parents[d_name] = set()
            child_to_parents[d_name].add(pkg_name)

result = {pkg: list(child_to_parents.get(pkg, [])) for pkg in packages}
print(json.dumps(result, indent=2))
