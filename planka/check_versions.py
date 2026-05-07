import json
import os

def get_version(path, pkg):
    if not os.path.exists(path):
        return "Not found"
    try:
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            # Check 'packages' (npm v7+)
            v = data.get('packages', {}).get('node_modules/' + pkg, {}).get('version')
            if not v:
                # Check 'dependencies' (npm v6 or legacy)
                v = data.get('dependencies', {}).get(pkg, {}).get('version')
            if not v:
                # Check for transitive dependencies in 'packages'
                for node_path, info in data.get('packages', {}).items():
                    if node_path.endswith('/node_modules/' + pkg):
                        return info.get('version')
            return v if v else "Not found"
    except Exception as e:
        return f"Error: {str(e)}"

libs = ['fast-xml-parser', 'flatted', 'underscore', 'diff', 'elliptic', 'serialize-javascript', 'markdown-it']
print("Library,Client Version,Server Version")
for lib in libs:
    cv = get_version('client/package-lock.json', lib)
    sv = get_version('server/package-lock.json', lib)
    print(f"{lib},{cv},{sv}")
