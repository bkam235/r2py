# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 10

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/train_outputs/dplyr__rd_example__storms_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'dplyr__rd_example__storms_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['storms']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np
from plotnine import *

# storms
# r2py:entity:storms
storms = pd.DataFrame(storms)
print(storms)

# Show a few recent storm paths
# filter(year >= 2000)
# r2py:entity:filter
storms_filtered = storms[storms['year'] >= 2000].copy()

# Prepare color column for ggplot (paste(year, name))
storms_filtered['year_name'] = storms_filtered['year'].astype(str) + " " + storms_filtered['name']

# ggplot(aes(long, lat, color = paste(year, name)))
# r2py:entity:ggplot
plot = (
    ggplot(storms_filtered, aes(x='long', y='lat', color='year_name'))
    # geom_path(show.legend = FALSE)
# r2py:entity:geom_path
    + geom_path(show_legend=False)
    # facet_wrap(~year)
# r2py:entity:facet_wrap
    + facet_wrap('~year')
)

print(plot)

# storms
# r2py:entity:storms_1
print(storms)