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
`finals_epoch10.jsonl`). From epoch 17 (2026-11-21, R row names in the data shim): `work/replay_default_e16/finals_epoch17.jsonl` (purrr attr_getter 0.926 -> 1.000 leaves the table; ec_dh 0.660 -> 0.675, its noise). From epoch 13 (2026-11-15, forged fingerprints refused): `finals_epoch13.jsonl`; from epoch 14 (2026-11-16, Python capture as R's): `finals_epoch14.jsonl`; from epoch 15 (2026-11-16, graphics pages attributed as R's): `finals_epoch15.jsonl`; from epoch 16 (2026-11-16, the Python graphics fingerprint keeps every point): `finals_epoch16.jsonl`. **From 2026-11-16 the source is the default's own replay under epoch 16** (`work/replay_default_e16/finals_epoch16.jsonl`, test `default-e16-replay`), no longer the epoch-9 replay re-scored.

## Summary (default-e16-replay finals, epoch 17)

Classified on 2026-11-15 (16 of the 17 `unknown` rows, offline: `work/analysis/tempfile_names.py`,
`entity_zero.py`, `fb_full.py`, and the replay's trajectories). Several classes are hypotheses; the row says which. Corrected the same day by threshold-095 (gtable, shape_string, value_box, sass_import reached >= 0.95 after being classed out of reach or measurement from reading values: a class read off values is weak until a program tests it). Epochs 13-16 changed rows as recorded in each row. On 2026-11-16 the source moved to the default's own replay under epoch 16 (0.9086; the epoch-9 replay re-scored was 0.8656): 5 states left (shiny updateRadioButtons 0.960, as epoch 11 predicted; proxy registry 0.962; gtable add_cols, rvest html_table, filledmultigonal 1.000) and 4 entered as unknown (pROC coords, purrr attr_getter, ragg agg_webp_anim, broom augment_felm). One replay sample per state: a row's final moves by its own noise between replays (bslib value_box 0.923 -> 0.678).

| plateau (primary) | states | points |
|---|---|---|
| gap (1 - mean final 0.9101 under epoch 17, 0.9086 under epoch 16; the epoch-9 replay re-scored under epoch 16: 0.8656) | 60 | 0.0899 |
| held by the states with final >= 0.95 (not listed) | 35 | 0.0058 |
| behaviour | 13 | 0.0337 |
| measurement (a scorer fix moves it as a correction) | 2 | 0.0076 (shown offline 0.0022: sass as_sass; hypothesis 0.0054: ec_dh; purrr attr_getter fixed in epoch 17) |
| capability | 4 | 0.0140 (all R's RNG stream under the harness's `set.seed(42)`: caret_s3, update_train, Arrows, boxplot_bclust) |
| out of reach | 4 | 0.0266 (aes_cbc, glyph_raster, ragg agg_capture; bslib page_fillable pending the py-shiny markup decision, 0.0105; shape_text left on 2026-11-21) |
| unknown | 2 | 0.0022 (ragg agg_webp_anim, broom augment_felm) |
| **reachable gap** (1 - mean final - out of reach) | | **0.061 to 0.063** (unknown counted both ways; noise floor about ±0.03, twice it 0.06: **at the headroom limit**; 2026-11-21, epoch 17) |

| share >= 0.95 (secondary) | states | share |
|---|---|---|
| room (1 - share 0.583 under epoch 17, 0.567 under epoch 16; the epoch-9 replay re-scored 0.550; held-out 0.565) | 25 | 0.417 |
| out of reach | 4 | 0.067 |
| unknown | 2 | 0.033 |
| **reachable room** | | **0.317 to 0.350** (noise floor of a replay about ±0.09, twice it 0.18; 2026-11-21, epoch 17) |

The 8 states at 0.90-0.95 were added on 2026-11-14 with the cut. In each, at least one of the 3 chains stopped
because its best reached the loop's stop threshold 0.9 (16 threshold stops of 24 chains; the replay's `stop`
counts), so the threshold, not the model, ended them below 0.95.

## States

