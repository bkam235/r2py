---
id: scales.demo-discrete
package: scales
confidence: tentative
seed: true
created: 2026-09-05
last_review: 2026-09-05
tie_count: 0
---

# scales.demo-discrete

## Guidance
Translate R `demo_discrete` (FunctionCall from scales) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "9a82f976", "r_snippet": "demo_discrete(species, labels = label_glue(\"The {x}\\n{animal}\"))", "py_snippet": "def demo_discrete(data, labels_expr=None, labels_val=None):\n    \"\"\"\n    Mimics scales::demo_discrete by printing the call and rendering a plot.\n    \"\"\"\n    # In R, demo_discrete prints the scale call it is using.\n    # We use labels_expr to mimic the R code string that produced the labels.\n    if labels_expr:\n        print(f\"      scale_x_discrete(labels = {labels_expr})\")\n    \n    # Construct a simple plot to satisfy the graphics requirement\n    df = pd.DataFrame({'x': data, 'y': [1] * len(data)})\n    \n    # Handle the labeling logic\n    plot_labels = labels_val if labels_val is not None else", "score": 0.9863, "script_id": "auto"}
- {"r_hash": "6ad3f9bd", "r_snippet": "demo_datetime(one_month)", "py_snippet": "def demo_datetime(dates, breaks=None, labels=None):\n    \"\"\"\n    Mimics scales::demo_datetime by printing the scale call it is using and rendering a plot.\n    \"\"\"\n    # Create a dummy dataframe for plotting\n    df = pd.DataFrame({'date': dates, 'value': np.arange(len(dates))})\n    \n    # Construct the R-style print string\n    parts = [\"scale_x_datetime(\"]\n    args = []\n    \n    if breaks is not None:\n        if isinstance(breaks, int):\n            args.append(f\"breaks = breaks_pretty({breaks})\")\n        else:\n            args.append(f\"breaks = {breaks}\")\n            \n    if labels is not None:\n", "score": 0.9855, "script_id": "auto"}

## Edit Examples
(none)
