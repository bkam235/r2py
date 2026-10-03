# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 9

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'pROC__rd_example__groupGeneric_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['aSAH']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np
from sklearn.metrics import roc_auc_score

# Load data
# r2py:entity:data
aSAH = pd.DataFrame(aSAH)

# aucobj1 <- auc(roc(aSAH$outcome, aSAH$s100b))
# aSAH['outcome'] is 1 (Good) and 2 (Poor). roc_auc_score expects binary 0/1 or labels.
# pROC by default treats the second level as the case.
# r2py:entity:aucobj1
aucobj1 = roc_auc_score(aSAH['outcome'], aSAH['s100b'])

# aucobj2 <- auc(roc(aSAH$outcome, aSAH$wfns))
# r2py:entity:aucobj2
aucobj2 = roc_auc_score(aSAH['outcome'], aSAH['wfns'])

# sqrt(aucobj1)
# r2py:entity:sqrt
res_sqrt1 = np.sqrt(aucobj1)

# round(aucobj2, digits=1)
# r2py:entity:round
res_round = round(aucobj2, 1)

# aucobj1 * 2
res_mul1 = aucobj1 * 2

# 2 * aucobj2
res_mul2 = 2 * aucobj2

# aucobj1 + aucobj2
res_add = aucobj1 + aucobj2

# ciaucobj <- ci(aucobj1)
# pROC::ci for AUC returns [lower, auc, upper].
# Using bootstrap to approximate.
# r2py:entity:ciaucobj
boot_aucs = []
for i in range(2000):
    sample = aSAH.sample(frac=1, replace=True)
    if len(sample['outcome'].unique()) > 1:
        boot_aucs.append(roc_auc_score(sample['outcome'], sample['s100b']))
    else:
        # In case of single class sample, we skip or use a fallback
        pass

lower = np.percentile(boot_aucs, 2.5)
upper = np.percentile(boot_aucs, 97.5)
ciaucobj = np.array([lower, aucobj1, upper])

# ciaucobj * 2
res_ci_mul = ciaucobj * 2

# sqrt(ciaucobj)
# r2py:entity:sqrt_1
res_ci_sqrt = np.sqrt(ciaucobj)