| state | final | points | class | evidence | set |
|---|---|---|---|---|---|
| bslib page_fillable | 0.368 | 0.0105 | out of reach (pending a scoring decision) | Epoch 12, offline (`work/analysis/tempfile_names.py`): the 151 `tempfile:*.woff2` keys (fonts bslib caches) reach no score (removed: 0.324 -> 0.368, inside its repeat range 0.29-0.37); they only fill the feedback. What loses is `ui` data 0.157: R's bslib renders `<body class="bslib-page-fill ...` and py-shiny `<html><head></head><body ...` (text similarity 0.63). Two libraries' markup; whether py-shiny's markup should count is the open "py-shiny vs R shiny markup" scoring decision (October). | 2026-11-15 |
| ggplot2 geom_bin_2d | 0.500 | 0.0083 | behaviour | Never improved in the replay (4 catastrophic crashing rewrites of 9); patience-dsflash reached +0.178 on it. | 2026-11-14 |
| openssl aes_cbc | 0.550 | 0.0075 | out of reach | `aes_cbc_encrypt` defaults to `iv = rand_bytes(16)`; R's `serialize` bytes (cycle of 2026-10-17). | 2026-11-14 |
| openssl ec_dh | 0.675 | 0.0054 | measurement (hypothesis) | Epoch 10: `alice_pub`/`bob_pub` sentinels now attributed score 0.25; R's key objects cannot be serialized, so R's bundle is empty and an entity Python computes is penalised. Hypothesis, not tested (IMPROVEMENT_PLAN, epoch 10). | 2026-11-14 |
| bslib value_box | 0.678 | 0.0054 | behaviour (corrected; faithfulness flagged) | Corrected after threshold-095: a continuation reached 0.9999 by building bslib's value_box HTML in Python (`_value_box_html`, about 110 lines). A port of bslib's markup rather than py-shiny; whether that is a faithful translation is for the person (flagged in the audit). The 151 `tempfile:*.woff2` keys reach no score. default-e16-replay: 0.678 (0.923 in the epoch-9 replay): one sample's draw. | 2026-11-15 |
| ragg agg_capture | 0.700 | 0.0050 | out of reach (hypothesis) | `raster`/`raster_n` are pixel arrays of R's AGG device (480 vs 432 rows); exact pixels need R's renderer. Stopped at the threshold: 1 of 3 chains. Epoch 15: 0.905 -> 0.500. The old Python capture closed `cap.fig` after `cap`, so the program's `cap()` read back a blank canvas that matched R's mostly white raster (0.78); the program now runs as on its own and reads back its plot (`raster` 0.25). Its `agg_capture` creates the figure under `cap`, where R starts no page (`plot` 1.0 -> 0.5). | 2026-11-16 |
| recipes step_kpca | 0.716 | 0.0047 | behaviour (hypothesis) | Feedback names a missing figure (R=1, Python=0: the ggplot) and kPCA values (`kpca_te` 0.25, `kpca_estimates` 0.35); chains went 0.56-0.73 with 21 probes, none adding the figure. kernlab's kPCA numerics not checked. | 2026-11-15 |
| e1071 boxplot_bclust | 0.734 | 0.0044 | capability (R's RNG stream) | `bclust` runs k-means with random starts; the harness seeds R (`set.seed(42)`), so `bc1` centers match only by reproducing R's Mersenne Twister and k-means draws (as caret_s3 did once). | 2026-11-15 |
| caret caret_s3 | 0.750 | 0.0042 | capability | Reached 1.0 in one width chain of patience-dsflash by reimplementing R's Mersenne Twister and `sample()`; no other chain did. | 2026-11-14 |
| systemfonts glyph_raster | 0.786 | 0.0036 | out of reach | Glyph bitmaps need the font engine; programs that match paste R's metrics (model-screen audit). | 2026-11-14 |
| shape Arrows | 0.829 | 0.0028 | capability (R's RNG stream) | `x0 <- runif(100, ...)` etc. under the harness's `set.seed(42)`: `x0`, `y0` 0.25 and the arrow plots depend on R's draws. The rest (curve, xd) is graphics feedback as getellipse. Epoch 15: later `Arrows` calls now land on the `plot` pages (`plot`, `plot_1`, `plot_2` 0.6 -> 0.786, `curve`, `plot_3` -> 1.0); what is left is R's RNG stream. | 2026-11-16 |
| caret update_train | 0.845 | 0.0026 | capability (R's RNG stream) | `train(..., trControl = trainControl(method = "cv"))`: `knnFit1` results (Accuracy, Kappa) and seeds come from R's fold draws; 0/13 numeric fields found. As caret_s3. | 2026-11-15 |
| sass as_sass | 0.867 | 0.0022 | measurement (shown offline) | `input` 0.25: R's value is the Sass text with `@import "...RtmpCgcbhs/variables5e00e5c1d6a"` (R's temp path), Python's the same text with its own temp path (`...Rtmpd5KSNZ/variablesdcbf739e872b`). The temp-path rule (2026-10-18) treats whole-string paths only; a temp path inside a string scores 0. The FILES key `tempfile:variables5e00e5c1d6a` (R's random name) reaches no score (removed: 0.8674 -> 0.8676) but tops every entity's feedback. (`work/analysis/entity_zero.py`, `tempfile_names.py`) | 2026-11-15 |
| isoband isoband3_s2 | 0.869 | 0.0022 | behaviour | feedback-e10 reached 0.869 (same score under the old rule: a better program). Epoch 15: R's page starts at `grid.newpage` (grid.draw draws on it); the final creates its figure at `grid.draw`, so `grid.newpage` scores R=1 Python=0. A translation that opens its figure at `grid.newpage` matches the attribution. | 2026-11-16 |
| farver convert_colour | 0.890 | 0.0018 | behaviour | feedback-e10 reached 0.890 (marked `spec_lab`); some chains pasted `convert_colour` outputs (model-screen audit). default-e16-replay: 0.890; its 8 new literals are colour-science constants (D65/D50 white points, CIE kappa 24389), not R outputs. | 2026-11-14 |
| prodlim backGround | 0.900 | 0.0017 | behaviour (measurement part fixed in epoch 15) | 9 rewrites, all `unchanged`; `plot(0,0)` scores plotted similarity exactly 0.000 and R records no figure at the `backGround` calls (draws on the open plot). The feedback gives a similarity, not the difference. Suspected measurement (exact 0 on a one-point plot), not shown. Epoch 15 (`work/analysis/graphics_meta_dump_epoch15.txt`): two faults were measurement: the Python capture closed figures at each checkpoint, so `backGround`'s drawing became a page of its own while R draws it on `plot`'s page; and R's one-point series arrived unboxed (`py` 0, read as nothing plotted). Fixed: `plot` 0.5 -> 0.75. What is left is the program: the final draws the background (23 bars) on a new figure at `backGround`, R on the open page. default-e16-replay: 0.900. | 2026-11-16 |
| textshaping get_font_features | 0.904 | 0.0016 | behaviour (hypothesis) | Only `sys_fonts` loses (0.71): R lists 406 fonts, Python 405 and in another order (`Barrio` first). October: Python can read the same font files. In feedback-e10 a new run on it ended 0.217 lower. threshold-095-e16 (2026-11-21): a chain continued at 0.95 reached 0.960, no new literal. | 2026-11-21 |
| rvest html_children | 0.905 | 0.0016 | behaviour (since epoch 14) | Epoch 13: `html`, `ul`, `p` written as forged fingerprint dicts (a `_node` helper); refused, 0.25 each ("Python has no text form"; `ul[0]`, `p[0]`: lists of nodes). `html_children*` 1.0. As html_table. Epoch 14: the start program, with real lxml nodes, scores `ul` and `p` 1.0 (start 0.605 -> 0.905, check 20261116_0930), so the state is reachable; the default final forged instead. default-e16-replay: 0.905, real lxml nodes, no forging. | 2026-11-15 |
| textshaping shape_text | 0.912 | 0.0015 | behaviour (the stop threshold) | Font metrics, as glyph_raster; 3 literal-check rejections in the replay. default-e16-replay: 0.912 with no new 4-digit literal (`work/replay_default_e16/audit.txt`): the class is in doubt. threshold-095-e16 (2026-11-21): a chain continued at 0.95 reached 0.970 with no new 4-digit literal (audit read); not out of reach. | 2026-11-21 |
| sass sass_import | 0.917 | 0.0014 | behaviour (corrected) | Corrected after threshold-095: two continuations reached 0.977, so the printed temp path does not block it. FILES key `tempfile:file522c7cde307a.scss` reaches no score (removed: 0.9065 -> 0.9059). | 2026-11-15 |
| pROC coords | 0.921 | 0.0013 | behaviour (the stop threshold) | Enters with default-e16-replay (0.921); two accepted intermediate programs wrote `__r2py_fp__` dicts (refused since epoch 13), the final does not. threshold-095-e16 (2026-11-21): a chain continued at threshold 0.95 reached 0.968 (t90 chains +0.019). | 2026-11-21 |
| openssl certificates | 0.926 | 0.0012 | behaviour | `chain` 0.25: the final binds `chain` under the `print` entity; at `chain` it only defines `download_ssl_cert`, so nothing is recorded there. (Network value: R's capture holds the CRAN certificate valid 2025-12-16 to 2027-01-16.) | 2026-11-15 |
| ragg agg_webp_anim | 0.933 | 0.0011 | unknown | Enters with default-e16-replay (0.933). threshold-095-e16 (2026-11-21): no gain in 17 calls at 0.95 nor in 10 at 0.9. Not read. | 2026-11-21 |
| broom augment_felm | 0.935 | 0.0011 | unknown | Enters with default-e16-replay (0.935, 0.961 in the epoch-9 replay); the final writes three `__r2py_fp__` dicts, refused since epoch 13, so the forging costs it. Not read further. | 2026-11-16 |
| systemfonts shape_string | 0.942 | 0.0010 | behaviour (corrected) | Corrected after threshold-095: a continuation reached 0.981 by reading the font file with fontTools (`shape_string`, 289 lines, no pasted decimals; literal_check and review passed). Not out of reach; the default's chains had pasted metrics instead. | 2026-11-15 |
