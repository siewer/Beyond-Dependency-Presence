import json

def find_runtime_dependencies(package_lock):
    packages = package_lock.get("packages", {})
    runtime_packages = {}
    
    # Start with direct dependencies from the root package
    root_deps = packages.get("", {}).get("dependencies", {})
    
    queue = list(root_deps.keys())
    visited = set()
    
    while queue:
        dep_name = queue.pop(0)
        if dep_name in visited:
            continue
        visited.add(dep_name)
        
        # Find the package in node_modules
        pkg_path = f"node_modules/{dep_name}"
        pkg_info = packages.get(pkg_path)
        
        if pkg_info:
            runtime_packages[dep_name] = pkg_info.get("version")
            # Add its dependencies
            deps = pkg_info.get("dependencies", {})
            for d in deps:
                if d not in visited:
                    queue.append(d)
        else:
            # Try to find it without node_modules/ prefix if it's nested (though lockfile v3 uses full paths)
            pass
            
    return runtime_packages

with open("package-lock.json", "r") as f:
    lock_data = json.load(f)

runtime_deps = find_runtime_dependencies(lock_data)
print(json.dumps(runtime_deps, indent=2))

# Now check if any of the vulnerable libraries are in runtime_deps or their versions match
vulnerable_libs = ["minimatch", "flatted", "glob", "ajv", "brace-expansion"]
found_vulnerable = {lib: [] for lib in vulnerable_libs}

for pkg_path, pkg_info in lock_data.get("packages", {}).items():
    if pkg_path == "": continue
    name = pkg_path.split("/")[-1]
    if name in vulnerable_libs:
        is_dev = pkg_info.get("dev", False)
        found_vulnerable[name].append({
            "path": pkg_path,
            "version": pkg_info.get("version"),
            "is_dev": is_dev
        })

print("\nVulnerable Libraries in Lockfile:")
print(json.dumps(found_vulnerable, indent=2))
