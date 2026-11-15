# Gap ledger

One row per training state whose final under the production default is below 0.95 (below 0.9 until 2026-11-14, when
the share of finals >= 0.95 became the secondary metric; META_LOOP.md, "The objective"). Points = (1 - final) / 60, so the
rows add up to the part of the gap (1 - mean final) held below 0.95. Classes: **measurement** (a faithful program is
scored wrong, shown offline), **out of reach** (no faithful program can match the value, or a measurement fault not
yet fixable), **behaviour** (scorer right, the loop fails to fix it), **capability** (scorer right, feedback names the
difference, the model rarely proposes a correct program), **unknown** (not yet classed). A state stays `unknown` until
a test or a trajectory reading classes it. The headroom check (META_LOOP.md, "Headroom") reads the reachable gap here.

Created 2026-11-14 (cycle of 2026-11-14). Source: `work/dsflash_default/finals_epoch11.jsonl` (default_2026_11_12,
sample 0, finals re-verified under epoch 11, scorer d5609fe186a0-db31b28ade02; epoch 10 in
`finals_epoch10.jsonl`).

## Summary (epoch 11)

| plateau (primary) | points |
|---|---|
| gap (1 - mean final 0.8806) | 0.1194 |
| held by the 33 states with final >= 0.95 (not listed) | 0.0048 |
| held by the 27 states below 0.95 | 0.1147 (of it 0.0112 in the 8 states at 0.90-0.95) |
| out of reach | 0.0143 |
| **reachable gap** | **0.053 to 0.105** (unknown 0.0525 counted both ways; noise floor about ±0.03) |
| measurement (hypothesised; a scorer fix would move it as a correction) | 0.0097 (ec_dh); the 0.0140 shown offline on 2026-11-14 was fixed in epoch 11 |

Share of finals >= 0.95 (the secondary metric): 33 of 60 = **0.550** (held-out 30 of 46 = 0.652).

| share >= 0.95 (secondary) | states | share |
|---|---|---|
| room (1 - share) | 27 | 0.450 |
| out of reach (aes_cbc, glyph_raster, shape_text) | 3 | 0.050 |
| unknown (counted both ways) | 17 | 0.283 |
| **reachable room** | | **0.117 to 0.400** (noise floor of a replay about ±0.09; twice it 0.18) |

The 8 states at 0.90-0.95 were added on 2026-11-14 with the cut. In each, at least one of the 3 chains stopped
because its best reached the loop's stop threshold 0.9 (16 threshold stops of 24 chains; the replay's `stop`
counts), so the threshold, not the model, ended them below 0.95.

## States

| state | final | points | class | evidence | set |
|---|---|---|---|---|---|
| shiny updateRadioButtons | 0.250 | 0.0125 | measurement, fixed in epoch 11 (expected to close in the next replay) | Epoch 11 (module-rebind): all 27 rewrites DeepSeek Flash chains logged on this state, re-scored offline (`work/analysis/shiny_e11_rescore.txt`): the first rewrite of 16 of 18 chains scores 0.96 (logged: 3 of 18 >= 0.9). The recorded final is the start, which never assigns `ui` (0.25, scored right). Counterfactual, not a run. Before: all 4 rewrites of the default replay scored 0.25 with the same `ui` HTML (similarity 0.99) as the 0.96 program of feedback-e10. The only difference: `from shiny import ui` then `ui = ui.page_fluid(...)` rebinds the module name. Renaming the module import alone (offline, same program otherwise) gives `ui` 0.96, aggregate 0.96. With the rebinding, `ui` scores 0 on data, value and type while its feedback shows the 0.99-similar HTML: the feedback misleads. Cause: the checkpoint baseline kept no id for modules. (`work/analysis/shiny_trace.py`, `unshadow.py`) | 2026-11-14 |
| bslib page_fillable | 0.287 | 0.0119 | unknown | Same rebinding (`ui = ui.page_fillable`), fixed in epoch 11: 0.25 -> 0.29-0.37 between repeats. The rest: woff2 files R writes to tempfile missing on the Python side, html content. Suspected measurement, not shown. | 2026-11-14 |
| openssl ec_dh | 0.418 | 0.0097 | measurement (hypothesis) | Epoch 10: `alice_pub`/`bob_pub` sentinels now attributed score 0.25; R's key objects cannot be serialized, so R's bundle is empty and an entity Python computes is penalised. Hypothesis, not tested (IMPROVEMENT_PLAN, epoch 10). | 2026-11-14 |
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
| textshaping get_font_features | 0.903 | 0.0016 | unknown | Stops: threshold 1, stalled 2. In feedback-e10 a new run on it ended 0.217 lower. | 2026-11-14 |
| ragg agg_capture | 0.905 | 0.0016 | unknown | Stops: threshold 1, done 1, stalled 1. | 2026-11-14 |
| sass sass_import | 0.906 | 0.0016 | unknown | Stops: threshold 3. | 2026-11-14 |
| systemfonts shape_string | 0.909 | 0.0015 | unknown | Stops: threshold 1, stalled 1, budget 1. Font metrics, perhaps out of reach as shape_text. | 2026-11-14 |
| gtable gtable_add_cols | 0.915 | 0.0014 | unknown | Stops: threshold 3. | 2026-11-14 |
| xml2 xml_attr | 0.921 | 0.0013 | unknown | Stops: threshold 3. | 2026-11-14 |
| bslib value_box | 0.923 | 0.0013 | unknown | Stops: threshold 1, done 2. | 2026-11-14 |
| proxy registry | 0.947 | 0.0009 | unknown | Stops: threshold 3. | 2026-11-14 |
