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

# r2py:entity:is_installed
import pandas as pd
import numpy as np

# r2py:entity:discretize
class DiscretizeModel:
    def __init__(self, bins, prefix="", infs=True):
        self.bins = bins
        self.prefix = prefix
        self.infs = infs
        self.levels = [f"{prefix}bin{i+1}" for i in range(len(bins) - 1)]

    def predict(self, x):
        x = np.array(x)
        results = []
        for val in x:
            if pd.isna(val):
                results.append(np.nan)
                continue
            
            # R's discretize usually uses (low, high]
            # For the first bin, if it's the minimum, it is included [min, high]
            # We check against bins
            found = False
            for i in range(len(self.bins) - 1):
                low = self.bins[i]
                high = self.bins[i+1]
                
                # First bin include lowest
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
    # Quantiles for breaks
    qs = np.linspace(0, 1, cuts + 1)
    bins = np.quantile(s.dropna(), qs)
    
    # If infs=False, replace min/max with -inf/inf
    if not infs:
        bins[0] = -np.inf
        bins[-1] = np.inf
    
    model = DiscretizeModel(bins, prefix=prefix, infs=infs)
    
    # Formatting for R's specific stdout: "      Breaks: b1, b2, b3Bins: n (includes missing category)"
    breaks_str = ", ".join([f"{b:.2f}".rstrip('0').rstrip('.') if abs(b) != np.inf else str(b) for b in bins])
    num_bins = len(bins) - 1
    missing_msg = " (includes missing category)" if keep_na else ""
    
    # R prints this as one line or very close
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
carbon_binned = discretize(biomass_tr['carbon'])

# table(predict(carbon_binned, biomass_tr$carbon))
# r2py:entity:table
preds = carbon_binned.predict(biomass_tr['carbon'])
# R table shows counts for each level of the factor
counts_dict = {}
for level in carbon_binned.levels:
    counts_dict[level] = np.sum(preds == level)

# Formatting the table output
# R: Breaks: -Inf, 47.1, Inf \n bin1 bin2 bin3 bin4 \n 114 115 113 114
# Actually, for cuts=3, there are 3 bins. The provided R output in verification was a bit confusing.
# Let's follow the levels found in the model.
print(f"      Breaks: {', '.join([f'{b:.1f}' if abs(b) != np.inf else str(b) for b in carbon_binned.bins])}")
print(f"{' '.join(counts_dict.keys())} ")
print(f"{' '.join(map(str, counts_dict.values()))}")

# carbon_no_infs <- discretize(biomass_tr$carbon, infs = FALSE)
# r2py:entity:carbon_no_infs
carbon_no_infs = discretize(biomass_tr['carbon'], infs=False)

# predict(carbon_no_infs, c(50, 100))
# r2py:entity:predict
final_preds = carbon_no_infs.predict([50, 100])
# R's predict often returns [1] binX binY
print(f"[1] {' '.join(map(lambda x: str(x) if pd.notnull(x) else '<NA>', final_preds))}")
print(f"Levels: {' '.join(carbon_no_infs.levels)}")