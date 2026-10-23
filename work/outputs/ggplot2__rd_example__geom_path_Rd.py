# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 38

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/outputs/ggplot2__rd_example__geom_path_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'ggplot2__rd_example__geom_path_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['economics', 'economics_long', 'x']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np
from plotnine import *

# Convert shim data to DataFrames
economics = pd.DataFrame(economics)
economics['date'] = pd.to_datetime(economics['date'])

economics_long = pd.DataFrame(economics_long)
economics_long['date'] = pd.to_datetime(economics_long['date'])

# geom_line() is suitable for time series
# r2py:entity:ggplot
(ggplot(economics, aes('date', 'unemploy')) 
# r2py:entity:geom_line
 + geom_line())

# separate by colour and use "timeseries" legend key glyph
# r2py:entity:ggplot_1
(ggplot(economics_long, aes('date', 'value01', colour='variable')) 
# r2py:entity:geom_line_1
 + geom_line())

# You can get a timeseries that run vertically by setting the orientation
# r2py:entity:ggplot_2
(ggplot(economics, aes('unemploy', 'date')) 
# r2py:entity:geom_line_2
 + geom_line())

# geom_step() is useful when you want to highlight exactly when the y value changes
# r2py:entity:as.Date
recent = economics[economics['date'] > pd.to_datetime("2013-01-01")]
# r2py:entity:ggplot_3
(ggplot(recent, aes('date', 'unemploy')) 
# r2py:entity:geom_line_3
 + geom_line())
# r2py:entity:ggplot_4
(ggplot(recent, aes('date', 'unemploy')) 
# r2py:entity:geom_step
 + geom_step())

# geom_path lets you explore how two variables are related over time
# r2py:entity:m
m = ggplot(economics, aes('unemploy/pop', 'psavert'))
# r2py:entity:geom_path
(m + geom_path())
# r2py:entity:geom_path_1
(m + geom_path(aes(colour='date')))

# Changing parameters ----------------------------------------------
# r2py:entity:ggplot_5
(ggplot(economics, aes('date', 'unemploy')) 
# r2py:entity:geom_line_4
 + geom_line(colour="red"))

# Use the arrow parameter to add an arrow to the line
# r2py:entity:c
c = ggplot(economics, aes(x='date', y='pop'))
# r2py:entity:geom_line_5
(c + geom_line())
# r2py:entity:geom_line_6
(c + geom_line())

# Control line join parameters
# r2py:entity:df
df = pd.DataFrame({'x': [1, 2, 3], 'y': [4, 1, 9]})
# r2py:entity:base
base = ggplot(df, aes('x', 'y'))
# r2py:entity:geom_path_2
(base + geom_path(size=10))
# r2py:entity:geom_path_3
(base + geom_path(size=10, lineend="round"))
# r2py:entity:geom_path_4
(base + geom_path(size=10, linejoin="mitre", lineend="butt"))

# You can use NAs to break the line.
# r2py:entity:df_1
df_1 = pd.DataFrame({'x': [1, 2, 3, 4, 5], 'y': [1, 2, np.nan, 4, 5]})
# r2py:entity:ggplot_6
(ggplot(df_1, aes('x', 'y')) 
# r2py:entity:geom_point
 + geom_point() 
# r2py:entity:geom_line_7
 + geom_line())

# Setting line type vs colour/size
# r2py:entity:x
x_vals = np.linspace(0.01, 0.99, 100)
def qlogis(p):
    return np.log(p / (1 - p))

# r2py:entity:df_2
df_2 = pd.DataFrame({
    'x': np.tile(x_vals, 2),
    'y': np.concatenate([qlogis(x_vals), 2 * qlogis(x_vals)]),
    'group': np.repeat(['a', 'b'], 100)
})

# r2py:entity:p
p = ggplot(df_2, aes(x='x', y='y', group='group'))
# r2py:entity:geom_line_8
(p + geom_line(linetype='dashed'))
# r2py:entity:geom_line_9
(p + geom_line(aes(colour='group'), linetype='dashed'))
# r2py:entity:geom_line_10
(p + geom_line(aes(colour='x')))

# r2py:entity:should_stop
def should_stop(expr):
    try:
        expr.draw()
        raise RuntimeError("No error!")
    except Exception as e:
        print(f"Caught expected error: {e}")

should_stop(p + geom_line(aes(colour='x'), linetype='dashed'))