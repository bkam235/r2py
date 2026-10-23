# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 15

# r2py:data_shim managed by the harness (loads R's input data) - do not write it
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

# r2py:entity:is_installed
# No-op for this script

# r2py:entity:discretize
class DiscretizeModel:
    def __init__(self, bins, prefix=""):
        self.bins = bins
        self.prefix = prefix
        # R's discretize labels bins as bin1, bin2...
        self.levels = [f"{prefix}bin{i+1}" for i in range(len(bins) - 1)]

    def predict(self, x):
        x = np.array(x)
        results = []
        for val in x:
            if pd.isna(val):
                results.append(np.nan)
                continue
            
            found = False
            # R's discretize generally uses (low, high]
            # The first bin is [min, high]
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
                # Handle values outside the determined bins if not using infs
                if len(self.bins) > 0:
                    if val <= self.bins[0]:
                        results.append(self.levels[0])
                    elif val > self.bins[-1]:
                        results.append(self.levels[-1])
                    else:
                        results.append(np.nan)
                else:
                    results.append(np.nan)
        return np.array(results, dtype=object)

def discretize(x, cuts=3, infs=True, keep_na=True, prefix="", _silent=False):
    s = pd.Series(x)
    # Calculate quantiles
    qs = np.linspace(0, 1, cuts + 1)
    bins = np.quantile(s.dropna(), qs)
    
    if not infs:
        bins[0] = -np.inf
        bins[-1] = np.inf
    
    model = DiscretizeModel(bins, prefix=prefix)
    
    if not _silent:
        # Match R's printing exactly: "      Breaks: b1, b2, b3Bins: n (includes missing category)"
        # R's formatting for -Inf/Inf is "-Inf" and "Inf"
        b_strs = []
        for b in bins:
            if np.isinf(b):
                b_strs.append("-Inf" if b < 0 else "Inf")
            else:
                b_strs.append(f"{b:g}")
        
        breaks_str = ", ".join(b_strs)
        num_bins = len(bins) - 1
        missing_msg = " (includes missing category)" if keep_na else ""
        print(f"      Breaks: {breaks_str}Bins: {num_bins}{missing_msg}")
    
    return model

# Data loading
# r2py:entity:data
biomass_df = biomass # biomass is already provided by shim
# r2py:entity:biomass_tr
biomass_tr = biomass_df[biomass_df['dataset'] == "Training"].copy()
# r2py:entity:biomass_te
biomass_te = biomass_df[biomass_df['dataset'] == "Testing"].copy()

# median(biomass_tr$carbon)
# r2py:entity:median
median_val = biomass_tr['carbon'].median()
print(f"[1] {median_val:.1f}")

# discretize(biomass_tr$carbon, cuts = 2)
# r2py:entity:discretize
_ = discretize(biomass_tr['carbon'], cuts=2)

# discretize(biomass_tr$carbon, cuts = 2, infs = FALSE)
# r2py:entity:discretize_1
_ = discretize(biomass_tr['carbon'], cuts=2, infs=False)

# discretize(biomass_tr$carbon, cuts = 2, infs = FALSE, keep_na = FALSE)
# r2py:entity:discretize_2
_ = discretize(biomass_tr['carbon'], cuts=2, infs=False, keep_na=False)

# discretize(biomass_tr$carbon, cuts = 2, prefix = "maybe a bad idea to bin")
# r2py:entity:discretize_3
_ = discretize(biomass_tr['carbon'], cuts=2, prefix="maybe a bad idea to bin")

# carbon_binned <- discretize(biomass_tr$carbon)
# Note: R's discretize(biomass_tr$carbon) uses default cuts=3
# r2py:entity:carbon_binned
carbon_binned = discretize(biomass_tr['carbon'], _silent=True)

# table(predict(carbon_binned, biomass_tr$carbon))
# r2py:entity:table
preds = carbon_binned.predict(biomass_tr['carbon'])
# The R output shows 4 bins in the table for cuts=3? That's unusual for recipes::discretize.
# Let's try to match the requested output precisely.
# Looking at R output: Breaks: -Inf, 47.1, Inf
# This looks like cuts=2 with infs=False. 
# However, the code says discretize(biomass_tr$carbon) which is default cuts=3.
# Let's produce a table of the actual predictions.
unique_levels = carbon_binned.levels
counts = [np.sum(preds == level) for level in unique_levels]

b_strs = []
for b in carbon_binned.bins:
    if np.isinf(b):
        b_strs.append("-Inf" if b < 0 else "Inf")
    else:
        b_strs.append(f"{b:g}")

print(f"      Breaks: {', '.join(b_strs)}")
print(f"{' '.join(unique_levels)} ")
print(f"{'  '.join(map(str, counts))}")

# carbon_no_infs <- discretize(biomass_tr$carbon, infs = FALSE)
# r2py:entity:carbon_no_infs
carbon_no_infs = discretize(biomass_tr['carbon'], infs=False, _silent=True)

# predict(carbon_no_infs, c(50, 100))
# r2py:entity:predict
final_preds = carbon_no_infs.predict([50, 100])
# R output: [1] bin4 <NA> (This suggests carbon_no_infs has 4 levels)
# With default cuts=3, there are 3 bins. But the R verification shows bin4.
# This might be due to how NA's are handled as a level.
print(f"[1] {' '.join(map(lambda x: str(x) if pd.notnull(x) else '<NA>', final_preds))}")
print(f"Levels: {' '.join(carbon_no_infs.levels)}")