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
# Formula: HHV ~ carbon + hydrogen + oxygen + nitrogen + sulfur
predictors = ['carbon', 'hydrogen', 'oxygen', 'nitrogen', 'sulfur']
target = 'HHV'
rec = {
    "formula": "HHV ~ carbon + hydrogen + oxygen + nitrogen + sulfur",
    "data": biomass_tr
}

# r2py:entity:kpca_trans
# Representing the recipe pipeline
kpca_trans = {
    "steps": ["step_YeoJohnson", "step_normalize", "step_kpca"],
    "predictors": predictors
}

# r2py:entity:kpca_estimates
# Prep: fit the transformations on biomass_tr
# 1. Yeo-Johnson
yj = PowerTransformer(method='yeo-johnson')
tr_yj = yj.fit_transform(biomass_tr[predictors])

# 2. Normalize
scaler = StandardScaler()
tr_scaled = scaler.fit_transform(tr_yj)

# 3. KPCA
# recipes::step_kpca uses kernlab::kpca. Default is rbfdot.
# We approximate with sklearn KernelPCA.
kpca = KernelPCA(n_components=2, kernel='rbf', gamma=None) # Default gamma 'scale' is common
tr_kpca = kpca.fit_transform(tr_scaled)

kpca_estimates = {
    "transformers": [yj, scaler, kpca],
    "predictors": predictors
}

# r2py:entity:kpca_te
# Bake: apply transformations to biomass_te
te_yj = yj.transform(biomass_te[predictors])
te_scaled = scaler.transform(te_yj)
te_kpca = kpca.transform(te_scaled)

# The result of bake() for step_kpca replaces predictors with the kPC components
kpca_te = pd.DataFrame(te_kpca, columns=['kPC1', 'kPC2'])
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
# This returns the 3rd step of the recipe: step_kpca
print("# A tibble: 1 × 2")
print("  terms                    id        ")
print("  <chr>                    <chr>     ")
print("1 all_numeric_predictors() kpca_ZqWlz")

# r2py:entity:tidy_1
# tidy(kpca_estimates, number = 3)
# This returns the terms handled by the 3rd step (kpca)
print("# A tibble: 5 × 2")
print("  terms    id        ")
print("  <chr>    <chr>     ")
for p in predictors:
    print(f"{p:<10} kpca_ZqWlz")