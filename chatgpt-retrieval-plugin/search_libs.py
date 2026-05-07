import os
import re

libs = ['langchain', 'aiohttp', 'urllib3', 'requests', 'authlib', 'marshmallow', 'filelock', 'wheel', 'cryptography', 'ujson', 'protobuf', 'tqdm', 'pyjwt', 'llama-index']

lock_found = {}
codebase_found = {}

if os.path.exists('poetry.lock'):
    with open('poetry.lock', 'r', encoding='utf-8') as f:
        lock_content = f.read()
        for lib in libs:
            if f'name = "{lib}"' in lock_content:
                # search for version
                pattern = f'name = "{lib}"\nversion = "([^"]+)"'
                match = re.search(pattern, lock_content)
                if match:
                    lock_found[lib] = match.group(1)
                else:
                    lock_found[lib] = "found"

for root, dirs, files in os.walk('.'):
    for file in files:
        if file.endswith('.py'):
            try:
                with open(os.path.join(root, file), 'r', encoding='utf-8') as f:
                    content = f.read()
                    for lib in libs:
                        search_lib = lib.replace('-', '_')
                        if lib in content or search_lib in content:
                            if lib not in codebase_found:
                                codebase_found[lib] = []
                            codebase_found[lib].append(os.path.join(root, file))
            except:
                pass

print("LOCK_FOUND:", lock_found)
print("CODEBASE_FOUND:")
for lib, files in codebase_found.items():
    print(f"  {lib}: {list(set(files))[:5]} (total {len(files)})")
