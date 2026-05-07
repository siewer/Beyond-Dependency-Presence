import pandas as pd
import json

df = pd.read_csv('c:/Users/majab/OneDrive/Desktop/repo/axios/vulnerabilities.csv')

# Presence and Reachability mapping (verified in previous steps)
in_tree_dev = [
    "braces", "ajv", "http-cache-semantics", "qs", "micromatch", 
    "multer", "cross-spawn", "tar", "serialize-javascript"
]
in_tree_prod = ["form-data"]
missing = ["tough-cookie", "dicer", "got", "request", "semver-regex", "babel-traverse", "elliptic"]

# Deep Research mapping (exploitation conditions)
conditions = {
    "CVE-2024-4068": "Przekazanie nieprawidłowo zbalansowanych nawiasów klamrowych do funkcji `braces()` (ReDoS).",
    "CVE-2023-26136": "Użycie `CookieJar` z flagą `rejectPublicSuffixes=false` (Prototype Pollution).",
    "CVE-2022-24434": "Przesłanie złośliwie sformatowanego boundary w żądaniu multipart (DoS).",
    "CVE-2022-33987": "Przekierowanie żądania HTTP na lokalny UNIX socket (SSRF).",
    "CVE-2023-28155": "Obejście mitygacji SSRF poprzez przekierowanie międzyprotokołowe (SSRF).",
    "CVE-2021-3795": "Przetworzenie długiego, spreparowanego ciągu wersji przez `semverRegex()` (ReDoS).",
    "CVE-2020-15366": "Przekazanie złośliwego schematu JSON do `ajv.validate()` (Prototype Pollution).",
    "CVE-2025-7783": "Automatyczne generowanie boundaries przy użyciu Math.random() (Przewidywalne boundaries).",
    "CVE-2022-25881": "Przesłanie złośliwych nagłówków Cache-Control do sparsowania (ReDoS).",
    "CVE-2025-15284": "Użycie notacji klamrowej w parametrach zapytania (np. a[]=1) (DoS).",
    "CVE-2021-43307": "Przetworzenie złośliwego ciągu przez `semverRegex()` (ReDoS).",
    "CVE-2023-45133": "Kompilacja niezaufanego kodu z użyciem specyficznych pluginów Babel (ACE).",
    "CVE-2024-4067": "Użycie zachłannych wzorców w `micromatch.braces()` (ReDoS).",
    "CVE-2025-48997": "Wysłanie pliku z pustym ciągiem jako nazwą pola w multipart (DoS).",
    "CVE-2024-21538": "Przekazanie ogromnego ciągu do mitygacji regex w `cross-spawn` (ReDoS).",
    "CVE-2026-3520": "Wysłanie żądania multipart z ogromną liczbą małych części (DoS/Stack overflow).",
    "CVE-2026-2359": "Wysłanie żądania multipart z złośliwymi nazwami plików (DoS).",
    "CVE-2026-3304": "Wysłanie żądania multipart wyzwalającego niekontrolowaną rekurencję (DoS).",
    "CVE-2025-47935": "Wysłanie żądania multipart z pustą nazwą pola (DoS).",
    "CVE-2026-29786": "Rozpakowanie archiwum TAR z hardlinkami wskazującymi poza katalog (Path Traversal).",
    "CVE-2026-24842": "Rozpakowanie archiwum TAR z hardlinkami omijającymi walidację (Path Traversal).",
    "CVE-2025-7338": "Wysłanie pliku wyzwalającego błąd parsowania w Mulder (DoS).",
    "CVE-2026-26960": "Rozpakowanie archiwum TAR z drive-relative targets (Path Traversal).",
    "CVE-2025-47944": "Wysłanie żądania multipart z pustą nazwą pola (DoS).",
    "CVE-2026-23950": "Rozpakowanie archiwum TAR z hardlinkami (Path Traversal).",
    "CVE-2026-23745": "Rozpakowanie archiwum TAR z hardlinkami (Path Traversal).",
    "CVE-2026-31802": "Rozpakowanie archiwum TAR z hardlinkami (Path Traversal).",
    "CVE-2025-14505": "Generowanie podpisów ECDSA, gdy parametr 'k' ma wiodące zera (Crypto Fault).",
    "GHSA-5c6j-r48x-rmvq": "Serializacja złośliwych obiektów JavaScript (Prototype Pollution/DoS).",
    "CVE-2025-69873": "Przekazanie złośliwego schematu JSON do walidacji (Prototype Pollution/DoS)."
}

results = []

for _, row in df.iterrows():
    name = row['Name']
    loc = row['Location']
    orig = row['Exploitability']
    pkg = loc.split(':')[0]
    
    satisfied_count = 1 # Version always satisfied
    explanation = f"Warunek: {conditions.get(name, 'Brak szczegółowych danych o warunku.')} "
    
    if pkg in in_tree_prod:
         satisfied_count += 3 # Presence + Reachability + Usage
         explanation += f"Biblioteka `{pkg}` jest bezpośrednią zależnością produkcyjną Axios i jest używana w kodzie `lib/` do przetwarzania danych użytkownika."
    elif pkg in in_tree_dev:
         satisfied_count += 1 # Presence in repo
         explanation += f"Biblioteka `{pkg}` znajduje się w repozytorium jako zależność dev, ale nie jest używana w kodzie produkcyjnym `lib/` (brak reachability)."
    else:
         explanation += f"Biblioteka `{pkg}` nie została znaleziona w aktualnym drzewie zależności Axios."
         
    # Scoring Levels (25% satisfied = 15.0, 50% satisfied = 35.0, 75% satisfied = 60.0, 100% satisfied = 77.5)
    score_map = {1: 15, 2: 35, 3: 60, 4: 77.5}
    recal = score_map.get(satisfied_count, 15)
    
    # Assess (20 absolute points tolerance)
    diff = abs(orig - recal)
    assessment = "Correct" if diff <= 20 else "Incorrect"
    
    results.append({
        "Vulnerability": name,
        "Location": loc,
        "Original_exploitability": orig,
        "Exploitability": recal,
        "Exploitability_explanation": explanation.strip(),
        "Assessment": assessment
    })

with open('c:/Users/majab/OneDrive/Desktop/repo/axios/wyniki.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

print(f"Generated {len(results)} refined entries.")
