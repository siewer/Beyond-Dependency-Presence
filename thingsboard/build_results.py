import json

def process():
    with open('vulnerabilities_extracted.json', 'r', encoding='utf-8') as f:
        vulns = json.load(f)
    
    # We will build results here
    
    with open('wyniki.json', 'w', encoding='utf-8') as f:
        json.dump([], f, indent=2)

if __name__ == '__main__':
    process()
