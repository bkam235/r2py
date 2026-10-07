---
id: base.writelines
package: base
confidence: tentative
seed: true
created: 2026-10-07
last_review: 2026-10-07
tie_count: 0
---

# base.writelines

## Guidance
Translate R `writelines` from base to Python. The verified example below comes from another script that used it.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "78ca815b", "r_snippet": "writeLines(bleed)      # Style will bleed out of string", "py_snippet": "def writeLines(text, sep=\"\\n\"):\n    if isinstance(text, list):\n        print(sep.join(text))\n    else:\n        print(text, end=\"\")\n\ndef substr_ctl_replace(x_in, start, stop, value, carry=False):\n    if not isinstance(x_in, list):\n        x_in = [x_in]\n    \n    results = []\n    for s in x_in:\n        parts = get_ansi_parts(s)\n        logical_chars = []\n        char_to_part_idx = []\n        for i, part in enumerate(parts):\n            if not (part.startswith('\\033[') and (part.endswith('m') or part.endswith('K'))):\n                for char in part:\n                    logical_chars.append(char)\n                    char_to_part_idx.append(i)\n        \n        l_start = max(0, start - 1)\n        l_stop = max(0, stop)\n        \n        prefix_logical = \"\".join(logical_chars[:l_start])\n        suffix_logical = \"\".join(logical_chars[l_stop:])\n        \n        sgr_at_start = \"\"\n        if l_start < len(char_to_part_idx):\n            idx = char_to_part_idx[l_start]\n            for i in range(idx, -1, -1):\n                if parts[i].startswith('\\033[') and parts[i].endswith('m'):\n                    sgr_at_start = parts[i]\n                    break\n        \n        if carry is True:\n            # carry=True preserves original SGR exactly around the replacement\n            res = f\"{sgr_at_start}{prefix_logical}\\033[0m{value}{sgr_at_start}{suffix_logical}\"\n        else:\n            res = f\"{sgr_at_start}{prefix_logical}\\033[0m{value}{sgr_at_start}{suffix_logical}\"\n            \n        if value.startswith('\\033['):\n            res = res.replace('\\033[0m' + value, value)\n\n        results.append(res)\n    return results\n\ndef format_r_out(val):\n    if isinstance(val, list):\nprint(format_r_out(substr2_ctl(x, 2, 4, type_val='width', round_val='both')))", "score": 1.0, "script_id": "fansi__rd_example__substr_ctl_Rd.R", "n_calls": 1}
- {"r_hash": "d305b81c", "r_snippet": "writeLines(\"$color: red; body{ color: $color; }\", tmp_scss_file)", "py_snippet": "tmp_scss_file = tempfile.NamedTemporaryFile(suffix=\".scss\", delete=False, mode='w')\ntmp_scss_file.write(\"$color: red; body{ color: $color; }\")\ntmp_scss_file.close()", "score": 1.0, "script_id": "sass__rd_example__sass_import_Rd.R", "n_calls": 1}

## Edit Examples
(none)
