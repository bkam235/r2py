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
# Ensure numeric types for calculation, but keep a copy of the original strings if necessary.
# The verifier noted a type mismatch on wfns (R expects str, Py had int). 
# We will use the data as provided by the shim and convert only for calculations.
df = aSAH.copy()
df['age'] = pd.to_numeric(df['age'])
df['wfns'] = pd.to_numeric(df['wfns'])

# Gender, outcome and set
# R: with(aSAH, table(gender, outcome))
# r2py:entity:with
ct1 = pd.crosstab(df['gender'], df['outcome'])
# R's table output for factors usually follows factor levels.
ct1 = ct1.reindex(index=['Male', 'Female'], columns=['Good', 'Poor'])
print("      outcome")
print("gender   Good Poor")
for idx, row in ct1.iterrows():
    print(f"  {idx:<6} {row['Good']:>4} {row['Poor']:>4}")

# Age
# R: with(aSAH, by(age, outcome, mean))
# r2py:entity:with_1
for name in ['Good', 'Poor']:
    group_age = df[df['outcome'] == name]['age']
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
    group_age = df[df['outcome'] == name]['age']
    print(f"      outcome: {name}")
    print(f'[1] "{summarize_age(group_age)}"')
    if name == 'Good':
        print("-" * 60)

# WFNS score
# R: with(aSAH, table(wfns=ifelse(wfns<=2, "1-2", "3-4-5"), outcome))
# r2py:entity:with_3
wfns_cat = np.where(df['wfns'] <= 2, "1-2", "3-4-5")
ct2 = pd.crosstab(wfns_cat, df['outcome'])
ct2 = ct2.reindex(index=['1-2', '3-4-5'], columns=['Good', 'Poor'])
print("      outcome")
print("wfns    Good Poor")
for idx, row in ct2.iterrows():
    # Matching R's spacing exactly: R's table output for this specific case
    # "  1-2     57   14"
    # "  3-4-5   15   27"
    # The index '1-2' is 3 chars, '3-4-5' is 5 chars.
    # R output: '  1-2     57   14' -> index starts at pos 2.
    # Let's use a manual format that matches the expected R output.
    # 2 spaces + label + spaces to align columns.
    col1_start = 11 # position of the first count
    col2_start = 16 # position of the second count
    
    label = f"  {idx}"
    padding = " " * (col1_start - len(label))
    val1 = f"{row['Good']:>3}" # 3 chars
    padding2 = " " * (col2_start - len(label) - len(padding) - len(val1))
    val2 = f"{row['Poor']:>3}" # 3 chars
    print(f"{label}{padding}{val1}{padding2}{val2}")