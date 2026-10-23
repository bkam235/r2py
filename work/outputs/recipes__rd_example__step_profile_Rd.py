# Translated from <R script> by r2py v0.3.0
# Model: ollama:gemma4:31b-cloud  ScriptMap entities: 28

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/outputs/recipes__rd_example__step_profile_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'recipes__rd_example__step_profile_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['Sacramento', 'mpg', 'mtcars']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from plotnine import ggplot, aes, geom_point, facet_wrap

# Convert shim data to DataFrames
# r2py:entity:data
Sacramento = pd.DataFrame(Sacramento)
mtcars = pd.DataFrame(mtcars)

# r2py:entity:step_profile
def step_profile_implementation(df, profile_col, other_cols, grid_type='pctl', length=100):
    """
    Simulates recipes::step_profile.
    R's step_profile creates a grid for the profile variable and
    sets other variables to the value of the first row of the training data.
    """
    if grid_type == 'pctl':
        # R's seq(0, 1, length.out = 6) is [0, 0.2, 0.4, 0.6, 0.8, 1]
        # np.percentile handles this.
        vals = np.percentile(df[profile_col], np.linspace(0, 100, length))
    else:
        vals = np.linspace(df[profile_col].min(), df[profile_col].max(), length)
    
    grid_df = pd.DataFrame({profile_col: vals})
    
    for col in other_cols:
        # step_profile by default uses the first observation's value for other predictors
        grid_df[col] = df[col].iloc[0]
        
    # Reorder columns to match R output: [other_cols, profile_col]
    return grid_df[other_cols + [profile_col]]

# Section 1: Sacramento
# recipe(~ city + price + beds, data = Sacramento) |> step_profile(-beds, profile = beds)
# r2py:entity:recipe
sac_cols = ['city', 'price']
# r2py:entity:bake
sac_result = step_profile_implementation(Sacramento, 'beds', sac_cols, grid_type='pctl', length=6)
print(sac_result.to_string(index=False))

# Section 2: Linear Model
# lin_mod <- lm(mpg ~ poly(disp, 2) + cyl + hp, data = mtcars)
# poly(disp, 2) in R defaults to orthogonal polynomials. 
# For prediction on a grid, we can fit a standard polynomial model as it's mathematically equivalent
# to the orthogonal one for the purpose of generating predictions.
# r2py:entity:lin_mod
X_disp = mtcars['disp'].values
y = mtcars['mpg'].values
X_cyl = mtcars['cyl'].values
X_hp = mtcars['hp'].values

# Construct design matrix with x, x^2, cyl, hp
X_poly = np.column_stack([X_disp, X_disp**2, X_cyl, X_hp])
lin_mod = LinearRegression().fit(X_poly, y)

def predict_lin_mod(df):
    X_p = np.column_stack([df['disp'].values, df['disp'].values**2, df['cyl'].values, df['hp'].values])
    return lin_mod.predict(X_p)

# Section 3: Grid vs Percentile
# disp_pctl
# r2py:entity:pctl_data
pctl_data = step_profile_implementation(mtcars, 'disp', ['cyl', 'hp'], grid_type='pctl', length=100)
# r2py:entity:pctl_data_1
pctl_data['pred'] = predict_lin_mod(pctl_data)
pctl_data['method'] = 'percentile'

# disp_grid
# r2py:entity:grid_data
grid_data = step_profile_implementation(mtcars, 'disp', ['cyl', 'hp'], grid_type='grid', length=100)
# r2py:entity:grid_data_1
grid_data['pred'] = predict_lin_mod(grid_data)
grid_data['method'] = 'grid'

# r2py:entity:plot_data
plot_data = pd.concat([grid_data, pctl_data], ignore_index=True)

# Section 4: Plotting
# r2py:entity:ggplot
plot = (
    ggplot(plot_data, aes(x='disp', y='pred'))
# r2py:entity:geom_point
    + geom_point(alpha=0.5, size=1)
# r2py:entity:facet_wrap
    + facet_wrap('~method')
)

print(plot)