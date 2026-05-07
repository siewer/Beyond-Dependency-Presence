import sys

def find_dependents(target_lib, lockfile):
    with open(lockfile, 'r') as f:
        lines = f.readlines()
    
    current_package = None
    dependents = {}
    
    for i, line in enumerate(lines):
        if line.strip() and not line.startswith(" "):
            current_package = line.strip().split("@")[0].replace('"', '')
        elif "dependencies:" in line:
            j = i + 1
            while j < len(lines) and lines[j].startswith("    "):
                dep_line = lines[j].strip()
                dep_name = dep_line.split(" ")[0].replace('"', '')
                if dep_name == target_lib:
                    if target_lib not in dependents:
                        dependents[target_lib] = []
                    dependents[target_lib].append(current_package)
                j += 1
    return dependents.get(target_lib, [])

lockfile = 'yarn.lock'
libs_to_check = ["ssri", "json-schema", "browserify-sign", "minimatch", "ip"]

for lib in libs_to_check:
    deps = find_dependents(lib, lockfile)
    print(f"Library '{lib}' is a dependency of: {list(set(deps))}")
