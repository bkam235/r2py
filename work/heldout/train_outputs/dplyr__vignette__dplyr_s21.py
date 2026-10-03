# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 3

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'dplyr__vignette__dplyr_s21.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['starwars']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np

# Convert the shimmed dictionary to a DataFrame
starwars = pd.DataFrame(starwars)

# Translation of the dplyr pipeline:
# group_by(starwars, species, sex)
# select(..., height, mass)
# summarise(height = mean(height, na.rm = TRUE), mass = mean(mass, na.rm = TRUE))

# r2py:entity:summarise
result = (
    starwars.groupby(['species', 'sex'], as_index=False)[['height', 'mass']]
    .mean(numeric_only=True)
)