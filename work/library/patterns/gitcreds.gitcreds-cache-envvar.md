---
id: gitcreds.gitcreds-cache-envvar
package: gitcreds
confidence: tentative
seed: true
created: 2026-09-06
last_review: 2026-09-06
tie_count: 0
---

# gitcreds.gitcreds-cache-envvar

## Guidance
Translate R `gitcreds_cache_envvar` (FunctionCall from gitcreds) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "20fef4a7", "r_snippet": "gitcreds_cache_envvar(\"https://github.com\")", "py_snippet": "def gitcreds_cache_envvar(url):\n    parsed = urlparse(url)\n    protocol = parsed.scheme\n    host = parsed.hostname\n    username = parsed.username if parsed.username else \"\"\n\n    if not protocol or not host:\n        raise ValueError(f\"Invalid URL(s): {url}\")\n\n    # proto <- sub(\"^https?_$\", \"\", paste0(pcs$protocol, \"_\"))\n    proto_val = f\"{protocol}_\"\n    proto_val = re.sub(r\"^https?_$\", \"\", proto_val)\n\n    # user <- ifelse(pcs$username != \"\", paste0(pcs$username, \"_AT_\"), \"\")\n    user_val = f\"{username}_AT_\" if username != \"\" else \"\"\n\n    # host0 <- sub(\"^api[.]github[.]com$\", \"github.com\", pc", "score": 1.0, "script_id": "auto"}

## Edit Examples
(none)
