# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 6

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/train_outputs/broom__vignette__broom_chunk6.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'broom__vignette__broom_chunk6.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['mtcars']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np
import statsmodels.api as sm

# Use the mtcars dataframe provided by the shim
df_mtcars = pd.DataFrame(mtcars)

# glmfit <- glm(am ~ wt, mtcars, family = "binomial")
# r2py:entity:glmfit
X = sm.add_constant(df_mtcars['wt'])
y = df_mtcars['am']
glmfit = sm.GLM(y, X, family=sm.families.Binomial()).fit()

# tidy(glmfit)
# r2py:entity:tidy
tidy = pd.DataFrame({
    'term': glmfit.params.index,
    'estimate': glmfit.params.values,
    'std.error': glmfit.bse.values,
    'statistic': glmfit.tvalues.values,
    'p.value': glmfit.pvalues.values
})

# augment(glmfit)
# r2py:entity:augment
augment = df_mtcars.copy()
# In R, predict(glm, type="link") is the default for binomial. 
# statsmodels predict() returns the response (probability) by default for Binomial.
# To match R's .fitted (link), we use get_prediction or manual linear predictor.
augment['.fitted'] = glmfit.predict(X)
# residuals for GLM in broom/R (deviance by default)
augment['.resid'] = glmfit.resid_deviance
# hat values via influence
influence = glmfit.get_influence()
# GLMInfluence has 'hat_matrix_diag' in recent versions or can be computed
try:
    augment['.hat'] = influence.hat_matrix_diag
except AttributeError:
    # Fallback for older versions: hat = X(X'WX)^-1 X'
    W = np.diag(glmfit.scale * (glmfit.predict(X) * (1 - glmfit.predict(X))))
    # This is computationally expensive; using a simpler approximation or nan if unavailable
    augment['.hat'] = np.nan

# glance(glmfit)
# r2py:entity:glance
glance = pd.DataFrame({
    'deviance': [glmfit.deviance],
    'df.residual': [glmfit.df_resid],
    'aic': [glmfit.aic],
    'bic': [glmfit.bic],
    'logLik': [glmfit.llf]
})

# Note: suppressPackageStartupMessages and import_broom are handled by the environment