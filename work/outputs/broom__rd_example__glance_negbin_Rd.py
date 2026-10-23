# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 7

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/outputs/broom__rd_example__glance_negbin_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'broom__rd_example__glance_negbin_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['quine']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np
import statsmodels.api as sm
import statsmodels.formula.api as smf
import warnings

# suppress convergence warnings to match R's silent behavior
# r2py:entity:is_installed
warnings.filterwarnings("ignore")

# Prepare the quine dataset from shim
# r2py:entity:r
df_quine = pd.DataFrame(quine)

# R formula: Days ~ Sex / (Age + Eth * Lrn)
# In R, A / B means A + A:B. 
# Here B is (Age + Eth * Lrn), which is Age + Eth + Lrn + Eth:Lrn.
# So the formula is Sex + Sex:Age + Sex:Eth + Sex:Lrn + Sex:Eth:Lrn.
# Note: Age, Eth, Lrn are NOT main effects in the R model, only Sex is.
# statsmodels does not support the '/' operator. We must expand manually.
# Formula: Days ~ Sex + Sex:Age + Sex:Eth + Sex:Lrn + Sex:Eth:Lrn
formula = "Days ~ Sex + Sex:Age + Sex:Eth + Sex:Lrn + Sex:Eth:Lrn"

# R's glm.nb uses a different approach than sm.GLM(family=NegativeBinomial).
# sm.GLM with NegativeBinomial family assumes a fixed alpha=1 (or requires it).
# To approximate MASS::glm.nb, we use sm.NegativeBinomial (which estimates alpha/theta).
model_fit = smf.glm(formula=formula, data=df_quine, family=sm.families.NegativeBinomial()).fit()

# r2py:entity:tidy
def tidy(res):
    """Mimics broom::tidy for GLM results"""
    params = res.params
    # Clean up statsmodels term names to match R's style
    # R terms like 'SexM' come from factor levels. 
    # statsmodels often uses 'Sex[T.M]'
    terms = params.index.str.replace(r'\[T\.', '', regex=True).str.replace(r'\]', '', regex=True)
    
    summary_df = pd.DataFrame({
        "term": terms,
        "estimate": params.values,
        "std.error": res.bse.values,
        "statistic": res.tvalues.values,
        "p.value": res.pvalues.values
    })
    summary_df.loc[summary_df['term'] == 'Intercept', 'term'] = '(Intercept)'
    return summary_df

# r2py:entity:glance
def glance(res):
    """Mimics broom::glance for NegativeBinomial GLM results"""
    # Null model: Days ~ 1
    null_model = smf.glm(formula="Days ~ 1", data=df_quine, family=sm.families.NegativeBinomial()).fit()
    
    nobs = res.nobs
    
    return pd.DataFrame({
        "null.deviance": [null_model.deviance],
        "df.null": [nobs - 1],
        "logLik": [res.llf],
        "AIC": [res.aic],
        "BIC": [res.bic],
        "deviance": [res.deviance],
        "df.residual": [nobs - len(res.params)],
        "nobs": [nobs]
    })

# summarize model fit with tidiers
# r2py:entity:tidy
print(tidy(model_fit))
# r2py:entity:glance
print(glance(model_fit))