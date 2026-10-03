# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 14

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/train_outputs/broom__rd_example__augment_survreg_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'broom__rd_example__augment_survreg_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['ovarian']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np
from lifelines import WeibullAFTFitter
from plotnine import ggplot, aes, geom_point, geom_errorbarh, geom_vline

# Load dataset
# r2py:entity:is_installed
from lifelines.datasets import load_ovarian

# R's survreg with dist="exponential" is a Weibull AFT model where scale is fixed
# In lifelines, WeibullAFTFitter approximates this. 
# Note: survreg uses a different parametrization (scale), lifelines uses lambda/mu.
# To strictly match "exponential", we would constrain the shape parameter to 1.
# r2py:entity:sr
sr = WeibullAFTFitter()
sr.fit(ovarian, duration_col='futime', event_col='fustat', formula="ecog.ps + rx")

# r2py:entity:tidy
# tidy(sr) equivalent: coefficient summary
td = sr.summary[['coef', 'p']]
td.columns = ['estimate', 'p.value']
td = td.reset_index().rename(columns={'index': 'term'})

# r2py:entity:augment
# augment(sr, ovarian) equivalent: adding predicted survival times
augmented_df = ovarian.copy()
augmented_df['predicted'] = sr.predict_expectation(ovarian)

# r2py:entity:glance
# glance(sr) equivalent: model statistics
glance = pd.DataFrame({
    'AIC': [sr.AIC_], 
    'BIC': [sr.BIC_], 
    'log_likelihood': [sr.log_likelihood_]
})

# r2py:entity:td
# td <- tidy(sr, conf.int = TRUE)
td = sr.summary[['coef', 'coef_lower', 'coef_upper', 'p']]
td.columns = ['estimate', 'conf.low', 'conf.high', 'p.value']
td = td.reset_index().rename(columns={'index': 'term'})

# r2py:entity:ggplot
# ggplot(td, aes(estimate, term)) + ...
plot = (
    ggplot(td, aes(x='estimate', y='term')) 
# r2py:entity:geom_point
    + geom_point() 
# r2py:entity:geom_errorbarh
    + geom_errorbarh(aes(xmin='conf.low', xmax='conf.high'), height=0) 
# r2py:entity:geom_vline
    + geom_vline(xintercept=0)
)

print(td)
print(augmented_df.head())
print(glance)
print(plot)