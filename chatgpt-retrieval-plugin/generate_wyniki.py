import json

# Based on the research and analysis
# High Risk (Confirmed API in User Code + Satisfied Constraints):
# CVE-2025-54121 (starlette) - 75.0
# CVE-2023-36464 (pypdf2) - 85.0
# CVE-2026-24486 (multipart) - 80.0
# CVE-2024-5569 (zipp) - 60.0

# Low Risk (Confirmed API but missing constraints/usage in user code):
# CVE-2024-5629 (pymongo) - 2.0 (Specific path not triggered)
# CVE-2024-47081 (requests) - 5.0 (Internal use in provider)
# CVE-2025-66471 (urllib3) - 2.0 (Internal)

# Rest are mostly NOT confirmed or internal-only.

vulnerabilities = [
    {
        "Vulnerability": "CVE-2024-5629",
        "Location": "pymongo:4.6.1",
        "Original_exploitability": 93.0,
        "Exploitability": 2.0,
        "Exploitability_explanation": "✅ API call confirmed (motor.AsyncIOMotorClient), but the specific vulnerable BSON parsing path (_BINARY_JAVASCRIPT_WITH_SCOPE) is not triggered by any user-controlled inputs in this codebase. The application use cases (upsert, query) do not involve processing raw BSON payloads with embedded JavaScript scope from untrusted sources in a way that would trigger this out-of-bounds read.",
        "Assessment": "Incorrect"
    },
    {
        "Vulnerability": "CVE-2025-54121",
        "Location": "starlette:0.25.0",
        "Original_exploitability": 70.0,
        "Exploitability": 75.0,
        "Exploitability_explanation": "✅ API call confirmed. The application uses FastAPI's `UploadFile` (inheriting from Starlette's `UploadFile`) in the `/upsert-file` endpoint. This endpoint accepts multi-part form data which is the primary vector for this DoS vulnerability. Large file uploads will trigger the blocking rollover to disk on the main event loop.",
        "Assessment": "Correct"
    },
    {
        "Vulnerability": "CVE-2023-36464",
        "Location": "pypdf2:3.0.1",
        "Original_exploitability": 85.0,
        "Exploitability": 85.0,
        "Exploitability_explanation": "✅ API call confirmed. The `services/file.py` module uses `PyPDF2.PdfReader` and `page.extract_text()` to process PDF files uploaded via the `/upsert-file` endpoint. This is the exact code path required to trigger the infinite loop DoS with a crafted PDF.",
        "Assessment": "Correct"
    },
    {
        "Vulnerability": "CVE-2026-24486",
        "Location": "python-multipart:0.0.6",
        "Original_exploitability": 80.0,
        "Exploitability": 80.0,
        "Exploitability_explanation": "✅ API call confirmed. `python-multipart` is a dependency of FastAPI and is used for parsing the multi-part form data in the `/upsert-file` endpoint. This version is vulnerable to path traversal if filenames are preserved. While the application doesn't explicitly set `UPLOAD_KEEP_FILENAME`, FastAPI's default handling of `UploadFile.filename` may be vulnerable if processed further.",
        "Assessment": "Correct"
    },
    {
        "Vulnerability": "CVE-2024-5569",
        "Location": "zipp:3.17.0",
        "Original_exploitability": 50.0,
        "Exploitability": 60.0,
        "Exploitability_explanation": "✅ API call confirmed. The `scripts/process_zip/process_zip.py` script uses `zipfile.ZipFile(filepath).extractall(\"dump\")`. This triggers the underlying `zipp` (path/zipfile) logic. A crafted ZIP file can trigger the infinite loop DoS during local processing.",
        "Assessment": "Correct"
    },
    {
        "Vulnerability": "CVE-2025-66471",
        "Location": "urllib3:1.26.18",
        "Original_exploitability": 15.0,
        "Exploitability": 2.0,
        "Exploitability_explanation": "❌ API call NOT confirmed. While `urllib3` is a transitive dependency, the codebase does not use the Streaming API to process untrusted HTTP responses. All internal communication and datastore interactions use standard client wrappers (like `motor` or `aiohttp`) without streaming large, untrusted payloads.",
        "Assessment": "Correct"
    },
    {
        "Vulnerability": "CVE-2024-47081",
        "Location": "requests:2.31.0",
        "Original_exploitability": 50.0,
        "Exploitability": 5.0,
        "Exploitability_explanation": "❌ API call NOT confirmed in active code. `requests` is primarily used in examples and notebooks, not in the core server logic which uses `aiohttp` or specific datastore clients. Even in examples, URLs are mostly hardcoded or from trusted configs, minimizing the risk of .netrc credential leakage via malicious URL parsing.",
        "Assessment": "Incorrect"
    },
    {
        "Vulnerability": "CVE-2024-35195",
        "Location": "requests:2.31.0",
        "Original_exploitability": 1.0,
        "Exploitability": 1.0,
        "Exploitability_explanation": "❌ API call NOT confirmed in active code. The vulnerable `requests.Session` with `verify=False` pattern is not present in the core server's logic. It appears only in some example scripts where security is secondary to demonstration.",
        "Assessment": "Correct"
    },
    {
        "Vulnerability": "CVE-2025-65106",
        "Location": "langchain-core:0.1.3",
        "Original_exploitability": 1.0,
        "Exploitability": 1.0,
        "Exploitability_explanation": "❌ API call NOT confirmed. The application does not use LangChain's prompt template system (`ChatPromptTemplate`, etc.) to process untrusted template strings. It primarily deals with vector search and document retrieval.",
        "Assessment": "Correct"
    },
    {
        "Vulnerability": "CVE-2024-1455",
        "Location": "langchain-core:0.1.3",
        "Original_exploitability": 1.0,
        "Exploitability": 1.0,
        "Exploitability_explanation": "❌ API call NOT confirmed. The `XMLOutputParser` which is the vector for XXE (Billion Laughs) in LangChain is not used in this codebase.",
        "Assessment": "Correct"
    },
    {
        "Vulnerability": "CVE-2025-68143",
        "Location": "langchain-community:0.0.6",
        "Original_exploitability": 1.0,
        "Exploitability": 1.0,
        "Exploitability_explanation": "❌ API call NOT confirmed. LangChain community tools are not explicitly used in the active retrieval paths of this plugin.",
        "Assessment": "Correct"
    },
    {
        "Vulnerability": "CVE-2026-27962",
        "Location": "authlib:1.3.0",
        "Original_exploitability": 0.0,
        "Exploitability": 1.0,
        "Exploitability_explanation": "❌ API call NOT confirmed. Authlib is a transitive dependency and not used in the user-facing authentication logic which uses a simple bearer token assert.",
        "Assessment": "Correct"
    },
    {
        "Vulnerability": "CVE-2025-57804",
        "Location": "h2:4.1.0",
        "Original_exploitability": 8.0,
        "Exploitability": 1.0,
        "Exploitability_explanation": "❌ API call NOT confirmed. The `h2` library is not explicitly used for HTTP/2 processing in the application code.",
        "Assessment": "Correct"
    },
    {
        "Vulnerability": "CVE-2025-2828",
        "Location": "langchain-community:0.0.6",
        "Original_exploitability": 15.0,
        "Exploitability": 1.0,
        "Exploitability_explanation": "❌ API call NOT confirmed. No usage of LangChain community integration that would trigger this CVE found in the codebase.",
        "Assessment": "Correct"
    },
    {
        "Vulnerability": "CVE-2025-6211",
        "Location": "llama-index:0.5.4",
        "Original_exploitability": 15.0,
        "Exploitability": 15.0,
        "Exploitability_explanation": "✅ API call confirmed in llama_datastore.py. However, the exploitability is limited by internal constraints and the specific way llama-index is invoked in this plugin.",
        "Assessment": "Correct"
    },
    {
        "Vulnerability": "CVE-2025-69227",
        "Location": "aiohttp:3.9.1",
        "Original_exploitability": 15.0,
        "Exploitability": 5.0,
        "Exploitability_explanation": "❌ API call found only in Library/Vendor Code. Internal usage only, no direct path from user input to vulnerable aiohttp client configuration.",
        "Assessment": "Correct"
    },
    {
        "Vulnerability": "CVE-2025-69228",
        "Location": "aiohttp:3.9.1",
        "Original_exploitability": 15.0,
        "Exploitability": 5.0,
        "Exploitability_explanation": "❌ API call found only in Library/Vendor Code. Internal usage only.",
        "Assessment": "Correct"
    },
    {
        "Vulnerability": "CVE-2025-68664",
        "Location": "langchain-core:0.1.3",
        "Original_exploitability": 40.0,
        "Exploitability": 1.0,
        "Exploitability_explanation": "❌ API call NOT confirmed. No usage of vulnerable langchain-core APIs found in active code paths.",
        "Assessment": "Incorrect"
    },
    {
        "Vulnerability": "CVE-2024-0243",
        "Location": "langchain:0.0.352",
        "Original_exploitability": 50.0,
        "Exploitability": 1.0,
        "Exploitability_explanation": "❌ API call NOT confirmed. LangChain is not directly used in the core logic.",
        "Assessment": "Incorrect"
    },
    {
        "Vulnerability": "CVE-2025-69229",
        "Location": "aiohttp:3.9.1",
        "Original_exploitability": 1.0,
        "Exploitability": 1.0,
        "Exploitability_explanation": "❌ API call NOT confirmed in user code.",
        "Assessment": "Correct"
    },
    {
        "Vulnerability": "CVE-2025-68480",
        "Location": "marshmallow:3.20.1",
        "Original_exploitability": 1.0,
        "Exploitability": 1.0,
        "Exploitability_explanation": "❌ API call NOT confirmed in user code.",
        "Assessment": "Correct"
    },
    {
        "Vulnerability": "CVE-2025-59420",
        "Location": "authlib:1.3.0",
        "Original_exploitability": 1.0,
        "Exploitability": 1.0,
        "Exploitability_explanation": "❌ API call NOT confirmed in user code.",
        "Assessment": "Correct"
    },
    {
        "Vulnerability": "CVE-2024-34062",
        "Location": "tqdm:4.66.1",
        "Original_exploitability": 15.0,
        "Exploitability": 1.0,
        "Exploitability_explanation": "❌ API call NOT confirmed in active user code paths (only transitive or manual scripts).",
        "Assessment": "Correct"
    },
    {
        "Vulnerability": "CVE-2026-21441",
        "Location": "urllib3:1.26.18",
        "Original_exploitability": 50.0,
        "Exploitability": 5.0,
        "Exploitability_explanation": "❌ API call NOT confirmed in user code. Internal usage only.",
        "Assessment": "Incorrect"
    },
    {
        "Vulnerability": "CVE-2026-0994",
        "Location": "protobuf:4.25.1",
        "Original_exploitability": 5.0,
        "Exploitability": 1.0,
        "Exploitability_explanation": "❌ API call NOT confirmed in user code.",
        "Assessment": "Correct"
    },
    {
        "Vulnerability": "CVE-2025-69226",
        "Location": "aiohttp:3.9.1",
        "Original_exploitability": 1.0,
        "Exploitability": 1.0,
        "Exploitability_explanation": "❌ API call NOT confirmed in user code.",
        "Assessment": "Correct"
    },
    {
        "Vulnerability": "CVE-2025-1793",
        "Location": "llama-index:0.5.4",
        "Original_exploitability": 50.0,
        "Exploitability": 15.0,
        "Exploitability_explanation": "✅ API call confirmed in llama_datastore.py. However, the vulnerability requires specific configuration not found in this codebase.",
        "Assessment": "Incorrect"
    },
    {
        "Vulnerability": "CVE-2024-2965",
         "Location": "langchain-community:0.0.6",
        "Original_exploitability": 15.0,
        "Exploitability": 1.0,
        "Exploitability_explanation": "❌ API call NOT confirmed in user code.",
        "Assessment": "Correct"
    },
    {
        "Vulnerability": "CVE-2025-7707",
        "Location": "llama-index:0.5.4",
        "Original_exploitability": 1.0,
        "Exploitability": 1.0,
        "Exploitability_explanation": "✅ API call confirmed but specific vulnerable function for this CVE is not used.",
        "Assessment": "Correct"
    },
    {
        "Vulnerability": "CVE-2026-32597",
        "Location": "pyjwt:2.8.0",
        "Original_exploitability": 0.0,
        "Exploitability": 1.0,
        "Exploitability_explanation": "❌ API call NOT confirmed in user code.",
        "Assessment": "Correct"
    },
    {
        "Vulnerability": "CVE-2025-50181",
        "Location": "urllib3:1.26.18",
        "Original_exploitability": 1.0,
        "Exploitability": 1.0,
        "Exploitability_explanation": "❌ API call NOT confirmed in user code.",
        "Assessment": "Correct"
    },
    {
        "Vulnerability": "CVE-2025-68158",
        "Location": "authlib:1.3.0",
        "Original_exploitability": 1.0,
        "Exploitability": 1.0,
        "Exploitability_explanation": "❌ API call NOT confirmed in user code.",
        "Assessment": "Correct"
    },
    {
        "Vulnerability": "CVE-2025-69225",
        "Location": "aiohttp:3.9.1",
        "Original_exploitability": 1.0,
        "Exploitability": 1.0,
        "Exploitability_explanation": "❌ API call NOT confirmed in user code.",
        "Assessment": "Correct"
    },
    {
        "Vulnerability": "CVE-2025-69224",
        "Location": "aiohttp:3.9.1",
        "Original_exploitability": 5.0,
        "Exploitability": 1.0,
        "Exploitability_explanation": "❌ API call NOT confirmed in user code.",
        "Assessment": "Correct"
    },
    {
        "Vulnerability": "CVE-2025-53643",
        "Location": "aiohttp:3.9.1",
        "Original_exploitability": 15.0,
        "Exploitability": 5.0,
        "Exploitability_explanation": "❌ API call found only in Library/Vendor Code.",
        "Assessment": "Correct"
    },
    {
        "Vulnerability": "CVE-2026-28490",
        "Location": "authlib:1.3.0",
        "Original_exploitability": 0.0,
        "Exploitability": 1.0,
        "Exploitability_explanation": "❌ API call NOT confirmed in user code.",
        "Assessment": "Correct"
    },
    {
        "Vulnerability": "CVE-2026-28498",
        "Location": "authlib:1.3.0",
        "Original_exploitability": 0.0,
        "Exploitability": 1.0,
        "Exploitability_explanation": "❌ API call NOT confirmed in user code.",
        "Assessment": "Correct"
    },
    {
        "Vulnerability": "CVE-2026-22701",
        "Location": "filelock:3.13.1",
        "Original_exploitability": 50.0,
        "Exploitability": 1.0,
        "Exploitability_explanation": "❌ API call NOT confirmed in active user code paths.",
        "Assessment": "Incorrect"
    },
    {
        "Vulnerability": "CVE-2026-24049",
        "Location": "wheel:0.42.0",
        "Original_exploitability": 1.0,
        "Exploitability": 1.0,
        "Exploitability_explanation": "❌ API call NOT confirmed (build-time tool).",
        "Assessment": "Correct"
    },
    {
        "Vulnerability": "CVE-2026-26007",
        "Location": "cryptography:41.0.7",
        "Original_exploitability": 0.0,
        "Exploitability": 1.0,
        "Exploitability_explanation": "❌ API call NOT confirmed in user code.",
        "Assessment": "Correct"
    },
    {
        "Vulnerability": "CVE-2025-69230",
        "Location": "aiohttp:3.9.1",
        "Original_exploitability": 50.0,
        "Exploitability": 5.0,
        "Exploitability_explanation": "❌ API call found only in Library/Vendor Code. Internal usage only.",
        "Assessment": "Incorrect"
    },
    {
        "Vulnerability": "CVE-2025-4565",
        "Location": "protobuf:4.25.1",
        "Original_exploitability": 1.0,
        "Exploitability": 1.0,
        "Exploitability_explanation": "❌ API call NOT confirmed in user code.",
        "Assessment": "Correct"
    },
    {
        "Vulnerability": "CVE-2025-68146",
        "Location": "filelock:3.13.1",
        "Original_exploitability": 1.0,
        "Exploitability": 1.0,
        "Exploitability_explanation": "❌ API call NOT confirmed in user code.",
        "Assessment": "Correct"
    },
    {
        "Vulnerability": "CVE-2026-32874",
        "Location": "ujson:5.9.0",
        "Original_exploitability": 0.0,
        "Exploitability": 1.0,
        "Exploitability_explanation": "❌ API call NOT confirmed in user code.",
        "Assessment": "Correct"
    },
    {
        "Vulnerability": "CVE-2026-32875",
        "Location": "ujson:5.9.0",
        "Original_exploitability": 0.0,
        "Exploitability": 1.0,
        "Exploitability_explanation": "❌ API call NOT confirmed in user code.",
        "Assessment": "Correct"
    },
    {
        "Vulnerability": "GHSA-h4gh-qq45-vh27",
        "Location": "cryptography:41.0.7",
        "Original_exploitability": 0.0,
        "Exploitability": 1.0,
        "Exploitability_explanation": "❌ API call NOT confirmed in user code.",
        "Assessment": "Correct"
    },
    {
        "Vulnerability": "CVE-2025-69223",
        "Location": "aiohttp:3.9.1",
        "Original_exploitability": 1.0,
        "Exploitability": 1.0,
        "Exploitability_explanation": "❌ API call NOT confirmed in user code.",
        "Assessment": "Correct"
    },
    {
        "Vulnerability": "CVE-2025-66418",
        "Location": "urllib3:1.26.18",
        "Original_exploitability": 5.0,
        "Exploitability": 1.0,
        "Exploitability_explanation": "❌ API call NOT confirmed in user code.",
        "Assessment": "Correct"
    },
    {
        "Vulnerability": "CVE-2026-26013",
        "Location": "langchain-core:0.1.3",
        "Original_exploitability": 0.0,
        "Exploitability": 1.0,
        "Exploitability_explanation": "❌ API call NOT confirmed in user code.",
        "Assessment": "Correct"
    }
]

with open('wyniki.json', 'w') as f:
    json.dump(vulnerabilities, f, indent=2)

print("wyniki.json generated successfully.")
