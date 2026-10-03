# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 12

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/train_outputs/caret__rd_example__lift_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'caret__rd_example__lift_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['letters', 'lift1', 'lift2']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import string

# r2py:entity:set.seed
np.random.seed(1)

# To match R's runif(200) better, we can't easily without a specific R-engine, 
# but we maintain the logic.
# r2py:entity:simulated
simulated = pd.DataFrame({
    'obs': pd.Categorical(np.repeat(list(string.ascii_lowercase[:2]), 100), categories=list(string.ascii_lowercase[:2])),
    'perfect': np.sort(np.random.uniform(0, 1, 200))[::-1],
    'random': np.random.uniform(0, 1, 200)
})

# r2py:entity:lift1
def lift(formula, data):
    parts = formula.split('~')
    target_var = parts[0].strip()
    feature_vars = [f.strip() for f in parts[1].split('+')]
    
    df = data.copy()
    # R's factor levels: the first level is usually the positive class for lift
    pos_class = df[target_var].cat.categories[0]
    p_overall = (df[target_var] == pos_class).mean()
    
    all_lift_data = []
    
    for feat in feature_vars:
        # Sort by predictor in descending order (Standard for lift charts)
        sorted_df = df.sort_values(by=feat, ascending=False).reset_index(drop=True)
        
        lifts = []
        pcts = []
        for i in range(1, 11):
            cutoff = int(np.ceil(i * 0.1 * len(sorted_df)))
            subset = sorted_df.iloc[:cutoff]
            p_bin = (subset[target_var] == pos_class).mean()
            lifts.append(p_bin / p_overall)
            pcts.append(i * 10.0)
            
        feat_df = pd.DataFrame({
            'lift': lifts,
            'cuts': list(range(1, 11)),
            'pct': pcts,
            'liftModelVar': [feat] * 10
        })
        all_lift_data.append(feat_df)
        
    res_data = pd.concat(all_lift_data).reset_index(drop=True)
    
    return {
        'data': res_data,
        'call': f"lift(formula = {formula}, data = simulated)",
        'class': pos_class,
        'probNames': feature_vars,
        'pct': list(range(10, 110, 10))
    }

lift1 = lift('obs ~ random', data=simulated)

# r2py:entity:lift1_1
lift1_df = lift1['data']
# r2py:entity:xyplot
plt.figure()
plt.plot(lift1_df['cuts'], lift1_df['lift'], marker='o')
plt.xlabel("Cut-Off")
plt.ylabel("Lift")
plt.show()

# r2py:entity:lift2
lift2 = lift('obs ~ random + perfect', data=simulated)

# r2py:entity:lift2_1
lift2_df = lift2['data']

# r2py:entity:xyplot_1
plt.figure()
for var in lift2_df['liftModelVar'].unique():
    subset = lift2_df[lift2_df['liftModelVar'] == var]
    plt.plot(subset['cuts'], subset['lift'], marker='o', label=var)
plt.xlabel("Cut-Off")
plt.ylabel("Lift")
plt.legend(ncol=2)
plt.show()

# R: xyplot(lift2, auto.key = list(columns = 2), value = c(10, 30))
# In caret::lift's xyplot, 'value' (when passed to the underlying lattice call) 
# often refers to the y-axis limits in this context.
# r2py:entity:xyplot_2
plt.figure()
for var in lift2_df['liftModelVar'].unique():
    subset = lift2_df[lift2_df['liftModelVar'] == var]
    plt.plot(subset['cuts'], subset['lift'], marker='o', label=var)
plt.ylim(10, 30)
plt.xlabel("Cut-Off")
plt.ylabel("Lift")
plt.legend(ncol=2)
plt.show()

# R: xyplot(lift2, plot = "lift", auto.key = list(columns = 2))
# r2py:entity:xyplot_3
plt.figure()
for var in lift2_df['liftModelVar'].unique():
    subset = lift2_df[lift2_df['liftModelVar'] == var]
    plt.plot(subset['cuts'], subset['lift'], marker='o', label=var)
plt.axhline(y=1, color='gray', linestyle='--')
plt.xlabel("Cut-Off")
plt.ylabel("Lift")
plt.legend(ncol=2)
plt.show()