import pandas as pd
import numpy as np
from plotnine import ggplot, aes, geom_point, coord_fixed
from sklearn.preprocessing import PowerTransformer, StandardScaler
from sklearn.decomposition import KernelPCA

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/train_outputs/recipes__rd_example__step_kpca_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'recipes__rd_example__step_kpca_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['biomass']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

# r2py:entity:biomass_tr
biomass_tr = biomass[biomass['dataset'] == 'Training'].copy()
# r2py:entity:biomass_te
biomass_te = biomass[biomass['dataset'] == 'Testing'].copy()

# r2py:entity:rec
predictors = ['carbon', 'hydrogen', 'oxygen', 'nitrogen', 'sulfur']
target = 'HHV'
rec = {
    "recipe": "HHV ~ carbon + hydrogen + oxygen + nitrogen + sulfur",
    "data": biomass_tr,
    "steps": [],
    "var_info": pd.DataFrame({
        "variable": predictors + [target],
        "role": ["predictor"] * len(predictors) + ["outcome"]
    })
}

# r2py:entity:kpca_trans
# Representing the pipeline sequence
kpca_trans = {
    "recipe": rec["recipe"],
    "steps": [
        {"step": "step_YeoJohnson", "terms": "all_numeric_predictors()", "id": "YeoJohnson_1"},
        {"step": "step_normalize", "terms": "all_numeric_predictors()", "id": "normalize_1"},
        {"step": "step_kpca", "terms": "all_numeric_predictors()", "id": "kpca_ZqWlz"}
    ],
    "var_info": rec["var_info"].copy()
}

# r2py:entity:kpca_estimates
# Prep logic
yj = PowerTransformer(method='yeo-johnson')
tr_yj = yj.fit_transform(biomass_tr[predictors])

scaler = StandardScaler()
tr_scaled = scaler.fit_transform(tr_yj)

# recipes::step_kpca defaults to kernlab::kpca with kernel 'rbfdot' and sigma = 0.2.
# gamma for sklearn's rbf = 1 / (2 * sigma^2) = 1 / (2 * 0.04) = 12.5
kpca = KernelPCA(n_components=5, kernel='rbf', gamma=12.5)
tr_kpca = kpca.fit_transform(tr_scaled)

kpca_estimates = {
    "steps": kpca_trans["steps"],
    "trained_models": [yj, scaler, kpca],
    "var_info": kpca_trans["var_info"].copy(),
    "term_info": pd.DataFrame({
        "variable": [f"kPC{i+1}" for i in range(5)],
        "role": ["predictor"] * 5
    })
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
# tidy(kpca_trans, number = 3) -> Returns the 3rd step info
tidy = pd.DataFrame({
    "terms": ["all_numeric_predictors()"],
    "id": ["kpca_ZqWlz"]
})

# r2py:entity:tidy_1
# tidy(kpca_estimates, number = 3) -> Returns the terms for the 3rd step after prep
tidy_1 = pd.DataFrame({
    "terms": predictors,
    "id": ["kpca_ZqWlz"] * len(predictors)
})