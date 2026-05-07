import os
import re
import json

# Directory to search
search_dir = r"c:\Users\majab\OneDrive\Desktop\repo\atrilabs-engine\packages"

# Library signatures (regex)
signatures = {
    "json5": [r"json5\s*\.\s*parse", r"json5\s*\.\s*stringify"],
    "rollup": [r"rollup", r"watch"],
    "semver": [r"semver\s*\.\s*(parse|valid|clean|satisfies|gt|lt|major)"],
    "tar": [r"tar\s*\.\s*(x|u|c|list|extract|Pack|Parse)"],
    "braces": [r"braces\s*\(", r"braces\s*\.\s*expand"],
    "micromatch": [r"micromatch\s*\(", r"micromatch\s*\.\s*(isMatch|match)"],
    "ajv": [r"new\s+ajv", r"ajv\s*\(", r"\.\s*validate\s*\(", r"\.\s*compile\s*\("],
    "lodash": [r"\.\s*set\s*\(", r"\.\s*merge\s*\(", r"\.\s*defaultsDeep\s*\(", r"_\s*\.\s*(set|merge|defaultsDeep)\s*\("],
    "axios": [r"axios\s*\.\s*(get|post|put|delete|request)", r"axios\s*\("],
    "express": [r"express\s*\(", r"Router\s*\(", r"\.\s*static\s*\(", r"res\s*\.\s*send[Ff]ile"],
    "socket.io": [r"new\s+SocketServer", r"socket\s*\.\s*on\s*\(", r"io\s*\.\s*on\s*\("],
    "tinymce": [r"@tinymce/tinymce-react", r"Editor"],
    "word-wrap": [r"wordwrap\s*\(", r"word-wrap"],
    "parse-url": [r"parseUrl\s*\(", r"parse-url"],
    "http-proxy-middleware": [r"createProxyMiddleware"],
    "body-parser": [r"bodyParser\s*\.\s*(json|urlencoded)"],
    "serve-static": [r"serveStatic", r"express\s*\.\s*static"],
    "send": [r"res\s*\.\s*send[Ff]ile", r"send\s*\("],
    "qs": [r"qs\s*\.\s*(parse|stringify)"],
    "file-type": [r"fileTypeFrom(File|Buffer)", r"from(File|Buffer)"],
    "on-headers": [r"onHeaders\s*\("],
    "node-forge": [r"forge\s*\.\s*(util|pki|md)"],
    "brace-expansion": [r"brace-expansion\s*\("],
    "path-to-regexp": [r"pathToRegexp", r"path-to-regexp"],
    "svgo": [r"optimize\s*\(", r"new\s+SVGO"],
    "diff": [r"diff(Lines|Chars|Strings)"],
    "cookie": [r"cookie\s*\.\s*(parse|serialize)"],
    "ws": [r"new\s+WebSocket", r"new\s+ws\s*\.\s*Server"],
    "postcss": [r"postcss\s*\(\s*\["],
    "js-yaml": [r"yaml\s*\.\s*(load|safeLoad)"],
    "ip": [r"ip\s*\.\s*(address|isV4Format|isV6Format|cidrSubnet)"],
    "webpack": [r"webpack\s*\("]
}

found_usage = {lib: False for lib in signatures}
evidence = {lib: [] for lib in signatures}

for root, dirs, files in os.walk(search_dir):
    if "node_modules" in dirs:
        dirs.remove("node_modules")
    for file in files:
        if file.endswith((".ts", ".tsx", ".js", ".jsx", ".json")):
            path = os.path.join(root, file)
            try:
                with open(path, "r", encoding="utf-8") as f:
                    content = f.read()
                    for lib, sigs in signatures.items():
                        for sig in sigs:
                            if re.search(sig, content):
                                found_usage[lib] = True
                                evidence[lib].append(f"{path}: matched {sig}")
                                break
            except:
                pass

print("Search Complete")
for lib, found in found_usage.items():
    if found:
        print(f"CONFIRMED: {lib}")
    else:
        print(f"NOT_CONFIRMED: {lib}")

with open(r"c:\Users\majab\OneDrive\Desktop\repo\atrilabs-engine\research_results.json", "w") as f:
    json.dump({"found_usage": found_usage, "evidence": evidence}, f)
