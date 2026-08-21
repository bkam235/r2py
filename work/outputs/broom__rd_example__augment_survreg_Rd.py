# Translated from <R script> by r2py v0.3.0
# Model: ollama:gemma4:31b-cloud  ScriptMap entities: 14

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/outputs/broom__rd_example__augment_survreg_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'broom__rd_example__augment_survreg_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['ovarian']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np
from lifelines import WeibullAFTFitter
from plotnine import *

# Load dataset
from lifelines.datasets import load_ovarian

# survreg with dist="exponential" in R is equivalent to a Weibull AFT 
# with shape fixed to 1 in lifelines.
# r2py:entity:sr
aft = WeibullAFTFitter()
# In lifelines, the target columns are durations and event indicators
aft.fit(ovarian, duration_col='futime', event_col='fustat', formula="futime ~ ecog.ps + rx")

# tidy() equivalent: summary of coefficients
# r2py:entity:tidy
td = aft.summary[['coef', 'std err', 'p']]
td['conf_low'] = aft.confidence_interval_.iloc[:, 0]
td['conf_high'] = aft.confidence_interval_.iloc[:, 1]
td = td.reset_index()

# augment() equivalent: predicted values
# r2py:entity:augment
augment_df = ovarian.copy()
augment_df['predict'] = aft.predict_expectation(ovarian)

# glance() equivalent: model summary metrics
# r2py:entity:glance
glance_df = pd.DataFrame({
    'aic': [aft.AIC_],
    'bic': [aft.BIC_],
    'log_likelihood': [aft.log_likelihood_]
})

# Plotting
# r2py:entity:ggplot
plot = (
    ggplot(td, aes(x='coef', y='index'))
# r2py:entity:geom_point
    + geom_point()
# r2py:entity:geom_errorbarh
    + geom_errorbarh(aes(xmin='conf_low', xmax='conf_high'), height=0)
# r2py:entity:geom_vline
    + geom_vline(xintercept=0)
)

print(td)
print(augment_df.head())
print(glance_df)
print(plot)