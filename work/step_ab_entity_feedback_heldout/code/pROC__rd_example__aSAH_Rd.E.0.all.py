# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 7

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'pROC__rd_example__aSAH_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['aSAH']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np

# Load dataset
# R: data(aSAH)
# aSAH is already loaded by the data_shim.
# To match R's internal data types (wfns as strings/factors), we keep them as is or cast carefully.
aSAH['age'] = pd.to_numeric(aSAH['age'])
aSAH['wfns'] = pd.to_numeric(aSAH['wfns'])

# Gender, outcome and set
# R: with(aSAH, table(gender, outcome))
ct1 = pd.crosstab(aSAH['gender'], aSAH['outcome'])
# Ensure categories match R's factor ordering if necessary
ct1 = ct1.reindex(index=['Male', 'Female'], columns=['Good', 'Poor'])
print("      outcome")
print("gender   Good Poor")
for idx, row in ct1.iterrows():
    print(f"  {idx:<6} {row['Good']:>4} {row['Poor']:>4}")

# Age
# R: with(aSAH, by(age, outcome, mean))
for name in ['Good', 'Poor']:
    group_age = aSAH[aSAH['outcome'] == name]['age']
    header = f"      outcome: {name}" if name == 'Good' else f"outcome: {name}"
    print(header)
    print(f"[1] {group_age.mean():.5f}")
    if name == 'Good':
        print("-" * 60)

# R: with(aSAH, by(age, outcome, function(x) ...))
def summarize_age(x):
    return "mean: {:.1f} (+/- {:.1f}), median: {:.1f} ({:d}-{:d})".format(
        x.mean(), x.std(), x.median(), int(x.min()), int(x.max())
    )

for name in ['Good', 'Poor']:
    group_age = aSAH[aSAH['outcome'] == name]['age']
    header = f"      outcome: {name}" if name == 'Good' else f"outcome: {name}"
    print(header)
    print(f'[1] "{summarize_age(group_age)}"')
    if name == 'Good':
        print("-" * 60)

# WFNS score
# R: with(aSAH, table(wfns=ifelse(wfns<=2, "1-2", "3-4-5"), outcome))
wfns_cat = np.where(aSAH['wfns'] <= 2, "1-2", "3-4-5")
ct2 = pd.crosstab(wfns_cat, aSAH['outcome'])
ct2 = ct2.reindex(index=['1-2', '3-4-5'], columns=['Good', 'Poor'])
print("      outcome")
print("wfns    Good Poor")
for idx, row in ct2.iterrows():
    # Precise spacing to match R's table output
    print(f"  {idx:<5} {row['Good']:>4} {row['Poor']:>4}")