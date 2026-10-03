---
id: systemfonts.match-fonts
package: systemfonts
confidence: tentative
seed: true
created: 2026-09-24
last_review: 2026-09-24
tie_count: 0
---

# systemfonts.match-fonts

## Guidance
Translate R `match_fonts` (FunctionCall from systemfonts) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "0f550c15", "r_snippet": "match_fonts('sans', italic = TRUE)", "py_snippet": "def match_fonts(family, italic=False, weight=\"normal\", width=\"undefined\"):\n    \"\"\"\n    Approximates R's systemfonts::match_fonts.\n    Resolves font families and styles to system font paths.\n    \"\"\"\n    # Weights defined in systemfonts\n    r_weights = [\"thin\", \"extralight\", \"light\", \"normal\", \"medium\", \"semibold\", \"bold\", \"extrabold\", \"black\", \"undefined\"]\n    weights_map = {w: (i) * 100 for i, w in enumerate(r_weights)}\n    \n    # R's systemfonts uses system-specific aliases. \n    generic_map = {\n        'sans': 'Arial',\n        'serif': 'Times New Roman',\n        'mono': 'Courier New'\n    }\n\n    # Handle vector input for family\n    families = [family] if isinstance(family, str) else list(family)\n    \n    # Normalize inputs\n    n_max = len(families)\n    italic_list = [italic] * n_max if not isinstance(italic, (list, np.ndarray)) else italic\n    weight_list = [weight] * n_max if not isinstance(weight, (list, np.ndarray)) else weight\n    \n    all_fonts = fm.findSystemFonts()\n    results = []\n    \n    for fam, it, wt in zip(families, italic_list, weight_list):\n        # Translate R weight string to numeric\n        target_weight = weights_map.get(wt.lower() if isinstance(wt, str) else \"normal\", 300)\n        \n        # Resolve family alias\n        target_fam = generic_map.get(fam.lower(), fam)\n        \n        best_match = None\n        min_score = float('inf')\n        \n        for font_path in all_fonts:\n            try:\n                prop = fm.FontProperties(fname=font_path)\n                name = prop.get_name()\n                style = prop.get_style()\n                weight_val = prop.get_weight()\n                \n                # Family match (case insensitive)\n                if target_fam.lower() not in name.lower():\n                    continue\n                \n                # Style Score: Absolute requirement for italic/regular\n                is_italic = style.lower() in ['italic', 'oblique']\n                if it != is_italic:\n# ...", "score": 0.9163, "script_id": "systemfonts__rd_example__match_fonts_Rd", "n_calls": 0}

## Edit Examples
(none)
