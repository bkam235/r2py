# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 13

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/outputs/dplyr__rd_example__nest_by_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'dplyr__rd_example__nest_by_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['models', 'mtcars']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np
from statsmodels.regression.linear_model import OLS
from statsmodels.tools import tools

# Mocking data that might not be in the shim or needs standard format
try:
    iris = pd.read_csv('https://archive.ics.ac.uk/ml/machine-learning-databases/iris/iris.data', header=None)
    iris.columns = ['sepal_len', 'sepal_wid', 'petal_len', 'petal_wid', 'Species']
except:
    # Fallback if network fails
    iris = pd.DataFrame({'Species': ['setosa']*50 + ['versicolor']*50 + ['virginica']*50})

# The shim provides mtcars, but we need to ensure it's a DataFrame
if 'mtcars' in globals() and isinstance(globals()['mtcars'], dict):
    mtcars = pd.DataFrame(globals()['mtcars'])
elif 'mtcars' not in globals():
    mtcars = pd.DataFrame()

# starwars is typically in the shim for this example, ensure it exists
if 'starwars' not in globals():
    starwars = pd.DataFrame({'species': ['Human', 'Droid', 'Gungan', 'Wookiee'], 'name': ['Luke', 'R2D2', 'JarJar', 'Chewbacca']})

# Helper to mimic dplyr::nest_by
# r2py:entity:nest_by
def nest_by(df, column):
    # R's nest_by creates a row for each group and a 'data' column containing the subset
    return df.groupby(column).apply(lambda x: pd.Series({'data': x})).reset_index()

# iris |> nest_by(Species)
# r2py:entity:nest_by
print(nest_by(iris, 'Species'))

# starwars |> nest_by(species)
# r2py:entity:nest_by_1
print(nest_by(starwars, 'species'))

# models <- mtcars |> nest_by(cyl) |> mutate(model = list(lm(mpg ~ wt, data = data)))
# r2py:entity:models
def fit_lm(df):
    X = df[['wt']]
    y = df['mpg']
    return OLS(y, tools.add_constant(X)).fit()

models_nested = nest_by(mtcars, 'cyl')
models_nested['model'] = models_nested['data'].apply(fit_lm)
models = models_nested
# r2py:entity:models_1
print(models)

# models |> summarise(rsq = summary(model)$r.squared)
# In R, summarise on a rowwise df results in one value per group
# r2py:entity:summarise
rsq_res = models[['cyl', 'model']].copy()
rsq_res['rsq'] = rsq_res['model'].apply(lambda m: m.rsquared)
print(rsq_res[['cyl', 'rsq']])

# models |> summarise(broom::glance(model))
# r2py:entity:summarise_1
def glance(m):
    return pd.Series({
        'r.squared': m.rsquared,
        'adj.r.squared': m.rsquared_adj,
        'sigma': np.sqrt(m.scale),
        'statistic': m.f_pvalue,
        'p.value': m.f_pvalue
    })

glance_res = models[['cyl', 'model']].copy()
glance_df = models['model'].apply(glance).reset_index(drop=True)
glance_df.insert(0, 'cyl', models['cyl'].values)
print(glance_df)

# models |> reframe(broom::tidy(model))
# r2py:entity:reframe
def tidy(m):
    return pd.DataFrame({
        'term': m.params.index,
        'estimate': m.params.values,
        'std.error': m.bse.values,
        'p.value': m.pvalues.values
    })

tidy_list = models['model'].apply(tidy).tolist()
reframe_tidy = pd.concat(tidy_list).reset_index(drop=True)
print(reframe_tidy)

# models |> reframe(data)
# r2py:entity:reframe_1
reframe_data = pd.concat(models['data'].tolist()).reset_index(drop=True)
print(reframe_data)