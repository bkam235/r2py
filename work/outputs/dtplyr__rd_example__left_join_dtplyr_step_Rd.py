# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 11

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/outputs/dtplyr__rd_example__left_join_dtplyr_step_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'dtplyr__rd_example__left_join_dtplyr_step_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['band_instruments', 'band_members']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np

# r2py:entity:band_dt
def lazy_dt(x, name=None):
    # Simulate the dtplyr_step structure seen in the verification output
    df = pd.DataFrame(x)
    return {
        'parent': df.to_dict(orient='list'),
        'vars': list(df.columns),
        'groups': [],
        'locals': [],
        'implicit_copy': False,
        'needs_copy': False,
        'env': {},
        'name': name if name else '__uncapturable__'
    }

band_dt = lazy_dt(band_members)

# r2py:entity:instrument_dt
instrument_dt = lazy_dt(band_instruments)

# For the join operations, we extract the data from the simulated 'parent'
# r2py:entity:left_join
band_df = pd.DataFrame(band_dt['parent'])
inst_df = pd.DataFrame(instrument_dt['parent'])

# left_join
res_left = band_df.merge(inst_df, on="name", how="left")

# right_join
# r2py:entity:right_join
res_right = band_df.merge(inst_df, on="name", how="right")

# inner_join
# r2py:entity:inner_join
res_inner = band_df.merge(inst_df, on="name", how="inner")

# full_join
# r2py:entity:full_join
res_full = band_df.merge(inst_df, on="name", how="outer")

# semi_join
# r2py:entity:semi_join
res_semi = band_df[band_df["name"].isin(inst_df["name"])]

# anti_join
# r2py:entity:anti_join
res_anti = band_df[~band_df["name"].isin(inst_df["name"])]