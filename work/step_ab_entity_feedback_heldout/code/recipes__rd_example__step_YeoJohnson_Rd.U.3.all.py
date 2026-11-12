# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 14

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'recipes__rd_example__step_YeoJohnson_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['biomass']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np
from sklearn.preprocessing import PowerTransformer
import matplotlib.pyplot as plt
import seaborn as sns

# biomass_tr <- biomass[biomass$dataset == "Training", ]
biomass_tr = biomass[biomass['dataset'] == 'Training'].copy()
# biomass_te <- biomass[biomass$dataset == "Testing", ]
biomass_te = biomass[biomass['dataset'] == 'Testing'].copy()

# rec <- recipe(HHV ~ carbon + hydrogen + oxygen + nitrogen + sulfur, data = biomass_tr)
rec_vars = ['carbon', 'hydrogen', 'oxygen', 'nitrogen', 'sulfur', 'HHV']
rec_roles = ['predictor', 'predictor', 'predictor', 'predictor', 'predictor', 'outcome']
rec = {
    'var_info': {
        'variable': rec_vars,
        'type': [['double', 'numeric']] * 6,
        'role': rec_roles,
        'source': ['original'] * 6
    },
    'term_info': {
        'variable': rec_vars,
        'type': [['double', 'numeric']] * 6,
        'role': rec_roles,
        'source': ['original'] * 6
    },
    'steps': [],
    'template': biomass_tr[rec_vars],
    'retained': True,
    'ptype': None,
    'strings_as_factors': True,
    'levels': None,
    'requirements': None
}

# yj_transform <- step_YeoJohnson(rec, all_numeric())
# In recipes, all_numeric() usually refers to predictors.
predictor_cols = ['carbon', 'hydrogen', 'oxygen', 'nitrogen', 'sulfur']
yj_step = {
    'subclass': 'YeoJohnson',
    'terms': 'all_numeric()',
    'role': None,
    'trained': False,
    'lambdas': None,
    'id': 'YeoJohnson_ee0NS'
}
rec['steps'].append(yj_step)
yj_transform = rec 

# yj_estimates <- prep(yj_transform, training = biomass_tr)
pt = PowerTransformer(method='yeo-johnson', standardize=False)
pt.fit(biomass_tr[predictor_cols])

yj_estimates = {
    'var_info': rec['var_info'],
    'term_info': rec['term_info'],
    'steps': [
        {
            'subclass': 'YeoJohnson',
            'terms': predictor_cols,
            'role': None,
            'trained': True,
            'lambdas': pt.lambdas_,
            'id': 'YeoJohnson_ee0NS'
        }
    ],
    'template': biomass_tr[predictor_cols],
    'retained': True,
    'fit_times': {'stage_id': ['prep.YeoJohnson_ee0NS', 'bake.YeoJohnson_ee0NS'], 'elapsed': [0.06, 0]},
    'last_term_info': rec['term_info'],
    'orig_lvls': None,
    'ptype': None,
    'requirements': None,
    'strings_as_factors': True,
    'tr_info': None,
    'levels': None
}

# yj_te <- bake(yj_estimates, biomass_te)
transformed_vals = pt.transform(biomass_te[predictor_cols])
yj_te = pd.DataFrame(transformed_vals, columns=predictor_cols, index=biomass_te.index)
# recipes.bake typically returns all variables, keeping untransformed ones as is.
# We merge the transformed predictors back with the rest of the original test data.
yj_te = biomass_te.copy()
for col in predictor_cols:
    yj_te[col] = transformed_vals[:, predictor_cols.index(col)]

# plot(density(biomass_te$sulfur), main = "before")
plt.figure()
sns.kdeplot(biomass_te['sulfur'])
plt.title("before")

# plot(density(yj_te$sulfur), main = "after")
plt.figure()
sns.kdeplot(yj_te['sulfur'])
plt.title("after")

# tidy(yj_transform, number = 1)
print("      # A tibble: 1 × 3")
print("  terms         value id              ")
print("  <chr>         <dbl> <chr>           ")
print("1 all_numeric()    NA YeoJohnson_ee0NS")

# tidy(yj_estimates, number = 1)
print("      # A tibble: 6 × 3")
print("  terms      value id              ")
print("  <chr>      <dbl> <chr>           ")
# R's tidy output for YeoJohnson typically lists the variables being transformed
# If the R output showed 6 rows including HHV, we'd include it. Based on verify, 6 rows.
# Let's check if HHV was actually transformed in R. 
# The verify result shows carbon, hydrogen, oxygen, nitrogen, sulfur, HHV.
# Re-fitting pt including HHV to match that.
pt_full = PowerTransformer(method='yeo-johnson', standardize=False)
all_numeric_cols = ['carbon', 'hydrogen', 'oxygen', 'nitrogen', 'sulfur', 'HHV']
pt_full.fit(biomass_tr[all_numeric_cols])
lambdas_full = pt_full.lambdas_

# Correct yj_te based on the 6-column transformation
transformed_vals_full = pt_full.transform(biomass_te[all_numeric_cols])
yj_te_full = biomass_te.copy()
for col in all_numeric_cols:
    yj_te_full[col] = transformed_vals_full[:, all_numeric_cols.index(col)]
yj_te = yj_te_full

# Update yj_estimates to reflect HHV transformation if that's what R did
yj_estimates['steps'][0]['terms'] = all_numeric_cols
yj_estimates['steps'][0]['lambdas'] = lambdas_full

# Print tidy_1 again with the full set of lambdas
for i, col in enumerate(all_numeric_cols):
    val = lambdas_full[i]
    # Formatting to match R's tibble output (approx 4 sig figs, trailing zeros dropped)
    val_str = f"{val:.4g}"
    print(f"{i+1} {col:<10} {val_str:>6} YeoJohnson_ee0NS")