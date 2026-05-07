import os
import re

packages = [
    'lodash', 'minimist', 'json5', 'tough-cookie', 'hoek', 'qs', 'json-schema', 
    'pug-code-gen', 'markdown-it', 'decode-uri-component', 'semver', 'ws', 
    'merge', 'y18n', 'minimatch', 'tmpl', 'request', 'hosted-git-info', 'ajv', 
    'node-notifier', 'hawk', '@babel/traverse', '@babel/helpers', 'yargs-parser', 
    'micromatch', 'cross-spawn', 'debug', 'word-wrap', 'js-yaml', 'brace-expansion', 
    'pug', 'path-parse', 'braces', 'form-data', 'ansi-regex'
]

# Vulnerable functions to look for
vulnerable_functions = [
    'parse', 'zipObjectDeep', 'set', 'setWith', 'update', 'updateWith', 'pick', 
    'template', 'merge', 'applyToDefaults', 'validate', 'compileClient', 
    'compileFileClient', 'WebSocketServer', 'handleUpgrade', 'Range', 'ansiRegex',
    'spawn', 'exec', 'fork'
]

results = []

for root, dirs, files in os.walk('.'):
    if 'node_modules' in dirs:
        dirs.remove('node_modules')
    if '.git' in dirs:
        dirs.remove('.git')
    for file in files:
        if file.endswith('.js'):
            path = os.path.join(root, file)
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                # Check for requires
                for pkg in packages:
                    if re.search(r"require\(['\"]" + re.escape(pkg) + r"['\"]\)", content):
                        results.append(f"FOUND REQUIRE: {pkg} in {path}")
                    if re.search(r"from ['\"]" + re.escape(pkg) + r"['\"]", content):
                        results.append(f"FOUND IMPORT: {pkg} in {path}")
                
                # Check for function calls (broadly)
                for func in vulnerable_functions:
                    if re.search(r"\b" + re.escape(func) + r"\(", content):
                        # Get some context
                        matches = re.finditer(r".*?\b" + re.escape(func) + r"\(.*", content)
                        for match in matches:
                            results.append(f"POTENTIAL CALL: {func} in {path}: {match.group(0).strip()}")
            except Exception as e:
                pass

for res in results:
    print(res)
