---
id: r-shape-to-scipy
package: shape
confidence: tentative
seed: false
created: 2026-06-08
last_review: 2026-07-02
tie_count: 68
---

# r-shape-to-scipy

## Guidance
The R 'shape' package provides functions for shape analysis and interpolation. For tasks involving grid data or surface interpolation (common in 'shape' use cases), scipy.interpolate is the closest Python equivalent.

## Evidence
- dd2e0ea0b08b → score 0.015 (path: exact, variable: )
- dd2e0ea0b08b → score 0.003 (path: exact, variable: )
- dd2e0ea0b08b → score 0.005 (path: exact, variable: )
- d42c7e223bcd → score 0.027 (path: exact, variable: )

## Contradictions
- dd2e0ea0b08b/: score regressed to 0.472
- dd2e0ea0b08b/: score regressed to 0.359
- dd2e0ea0b08b/: score regressed to 0.491
- dd2e0ea0b08b/: score regressed to 0.497
- d42c7e223bcd/: score regressed to 0.233
- d42c7e223bcd/: score regressed to 0.233
- d42c7e223bcd/: score regressed to 0.233
- d42c7e223bcd/: score regressed to 0.672
- d42c7e223bcd/: score regressed to 0.242
- d42c7e223bcd/: score regressed to 0.242
- d42c7e223bcd/: score regressed to 0.200
- d42c7e223bcd/: score regressed to 0.200
- d42c7e223bcd/: score regressed to 0.233
- d42c7e223bcd/: score regressed to 0.588

## Translation Examples
- {"r_hash": "699c0442", "r_snippet": "suppressPackageStartupMessages(library(shape))", "py_snippet": "# The 'shape' R package functions (graycol, shadepalette, intpalette) are implemented inline below\nimport warnings\nwarnings.filterwarnings('ignore')", "score": 1.0, "script_id": "d42c7e223bcd"}
- {"r_hash": "d6fe193f", "r_snippet": "image(\n      matrix(nrow = 1, ncol = 100, data = 1:100),\n      col = graycol(100),\n      main = \"greycol,graycol\"\n)", "py_snippet": "# image(matrix(nrow = 1, ncol = 100, data = 1:100), col = graycol(100), main = \"greycol,graycol\")\ndata_matrix = np.arange(1, 101).reshape(1, 100)\ncolors_100 = graycol(100)\ncmap_100 = ListedColormap(colors_100)\n\nplt.figure()\n# imshow displays matrices; we use aspect='auto' and the calculated cmap\nplt.imshow(data_matrix, aspect='auto', cmap=cmap_100, extent=[0, 100, 0, 1])\nplt.title(\"greycol,graycol\")\nplt.axis('off')\nplt.show()", "score": 0.8654, "script_id": "d42c7e223bcd"}
- {"r_hash": "71b1244c", "r_snippet": "filled.contour(volcano, color = graycol, asp = 1, main = \"greycol,graycol\")", "py_snippet": "# filled.contour(volcano, color = graycol, asp = 1, main = \"greycol,graycol\")\nplt.figure()\n# R's filled.contour and image treat the matrix differently than imshow.\n# We transpose to match R's visual orientation for the volcano dataset.\nplt.contourf(volcano.T, cmap=ListedColormap(graycol(100)))\nplt.gca().set_aspect('equal')\nplt.title(\"greycol,graycol\")\nplt.show()", "score": 0.8043, "script_id": "d42c7e223bcd"}

## Edit Examples
- {"failure_class": "warnings", "old_code": "import numpy as np\nimport matplotlib.pyplot as plt\nfrom matplotlib.colors import ListedColormap, to_rgb\n\n# Load volcano dataset (87x61 matrix)\n# Load volcano dataset from R\nfrom sklearn.datasets import load_sample_image\ntry:\n    # Try to load volcano from scipy if available\n    from scipy.datasets i", "new_code": "import warnings\nwarnings.filterwarnings('ignore')\n\nimport numpy as np\nimport matplotlib.pyplot as plt\nfrom matplotlib.colors import ListedColormap, to_rgb\nfrom scipy.interpolate import griddata", "score_delta": 0.0267, "script_id": "d42c7e223bcd"}
- {"failure_class": "warnings", "old_code": "import matplotlib.patches as mpatches\nimport matplotlib.pyplot as plt\nimport numpy as np\n\n\n# r2py:entity:import_shape\n\n# suppressPackageStartupMessages(library(shape))\n# Python doesn't have a direct equivalent to the 'shape' package for all its functionality,\n# but we import the necessary libraries ", "new_code": "import matplotlib.patches as mpatches\nimport matplotlib.pyplot as plt\nimport numpy as np\nfrom scipy.interpolate import griddata\n\n# r2py:entity:import_shape\n# suppressPackageStartupMessages(library(shape))", "score_delta": 0.0149, "script_id": "dd2e0ea0b08b"}
