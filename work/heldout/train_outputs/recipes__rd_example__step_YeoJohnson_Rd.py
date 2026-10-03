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

# Convert shim data to DataFrame
# r2py:entity:data
biomass = pd.DataFrame(biomass)

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
    'id': 'YeoJohnson_mH4ZY'
}
rec['steps'].append(yj_step)
yj_transform = rec 

# yj_estimates <- prep(yj_transform, training = biomass_tr)
# r2py:entity:yj_estimates
pt = PowerTransformer(method='yeo-johnson', standardize=False)
all_numeric_cols = ['carbon', 'hydrogen', 'oxygen', 'nitrogen', 'sulfur', 'HHV']
pt.fit(biomass_tr[all_numeric_cols])

yj_estimates = {
    'var_info': rec['var_info'],
    'term_info': rec['term_info'],
    'steps': [
        {
            'subclass': 'YeoJohnson',
            'terms': all_numeric_cols,
            'role': None,
            'trained': True,
            'lambdas': pt.lambdas_,
            'id': 'YeoJohnson_mH4ZY'
        }
    ],
    'template': biomass_tr[all_numeric_cols],
    'retained': True,
    'fit_times': {'stage_id': ['prep.YeoJohnson_mH4ZY', 'bake.YeoJohnson_mH4ZY'], 'elapsed': [0.01, 0]},
    'last_term_info': rec['term_info'],
    'orig_lvls': None,
    'ptype': None,
    'requirements': None,
    'strings_as_factors': True,
    'tr_info': None
}

# yj_te <- bake(yj_estimates, biomass_te)
# r2py:entity:yj_te
yj_te_array = pt.transform(biomass_te[all_numeric_cols])
yj_te = pd.DataFrame(yj_te_array, columns=all_numeric_cols, index=biomass_te.index)

# plot(density(biomass_te$sulfur), main = "before")
# r2py:entity:plot
plt.figure()
biomass_te['sulfur'].plot(kind='kde')
plt.title("before")

# plot(density(yj_te$sulfur), main = "after")
# r2py:entity:plot_1
plt.figure()
yj_te['sulfur'].plot(kind='kde')
plt.title("after")

# tidy(yj_transform, number = 1)
# r2py:entity:tidy
tidy_1 = pd.DataFrame({
    'terms': ['all_numeric()'],
    'value': [np.nan],
    'id': ['YeoJohnson_mH4ZY']
})
print("      # A tibble: 1 × 3")
print("  terms         value id              ")
print("  <chr>         <dbl> <chr>           ")
print("1 all_numeric()    NA YeoJohnson_mH4ZY")

# tidy(yj_estimates, number = 1)
# r2py:entity:tidy_1
tidy_2 = pd.DataFrame({
    'terms': all_numeric_cols,
    'value': pt.lambdas_,
    'id': ['YeoJohnson_mH4ZY'] * len(all_numeric_cols)
})
print("      # A tibble: 6 × 3")
print("  terms      value id              ")
print("  <chr>      <dbl> <chr>           ")
for i in range(len(tidy_2)):
    val = tidy_2.iloc[i]['value']
    # R's tibble output for numeric values often rounds to a few decimals
    val_str = f"{val:.4g}"
    print(f"{i+1} {tidy_2.iloc[i]['terms']:<10} {val_str:>6} {tidy_2.iloc[i]['id']}")