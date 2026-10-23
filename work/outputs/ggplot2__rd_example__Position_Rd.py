# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 6

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/outputs/ggplot2__rd_example__Position_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'ggplot2__rd_example__Position_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['mpg']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np
from plotnine import ggplot, aes, geom_point
from plotnine.data import mpg

# r2py:entity:position_rank
def position_rank(df, x_col, y_col, group_col, width=0.5):
    """
    Python implementation of a rank-based jitter/position adjustment.
    Since plotnine does not allow custom Position objects like ggplot2, 
    we preprocess the data.
    """
    df = df.copy()
    
    # Calculate rank within each group
    # rank() returns 1-based ranks; we subtract the mean and scale it
    df['rank'] = df.groupby(group_col)[y_col].rank(method='average')
    
    # Rescale rank to be centered around 0 within the specified width
    # Formula: (rank - mean) / range * width
    def rescale(series, width):
        if series.max() == series.min():
            return 0
        return ((series - series.mean()) / (series.max() - series.min())) * width

    df['x_offset'] = df.groupby(group_col)['rank'].transform(lambda x: rescale(x, width))
    
    # In plotnine, x is often categorical. To add offsets, 
    # we must convert the categorical x to numeric indices.
    categories = df[x_col].unique()
    cat_map = {cat: i for i, cat in enumerate(categories)}
    df['x_numeric'] = df[x_col].map(cat_map) + df['x_offset']
    
    return df

# Prepare the data
df_ranked = position_rank(mpg, 'drv', 'displ', 'drv', width=0.5)

# Plot using the adjusted numeric x values
# Note: we use a custom scale for x to keep the original labels
# r2py:entity:ggplot
plot = (
    ggplot(df_ranked, aes(x='x_numeric', y='displ')) 
# r2py:entity:geom_point
    + geom_point()
)

print(plot)