# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 20

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/train_outputs/broom__rd_example__augment_felm_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'broom__rd_example__augment_felm_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['airquality']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np
from linearmodels.panel import PanelOLS
from linearmodels.iv import AbsorbingLS
import statsmodels.api as sm

# Load data
d = sm.datasets.get_rdataset("airquality").data

# r2py:entity:head
print(d.head())

# est0: Basic OLS (Ozone ~ Temp + Wind + Solar.R)
# Note: felm without fixed effects is equivalent to OLS
# r2py:entity:est0
X0 = sm.add_constant(d[['Temp', 'Wind', 'Solar.R']])
y0 = d['Ozone']
est0 = sm.OLS(y0, X0).fit()

# r2py:entity:tidy
print(est0.summary()) # Equivalent to tidy(est0)
# augment(est0) equivalent
# r2py:entity:augment
augment0 = pd.DataFrame({
    'fitted': est0.predict(X0),
    'resid': est0.resid
})
print(augment0)

# est1: Fixed Effects for Month (Ozone ~ Temp + Wind + Solar.R | Month)
# We set Month as the index for PanelOLS
# r2py:entity:est1
d_panel = d.set_index(['Month', d.index]) # Dummy entity is Month, time is observation index
X1 = sm.add_constant(d[['Temp', 'Wind', 'Solar.R']])
y1 = d['Ozone']
# entity_effects=True approximates felm(..., | Month)
est1 = PanelOLS(y1, X1, entity_effects=True).fit()

# r2py:entity:tidy_1
print(est1.summary) # Equivalent to tidy(est1)
# r2py:entity:tidy_2
# tidy(est1, fe=True) - in Python, PanelOLS summary typically omits the FE coefficients
# augment(est1)
# r2py:entity:augment_1
augment1 = pd.DataFrame({
    'fitted': est1.predict(),
    'resid': est1.resids
})
print(augment1)
# glance(est1)
# r2py:entity:glance
print(est1.rsquared, est1.nobs)

# SE types for est1
# r2py:entity:tidy_3
print(est1.fit(cov_type='unadjusted').summary) # se.type = "iid"
# r2py:entity:tidy_4
print(est1.fit(cov_type='robust').summary)     # se.type = "robust"

# est2: Fixed effects and Clustered SEs (Ozone ~ Temp + Wind + Solar.R | Month | 0 | Month)
# In felm: | Month (FE) | 0 (IV) | Month (Cluster)
# We use the same PanelOLS setup but change the cov_type to 'clustered'
# r2py:entity:est2
est2 = PanelOLS(y1, X1, entity_effects=True).fit(cov_type='clustered', cluster_entity=True)

# tidy(est2, conf.int = TRUE) - standard summary
# r2py:entity:tidy_5
print(est2.summary)

# tidy(est2, conf.int = TRUE, se.type = "cluster")
# r2py:entity:tidy_6
print(est2.fit(cov_type='clustered', cluster_entity=True).summary)

# tidy(est2, conf.int = TRUE, se.type = "robust")
# r2py:entity:tidy_7
print(est2.fit(cov_type='robust').summary)

# tidy(est2, conf.int = TRUE, se.type = "iid")
# r2py:entity:tidy_8
print(est2.fit(cov_type='unadjusted').summary)