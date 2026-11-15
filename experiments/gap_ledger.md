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

## Summary (epoch 11 finals; epoch 12 gives the same scores)

Classified on 2026-11-15 (16 of the 17 `unknown` rows, offline: `work/analysis/tempfile_names.py`,
`entity_zero.py`, `fb_full.py`, and the replay's trajectories). Several classes are hypotheses; the row says which.

| plateau (primary) | states | points |
|---|---|---|
| gap (1 - mean final 0.8806) | 60 | 0.1194 |
| held by the states with final >= 0.95 (not listed) | 33 | 0.0048 |
| behaviour | 9 | 0.0334 |
| measurement (a scorer fix moves it as a correction) | 6 | 0.0287 (shiny 0.0125, fixed in epoch 11, closes in the next replay; shown offline 0.0049: sass as_sass, gtable add_cols, xml2 xml_attr; hypotheses 0.0113: ec_dh, sass_import) |
| capability | 4 | 0.0137 (all R's RNG stream under the harness's `set.seed(42)`: caret_s3, update_train, Arrows, boxplot_bclust) |
| out of reach | 7 | 0.0306 (aes_cbc, glyph_raster, shape_text, shape_string, ragg agg_capture; bslib page_fillable and value_box pending the py-shiny markup decision, 0.0132) |
| unknown | 1 | 0.0083 (prodlim backGround) |
| **reachable gap** (1 - mean final - out of reach) | | **0.081 to 0.089** (unknown counted both ways; noise floor about ±0.03, twice it 0.06) |

| share >= 0.95 (secondary) | states | share |
|---|---|---|
| room (1 - share 0.550; held-out 0.652) | 27 | 0.450 |
| out of reach | 7 | 0.117 |
| unknown | 1 | 0.017 |
| **reachable room** | | **0.317 to 0.333** (noise floor of a replay about ±0.09) |

The 8 states at 0.90-0.95 were added on 2026-11-14 with the cut. In each, at least one of the 3 chains stopped
because its best reached the loop's stop threshold 0.9 (16 threshold stops of 24 chains; the replay's `stop`
counts), so the threshold, not the model, ended them below 0.95.

## States

