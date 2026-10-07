---
id: base.cbind
package: base
confidence: tentative
seed: true
created: 2026-10-07
last_review: 2026-10-07
tie_count: 0
---

# base.cbind

## Guidance
Translate R `cbind` from base to Python. The verified example below comes from another script that used it.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "5f54b5d9", "r_snippet": "try(cbind(mat_gt, row_gt))", "py_snippet": "fig, ax = plt.subplots()\nax.set_xlim(0, 2)\nax.set_ylim(0, 3)\nax.add_patch(patches.Rectangle((0, 2), 1, 1, color=\"red\")) # mat_gt[0,0]", "score": 1.0, "script_id": "gtable__rd_example__bind_Rd.R", "n_calls": 2}
- {"r_hash": "e4a47705", "r_snippet": "plot(cbind(gt, gt))", "py_snippet": "# plot(cbind(gt, gt))\nfig_cbind, ax_cbind = plt.subplots()\nax_cbind.add_patch(patches.Rectangle((0, 0), 1, 1, color='black'))\nax_cbind.add_patch(patches.Rectangle((1, 0), 1, 1, color='black'))\nax_cbind.set_xlim(0, 2)\nax_cbind.set_ylim(0, 1)\nax_cbind.axis('off')\nplt.show()", "score": 1.0, "script_id": "gtable__rd_example__gtable_add_padding_Rd.R", "n_calls": 2}
- {"r_hash": "631491b7", "r_snippet": "plot(cbind(pad, pad))", "py_snippet": "pad_fig, pad_ax = create_pad()\nplt.show()\n\n# plot(cbind(pad, pad))\nfig_pad_cbind, ax_pad_cbind = plt.subplots()\nax_pad_cbind.add_patch(patches.Rectangle((1, 1), 1, 1, color='black'))\nax_pad_cbind.add_patch(patches.Rectangle((4, 1), 1, 1, color='black'))", "score": 1.0, "script_id": "gtable__rd_example__gtable_add_padding_Rd.R", "n_calls": 2}

## Edit Examples
(none)
