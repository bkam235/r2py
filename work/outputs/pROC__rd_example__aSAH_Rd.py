# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 7

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/outputs/pROC__rd_example__aSAH_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'pROC__rd_example__aSAH_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['aSAH']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np

# Load the dataset
# r2py:entity:data
df = pd.DataFrame(aSAH)

# Ensure numeric types for calculations
df['age'] = pd.to_numeric(df['age'])
df['wfns'] = pd.to_numeric(df['wfns'])

# Gender, outcome and set
# with(aSAH, table(gender, outcome))
# r2py:entity:with
gender_order = ['Male', 'Female']
outcome_order = ['Good', 'Poor']
ct_gender = pd.crosstab(df['gender'], df['outcome'])
ct_gender = ct_gender.reindex(index=gender_order, columns=outcome_order)
print("      outcome")
print("gender   Good Poor")
for idx, row in ct_gender.iterrows():
    print(f"  {idx:6} {row['Good']:4} {row['Poor']:4}")

# Age
# with(aSAH, by(age, outcome, mean))
# r2py:entity:with_1
means = df.groupby('outcome', sort=False)['age'].mean()
for outcome in outcome_order:
    print(f"      outcome: {outcome}")
    print(f"[1] {means[outcome]:.5f}")
    if outcome != outcome_order[-1]:
        print("-" * 60)

# with(aSAH, by(age, outcome, function(x) ...))
# r2py:entity:with_2
def summarize_age(x):
    return f"mean: {x.mean():.1f} (+/- {x.std():.1f}), median: {x.median():.1f} ({int(x.min())}-{int(x.max())})"

summaries = df.groupby('outcome', sort=False)['age'].apply(summarize_age)
for outcome in outcome_order:
    print(f"      outcome: {outcome}")
    print(f'[1] "{summaries[outcome]}"')
    if outcome != outcome_order[-1]:
        print("-" * 60)

# WFNS score
# with(aSAH, table(wfns=ifelse(wfns<=2, "1-2", "3-4-5"), outcome))
# r2py:entity:with_3
df['wfns_cat'] = np.where(df['wfns'] <= 2, "1-2", "3-4-5")
ct_wfns = pd.crosstab(df['wfns_cat'], df['outcome'])
ct_wfns = ct_wfns.reindex(index=['1-2', '3-4-5'], columns=outcome_order)
print("      outcome")
print("wfns    Good Poor")
for idx, row in ct_wfns.iterrows():
    print(f"  {idx:5} {row['Good']:4} {row['Poor']:4}")