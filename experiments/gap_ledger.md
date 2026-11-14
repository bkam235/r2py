# Gap ledger

One row per training state whose final under the production default is below 0.9. Points = (1 - final) / 60, so the
rows add up to the part of the gap (1 - mean final) held below 0.9. Classes: **measurement** (a faithful program is
scored wrong, shown offline), **out of reach** (no faithful program can match the value, or a measurement fault not
yet fixable), **behaviour** (scorer right, the loop fails to fix it), **capability** (scorer right, feedback names the
difference, the model rarely proposes a correct program), **unknown** (not yet classed). A state stays `unknown` until
a test or a trajectory reading classes it. The headroom check (META_LOOP.md, "Headroom") reads the reachable gap here.

Created 2026-11-14 (cycle of 2026-11-14). Source: `work/dsflash_default/finals_epoch10.jsonl` (default_2026_11_12,
sample 0, finals re-verified under epoch 10, scorer 06e4778f626b-db31b28ade02).

## Summary (epoch 10)

| | points |
|---|---|
| gap (1 - mean final 0.8799) | 0.1201 |
| held by the 41 states with final >= 0.9 (not listed) | 0.0159 |
| held by the 19 states below 0.9 | 0.1042 |
| out of reach | 0.0143 |
| **reachable gap** | **0.1058** (noise floor of a replay about ±0.03; twice it 0.06) |
| measurement (shown or hypothesised; a scorer fix would move it as a correction) | 0.0238 of which 0.0140 shown offline |

## States

| state | final | points | class | evidence | set |
|---|---|---|---|---|---|
| shiny updateRadioButtons | 0.250 | 0.0125 | measurement | All 4 rewrites of the default replay scored 0.25 with the same `ui` HTML (similarity 0.99) as the 0.96 program of feedback-e10. The only difference: `from shiny import ui` then `ui = ui.page_fluid(...)` rebinds the module name. Renaming the module import alone (offline, same program otherwise) gives `ui` 0.96, aggregate 0.96. With the rebinding, `ui` scores 0 on data, value and type while its feedback shows the 0.99-similar HTML: the feedback misleads. Root cause in the scorer not yet traced. (`work/analysis/shiny_trace.py`, `unshadow.py`) | 2026-11-14 |
| bslib page_fillable | 0.250 | 0.0125 | measurement (0.0022) + unknown (0.0103) | Same rebinding (`ui = ui.page_fillable`); unshadowed offline 0.25 -> 0.382. The rest: woff2 files R writes to tempfile missing on the Python side, html content. Suspected measurement, not shown. | 2026-11-14 |
| openssl ec_dh | 0.411 | 0.0098 | measurement (hypothesis) | Epoch 10: `alice_pub`/`bob_pub` sentinels now attributed score 0.25; R's key objects cannot be serialized, so R's bundle is empty and an entity Python computes is penalised. Hypothesis, not tested (IMPROVEMENT_PLAN, epoch 10). | 2026-11-14 |
| ggplot2 geom_bin_2d | 0.500 | 0.0083 | behaviour | Never improved in the replay (4 catastrophic crashing rewrites of 9); patience-dsflash reached +0.178 on it. | 2026-11-14 |
| prodlim backGround | 0.500 | 0.0083 | unknown | 9 rewrites, all `unchanged` (plotted content similarity 0). | 2026-11-14 |
| openssl aes_cbc | 0.550 | 0.0075 | out of reach | `aes_cbc_encrypt` defaults to `iv = rand_bytes(16)`; R's `serialize` bytes (cycle of 2026-10-17). | 2026-11-14 |
| farver convert_colour | 0.703 | 0.0050 | behaviour | feedback-e10 reached 0.890 (marked `spec_lab`); some chains pasted `convert_colour` outputs (model-screen audit). | 2026-11-14 |
| recipes step_kpca | 0.725 | 0.0046 | unknown | In-loop vs offline score of the same program differ (0.701 vs 0.772, patience-dsflash). | 2026-11-14 |
| caret caret_s3 | 0.743 | 0.0043 | capability | Reached 1.0 in one width chain of patience-dsflash by reimplementing R's Mersenne Twister and `sample()`; no other chain did. | 2026-11-14 |
| shape filledmultigonal | 0.750 | 0.0042 | behaviour | 5 catastrophic crashing rewrites; patience-dsflash +0.027. | 2026-11-14 |
| e1071 boxplot_bclust | 0.765 | 0.0039 | unknown | | 2026-11-14 |
| isoband isoband3_s2 | 0.767 | 0.0039 | behaviour | feedback-e10 reached 0.869 (same score under the old rule: a better program). | 2026-11-14 |
| systemfonts glyph_raster | 0.786 | 0.0036 | out of reach | Glyph bitmaps need the font engine; programs that match paste R's metrics (model-screen audit). | 2026-11-14 |
| textshaping shape_text | 0.807 | 0.0032 | out of reach | Font metrics, as glyph_raster; 3 literal-check rejections in the replay. | 2026-11-14 |
| shape getellipse | 0.815 | 0.0031 | unknown | | 2026-11-14 |
| shape Arrows | 0.826 | 0.0029 | unknown | 10 review rejections in the replay, none above the final. | 2026-11-14 |
| caret update_train | 0.843 | 0.0026 | unknown | | 2026-11-14 |
| sass as_sass | 0.867 | 0.0022 | unknown | | 2026-11-14 |
| openssl certificates | 0.893 | 0.0018 | unknown | | 2026-11-14 |
