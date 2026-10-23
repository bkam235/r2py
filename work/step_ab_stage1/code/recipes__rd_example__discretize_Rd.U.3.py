# Translated from <R script> by r2py v0.3.0
import pandas as pd
import numpy as np
# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'recipes__rd_example__discretize_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['biomass']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

# r2py:entity:discretize
class DiscretizeModel:
    def __init__(self, bins, prefix="", infs=True):
        self.bins = bins
        self.prefix = prefix
        self.infs = infs
        # R labels bins as bin1, bin2, ...
        self.levels = [f"{prefix}bin{i+1}" for i in range(len(bins) - 1)]

    def predict(self, x):
        x = np.array(x)
        results = []
        for val in x:
            if pd.isna(val):
                results.append(np.nan)
                continue
            
            found = False
            for i in range(len(self.bins) - 1):
                low = self.bins[i]
                high = self.bins[i+1]
                
                # R's discretize typically uses (low, high] 
                # but the first bin is [low, high]
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
    # Quantiles for internal breaks
    qs = np.linspace(0, 1, cuts + 1)
    bins = np.quantile(s.dropna(), qs)
    
    # R's recipes::discretize behavior:
    # If infs=TRUE, it adds -Inf and Inf to the ends, increasing bin count by 1 (or keeping it if cuts=1)
    # But actually, looking at the R output: cuts=2 with infs=TRUE gives 3 bins.
    # That means it takes the quantiles and wraps them with -Inf and Inf.
    if infs:
        bins = np.concatenate([[-np.inf], bins, [np.inf]])
    # If infs=FALSE, it just uses the quantiles as they are.
    
    model = DiscretizeModel(bins, prefix=prefix, infs=infs)
    
    # R output formatting
    # If infs=TRUE, it prints "Breaks: -Inf, ..., InfBins: N (includes missing category)"
    # If infs=FALSE, it prints "Breaks: b1, ..., bN Bins: N-1"
    
    # Format floats to match R's output (usually 1 or 2 decimals, no trailing zeros)
    formatted_breaks = []
    for b in bins:
        if np.isinf(b):
            formatted_breaks.append("-Inf" if b < 0 else "Inf")
        else:
            # This mimics R's default numeric print
            s_val = f"{b:.2f}".rstrip('0').rstrip('.')
            formatted_breaks.append(s_val)
    
    breaks_str = ", ".join(formatted_breaks)
    num_bins = len(bins) - 1
    missing_msg = " (includes missing category)" if keep_na else ""
    
    # The R output is a bit strange: "      Breaks: ...Bins: ..."
    # Sometimes the breaks line is separate or combined.
    print(f"      Breaks: {breaks_str}Bins: {num_bins}{missing_msg}")
    
    return model

# Data loading
# r2py:entity:data
biomass_df = pd.DataFrame(biomass)
# r2py:entity:biomass_tr
biomass_tr = biomass_df[biomass_df['dataset'] == "Training"].copy()
# r2py:entity:biomass_te
biomass_te = biomass_df[biomass_df['dataset'] == "Testing"].copy()

# median(biomass_tr$carbon)
# r2py:entity:median
median_val = biomass_tr['carbon'].median()
print(f"[1] {median_val}")

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
# r2py:entity:carbon_binned
carbon_binned = discretize(biomass_tr['carbon'])

# table(predict(carbon_binned, biomass_tr$carbon))
# r2py:entity:table
preds = carbon_binned.predict(biomass_tr['carbon'])
counts_dict = {}
for level in carbon_binned.levels:
    counts_dict[level] = np.sum(preds == level)

# R's table output for factors:
#      Breaks: -Inf, 47.1, Inf
# bin1 bin2 bin3 bin4 
# 114  115  113  114
formatted_breaks_table = []
for b in carbon_binned.bins:
    if np.isinf(b):
        formatted_breaks_table.append("-Inf" if b < 0 else "Inf")
    else:
        formatted_breaks_table.append(f"{b:.1f}")
print(f"      Breaks: {', '.join(formatted_breaks_table)}")
print(f"{' '.join(counts_dict.keys())} ")
print(f"{' '.join(map(str, counts_dict.values()))}")

# carbon_no_infs <- discretize(biomass_tr$carbon, infs = FALSE)
# r2py:entity:carbon_no_infs
carbon_no_infs = discretize(biomass_tr['carbon'], infs=False)

# predict(carbon_no_infs, c(50, 100))
# r2py:entity:predict
final_preds = carbon_no_infs.predict([50, 100])
print(f"[1] {' '.join(map(lambda x: str(x) if pd.notnull(x) else '<NA>', final_preds))}")
print(f"Levels: {' '.join(carbon_no_infs.levels)}")