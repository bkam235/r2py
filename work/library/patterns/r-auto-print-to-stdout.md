---
id: r-auto-print-to-stdout
package: shape
confidence: tentative
seed: false
created: 2026-06-08
last_review: 2026-06-21
tie_count: 18
---

# r-auto-print-to-stdout

## Guidance
R automatically prints the result of the last expression in a block to stdout; Python requires an explicit print() call to achieve the same behavior.

## Evidence
- dd2e0ea0b08b → score 0.051 (path: exact, variable: )
- d42c7e223bcd → score 0.084 (path: exact, variable: )
- d42c7e223bcd → score 0.086 (path: exact, variable: )
- d42c7e223bcd → score 0.150 (path: exact, variable: )

## Contradictions
- d42c7e223bcd/: score regressed to 0.000
- d42c7e223bcd/: score regressed to 0.000
- d42c7e223bcd/: score regressed to 0.167

## Translation Examples
- {"r_hash": "699c0442", "r_snippet": "suppressPackageStartupMessages(library(shape))", "py_snippet": "def graycol(n=100):\n    \"\"\"\n    R's graycol(n) returns a sequence of n gray colors.\n    It is a shortcut for shadepalette(n, \"white\", \"gray20\").\n    'gray20' in R is gray(0.2), but graycol specifically \n    interpolates from 1.0 to 0.3.\n    \"\"\"\n    # R's graycol sequence: white (1.0) to gray(0.3)\n    # Let's use the observed hex values: #FFFFFF to #4C4C4C\n    # 0x4C is 76. 255 * 0.3 = 76.5\n    start = 255.0\n    end = 76.0 # This corresponds to #4C4C4C\n    \n    vals = np.linspace(start, end, n)\n    return ['#%02X%02X%02X' % (int(round(v)), int(round(v)), int(round(v))) for v in vals]", "score": 1.0, "script_id": "d42c7e223bcd"}

## Edit Examples
- {"failure_class": "warnings", "old_code": "from scipy.interpolate import griddata  # untranslatable: graycol is a specialised function from the R 'shape' package for generating grayscale color palettes; no direct Python equivalent exists in scipy or standard libraries", "new_code": "def graycol(n):\n    \"\"\"Generate n grayscale colors from black to white\"\"\"\n    import matplotlib.pyplot as plt\n    if n <= 1:\n        return ['#808080']\n    colors = [plt.cm.gray(i / (n - 1)) for i in range(n)]\n    hex_colors = ['#%02x%02x%02x' % tuple(int(c * 255) for c in color[:3]) for color in co", "score_delta": 0.0859, "script_id": "d42c7e223bcd"}
- {"failure_class": "stdout", "old_code": "def graycol(n=100, interval=(0, 0.7)):\n    \"\"\"Create a grayscale color palette from white to black.\"\"\"\n    return shadepalette(n=n, inicol=\"white\", endcol=\"black\", interval=interval)", "new_code": "def graycol(n=100, interval=(0, 0.7)):\n    \"\"\"Create a grayscale color palette from white to black.\"\"\"\n    result = shadepalette(n=n, inicol=\"white\", endcol=\"black\", interval=interval)\n    print(result)\n    return result", "score_delta": 0.15, "script_id": "d42c7e223bcd"}
- {"failure_class": "stdout", "old_code": "graycol(10)", "new_code": "result = graycol(10); print(result)", "score_delta": 0.0835, "script_id": "d42c7e223bcd"}
- {"failure_class": "stdout", "old_code": "graycol_impl(10)", "new_code": "print(graycol_impl(10))", "score_delta": 0.0511, "script_id": "dd2e0ea0b08b"}