| state | final | points | class | evidence | set |
|---|---|---|---|---|---|
| shiny updateRadioButtons | 0.250 | 0.0125 | measurement, fixed in epoch 11 (expected to close in the next replay) | Epoch 11 (module-rebind): all 27 rewrites DeepSeek Flash chains logged on this state, re-scored offline (`work/analysis/shiny_e11_rescore.txt`): the first rewrite of 16 of 18 chains scores 0.96 (logged: 3 of 18 >= 0.9). The recorded final is the start, which never assigns `ui` (0.25, scored right). Counterfactual, not a run. Before: all 4 rewrites of the default replay scored 0.25 with the same `ui` HTML (similarity 0.99) as the 0.96 program of feedback-e10. The only difference: `from shiny import ui` then `ui = ui.page_fluid(...)` rebinds the module name. Renaming the module import alone (offline, same program otherwise) gives `ui` 0.96, aggregate 0.96. With the rebinding, `ui` scores 0 on data, value and type while its feedback shows the 0.99-similar HTML: the feedback misleads. Cause: the checkpoint baseline kept no id for modules. (`work/analysis/shiny_trace.py`, `unshadow.py`) | 2026-11-14 |
| bslib page_fillable | 0.287 | 0.0119 | out of reach (pending a scoring decision) | Epoch 12, offline (`work/analysis/tempfile_names.py`): the 151 `tempfile:*.woff2` keys (fonts bslib caches) reach no score (removed: 0.324 -> 0.368, inside its repeat range 0.29-0.37); they only fill the feedback. What loses is `ui` data 0.157: R's bslib renders `<body class="bslib-page-fill ...` and py-shiny `<html><head></head><body ...` (text similarity 0.63). Two libraries' markup; whether py-shiny's markup should count is the open "py-shiny vs R shiny markup" scoring decision (October). | 2026-11-15 |
| openssl ec_dh | 0.418 | 0.0097 | measurement (hypothesis) | Epoch 10: `alice_pub`/`bob_pub` sentinels now attributed score 0.25; R's key objects cannot be serialized, so R's bundle is empty and an entity Python computes is penalised. Hypothesis, not tested (IMPROVEMENT_PLAN, epoch 10). | 2026-11-14 |
| ggplot2 geom_bin_2d | 0.500 | 0.0083 | behaviour | Never improved in the replay (4 catastrophic crashing rewrites of 9); patience-dsflash reached +0.178 on it. | 2026-11-14 |
| prodlim backGround | 0.500 | 0.0083 | unknown | 9 rewrites, all `unchanged`; `plot(0,0)` scores plotted similarity exactly 0.000 and R records no figure at the `backGround` calls (draws on the open plot). The feedback gives a similarity, not the difference. Suspected measurement (exact 0 on a one-point plot), not shown. | 2026-11-15 |
| openssl aes_cbc | 0.550 | 0.0075 | out of reach | `aes_cbc_encrypt` defaults to `iv = rand_bytes(16)`; R's `serialize` bytes (cycle of 2026-10-17). | 2026-11-14 |
| farver convert_colour | 0.703 | 0.0050 | behaviour | feedback-e10 reached 0.890 (marked `spec_lab`); some chains pasted `convert_colour` outputs (model-screen audit). | 2026-11-14 |
| recipes step_kpca | 0.725 | 0.0046 | behaviour (hypothesis) | Feedback names a missing figure (R=1, Python=0: the ggplot) and kPCA values (`kpca_te` 0.25, `kpca_estimates` 0.35); chains went 0.56-0.73 with 21 probes, none adding the figure. kernlab's kPCA numerics not checked. | 2026-11-15 |
| caret caret_s3 | 0.743 | 0.0043 | capability | Reached 1.0 in one width chain of patience-dsflash by reimplementing R's Mersenne Twister and `sample()`; no other chain did. | 2026-11-14 |
| shape filledmultigonal | 0.750 | 0.0042 | behaviour | 5 catastrophic crashing rewrites; patience-dsflash +0.027. | 2026-11-14 |
| e1071 boxplot_bclust | 0.765 | 0.0039 | capability (R's RNG stream) | `bclust` runs k-means with random starts; the harness seeds R (`set.seed(42)`), so `bc1` centers match only by reproducing R's Mersenne Twister and k-means draws (as caret_s3 did once). | 2026-11-15 |
| isoband isoband3_s2 | 0.767 | 0.0039 | behaviour | feedback-e10 reached 0.869 (same score under the old rule: a better program). | 2026-11-14 |
| systemfonts glyph_raster | 0.786 | 0.0036 | out of reach | Glyph bitmaps need the font engine; programs that match paste R's metrics (model-screen audit). | 2026-11-14 |
| textshaping shape_text | 0.807 | 0.0032 | out of reach | Font metrics, as glyph_raster; 3 literal-check rejections in the replay. | 2026-11-14 |
| shape getellipse | 0.815 | 0.0031 | behaviour (graphics feedback) | Data entities all 1.0; only `plot` 0.27 and `emptyplot` 0.25 on plotted similarity. 29 rewrites over 6 chains; the feedback is a similarity number, not what differs, so no step can aim (the graphics-visibility bet). | 2026-11-15 |
| shape Arrows | 0.826 | 0.0029 | capability (R's RNG stream) | `x0 <- runif(100, ...)` etc. under the harness's `set.seed(42)`: `x0`, `y0` 0.25 and the arrow plots depend on R's draws. The rest (curve, xd) is graphics feedback as getellipse. | 2026-11-15 |
| caret update_train | 0.843 | 0.0026 | capability (R's RNG stream) | `train(..., trControl = trainControl(method = "cv"))`: `knnFit1` results (Accuracy, Kappa) and seeds come from R's fold draws; 0/13 numeric fields found. As caret_s3. | 2026-11-15 |
| sass as_sass | 0.867 | 0.0022 | measurement (shown offline) | `input` 0.25: R's value is the Sass text with `@import "...RtmpCgcbhs/variables5e00e5c1d6a"` (R's temp path), Python's the same text with its own temp path (`...Rtmpd5KSNZ/variablesdcbf739e872b`). The temp-path rule (2026-10-18) treats whole-string paths only; a temp path inside a string scores 0. The FILES key `tempfile:variables5e00e5c1d6a` (R's random name) reaches no score (removed: 0.8674 -> 0.8676) but tops every entity's feedback. (`work/analysis/entity_zero.py`, `tempfile_names.py`) | 2026-11-15 |
| openssl certificates | 0.893 | 0.0018 | behaviour | `chain` 0.25: the final binds `chain` under the `print` entity; at `chain` it only defines `download_ssl_cert`, so nothing is recorded there. (Network value: R's capture holds the CRAN certificate valid 2025-12-16 to 2027-01-16.) | 2026-11-15 |
| textshaping get_font_features | 0.903 | 0.0016 | behaviour (hypothesis) | Only `sys_fonts` loses (0.71): R lists 406 fonts, Python 405 and in another order (`Barrio` first). October: Python can read the same font files. In feedback-e10 a new run on it ended 0.217 lower. | 2026-11-15 |
| ragg agg_capture | 0.905 | 0.0016 | out of reach (hypothesis) | `raster`/`raster_n` are pixel arrays of R's AGG device (480 vs 432 rows); exact pixels need R's renderer. Stopped at the threshold: 1 of 3 chains. | 2026-11-15 |
| sass sass_import | 0.906 | 0.0016 | measurement (hypothesis, as as_sass) | `sass_file` 0.675, `sass` 0.893 on side effects: their printed output holds the @import of R's temp path. FILES key `tempfile:file522c7cde307a.scss` reaches no score (removed: 0.9065 -> 0.9059). Stops: threshold 3. | 2026-11-15 |
| systemfonts shape_string | 0.909 | 0.0015 | out of reach | Font metrics, as shape_text: chains' 0.91-0.92 programs were rejected by literal_check and the review (pasted metrics); `shape_string_1` 0.758. | 2026-11-15 |
| gtable gtable_add_cols | 0.915 | 0.0014 | measurement (shown offline) | `tab3` 0.25: the entity assigns `tab3` twice (`gtable_add_cols(tab, ...)`, then `gtable_add_cols(tab3, ..., 0)`). R's checkpoint holds the first value (4 widths, layout l 1,1,3), Python's the last (5 widths, l 2,2,5, which is R's own final `tab3`). A faithful program cannot match both. Stops: threshold 3. | 2026-11-15 |
| xml2 xml_attr | 0.921 | 0.0013 | measurement (shown offline) + library text form | `kids` 0.25: R's nodes are fingerprinted with their text (`<child id="a"/>`), Python's lxml elements only with `sourceline`, no text, so no lxml program can match. `doc` 0.14: lxml serializes in-scope `xmlns:` declarations, xml2 does not (similarity 0.61). Stops: threshold 3. | 2026-11-15 |
| bslib value_box | 0.923 | 0.0013 | out of reach (pending a scoring decision) | `value_box` 0.923 on printed HTML: py-shiny vs R bslib markup, as page_fillable. The 151 `tempfile:*.woff2` keys reach no score (removed: 0.9229 both). | 2026-11-15 |
| proxy registry | 0.947 | 0.0009 | behaviour | `as.data.frame` 0.69 and `get_entries_1` 0.89 on printed output; all 3 chains still improving when the 0.9 threshold stopped them (0.92-0.95). | 2026-11-15 |
