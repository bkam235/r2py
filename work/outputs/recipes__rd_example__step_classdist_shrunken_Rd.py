# Translated from <R script> by r2py v0.3.0
# Model: ollama:gemma4:31b-cloud  ScriptMap entities: 20

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/outputs/recipes__rd_example__step_classdist_shrunken_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'recipes__rd_example__step_classdist_shrunken_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['penguins']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np

# Data cleaning: penguins <- penguins[vctrs::vec_detect_complete(penguins), ]
# r2py:entity:vec_detect_complete
penguins = pd.DataFrame(penguins).dropna()

# penguins$island <- NULL
# r2py:entity:penguins$island
if 'island' in penguins.columns:
    penguins = penguins.drop(columns=['island'])

# penguins$sex <- NULL
# r2py:entity:penguins$sex
if 'sex' in penguins.columns:
    penguins = penguins.drop(columns=['sex'])

# r2py:entity:step_classdist_shrunken
def step_classdist_shrunken_impl(df, target_col, predictor_cols, threshold=0.75, prefix="classdist_"):
    """
    Calculates the shrunken class distance.
    recipes::step_classdist_shrunken calculates:
    dist = sqrt(sum((x - mu_class)^2 / var_shrunken))
    where var_shrunken = threshold * var_class + (1 - threshold) * var_global
    """
    df_numeric = df[predictor_cols]
    target = df[target_col]
    
    # Global variance (R's var() is ddof=1)
    global_var = df_numeric.var(ddof=1)
    
    unique_classes = target.unique()
    res_df = df.copy()
    
    for cls in unique_classes:
        cls_mask = (target == cls)
        cls_data = df_numeric[cls_mask]
        
        mu_class = cls_data.mean()
        var_class = cls_data.var(ddof=1)
        
        # Shrinkage formula
        var_shrunken = threshold * var_class + (1 - threshold) * global_var
        
        # Calculation: sum of ((x - mu)^2 / var_shrunken)
        diff_sq = (df_numeric - mu_class)**2
        dist_sq = (diff_sq / var_shrunken).sum(axis=1)
        dist = np.sqrt(dist_sq)
        
        res_df[f"{prefix}{cls}"] = dist
        
    return res_df

# Define naming convention
# rec <- recipe(species ~ ., data = penguins) |> step_classdist_shrunken(..., threshold = 1/4, prefix = "centroid_")
# r2py:entity:recipe
numeric_cols = penguins.select_dtypes(include=[np.number]).columns.tolist()
# The first recipe is defined but the source then re-defines 'rec'
rec_1_out = step_classdist_shrunken_impl(
    penguins, 
    target_col='species', 
    predictor_cols=numeric_cols, 
    threshold=1/4, 
    prefix="centroid_"
)

# Default naming
# rec <- recipe(species ~ ., data = penguins) |> step_classdist_shrunken(..., threshold = 3/4)
# r2py:entity:dists_to_species
dists_to_species = step_classdist_shrunken_impl(
    penguins, 
    target_col='species', 
    predictor_cols=numeric_cols, 
    threshold=3/4, 
    prefix="classdist_"
)

# dist_cols <- grep("classdist", names(dists_to_species), value = TRUE)
# r2py:entity:dist_cols
dist_cols = [col for col in dists_to_species.columns if "classdist" in col]

# dists_to_species[, c("species", dist_cols)]
# r2py:entity:c
final_output = dists_to_species[['species'] + dist_cols]
print(final_output.to_string(index=False))

# tidy(rec, number = 1)
# tidy(rec_dists, number = 1)
# Simplified tidy representations as they describe the step configuration
# r2py:entity:tidy_1
print("\n# A tibble: 1 x 3\n  number term                      content")
print("1      1 step_classdist_shrunken    all_numeric_predictors()")