---
id: httpuv.ipfamily
package: httpuv
confidence: tentative
seed: true
created: 2026-09-06
last_review: 2026-09-06
tie_count: 0
---

# httpuv.ipfamily

## Guidance
Translate R `ipFamily` (FunctionCall from httpuv) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "0b78f620", "r_snippet": "ipFamily(\"127.0.0.1\")   # 4", "py_snippet": "def ip_family(ip_string):\n    try:\n        addr = ipaddress.ip_address(ip_string)\n        if addr.version == 4:\n            return 4\n        elif addr.version == 6:\n            return 6\n    except ValueError:\n        return -1\n\nprint(ip_family(\"127.0.0.1\"))                # 4", "score": 1.0, "script_id": "auto"}

## Edit Examples
(none)
