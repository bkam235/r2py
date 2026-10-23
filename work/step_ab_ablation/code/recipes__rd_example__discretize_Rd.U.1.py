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

class DiscretizeModel:
    def __init__(self, bins, prefix="", infs=True, keep_na=True):
        self.bins = bins
        self.prefix = prefix
        self.infs = infs
        self.keep_na = keep_na
        # R levels are typically bin1, bin2, ...
        self.levels = [f"{prefix}bin{i+1}" for i in range(len(bins) - 1)]

    def predict(self, x):
        x = np.atleast_1d(x)
        results = []
        for val in x:
            if pd.isna(val):
                results.append(np.nan)
                continue
            
            # Find which bin it falls into
            # R's cut(..., include.lowest=TRUE) behavior
            # (bins[i], bins[i+1]]
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

def discretize(x, cuts=3, infs=True, keep_na=True, prefix="", _print=True):
    s = pd.Series(x)
    # Quantiles for breaks
    qs = np.linspace(0, 1, cuts + 1)
    bins = np.quantile(s.dropna(), qs)
    
    if not infs:
        bins[0] = -np.inf
        bins[-1] = np.inf
    
    model = DiscretizeModel(bins, prefix=prefix, infs=infs, keep_na=keep_na)
    
    if _print:
        # Format breaks
        breaks_list = []
        for b in bins:
            if np.isinf(b):
                breaks_list.append("-Inf" if b < 0 else "Inf")
            else:
                # R's output formatting for these breaks is usually 1-2 decimal places
                # but trailing zeros are dropped.
                breaks_list.append(f"{b:.2f}".rstrip('0').rstrip('.'))
        
        breaks_str = ", ".join(breaks_list)
        num_bins = len(bins) - 1
        missing_msg = " (includes missing category)" if keep_na else ""
        print(f"      Breaks: {breaks_str}Bins: {num_bins}{missing_msg}")
    
    return model

# Data processing
biomass_df = biomass
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
# Assignment in R prevents the printing of the discretize summary
carbon_binned = discretize(biomass_tr['carbon'], _print=False)

# table(predict(carbon_binned, biomass_tr$carbon))
preds = carbon_binned.predict(biomass_tr['carbon'])
# R's table output for factor levels
unique_levels = carbon_binned.levels
counts = [np.sum(preds == level) for level in unique_levels]

# Re-creating the R output format for table
# R's table for this specific call prints the breaks of the model first
breaks_list = []
for b in carbon_binned.bins:
    if np.isinf(b):
        breaks_list.append("-Inf" if b < 0 else "Inf")
    else:
        breaks_list.append(f"{b:.1f}")
print(f"      Breaks: {', '.join(breaks_list)}")
print(f"{' '.join(unique_levels)} ")
print(f"{' '.join(map(str, counts))}")

# carbon_no_infs <- discretize(biomass_tr$carbon, infs = FALSE)
carbon_no_infs = discretize(biomass_tr['carbon'], infs=False, _print=False)

# predict(carbon_no_infs, c(50, 100))
final_preds = carbon_no_infs.predict([50, 100])
# R output: [1] binX binY
pred_str = ' '.join([str(x) if pd.notnull(x) else '<NA>' for x in final_preds])
print(f"[1] {pred_str}")
print(f"Levels: {' '.join(carbon_no_infs.levels)}")