import json

with open('wyniki.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

lines = ['Oto szczegółowa analiza krok po kroku wszystkich 141 podatności:']
correct = 0
incorrect = 0

for i, x in enumerate(data, 1):
    lib = x['Location'].split(':')[0]
    vuln = x['Vulnerability']
    orig = x['Original_exploitability']
    exp = x['Exploitability']
    ass = x['Assessment']
    
    if ass == 'Correct': 
        correct += 1
    else: 
        incorrect += 1
        
    diff = abs(int(orig.strip('%')) - int(exp.strip('%')))
    lines.append(f"{i}. **{vuln} ({lib})**: Oryginalnie {orig} -> Moja ocena: {exp}. Różnica: {diff}% => {ass}")

lines.append('\n### Podsumowanie:')
lines.append(f'- Oceny poprawne (Correct): {correct}')
lines.append(f'- Oceny błędne (Incorrect): {incorrect}')
lines.append(f'- Razem: {len(data)}')

with open('summary.md', 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines))
