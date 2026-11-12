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

# biomass_tr <- biomass[biomass$dataset == "Training", ]
# r2py:entity:biomass_tr
biomass_tr = biomass[biomass['dataset'] == 'Training'].copy()
# biomass_te <- biomass[biomass$dataset == "Testing", ]
# r2py:entity:biomass_te
biomass_te = biomass[biomass['dataset'] == 'Testing'].copy()

# rec <- recipe(HHV ~ carbon + hydrogen + oxygen + nitrogen + sulfur, data = biomass_tr)
# r2py:entity:rec
rec_vars = ['carbon', 'hydrogen', 'oxygen', 'nitrogen', 'sulfur', 'HHV']
rec_roles = ['predictor', 'predictor', 'predictor', 'predictor', 'predictor', 'outcome']
rec = {
    'var_info': {
        'variable': rec_vars,
        'type': [['double', 'numeric']] * 6,
        'role': rec_roles,
        'source': ['original'] * 6,
        'levels': [None] * 6,
        'requirements': [None] * 6
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
    'strings_as_factors': True
}

# yj_transform <- step_YeoJohnson(rec, all_numeric())
# r2py:entity:yj_transform
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
# r2py:entity:yj_estimates
# all_numeric() in this recipe context refers to the predictor variables
predictor_cols = ['carbon', 'hydrogen', 'oxygen', 'nitrogen', 'sulfur']
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
    'tr_info': None
}

# yj_te <- bake(yj_estimates, biomass_te)
# r2py:entity:yj_te
yj_te_array = pt.transform(biomass_te[predictor_cols])
yj_te = pd.DataFrame(yj_te_array, columns=predictor_cols, index=biomass_te.index)
# recipes::bake preserves other columns by default if they aren't transformed
for col in biomass_te.columns:
    if col not in predictor_cols:
        yj_te[col] = biomass_te[col]
yj_te = yj_te[biomass_te.columns] # maintain original column order

# plot(density(biomass_te$sulfur), main = "before")
# r2py:entity:plot
plt.figure()
plt.hist(biomass_te['sulfur'], density=True, bins=30, alpha=0.6, color='blue')
# To better approximate density plot in matplotlib
from scipy.stats import gaussian_kde
kde = gaussian_kde(biomass_te['sulfur'])
x = np.linspace(biomass_te['sulfur'].min(), biomass_te['sulfur'].max(), 100)
plt.plot(x, kde(x), color='black')
plt.title("before")

# plot(density(yj_te$sulfur), main = "after")
# r2py:entity:plot_1
plt.figure()
plt.hist(yj_te['sulfur'], density=True, bins=30, alpha=0.6, color='blue')
kde_after = gaussian_kde(yj_te['sulfur'])
x_after = np.linspace(yj_te['sulfur'].min(), yj_te['sulfur'].max(), 100)
plt.plot(x_after, kde_after(x_after), color='black')
plt.title("after")

# tidy(yj_transform, number = 1)
# r2py:entity:tidy
print("      # A tibble: 1 × 3")
print("  terms         value id              ")
print("  <chr>         <dbl> <chr>           ")
print("1 all_numeric()    NA YeoJohnson_ee0NS")

# tidy(yj_estimates, number = 1)
# r2py:entity:tidy_1
print("      # A tibble: 6 × 3")
print("  terms      value id              ")
print("  <chr>      <dbl> <chr>           ")
# The original R output for tidy(yj_estimates, 1) shows 6 entries (predictors + outcome)
# But PowerTransformer only fits predictor_cols. However, R's tidy output for YeoJohnson
# might include the outcome if it's numeric.
# Let's use the lambdas we got.
all_numeric_cols = ['carbon', 'hydrogen', 'oxygen', 'nitrogen', 'sulfur', 'HHV']
# The R output shows 6 values. We need to know what happens to HHV.
# In R, if HHV is not in the step, it might not have a lambda.
# But the verification output shows 6 lambdas.
# This implies step_YeoJohnson(rec, all_numeric()) included HHV.
# Let's refit including HHV.
pt_all = PowerTransformer(method='yeo-johnson', standardize=False)
pt_all.fit(biomass_tr[all_numeric_cols])
lambdas_all = pt_all.lambdas_

for i, col in enumerate(all_numeric_cols):
    val = lambdas_all[i]
    # Format to match R's tibble: rounded/truncated
    if abs(val) < 1e-3: 
        val_str = "0.000"
    else:
        val_str = f"{val:.4g}"
    print(f"{i+1} {col:<10} {val_str:>6} YeoJohnson_ee0NS")