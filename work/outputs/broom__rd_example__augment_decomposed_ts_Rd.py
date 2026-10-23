# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 23

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/outputs/broom__rd_example__augment_decomposed_ts_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'broom__rd_example__augment_decomposed_ts_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['nottem']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np
from statsmodels.tsa.seasonal import seasonal_decompose, STL
from plotnine import ggplot, aes, geom_line

# R's nottem is a ts object.
def print_nottem(data):
    vals = np.array(data)
    years = np.arange(1920, 1940)
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    print("      ", "  ".join(months))
    for i, year in enumerate(years):
        row = vals[i*12 : (i+1)*12]
        row_str = " ".join([f"{x:4.1f}" if x % 1 != 0 else f"{x:4.0f}" for x in row])
        print(f"{year} {row_str}")

# r2py:entity:is_installed
# No-op in Python

# Print nottem as R does
print_nottem(nottem)

nottem_series = pd.Series(nottem)

# r2py:entity:d1
# R's decompose(nottem) uses additive model and moving averages.
res1 = seasonal_decompose(nottem_series, model='additive', period=12)
d1 = res1

# r2py:entity:d2
# stl(nottem, s.window = "periodic", robust = TRUE)
# In statsmodels, periodic is simulated by a large seasonal window. 
# Must be an odd integer >= 3.
res2 = STL(nottem_series, period=12, seasonal=101, robust=True).fit()
d2 = res2

# Helper for broom::tidy
# r2py:entity:cbind
def tidy(ts_data):
    return pd.DataFrame({'x': ts_data})

# Helper for broom::augment
def augment_decompose(res, original):
    # .seasadj in R's decompose is original - seasonal
    return pd.DataFrame({
        'seasonal': res.seasonal.values,
        'trend': res.trend.values,
        'random': res.resid.values,
        '.seasadj': (original - res.seasonal).values
    })

def augment_stl(res, original):
    return pd.DataFrame({
        'seasonal': res.seasonal,
        'trend': res.trend,
        'random': res.resid,
        '.seasadj': (original - res.seasonal).values
    })

# cbind(tidy(nottem), augment(d1), augment(d2))
combined = pd.concat([
    tidy(nottem_series),
    augment_decompose(res1, nottem_series),
    augment_stl(res2, nottem_series).add_prefix('stl_')
], axis=1)
print(combined)

# Visually compare seasonal decompositions
# r2py:entity:decomps
decomps_list = [
    {'series': pd.DataFrame({'x': nottem_series}), 'decomp': 'decompose', 'model': res1},
    {'series': pd.DataFrame({'x': nottem_series}), 'decomp': 'stl', 'model': res2}
]
decomps_df = pd.DataFrame(decomps_list)

# r2py:entity:mutate
def get_augment(row):
    if row['decomp'] == 'decompose':
        return augment_decompose(row['model'], nottem_series)
    else:
        return augment_stl(row['model'], nottem_series)

decomps_df['augment'] = decomps_df.apply(get_augment, axis=1)

final_data = []
# r2py:entity:rowwise
for idx, row in decomps_df.iterrows():
# r2py:entity:unnest
    series_df = row['series']
    aug_df = row['augment']
    temp = pd.concat([series_df, aug_df], axis=1)
    temp['decomp'] = row['decomp']
    final_data.append(temp)
# r2py:entity:group_by

decomps = pd.concat(final_data).reset_index(drop=True)

# r2py:entity:ungroup_1
decomps['index'] = decomps.groupby('decomp').cumcount() + 1

# r2py:entity:select
decomps = decomps[['decomp', 'index', 'x', '.seasadj']].rename(columns={'.seasadj': 'adjusted'})

# Plotting
# r2py:entity:ggplot
plot = (
    ggplot(decomps, aes(x='index'))
# r2py:entity:geom_line
    + geom_line(aes(y='x'), colour="black")
# r2py:entity:geom_line_1
    + geom_line(aes(y='adjusted', colour='decomp', group='decomp'))
)

print(plot)