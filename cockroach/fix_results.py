import json

with open('wyniki.json', 'r') as f:
    docs = json.load(f)

for d in docs:
    v = d['Vulnerability']
    l = d['Location'].lower()
    e = d['Exploitability_explanation']
    
    if 'WebSocket' in e:
        if 'ws' in l:
            # Correct for ws
            continue
        elif 'browserslist' in l:
            d['Exploitability_explanation'] = "ReDoS vulnerability in query parsing logic (e.g., version range matching). Browserslist queries in this codebase are typically static configurations in .browserslistrc or package.json and not constructed from untrusted user input, significantly limiting exploitability."
        else:
            d['Exploitability_explanation'] = "Vulnerability in dependency identified, but no explicit call path from User Code using untrusted input was found during analysis."

with open('wyniki.json', 'w') as f:
    json.dump(docs, f, indent=2)

print("Updated wyniki.json")
