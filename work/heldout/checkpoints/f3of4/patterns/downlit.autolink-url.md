---
id: downlit.autolink-url
package: downlit
confidence: tentative
seed: true
created: 2026-09-22
last_review: 2026-09-22
tie_count: 0
---

# downlit.autolink-url

## Guidance
Translate R `autolink_url` (FunctionCall from downlit) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "b05d496d", "r_snippet": "autolink_url(\"stats::median()\")", "py_snippet": "def href_topic_remote(topic, package=None):\n    # Based on verification: https://rdrr.io/r/stats/median.html\n    if package:\n        return f\"https://rdrr.io/r/{package}/{topic}.html\"\n    return f\"https://rdrr.io/r/{topic}.html\"\n\ndef href_article(topic, package=None):\n    # Based on verification: https://cran.rstudio.com/web/packages/grid/vignettes/grid.pdf\n    if package:\n        return f\"https://cran.rstudio.com/web/packages/{package}/vignettes/{topic}.pdf\"\n    return f\"https://cran.rstudio.com/web/packages/{topic}.pdf\"\n\ndef href_package(package):\n    return f\"https://cran.rstudio.com/web/packages/{package}\"\n\ndef autolink_url(text):\n    # Mimicking the R logic for the provided examples\n    # 1. pkg::fun()\n    ns_match = re.search(r\"([\\w.]+)::([\\w.]+)\\(\\)\", text)\n    if ns_match:\n        return href_topic_remote(ns_match.group(2), ns_match.group(1))\n    \n    # 2. vignette('topic', package = 'pkg')\n    vig_match = re.search(r\"vignette\\(['\\\"](.+?)['\\\"],\\s*package\\s*=\\s*['\\\"](.+?)['\\\"]\\)\", text)\n    if vig_match:\n        return href_article(vig_match.group(1), vig_match.group(2))\n    \n    # 3. fun()\n    fun_match = re.search(r\"^([\\w.]+)\\(\\)$\", text)\n    if fun_match:\n        return href_topic_remote(fun_match.group(1))\n        \n    return None\n\ndef autolink(text):\n    href = autolink_url(text)\n    if href is None:\n        return None\n    # R output shows: \"<a href='...'>text</a>\"\n    return f\"<a href='{href}'>{escape_html(text)}</a>\"\n\n# To match R's console output [1] \"...\", we wrap the result for printing\ndef r_print(val):\n    if val is None:\n        print(\"NULL\")\n    elif isinstance(val, str):\n        print(f'[1] \"{val}\"')\n    else:\n        print(f'[1] {val}')\n\n# Main execution\n\nr_print(autolink_url(\"stats::median()\"))", "score": 1.0, "script_id": "downlit__rd_example__autolink_Rd", "n_calls": 0}

## Edit Examples
(none)
