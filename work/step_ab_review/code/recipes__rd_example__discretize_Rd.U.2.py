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

class DiscretizeModel:
    def __init__(self, bins, prefix="", infs=True):
        self.bins = bins
        self.prefix = prefix
        self.infs = infs
        # R creates bins based on the number of breaks - 1
        self.num_bins = len(bins) - 1
        self.levels = [f"{prefix}bin{i+1}" for i in range(self.num_bins)]

    def predict(self, x):
        x = np.array(x)
        results = []
        for val in x:
            if pd.isna(val):
                results.append(np.nan)
                continue
            
            # R's discretize use (low, high]
            # The first bin is [min, high]
            found = False
            for i in range(self.num_bins):
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
                # In R, values outside bins might be NA or placed in the nearest bin 
                # depending on if infs=TRUE. If infs=TRUE, the first/last breaks 
                # are the min/max of the training data.
                results.append(np.nan)
                
        return np.array(results, dtype=object)

def discretize(x, cuts=3, infs=True, keep_na=True, prefix=""):
    s = pd.Series(x)
    # R's recipes::discretize uses quantile breaks
    # For cuts=3, it needs 4 breaks: 0, 1/3, 2/3, 1
    qs = np.linspace(0, 1, cuts + 1)
    bins = np.quantile(s.dropna(), qs)
    
    # If infs=True, the first and last breaks are replaced by -Inf and Inf
    # Note: In the R source examples, infs=FALSE is explicitly called. 
    # Default is actually infs=TRUE in recipes::discretize.
    if infs:
        bins[0] = -np.inf
        bins[-1] = np.inf
    
    model = DiscretizeModel(bins, prefix=prefix, infs=infs)
    
    # Formatting the output message: "      Breaks: b1, b2, b3Bins: n (includes missing category)"
    # We need to format numbers to match R's output (e.g. 47.1)
    formatted_breaks = []
    for b in bins:
        if np.isinf(b):
            formatted_breaks.append("-Inf" if b < 0 else "Inf")
        else:
            # R usually prints a few decimals. We'll use a format that strips trailing zeros.
            formatted_breaks.append(f"{b:.2f}".rstrip('0').rstrip('.'))
            
    breaks_str = ", ".join(formatted_breaks)
    num_bins = len(bins) - 1
    missing_msg = " (includes missing category)" if keep_na else ""
    
    # Print exactly as R does (no newline between Breaks and Bins)
    print(f"      Breaks: {breaks_str}Bins: {num_bins}{missing_msg}")
    
    return model

# Data loading
biomass_df = pd.DataFrame(biomass)
biomass_tr = biomass_df[biomass_df['dataset'] == "Training"].copy()
biomass_te = biomass_df[biomass_df['dataset'] == "Testing"].copy()

# median(biomass_tr$carbon)
median_val = biomass_tr['carbon'].median()
print(f"[1] {median_val:.1f}")

# discretize(biomass_tr$carbon, cuts = 2)
_ = discretize(biomass_tr['carbon'], cuts=2)

# discretize(biomass_tr$carbon, cuts = 2, infs = FALSE)
_ = discretize(biomass_tr['carbon'], cuts=2, infs=False)

# discretize(biomass_tr$carbon, cuts = 2, infs = FALSE, keep_na = FALSE)
_ = discretize(biomass_tr['carbon'], cuts=2, infs=False, keep_na=False)

# discretize(biomass_tr$carbon, cuts = 2, prefix = "maybe a bad idea to bin")
_ = discretize(biomass_tr['carbon'], cuts=2, prefix="maybe a bad idea to bin")

# carbon_binned <- discretize(biomass_tr$carbon)
# R's default cuts=3, and default infs=TRUE
carbon_binned = discretize(biomass_tr['carbon'])

# table(predict(carbon_binned, biomass_tr$carbon))
preds = carbon_binned.predict(biomass_tr['carbon'])
unique_levels = carbon_binned.levels
counts = [np.sum(preds == lvl) for lvl in unique_levels]

# R's table output formatting
formatted_breaks = []
for b in carbon_binned.bins:
    if np.isinf(b):
        formatted_breaks.append("-Inf" if b < 0 else "Inf")
    else:
        formatted_breaks.append(f"{b:.1f}")

print(f"      Breaks: {', '.join(formatted_breaks)}")
print(f"{' '.join(unique_levels)} ")
print(f"{' '.join(map(str, counts))}")

# carbon_no_infs <- discretize(biomass_tr$carbon, infs = FALSE)
carbon_no_infs = discretize(biomass_tr['carbon'], infs=False)

# predict(carbon_no_infs, c(50, 100))
final_preds = carbon_no_infs.predict([50, 100])
pred_str = ' '.join([str(x) if pd.notnull(x) else '<NA>' for x in final_preds])
print(f"[1] {pred_str}")
print(f"Levels: {' '.join(carbon_no_infs.levels)}")