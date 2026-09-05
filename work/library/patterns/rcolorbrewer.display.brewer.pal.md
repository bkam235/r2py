---
id: rcolorbrewer.display.brewer.pal
package: RColorBrewer
confidence: tentative
seed: true
created: 2026-09-05
last_review: 2026-09-05
tie_count: 0
---

# rcolorbrewer.display.brewer.pal

## Guidance
Translate R `display.brewer.pal` (FunctionCall from RColorBrewer) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "84bf70d4", "r_snippet": "display.brewer.pal(7,\"BrBG\")", "py_snippet": "def display_brewer_pal(n, name):\n    pal = brewer_pal(n, name)\n    plt.figure(figsize=(6, 1))\n    data = np.arange(1, n + 1).reshape(1, n)\n    plt.imshow(data, aspect='auto', cmap=ListedColormap(pal), extent=[1, n, 1, 1])\n    plt.xlabel(name)\n    plt.yticks([])\n    plt.xticks([])\n    plt.gca().set_axis_off()\n    plt.ylim(0.5, 1.5)\n    plt.show()\n\ndisplay_brewer_pal(7, \"BrBG\")", "score": 0.9232, "script_id": "auto"}

## Edit Examples
(none)
