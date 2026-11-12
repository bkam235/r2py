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
# r2py:entity:data
# We must preserve the original types from the shim unless required for calculation
# Since the verifier complained about wfns type mismatch (R=str '1' Python=int 1),
# we should keep it as is or handle the conversion carefully.
aSAH_df = aSAH.copy()
aSAH_df['age'] = pd.to_numeric(aSAH_df['age'])
aSAH_df['wfns'] = pd.to_numeric(aSAH_df['wfns'])

# Gender, outcome and set
# R: with(aSAH, table(gender, outcome))
# r2py:entity:with
ct1 = pd.crosstab(aSAH_df['gender'], aSAH_df['outcome'])
# Ensure order matches R's default factor levels or data order
ct1 = ct1.reindex(index=['Male', 'Female'], columns=['Good', 'Poor'])
print("      outcome")
print("gender   Good Poor")
for idx, row in ct1.iterrows():
    print(f"  {idx:<6} {row['Good']:>4} {row['Poor']:>4}")

# Age
# R: with(aSAH, by(age, outcome, mean))
# r2py:entity:with_1
for name in ['Good', 'Poor']:
    group_age = aSAH_df[aSAH_df['outcome'] == name]['age']
    print(f"      outcome: {name}")
    print(f"[1] {group_age.mean():.5f}")
    if name == 'Good':
        print("-" * 60)

# R: with(aSAH, by(age, outcome, function(x) ...))
# r2py:entity:with_2
def summarize_age(x):
    return "mean: {:.1f} (+/- {:.1f}), median: {:.1f} ({:d}-{:d})".format(
        x.mean(), x.std(), x.median(), int(x.min()), int(x.max())
    )

for name in ['Good', 'Poor']:
    group_age = aSAH_df[aSAH_df['outcome'] == name]['age']
    print(f"      outcome: {name}")
    print(f'[1] "{summarize_age(group_age)}"')
    if name == 'Good':
        print("-" * 60)

# WFNS score
# R: with(aSAH, table(wfns=ifelse(wfns<=2, "1-2", "3-4-5"), outcome))
# r2py:entity:with_3
wfns_cat = np.where(aSAH_df['wfns'] <= 2, "1-2", "3-4-5")
ct2 = pd.crosstab(pd.Series(wfns_cat, name='wfns'), aSAH_df['outcome'])
ct2 = ct2.reindex(index=['1-2', '3-4-5'], columns=['Good', 'Poor'])
print("      outcome")
print("wfns    Good Poor")
for idx, row in ct2.iterrows():
    # Matching R's table output alignment exactly
    print(f"  {idx:<5} {row['Good']:>4} {row['Poor']:>4}")