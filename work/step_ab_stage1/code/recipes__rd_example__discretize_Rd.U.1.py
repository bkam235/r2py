import pandas as pd
import numpy as np

# r2py:entity:discretize
class DiscretizeModel:
    def __init__(self, bins, prefix="", infs=True, keep_na=True):
        self.bins = bins
        self.prefix = prefix
        self.infs = infs
        self.keep_na = keep_na
        self.num_bins = len(bins) - 1
        self.levels = [f"{prefix}bin{i+1}" for i in range(self.num_bins)]

    def predict(self, x):
        x = np.array(x)
        results = []
        for val in x:
            if pd.isna(val):
                results.append(np.nan)
                continue
            
            # R's discretize bins: (bins[i], bins[i+1]]
            # Except for the first bin which is [bins[0], bins[1]]
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
                # If it's outside the calculated bins but infs=True, 
                # it might still fall into the first or last bin if they are -inf/inf
                results.append(np.nan)
                
        return np.array(results, dtype=object)

    def __str__(self):
        breaks_str = ", ".join([f"{b:.2f}".rstrip('0').rstrip('.') if abs(b) != np.inf else str(b).replace('inf', 'Inf') for b in self.bins])
        missing_msg = " (includes missing category)" if self.keep_na else ""
        return f"      Breaks: {breaks_str}Bins: {self.num_bins}{missing_msg}"

def discretize(x, cuts=3, infs=True, keep_na=True, prefix=""):
    s = pd.Series(x)
    # Quantiles: R's discretize uses cuts to determine number of bins
    # cuts=3 means 4 breakpoints (0, 1/3, 2/3, 1)
    qs = np.linspace(0, 1, cuts + 1)
    bins = np.quantile(s.dropna(), qs)
    
    if not infs:
        bins[0] = -np.inf
        bins[-1] = np.inf
    
    return DiscretizeModel(bins, prefix=prefix, infs=infs, keep_na=keep_na)

# Data loading
# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'recipes__rd_example__discretize_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['biomass']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

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
res_disc = discretize(biomass_tr['carbon'], cuts=2)
print(res_disc)

# discretize(biomass_tr$carbon, cuts = 2, infs = FALSE)
# r2py:entity:discretize_1
res_disc1 = discretize(biomass_tr['carbon'], cuts=2, infs=False)
print(res_disc1)

# discretize(biomass_tr$carbon, cuts = 2, infs = FALSE, keep_na = FALSE)
# r2py:entity:discretize_2
res_disc2 = discretize(biomass_tr['carbon'], cuts=2, infs=False, keep_na=False)
print(res_disc2)

# discretize(biomass_tr$carbon, cuts = 2, prefix = "maybe a bad idea to bin")
# r2py:entity:discretize_3
res_disc3 = discretize(biomass_tr['carbon'], cuts=2, prefix="maybe a bad idea to bin")
print(res_disc3)

# carbon_binned <- discretize(biomass_tr$carbon)
# r2py:entity:carbon_binned
carbon_binned = discretize(biomass_tr['carbon'])

# table(predict(carbon_binned, biomass_tr$carbon))
# r2py:entity:table
preds = carbon_binned.predict(biomass_tr['carbon'])
# R table for factors shows all levels
counts_dict = {level: np.sum(preds == level) for level in carbon_binned.levels}
print(f"      Breaks: {', '.join([f'{b:.1f}' if abs(b) != np.inf else str(b).replace('inf', 'Inf') for b in carbon_binned.bins])}")
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