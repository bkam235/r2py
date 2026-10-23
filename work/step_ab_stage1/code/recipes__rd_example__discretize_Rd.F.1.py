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
        # R's discretize labels are typically bin1, bin2, ...
        self.levels = [f"{prefix}bin{i+1}" for i in range(len(bins) - 1)]

    def predict(self, x):
        x = np.array(x)
        results = []
        for val in x:
            if pd.isna(val):
                results.append(np.nan)
                continue
            
            # R's discretize logic:
            # Bins are defined by the breaks.
            # Value is in bin i if bins[i-1] < val <= bins[i]
            # For the first bin, it is bins[0] <= val <= bins[1]
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
                # If it's outside the ranges, R might return NA or a specific bin
                # depending on if infs=True. If infs=True, the range is (-inf, inf).
                results.append(np.nan)
                
        return np.array(results, dtype=object)

def discretize(x, cuts=3, infs=True, keep_na=True, prefix=""):
    s = pd.Series(x)
    # Quantiles for breaks
    qs = np.linspace(0, 1, cuts + 1)
    bins = np.quantile(s.dropna(), qs)
    
    # If infs=True, the first and last breaks are replaced by -Inf and Inf
    if infs:
        bins[0] = -np.inf
        bins[-1] = np.inf
    
    model = DiscretizeModel(bins, prefix=prefix, infs=infs)
    
    # R prints only when the function is called without assignment
    # We'll return a wrapper or handle the print inside the function 
    # but in a way that simulates R's auto-printing.
    # However, the prompt asks for the Python translation to produce the same output.
    
    breaks_str = ", ".join([f"{b:.1f}".rstrip('0').rstrip('.') if abs(b) != np.inf else str(b).replace('inf', 'Inf') for b in bins])
    num_bins = len(bins) - 1
    missing_msg = " (includes missing category)" if keep_na else ""
    
    # The R output format seems to be: "      Breaks: ..., ...Bins: X (includes missing category)"
    # Note the spacing and the word "Bins:" immediately following the breaks list.
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
print(f"[1] {median_val:.1f}")

# To simulate R's behavior where assignment suppresses the print:
# We wrap the print logic in a way that only executes if the result isn't assigned.
# Since we can't truly detect assignment in Python, we'll only call the 
# 'print' part of the logic for the standalone calls.

def discretize_silent(x, cuts=3, infs=True, keep_na=True, prefix=""):
    s = pd.Series(x)
    qs = np.linspace(0, 1, cuts + 1)
    bins = np.quantile(s.dropna(), qs)
    if infs:
        bins[0] = -np.inf
        bins[-1] = np.inf
    return DiscretizeModel(bins, prefix=prefix, infs=infs)

# Replace the previous discretize with a version that can be silent
def discretize_full(x, cuts=3, infs=True, keep_na=True, prefix="", silent=False):
    model = discretize_silent(x, cuts, infs, keep_na, prefix)
    if not silent:
        bins = model.bins
        breaks_str = ", ".join([f"{b:.1f}".rstrip('0').rstrip('.') if abs(b) != np.inf else str(b).replace('inf', 'Inf') for b in bins])
        num_bins = len(bins) - 1
        missing_msg = " (includes missing category)" if keep_na else ""
        print(f"      Breaks: {breaks_str}Bins: {num_bins}{missing_msg}")
    return model

# discretize(biomass_tr$carbon, cuts = 2)
# r2py:entity:discretize
_ = discretize_full(biomass_tr['carbon'], cuts=2)

# discretize(biomass_tr$carbon, cuts = 2, infs = FALSE)
# r2py:entity:discretize_1
_ = discretize_full(biomass_tr['carbon'], cuts=2, infs=False)

# discretize(biomass_tr$carbon, cuts = 2, infs = FALSE, keep_na = FALSE)
# r2py:entity:discretize_2
_ = discretize_full(biomass_tr['carbon'], cuts=2, infs=False, keep_na=False)

# discretize(biomass_tr$carbon, cuts = 2, prefix = "maybe a bad idea to bin")
# r2py:entity:discretize_3
_ = discretize_full(biomass_tr['carbon'], cuts=2, prefix="maybe a bad idea to bin")

# carbon_binned <- discretize(biomass_tr$carbon)
# r2py:entity:carbon_binned
carbon_binned = discretize_full(biomass_tr['carbon'], silent=True)

# table(predict(carbon_binned, biomass_tr$carbon))
# r2py:entity:table
preds = carbon_binned.predict(biomass_tr['carbon'])
counts_dict = {}
for level in carbon_binned.levels:
    counts_dict[level] = np.sum(preds == level)

print(f"      Breaks: {', '.join([f'{b:.1f}' if abs(b) != np.inf else str(b).replace('inf', 'Inf') for b in carbon_binned.bins])}")
print(f"{' '.join(counts_dict.keys())} ")
print(f"{' '.join(map(str, counts_dict.values()))}")

# carbon_no_infs <- discretize(biomass_tr$carbon, infs = FALSE)
# r2py:entity:carbon_no_infs
carbon_no_infs = discretize_full(biomass_tr['carbon'], infs=False, silent=True)

# predict(carbon_no_infs, c(50, 100))
# r2py:entity:predict
final_preds = carbon_no_infs.predict([50, 100])
print(f"[1] {' '.join(map(lambda x: str(x) if pd.notnull(x) else '<NA>', final_preds))}")
print(f"Levels: {' '.join(carbon_no_infs.levels)}")