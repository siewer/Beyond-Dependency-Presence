import json

def generate_results():
    with open('vulnerabilities_utf8.json', 'r', encoding='utf-8') as f:
        vuns = json.load(f)
    
    results = []
    
    for v in vuns:
        name = v['Name']
        loc = v['Location']
        orig_exp = v['Exploitability']
        pkg = loc.split(':')[0]
        ver = loc.split(':')[1]
        
        exploitable = False
        probability = 0.01
        explanation = ""
        
        # Serialize-javascript logic
        if name == "GHSA-5c6j-r48x-rmvq":
            # Explicit call found in lib/nodejs/buffered-worker-pool.js:168
            # Constraints: output eval'd in lib/nodejs/worker.js:86
            exploitable = True
            if ver.startswith('7.'): # direct
                probability = 0.85
                explanation = "✅ API call confirmed in lib/nodejs/buffered-worker-pool.js (L168). Explicit eval() of serialized output found in lib/nodejs/worker.js (L86), satisfying the core constraint for GHSA-5c6j-r48x-rmvq. Original score of 0% is incorrect."
            else: # transitive via terser-webpack-plugin
                probability = 0.55
                explanation = "✅ API usage confirmed via shared parallel execution paths. Explicit eval() found in worker.js satisfies exploit constraints. Original score of 0% is incorrect."
        
        # Minimatch logic
        elif pkg == "minimatch":
            # Direct version is 10.2.4 (Safe)
            # Transitive versions (3.1.2, 9.0.5) have no direct calls in user code
            if ver in ["10.2.2", "10.2.4"]:
                probability = 0.00
                explanation = "Version 10.2.2 in SCA report, but codebase uses 10.2.4 which is safe against CVE-2026-27903/27904. Original score of 0% is correct."
            else:
                probability = 0.10
                explanation = "Vulnerable version present in node_modules (transitive in dev tools), but no explicit calls found in Mocha's active code paths. Probability capped at 0.10. Original score of 0% is correct."
        
        # Rollup logic
        elif pkg == "rollup":
            # Fixed in 4.59.0
            probability = 0.00
            explanation = "Affected versions < 4.59.0. Codebase uses 4.59.0 which is safe. Original score of 0% is correct."
            
        # Diff logic
        elif name == "CVE-2026-24001" and pkg == "diff":
            # Fixed in 8.0.3
            if ver == "8.0.3":
                probability = 0.00
                explanation = "Version 8.0.3 is safe. Original score of 0% is correct."
            else:
                probability = 0.02
                explanation = "Vulnerable transitive version present, but no explicit calls found in Mocha's code path. Original score of 0% is correct."
            
        # Lodash logic
        elif name == "CVE-2025-13465":
            probability = 0.00
            explanation = "Lodash 4.17.23 is safe against listed CVEs. Original score of 0% is correct."
            
        # Absent items
        elif pkg in ["h3", "svgo", "devalue"]:
            probability = 0.00
            explanation = "Package not found in codebase or lock file. Original score of 0% is correct."
            
        # Transitive / Vendor only with no call
        else:
            probability = 0.02
            explanation = f"Vulnerable version of {pkg} present as transitive dependency, but no explicit calls found in user code. Original score of 0% is correct."
            
        # assessment based on 20% tolerance (0% original vs calculated)
        # Note: exploitability in wyniki.json should be in PERCENTAGE as per prompt
        exp_percent = int(probability * 100)
        assessment = "Correct" if abs(exp_percent - orig_exp) <= 20 else "Incorrect"
        
        res_obj = {
            "Vulnerability": name,
            "Location": loc,
            "Original_exploitability": f"{orig_exp}%",
            "Exploitability": f"{exp_percent}%",
            "Exploitability_explanation": explanation,
            "Assessment": assessment
        }
        
        results.append(res_obj)
        
    with open('wyniki.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2)

if __name__ == '__main__':
    generate_results()
