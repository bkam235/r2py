import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from plotnine import *

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'caret__rd_example__lift_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['letters', 'lift1', 'lift2']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

# r2py:entity:set.seed
np.random.seed(1)

# R's runif is different from np.random.rand. To match the shim or R's logic:
# letters[1:2] is 'a', 'b'
# r2py:entity:simulated
simulated = pd.DataFrame({
    'obs': np.repeat(['a', 'b'], 100),
    'perfect': np.sort(np.random.uniform(0, 1, 200))[::-1],
    'random': np.random.uniform(0, 1, 200)
})

# r2py:entity:lift2
def lift_impl(formula, data):
    # Formula: "obs ~ random + perfect"
    parts = formula.split('~')
    target_col = parts[0].strip()
    predictor_cols = [p.strip() for p in parts[1].split('+')]
    
    # R's lift usually looks at the first level of the factor
    event_val = data[target_col].unique()[0] 
    overall_rate = (data[target_col] == event_val).mean()
    
    all_model_data = []
    
    for col in predictor_cols:
        # Sort by predictor descending
        sorted_df = data[[target_col, col]].sort_values(by=col, ascending=False).reset_index(drop=True)
        
        # Create 10 bins
        bins = np.arange(0, 201, 20)
        lifts = []
        cuts = []
        for i in range(1, 11):
            cutoff = i * 20 # index for 20, 40... 200
            # Actually R's lift uses deciles (10%, 20%... 100% of population)
            # 10% of 200 is 20 samples
            n_samples = (i * 200) // 10
            top_slice = sorted_df.iloc[:n_samples]
            bin_rate = (top_slice[target_col] == event_val).mean()
            lifts.append(bin_rate / overall_rate)
            cuts.append(i * 10)
            
        model_df = pd.DataFrame({
            'liftModelVar': [col] * 10,
            'cuts': cuts,
            'lift': lifts
        })
        all_model_data.append(model_df)
    
    lift_df = pd.concat(all_model_data, ignore_index=True)
    
    return {
        'call': f"lift.formula(x = {formula}, data = simulated)",
        'class': 'lift',
        'probNames': predictor_cols,
        'pct': list(range(10, 110, 10)),
        'data': lift_df,
        'event': f"{event_val} ({overall_rate:.0%})"
    }

# r2py:entity:lift1_1
lift1 = lift_impl("obs ~ random", simulated)

print(f"Call:\n{lift1['call']}\n\nModels: {'-'.join(lift1['probNames']).replace('-', ', ')} \nEvent: {lift1['event']}")

# r2py:entity:xyplot
def plot_lift(lift_obj, values=None, plot_type="lift"):
    df = lift_obj['data']
    if values is not None:
        df = df[df['cuts'].isin(values)]
    
    p = (ggplot(df, aes(x='cuts', y='lift', color='liftModelVar', group='liftModelVar')) + 
         geom_line() + geom_point() + 
         labs(x="Cut-Off", y="Lift") + 
         theme_minimal())
    return p

p1 = plot_lift(lift1)
plt.show()

# r2py:entity:lift2_1
lift2 = lift_impl("obs ~ random + perfect", simulated)

print(f"Call:\n{lift2['call']}\n\nModels: {'-'.join(lift2['probNames']).replace('-', ', ')} \nEvent: {lift2['event']}")

# r2py:entity:xyplot_1
p2 = plot_lift(lift2)
plt.show()

# r2py:entity:xyplot_2
p3 = plot_lift(lift2, values=[10, 30])
plt.show()

# r2py:entity:xyplot_3
p4 = plot_lift(lift2, plot_type="lift")
plt.show()