import os
import json

patterns = ['minimatch', 'ajv', 'flatted', 'serialize-javascript', 'form-data', 'vite', 'esbuild']
results = {p: [] for p in patterns}

repo_path = r'c:\Users\majab\OneDrive\Desktop\repo\svelte'

for root, dirs, files in os.walk(repo_path):
    # Skip noisy directories
    if any(d in root for d in ['.git', 'node_modules', '.svelte-kit', 'dist', 'artifacts', 'brain']):
        continue
    
    for file in files:
        if file.endswith(('.js', '.ts', '.json', '.yaml', '.md')) and not file.endswith('.test.ts'):
            file_path = os.path.join(root, file)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    for p in patterns:
                        if p in content:
                            if len(results[p]) < 10:
                                results[p].append(file_path)
            except Exception as e:
                pass

print(json.dumps(results, indent=2))
