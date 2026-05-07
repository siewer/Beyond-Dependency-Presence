import json
import re

DEPENDENCIES_CHECKS = {
    'tinymce': ['tinymce', 'tinymce-angular'],
    'okio': ['okio'],
    '@messageformat/runtime': ['@messageformat/runtime', 'messageformat'],
    'minimatch': ['minimatch'],
    'immutable': ['immutable'],
    'hono': ['hono', '@hono/node-server'],
    'ajv': ['ajv'],
    'dompurify': ['dompurify'],
    'katex': ['katex'],
    'tar': ['tar'],
    'lodash': ['lodash', 'lodash-es'],
    'qs': ['qs'],
    'wire-runtime': ['wire-runtime'],
    'body-parser': ['body-parser'],
    'js-yaml': ['js-yaml'],
    'express-rate-limit': ['express-rate-limit'],
    'assertj-core': ['assertj-core'],
    'mermaid': ['mermaid'],
    'diff': ['diff'],
    'logback-core': ['logback-core', 'logback-classic'],
    'on-headers': ['on-headers'],
    'serialize-javascript': ['serialize-javascript']
}

def analyze():
    # Read package.json and pom.xml etc, but simpler to just search via regex in files
    # Actually, we can just python search all package.json and pom.xml
    import glob
    
    files_to_check = glob.glob('**/package.json', recursive=True) + glob.glob('**/pom.xml', recursive=True)
    
    results = {k: False for k in DEPENDENCIES_CHECKS}
    
    for file in files_to_check:
        if 'node_modules' in file:
            continue
        try:
            with open(file, 'r', encoding='utf-8') as f:
                content = f.read()
                for dep, aliases in DEPENDENCIES_CHECKS.items():
                    for alias in aliases:
                        if alias in content:
                            results[dep] = True
        except Exception as e:
            pass

    print(json.dumps(results, indent=2))

if __name__ == '__main__':
    analyze()
