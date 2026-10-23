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

# r2py:entity:biomass_tr
biomass_tr = biomass[biomass['dataset'] == 'Training'].copy()
# r2py:entity:biomass_te
biomass_te = biomass[biomass['dataset'] == 'Testing'].copy()

# r2py:entity:rec
predictors = ['carbon', 'hydrogen', 'oxygen', 'nitrogen', 'sulfur']
target = 'HHV'
rec = {
    "predictors": predictors,
    "target": target,
    "data": biomass_tr
}

# r2py:entity:kpca_trans
kpca_trans = {
    "steps": [
        {"name": "YeoJohnson", "terms": "all_numeric_predictors()", "id": "yj_1"},
        {"name": "normalize", "terms": "all_numeric_predictors()", "id": "norm_1"},
        {"name": "kpca", "terms": "all_numeric_predictors()", "id": "kpca_ZqWlz"}
    ],
    "predictors": predictors
}

# r2py:entity:kpca_estimates
# 1. Yeo-Johnson
yj = PowerTransformer(method='yeo-johnson')
tr_yj = yj.fit_transform(biomass_tr[predictors])

# 2. Normalize
scaler = StandardScaler()
tr_scaled = scaler.fit_transform(tr_yj)

# 3. KPCA
# R's recipes::step_kpca defaults to kernlab::kpca with kernel 'rbfdot'.
# Default sigma in kernlab is often 1 or based on data, but recipes often defaults to a specific range.
# Scikit-learn's KernelPCA 'rbf' is equivalent.
kpca = KernelPCA(n_components=5, kernel='rbf', gamma=None) # gamma=None uses 1/n_features
tr_kpca = kpca.fit_transform(tr_scaled)

kpca_estimates = {
    "transformers": [yj, scaler, kpca],
    "predictors": predictors,
    "kpca_components": 5
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
    + geom_point() 
    + coord_fixed()
)
print(plot)

# r2py:entity:tidy
# tidy(kpca_trans, number = 3)
tidy_trans = pd.DataFrame([
    {"terms": "all_numeric_predictors()", "id": "kpca_ZqWlz"}
])
print(tidy_trans)

# r2py:entity:tidy_1
# tidy(kpca_estimates, number = 3)
tidy_estimates = pd.DataFrame([
    {"terms": p, "id": "kpca_ZqWlz"} for p in predictors
])
print(tidy_estimates)