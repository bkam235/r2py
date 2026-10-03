---
id: downlit.href-topic
package: downlit
confidence: tentative
seed: true
created: 2026-09-22
last_review: 2026-09-22
tie_count: 0
---

# downlit.href-topic

## Guidance
Translate R `href_topic` (FunctionCall from downlit) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "7568a489", "r_snippet": "href_topic(\"t\")", "py_snippet": "def find_rdname(package, topic):\n    # Mocking the topic index lookup\n    # base: t -> t\n    # downlit: href_topic -> href_topic\n    if package == \"base\" and topic == \"t\":\n        return \"t\"\n    if package == \"downlit\" and topic == \"href_topic\":\n        return \"href_topic\"\n    return None\n\ndef href_package_ref(package):\n    # Mocking the URL resolution for specific packages\n    if package == \"downlit\":\n        return \"https://downlit.r-lib.org\"\n    return f\"https://rdrr.io/r/{package}\"\n\ndef href_package(package):\n    # Based on package_urls logic\n    if not is_installed(package):\n        return None\n    \n    if package == \"downlit\":\n        return \"https://downlit.r-lib.org/\"\n    \n    # Fallback for other installed packages\n    return f\"https://rdrr.io/package/{package}\"\n\ndef href_topic_remote(topic, package):\n    rdname = find_rdname(package, topic)\n    if rdname is None:\n        return None\n    \n    # R source: paste0(href_package_ref(package), \"/\", rdname, \".html\")\n    ref = href_package_ref(package)\n    return f\"{ref}/{rdname}.html\"\n\ndef href_topic(topic, package=None, is_fun=False):\n    if topic is None or (isinstance(topic, (list, pd.Series)) and len(topic) != 1):\n        return None\n    \n    # Simple approximation of is_package_local and find_rdname_attached\n    # If package is None, it checks attached packages including base\n    if package is None:\n        attached_packages = [\"downlit\", \"datasets\", \"utils\", \"grDevices\", \"graphics\", \"stats\", \"base\"]\n        for pkg in attached_packages:\n            rdname = find_rdname(pkg, topic)\n            if rdname:\n                return href_topic_remote(topic, pkg)\n        return None\n    else:\n        return href_topic_remote(topic, package)\n\n# Translate: suppressPackageStartupMessages(library(downlit))\n# No action needed for suppressPackageStartupMessages in Python\n\n# Translate: href_topic(\"t\")\n\nhref_topic_val = href_topic(\"t\")\nprint(f'[1] \"{href_topic_val}\"' if href_topic_val else '[1] NA')\n\n# ...", "score": 1.0, "script_id": "downlit__rd_example__href_topic_Rd", "n_calls": 0}

## Edit Examples
(none)
