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

repo_path = r"c:\Users\majab\OneDrive\Desktop\repo\reactstrap"
found_mentions = {}

exclude_dirs = {"node_modules", ".git", "dist", "build", "esm", "lib"}

for root, dirs, files in os.walk(repo_path):
    # Skip excluded directories
    dirs[:] = [d for d in dirs if d not in exclude_dirs]
    
    for file in files:
        if file.endswith((".js", ".ts", ".tsx", ".json", ".md", ".yml", ".yaml")):
            file_path = os.path.join(root, file)
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    for lib in vulnerable_libs:
                        # Simple string match first, then we can refine
                        if lib in content:
                            if lib not in found_mentions:
                                found_mentions[lib] = []
                            found_mentions[lib].append(file_path)
            except Exception:
                pass

for lib, files in found_mentions.items():
    print(f"Library '{lib}' mentioned in {len(files)} files.")
    # Filter for interesting files (not package.json, not yarn.lock, not changelogs)
    interesting = [f for f in files if not any(x in f for x in ["package.json", "yarn.lock", "CHANGELOG.md", "vulnerabilities.json"])]
    if interesting:
        print(f"  Interesting files ({len(interesting)}):")
        for f in interesting[:5]:
            print(f"    - {f}")
