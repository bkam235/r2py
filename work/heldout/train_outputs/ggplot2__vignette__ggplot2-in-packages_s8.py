# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 4

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/train_outputs/ggplot2__vignette__ggplot2-in-packages_s8.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'ggplot2__vignette__ggplot2-in-packages_s8.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['mpg']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np
from plotnine import ggplot, aes, geom_bar, facet_wrap
from plotnine.data import mpg

# r2py:entity:col_summary_1
def col_summary(df, col, by):
    return (
        ggplot(df)
        + geom_bar(mapping=aes(y=col))
        + facet_wrap(by)
    )

# r2py:entity:col_summary_1
col_summary(mpg, "drv", "year")