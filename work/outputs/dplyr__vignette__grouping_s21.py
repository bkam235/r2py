# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 7

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'dplyr__vignette__grouping_s21.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['starwars']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np

# Convert shim data to DataFrame
starwars = pd.DataFrame(starwars)

# Overall rank
# r2py:entity:select
res1 = starwars[['name', 'homeworld', 'height']]
# r2py:entity:mutate
res1 = res1.assign(rank=res1['height'].rank(method='min').astype('Int64'))
print(res1)

# Rank per homeworld
# r2py:entity:select_1
res2 = starwars[['name', 'homeworld', 'height']]
# r2py:entity:mutate_1
res2 = res2.assign(rank=res2.groupby('homeworld')['height'].rank(method='min').astype('Int64'))
print(res2)