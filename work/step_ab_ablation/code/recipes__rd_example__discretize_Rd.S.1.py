# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 15

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'recipes__rd_example__discretize_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['biomass']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np

class DiscretizeModel:
    def __init__(self, bins, prefix=""):
        self.bins = bins
        self.prefix = prefix
        self.levels = [f"{prefix}bin{i+1}" for i in range(len(bins) - 1)]

    def predict(self, x):
        x = np.array(x)
        results = []
        for val in x:
            if pd.isna(val):
                results.append(np.nan)
                continue
            
            # R's discretize uses intervals (low, high] 
            # Except for the first bin which is [low, high]
            found = False
            for i in range(len(self.bins) - 1):
                low = self.bins[i]
                high = self.bins[i+1]
                if i == 0:
                    if low <= val <= high:
                        results.append(self.levels[i])
                        found = True
                        break
                else:
                    if low < val <= high:
                        results.append(self.levels[i])
                        found = True
                        break
            if not found:
                results.append(np.nan)
        return np.array(results, dtype=object)

def discretize(x, cuts=3, infs=True, keep_na=True, prefix=""):
    s = pd.Series(x)
    # R's quantile(x, probs = seq(0, 1, length.out = cuts + 1))
    qs = np.linspace(0, 1, cuts + 1)
    bins = np.quantile(s.dropna(), qs)
    
    if not infs:
        bins[0] = -np.inf
        bins[-1] = np.inf
    
    model = DiscretizeModel(bins, prefix=prefix)
    
    # Formatting to match R's discretize() print output
    breaks_str = ", ".join([f"{b:g}" for b in bins])
    print(f"      Breaks: {breaks_str}")
    print(f"Bins: {cuts}{' (includes missing category)' if keep_na else ''}")
    
    return model

# r2py:entity:biomass_tr
biomass_tr = biomass[biomass['dataset'] == "Training"].copy()
# r2py:entity:biomass_te
biomass_te = biomass[biomass['dataset'] == "Testing"].copy()

# r2py:entity:median
median_val = biomass_tr['carbon'].median()
print(f"[1] {median_val}")

# r2py:entity:discretize
_ = discretize(biomass_tr['carbon'], cuts=2)

# r2py:entity:discretize_1
_ = discretize(biomass_tr['carbon'], cuts=2, infs=False)

# r2py:entity:discretize_2
_ = discretize(biomass_tr['carbon'], cuts=2, infs=False, keep_na=False)

# r2py:entity:discretize_3
_ = discretize(biomass_tr['carbon'], cuts=2, prefix="maybe a bad idea to bin")

# r2py:entity:carbon_binned
carbon_binned = discretize(biomass_tr['carbon'])

# r2py:entity:table
preds = carbon_binned.predict(biomass_tr['carbon'])
counts = pd.Series(preds).value_counts().reindex(carbon_binned.levels).fillna(0).astype(int)
print(counts.to_string(header=False))

# r2py:entity:carbon_no_infs
carbon_no_infs = discretize(biomass_tr['carbon'], infs=False)

# r2py:entity:predict
final_preds = carbon_no_infs.predict([50, 100])
print(f"[1] {' '.join(map(str, final_preds))}")
print(f"Levels: {' '.join(carbon_no_infs.levels)}")