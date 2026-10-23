import pandas as pd
import numpy as np

# r2py:entity:discretize
class DiscretizeModel:
    def __init__(self, bins, prefix=""):
        self.bins = bins
        self.prefix = prefix
        # Levels are bin1, bin2, ... binN
        self.levels = [f"{prefix}bin{i+1}" for i in range(len(bins) - 1)]

    def predict(self, x):
        x = np.array(x)
        results = []
        for val in x:
            if pd.isna(val):
                results.append(np.nan)
                continue
            
            # R's discretize typically uses (low, high]
            # The first bin is [min, high]
            found = False
            for i in range(len(self.bins) - 1):
                low = self.bins[i]
                high = self.bins[i+1]
                
                if i == 0:
                    # First bin is inclusive of the lower bound
                    if low <= val <= high:
                        results.append(self.levels[i])
                        found = True
                        break
                else:
                    # Subsequent bins are (low, high]
                    if low < val <= high:
                        results.append(self.levels[i])
                        found = True
                        break
            if not found:
                # If it falls outside the bins, it's NA or we need to handle it
                # In R, if infs=True, it's always within (-inf, inf)
                results.append(np.nan)
                
        return np.array(results, dtype=object)

def discretize(x, cuts=3, infs=True, keep_na=True, prefix=""):
    s = pd.Series(x)
    # Quantiles for breaks: 0, 1/cuts, ..., 1
    qs = np.linspace(0, 1, cuts + 1)
    bins = np.quantile(s.dropna(), qs)
    
    # In R's recipes::discretize, if infs=True, the boundaries are expanded to +/- Inf
    if infs:
        bins[0] = -np.inf
        bins[-1] = np.inf
    
    model = DiscretizeModel(bins, prefix=prefix)
    
    # Format output to match R: "      Breaks: b1, b2... Bins: N (includes missing category)"
    # R's print method for discretize shows the breaks and the number of bins
    breaks_str = ", ".join([str(b) if abs(b) == np.inf else f"{b:.2f}".rstrip('0').rstrip('.') for b in bins])
    # R uses 'Inf' instead of 'inf'
    breaks_str = breaks_str.replace('inf', 'Inf').replace('-inf', '-Inf')
    
    num_bins = len(bins) - 1
    missing_msg = " (includes missing category)" if keep_na else ""
    
    # The R function prints this metadata when called as a top-level expression
    print(f"      Breaks: {breaks_str}Bins: {num_bins}{missing_msg}")
    
    return model

# Data loading
# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'recipes__rd_example__discretize_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['biomass']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

# r2py:entity:biomass_tr
biomass_tr = biomass[biomass['dataset'] == "Training"].copy()
# r2py:entity:biomass_te
biomass_te = biomass[biomass['dataset'] == "Testing"].copy()

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
# Note: R's discretize default cuts is 3
# r2py:entity:carbon_binned
carbon_binned = discretize(biomass_tr['carbon'], cuts=3)

# table(predict(carbon_binned, biomass_tr$carbon))
# r2py:entity:table
preds = carbon_binned.predict(biomass_tr['carbon'])
# In R, table() on a factor sorts by levels
unique_levels = carbon_binned.levels
counts = [np.sum(preds == level) for level in unique_levels]

# R's table output formatting for this specific case:
# Breaks are printed first, then the level names, then the counts.
breaks_formatted = ", ".join([str(b) if abs(b) == np.inf else f"{b:.1f}" for b in carbon_binned.bins])
breaks_formatted = breaks_formatted.replace('inf', 'Inf').replace('-inf', '-Inf')
print(f"      Breaks: {breaks_formatted}")
print(f"{' '.join(unique_levels)} ")
print(f"{' '.join(map(str, counts))}")

# carbon_no_infs <- discretize(biomass_tr$carbon, infs = FALSE)
# r2py:entity:carbon_no_infs
carbon_no_infs = discretize(biomass_tr['carbon'], infs=False)

# predict(carbon_no_infs, c(50, 100))
# r2py:entity:predict
final_preds = carbon_no_infs.predict([50, 100])
# Convert NaN to <NA> for R-like output
out_preds = [str(p) if pd.notnull(p) else "<NA>" for p in final_preds]
print(f"[1] {' '.join(out_preds)}")
print(f"Levels: {' '.join(carbon_no_infs.levels)}")