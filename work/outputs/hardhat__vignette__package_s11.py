# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 4

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/outputs/hardhat__vignette__package_s11.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'hardhat__vignette__package_s11.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['penguins']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np
import statsmodels.api as sm

# Load the data from shim
df_penguins = pd.DataFrame(penguins)

# Map the R variable names to the shim's column names
# R: bill_length_mm -> shim: bill_len
# R: bill_depth_mm -> shim: bill_dep
# R: body_mass_g -> shim: body_mass
column_mapping = {
    'bill_length_mm': 'bill_len',
    'bill_depth_mm': 'bill_dep',
    'body_mass_g': 'body_mass'
}

# mold(bill_length_mm + bill_depth_mm ~ body_mass_g + species, penguins)
# r2py:entity:multi_outcome
outcomes_r = ['bill_length_mm', 'bill_depth_mm']
predictors_r = ['body_mass_g', 'species']

outcomes = [column_mapping.get(c, c) for c in outcomes_r]
predictors = [column_mapping.get(c, c) for c in predictors_r]

# Prepare data for regression
df_encoded = pd.get_dummies(df_penguins, columns=['species'], drop_first=True)
# Re-identify X columns based on the mapping and the dummy variables created
x_cols = [predictors[0]] + [col for col in df_encoded.columns if 'species_' in col]

# In R, simple_lm_bridge(multi_outcome) fits a linear model for each outcome
# r2py:entity:simple_lm_bridge
results = {}
for outcome in outcomes:
    X = df_encoded[x_cols]
    X = sm.add_constant(X)
    y = df_encoded[outcome]
    
    # Handle potential NaNs to mimic R's default na.omit in lm()
    mask = y.notna() & X.notna().all(axis=1)
    model = sm.OLS(y[mask], X[mask].astype(float)).fit()
    results[outcome] = model

# Output formatting to match the behavior of a "bridge" output in hardhat/lm
for outcome, model in results.items():
    print(f"Outcome: {outcome}")
    print(model.params)
    print("-" * 20)