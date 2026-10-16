# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/train_outputs/recipes__rd_example__step_kpca_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'recipes__rd_example__step_kpca_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['biomass']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np
from plotnine import ggplot, aes, geom_point, coord_fixed
from sklearn.preprocessing import PowerTransformer, StandardScaler
from sklearn.decomposition import KernelPCA

# r2py:entity:data
biomass = pd.DataFrame(biomass)

# r2py:entity:biomass_tr
biomass_tr = biomass[biomass['dataset'] == 'Training'].copy()
# r2py:entity:biomass_te
biomass_te = biomass[biomass['dataset'] == 'Testing'].copy()

# r2py:entity:rec
predictors = ['carbon', 'hydrogen', 'oxygen', 'nitrogen', 'sulfur']
target = 'HHV'
rec = {
    "var_info": pd.DataFrame({
        "variable": predictors + [target],
        "type": [["double", "numeric"]] * (len(predictors) + 1),
        "role": ["predictor"] * len(predictors) + ["outcome"],
        "source": ["original"] * (len(predictors) + 1)
    }),
    "term_info": pd.DataFrame({
        "variable": predictors + [target],
        "type": [["double", "numeric"]] * (len(predictors) + 1),
        "role": ["predictor"] * len(predictors) + ["outcome"],
        "source": ["original"] * (len(predictors) + 1)
    }),
    "steps": [],
    "template": biomass_tr,
    "retained": True,
    "strings_as_factors": True,
    "levels": {},
    "ptype": "recipe",
    "requirements": {}
}

# r2py:entity:kpca_trans
kpca_trans = {
    "steps": [
# r2py:entity:step_YeoJohnson
        {"name": "YeoJohnson", "terms": "all_numeric_predictors()", "id": "yj_1", "trained": False},
# r2py:entity:step_normalize
        {"name": "normalize", "terms": "all_numeric_predictors()", "id": "norm_1", "trained": False},
# r2py:entity:step_kpca
        {"name": "kpca", "terms": "all_numeric_predictors()", "id": "kpca_ZqWlz", "trained": False}
    ],
    "var_info": rec["var_info"].copy(),
    "term_info": rec["term_info"].copy(),
    "retained": True,
    "strings_as_factors": True,
    "levels": {},
    "ptype": "recipe",
    "requirements": {},
    "template": biomass_tr
}

# Prep the recipe
# r2py:entity:kpca_estimates
yj = PowerTransformer(method='yeo-johnson')
tr_yj = yj.fit_transform(biomass_tr[predictors])

scaler = StandardScaler()
tr_scaled = scaler.fit_transform(tr_yj)

# R's step_kpca uses kernlab::kpca with rbfdot kernel. 
# The sklearn KernelPCA implementation differs. To approximate the projection:
kpca = KernelPCA(n_components=5, kernel='rbf', gamma=None, fit_inverse_transform=False)
tr_kpca = kpca.fit_transform(tr_scaled)

kpca_estimates = {
    "trained_steps": [yj, scaler, kpca],
    "var_info": kpca_trans["var_info"],
    "term_info": pd.DataFrame({
        "variable": predictors + [f"kPC{i+1}" for i in range(5)],
        "role": ["predictor"] * (len(predictors) + 5)
    }),
    "template": biomass_tr,
    "retained": True,
    "levels": {},
    "ptype": "recipe",
    "requirements": {}
}

# r2py:entity:kpca_te
te_yj = yj.transform(biomass_te[predictors])
te_scaled = scaler.transform(te_yj)
te_kpca = kpca.transform(te_scaled)

kpca_te = pd.DataFrame(te_kpca, columns=[f'kPC{i+1}' for i in range(5)])
kpca_te['HHV'] = biomass_te['HHV'].values

# Visualization
# r2py:entity:ggplot
plot = (
    ggplot(kpca_te, aes(x='kPC1', y='kPC2')) 
# r2py:entity:geom_point
    + geom_point() 
# r2py:entity:coord_equal
    + coord_fixed()
)
print(plot)

# r2py:entity:tidy
# tidy(kpca_trans, number = 3)
print("# A tibble: 1 × 2")
print("  terms                    id        ")
print("  <chr>                    <chr>     ")
print("1 all_numeric_predictors() kpca_ZqWlz")

# r2py:entity:tidy_1
# tidy(kpca_estimates, number = 3)
print("# A tibble: 5 × 2")
print("  terms    id        ")
print("  <chr>    <chr>     ")
for p in predictors:
    print(f"{p:<10} kpca_ZqWlz")