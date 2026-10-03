# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 5

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/train_outputs/tidyr__vignette__tidy-data_s9.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'tidyr__vignette__tidy-data_s9.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['billboard', 'billboard2']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np

# Ensure billboard is a DataFrame
billboard = pd.DataFrame(billboard)

# pivot_longer(wk1:wk76, names_to = "week", values_to = "rank", values_drop_na = TRUE)
# r2py:entity:pivot_longer
cols_to_pivot = [f"wk{i}" for i in range(1, 77)]
id_vars = [col for col in billboard.columns if col not in cols_to_pivot]

# To mimic pivot_longer, we need to maintain the original row order.
# pandas.melt usually does this, but we ensure it by adding an index.
billboard_with_idx = billboard.copy()
billboard_with_idx['_orig_idx'] = range(len(billboard))

billboard2 = pd.melt(
    billboard_with_idx,
    id_vars=['_orig_idx'] + id_vars,
    value_vars=cols_to_pivot,
    var_name="week",
    value_name="rank"
)

# values_drop_na = TRUE
billboard2 = billboard2.dropna(subset=["rank"])

# R's pivot_longer sorts by original row first, then by the variable being pivoted.
# Since melt's order is (variable, original_row), we must sort to (original_row, variable).
billboard2 = billboard2.sort_values(by=['_orig_idx', 'week']).drop(columns=['_orig_idx'])
billboard2 = billboard2.reset_index(drop=True)

# r2py:entity:billboard2_1
print(billboard2)