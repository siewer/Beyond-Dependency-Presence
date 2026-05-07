import pandas as pd
import json

# Ensure we have the CSV (re-read it if necessary)
# I'll just hardcode the logic for the update based on the previous structure.
df = pd.read_csv('vulnerabilities.csv')

def get_new_exploitability(row):
    name = row['Name']
    loc = row['Location']
    orig = row['Exploitability']
    
    # Common patterns
    if 'jackson-databind' in loc:
        # User requested 5 instead of 2 for these cases where API is not used
        return 5, "Vulnerable API enableDefaultTyping() is not used in the codebase."
        
    if 'spring-beans' in loc or 'spring-webmvc' in loc or 'spring-web' in loc:
        if name == 'CVE-2022-22965': # Spring4Shell
            return 5, "Java version is 1.8, while Spring4Shell requires JDK 9+."
        if name == 'CVE-2018-1271' or name == 'CVE-2024-38819': # Path Traversal
            return 85, "Confirmed active resource handler configuration in WebMvcConfig.java."
        if name == 'CVE-2024-22259' or name == 'CVE-2024-22243': # UriComponentsBuilder
            return 15, "UriComponentsBuilder used in RedirectController, but with hardcoded/controlled paths."
        if name == 'CVE-2018-15756': # DoS Range
            return 85, "Resource handlers are active, providing a vector for Range header DoS."
            
    if 'spring-security' in loc:
        # App only uses CsrfFilter. User requested 5 instead of 2.
        return 5, "Application only uses CsrfFilter, not the full Spring Security stack or vulnerable matchers."
        
    if 'hibernate-validator' in loc:
        return 45, "Validation is active in controllers via @Valid, satisfying main constraints."
        
    if 'commons-fileupload' in loc:
        return 85, "FileUploadController uses MultipartFile and CommonsMultipartResolver is configured."
        
    if 'commons-io' in loc:
        return 5, "Vulnerable functions (e.g. FileNameUtils.normalize) are not used in user code."

    # Default if no specific logic
    return orig, "Original assessment retained pending specific evidence."

results = []
for idx, row in df.iterrows():
    new_exp, explanation = get_new_exploitability(row)
    # Tolerance is 20%
    assessment = "Correct" if abs(new_exp - row['Exploitability']) <= 20 else "Incorrect"
    results.append({
        "Vulnerability": row['Name'],
        "Location": row['Location'],
        "Original_exploitability": row['Exploitability'],
        "Exploitability": new_exp,
        "Exploitability_explanation": explanation,
        "Assessment": assessment
    })

with open('wyniki.json', 'w') as f:
    json.dump(results, f, indent=2)
f.close()
print("Results generated.")
