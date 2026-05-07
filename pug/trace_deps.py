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

# Map each package version to its block in yarn.lock
blocks = content.split('\n\n')
dep_to_parents = {}

for block in blocks:
    lines = block.strip().split('\n')
    if not lines:
        continue
    header = lines[0]
    # Extract dependencies in this block
    deps = []
    in_deps = False
    for line in lines:
        if line.strip() == 'dependencies:':
            in_deps = True
            continue
        if in_deps:
            if line.startswith('    ') and not line.startswith('      '): # One level of indent for dep list
                m = re.match(r'^\s+(\"?.*?\"?)\s+\"(.*)\"', line)
                if m:
                    deps.append(m.group(1).replace('"', ''))
            elif not line.startswith('    '):
                in_deps = False
    
    # Header can have multiple packages
    pkg_headers = [h.strip().replace('"', '') for h in header.split(',')]
    for pkg_at_ver in pkg_headers:
        pkg_name = pkg_at_ver.split('@')[0]
        for d in deps:
            if d not in dep_to_parents:
                dep_to_parents[d] = set()
            dep_to_parents[d].add(pkg_name)

# Now recursively find if any vulnerable package is reachable from a PUG package
pug_packages = [
    'pug', 'pug-attrs', 'pug-code-gen', 'pug-error', 'pug-filters', 
    'pug-lexer', 'pug-linker', 'pug-load', 'pug-parser', 'pug-runtime', 
    'pug-strip-comments', 'pug-walk'
]

results = {}

def get_reachability(start_pkgs):
    reachable = set(start_pkgs)
    queue = list(start_pkgs)
    visited = set(start_pkgs)
    
    # Standard BFS to find all children
    # Wait, dep_to_parents maps CHILD to PARENTS.
    # To find if a VULNERABLE package is reachable from a PUG package:
    # We can start from PUG packages and find all their children.
    
    child_to_deps = {pkg: [] for pkg in dep_to_parents.keys()}
    for child, parents in dep_to_parents.items():
        for p in parents:
            if p not in child_to_deps:
                child_to_deps[p] = []
            child_to_deps[p].append(child)
            
    reachable_from_pug = set()
    queue = list(pug_packages)
    visited = set(pug_packages)
    
    while queue:
        current = queue.pop(0)
        reachable_from_pug.add(current)
        for child in child_to_deps.get(current, []):
            if child not in visited:
                visited.add(child)
                queue.append(child)
    
    return reachable_from_pug

reachable_from_pug = get_reachability(pug_packages)
results = [pkg for pkg in packages if pkg in reachable_from_pug]
print(json.dumps(results, indent=2))
