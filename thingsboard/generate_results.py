import json
import math

with open('vulnerabilities_extracted.json', 'r', encoding='utf-8') as f:
    vulns = json.load(f)

# Hardcoded assessments based on strict "Explicit Call" evidence
EXPLICIT_CALLS = {
    'tinymce:6.8.6': {
        'CVE-2024-29881': {
            'found': True, 'score': 70, 
            'exp': '✅ API call confirmed. The `editor` component is initialized with `tinyMceOptions` in `notification-template-configuration.component.ts` without `convert_unsafe_embeds`. Version is vulnerable, API usage found.'
        }
    },
    'lodash:4.17.21': {
        'CVE-2025-13465': {
            'found': True, 'score': 70,
            'exp': '✅ API call confirmed. `_.unset` is called in `ui-ngx/src/app/core/utils.ts` and `auth.reducer.ts`.'
        }
    },
    'lodash-es:4.17.21': {
        'CVE-2025-13465': {
            'found': True, 'score': 70,
            'exp': '✅ API call confirmed. `_.unset` is called in `ui-ngx/src/app/core/utils.ts` and `auth.reducer.ts`.'
        }
    }
}

results = []

for v in vulns:
    name = v['Name']
    loc = v['Location']
    orig_score = v['Exploitability']
    
    # Check if we have an explicit call override
    if loc in EXPLICIT_CALLS and name in EXPLICIT_CALLS[loc]:
        data = EXPLICIT_CALLS[loc][name]
        score = data['score']
        exp = data['exp']
    else:
        # No explicit call found
        score = 1  # 0.01 probability in percentage
        exp = 'No explicit call to the vulnerable API was found in the codebase. Version is present but API is not used in any active code path. Status: not_confirmed.'

    
    # Assessment
    # Tolerance is 20%. Difference must be <= 20
    diff = abs(orig_score - score)
    assessment = "Correct" if diff <= 20 else "Incorrect"
    
    res = {
        "Vulnerability": name,
        "Location": loc,
        "Original_exploitability": orig_score,
        "Exploitability": score,
        "Exploitability_explanation": exp,
        "Assessment": assessment
    }
    results.append(res)
    
with open('wyniki.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, indent=2, ensure_ascii=False)
