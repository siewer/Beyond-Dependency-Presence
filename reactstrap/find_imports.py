import os
import re

vulnerable_libs = [
    "ejs", "tar", "json5", "loader-utils", "shell-quote", "ssri", "json-schema", "minimist", "immer", 
    "tough-cookie", "trim", "qs", "body-parser", "trim-newlines", "elliptic", "glob-parent", 
    "node-fetch", "decode-uri-component", "lodash", "browserify-sign", "minimatch", "y18n", 
    "store2", "serve-static", "prismjs", "form-data", "ajv", "trim-off-newlines", "browserslist", 
    "path-to-regexp", "ansi-regex", "postcss", "braces", "markdown-to-jsx", "ansi-html", 
    "babel/traverse", "micromatch", "babel/helpers", "babel/runtime", "cookie", "send", 
    "nanoid", "cross-spawn", "express"
]

src_path = r"c:\Users\majab\OneDrive\Desktop\repo\reactstrap\src"
found_usages = {}

for root, dirs, files in os.walk(src_path):
    for file in files:
        if file.endswith((".js", ".ts", ".tsx")):
            file_path = os.path.join(root, file)
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                for lib in vulnerable_libs:
                    # Match import ... from 'lib' or require('lib')
                    pattern = rf"(['\"]){re.escape(lib)}(\/.*)?\1"
                    if re.search(pattern, content):
                        if lib not in found_usages:
                            found_usages[lib] = []
                        found_usages[lib].append(file_path)

for lib, files in found_usages.items():
    print(f"Library '{lib}' found in {len(files)} files:")
    for f in files[:5]: # Show first 5 files
        print(f"  - {f}")
    if len(files) > 5:
        print(f"  ... and {len(files) - 5} more")
