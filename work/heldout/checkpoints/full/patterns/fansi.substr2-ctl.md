---
id: fansi.substr2-ctl
package: fansi
confidence: tentative
seed: true
created: 2026-09-20
last_review: 2026-09-20
tie_count: 0
---

# fansi.substr2-ctl

## Guidance
Translate R `substr2_ctl` (FunctionCall from fansi) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "f155c27d", "r_snippet": "substr2_ctl(x, 2, 4, type='width', round='start')", "py_snippet": "def substr2_ctl(x, start, stop, type_val=\"chars\", round_val=\"start\", tabs_as_spaces=False, tab_stops=8, warn=True, term_cap=None, ctl=\"all\", normalize=False, carry=False, terminate=True):\n    if isinstance(x, list):\n        results = []\n        current_carry_sgr = \"\"\n        for item in x:\n            effective_carry = carry\n            if carry is True:\n                effective_carry = current_carry_sgr\n            \n            res = substr2_ctl(item, start, stop, type_val, round_val, tabs_as_spaces, tab_stops, warn, term_cap, ctl, normalize, effective_carry, terminate)\n            \n            parts = get_ansi_parts(item)\n            for p in reversed(parts):\n                if p.startswith('\\033[') and p.endswith('m'):\n                    current_carry_sgr = p\n                    break\n            results.append(res)\n        return results\n\n    parts = get_ansi_parts(x)\n    logical_chars = []\n    char_to_part_idx = []\n    \n    for i, part in enumerate(parts):\n        if not (part.startswith('\\033[') and (part.endswith('m') or part.endswith('K'))):\n            for char in part:\n                logical_chars.append(char)\n                char_to_part_idx.append(i)\n\n    if type_val == \"width\":\n        visual_positions = [0]\n        for char in logical_chars:\n            visual_positions.append(visual_positions[-1] + get_char_width(char))\n        \n        v_start = start - 1\n        v_stop = stop - 1\n        \n        def map_visual_to_logical(v, mode):\n            if v < 0: return 0\n            if v >= len(visual_positions): return len(logical_chars)\n            for i in range(len(visual_positions) - 1):\n                if visual_positions[i] <= v < visual_positions[i+1]:\n                    width = visual_positions[i+1] - visual_positions[i]\n                    if width == 2 and v == visual_positions[i] + 1:\n                        if mode == 'start': return i \n                        if mode == 'stop': return i + 1 \n# ...", "score": 1.0, "script_id": "fansi__rd_example__substr_ctl_Rd", "n_calls": 0}

## Edit Examples
(none)
