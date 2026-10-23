# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 12

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/outputs/broom__rd_example__data_frame_tidiers_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'broom__rd_example__data_frame_tidiers_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['mtcars']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np
from plotnine import ggplot, aes, geom_point, geom_text, scale_x_log10, scale_y_log10, geom_abline
from scipy.stats import skew, kurtosis

# r2py:entity:is_installed
def is_installed(pkg, version=None, compare=None):
    return True

# r2py:entity:td
def tidy(df):
    """
    Approximates broom::tidy for a data frame.
    R's broom::tidy(mtcars) produces summary stats for each numeric column.
    """
    df_numeric = pd.DataFrame(df) if isinstance(df, dict) else df
    df_numeric = df_numeric.select_dtypes(include=[np.number])
    
    results = []
    for col in df_numeric.columns:
        data = df_numeric[col].dropna()
        n = len(data)
        mean_val = data.mean()
        sd_val = data.std()
        median_val = data.median()
        
        # Trimmed mean (10% from each end)
        trimmed_val = data.quantile(0.1) # simplistic approximation
        # In R, trimmed mean is usually 10%
        low = data.quantile(0.1)
        high = data.quantile(0.9)
        trimmed_val = data[(data >= low) & (data <= high)].mean()
        
        mad_val = np.median(np.abs(data - median_val))
        min_val = data.min()
        max_val = data.max()
        range_val = max_val - min_val
        skew_val = skew(data)
        kurt_val = kurtosis(data)
        
        results.append({
            'column': col,
            'n': n,
            'mean': mean_val,
            'sd': sd_val,
            'median': median_val,
            'trimmed': trimmed_val,
            'mad': mad_val,
            'min': min_val,
            'max': max_val,
            'range': range_val,
            'skew': skew_val,
            'kurtosis': kurt_val
        })
    
    return pd.DataFrame(results)

# r2py:entity:glance
def glance(df):
    """
    Approximates broom::glance for a data frame.
    """
    df_numeric = pd.DataFrame(df) if isinstance(df, dict) else df
    df_numeric = df_numeric.select_dtypes(include=[np.number])
    return pd.DataFrame({
        'n': [len(df_numeric)],
        'mean_value': [df_numeric.values.mean()],
        'sd_value': [df_numeric.values.std()]
    })

# Execution
# Ensure mtcars is a DataFrame
mtcars_df = pd.DataFrame(mtcars)

td = tidy(mtcars_df)
print(td)

# r2py:entity:glance
print(glance(mtcars_df))

# Plotting
# compare mean and standard deviation
plot = (
# r2py:entity:ggplot
    ggplot(td, aes(x='mean', y='sd')) 
# r2py:entity:geom_point
    + geom_point() 
# r2py:entity:geom_text
    + geom_text(aes(label='column'), ha='right', va='top') 
# r2py:entity:scale_x_log10
    + scale_x_log10() 
# r2py:entity:scale_y_log10
    + scale_y_log10() 
# r2py:entity:geom_abline
    + geom_abline()
)
print(plot)