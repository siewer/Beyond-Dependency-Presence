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

found = {}
try:
    with open('yarn.lock', 'r', encoding='utf-8') as f:
        content = f.read()

    blocks = content.split('\n\n')
    for block in blocks:
        lines = block.strip().split('\n')
        if not lines:
            continue
        header = lines[0]
        for pkg in packages:
            # Match package name at the start of the header, followed by @
            if header.startswith(pkg + '@') or header.startswith('"' + pkg + '@'):
                version_match = re.search(r'^\s+version\s+"(.*)"', block, re.MULTILINE)
                if version_match:
                    version = version_match.group(1)
                    if pkg not in found:
                        found[pkg] = set()
                    found[pkg].add(version)

    # Convert sets to sorted lists for JSON serialization
    result = {k: sorted(list(v)) for k, v in found.items()}
    print(json.dumps(result, indent=2))
except Exception as e:
    print(json.dumps({"error": str(e)}))
