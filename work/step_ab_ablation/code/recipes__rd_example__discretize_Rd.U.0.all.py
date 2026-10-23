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
        # R's recipes discretize usually names bins as bin1, bin2...
        self.levels = [f"{prefix}bin{i+1}" for i in range(len(bins) - 1)]

    def predict(self, x):
        x = np.array(x)
        results = []
        for val in x:
            if pd.isna(val):
                results.append(np.nan)
                continue
            
            # Using pandas.cut logic for binning based on the stored breaks
            # R's discretize usually uses (low, high]
            # For the first bin, it is inclusive of the minimum.
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
    # Use qcut to get quantile breaks
    # R's cuts=2 means 2 bins, so 3 breaks
    bins = np.unique(pd.qcut(s, q=cuts, retbins=True, duplicates='drop')[1])
    
    # The 'infs' argument in recipes::discretize: 
    # If TRUE (default), the first and last breaks are replaced by -Inf and Inf.
    if infs:
        bins[0] = -np.inf
        bins[-1] = np.inf
    
    model = DiscretizeModel(bins, prefix=prefix, infs=infs, keep_na=keep_na)
    
    # R's output format
    # Breaks are usually formatted to 2 decimal places or Inf
    breaks_fmt = []
    for b in bins:
        if np.isinf(b):
            breaks_fmt.append("-Inf" if b < 0 else "Inf")
        else:
            # Match R's numeric printing (stripping trailing zeros)
            s_val = f"{b:.2f}"
            if '.' in s_val:
                s_val = s_val.rstrip('0').rstrip('.')
            breaks_fmt.append(s_val)
    
    breaks_str = ", ".join(breaks_fmt)
    num_bins = len(bins) - 1
    missing_msg = " (includes missing category)" if keep_na else ""
    
    # The R function prints this metadata
    print(f"      Breaks: {breaks_str}Bins: {num_bins}{missing_msg}")
    
    return model

# biomass_tr <- biomass[biomass$dataset == "Training", ]
biomass_tr = biomass[biomass['dataset'] == "Training"].copy()
# biomass_te <- biomass[biomass$dataset == "Testing", ]
biomass_te = biomass[biomass['dataset'] == "Testing"].copy()

# median(biomass_tr$carbon)
median_val = biomass_tr['carbon'].median()
print(f"[1] {median_val}")

# discretize(biomass_tr$carbon, cuts = 2)
_ = discretize(biomass_tr['carbon'], cuts=2)

# discretize(biomass_tr$carbon, cuts = 2, infs = FALSE)
_ = discretize(biomass_tr['carbon'], cuts=2, infs=False)

# discretize(biomass_tr$carbon, cuts = 2, infs = FALSE, keep_na = FALSE)
_ = discretize(biomass_tr['carbon'], cuts=2, infs=False, keep_na=False)

# discretize(biomass_tr$carbon, cuts = 2, prefix = "maybe a bad idea to bin")
_ = discretize(biomass_tr['carbon'], cuts=2, prefix="maybe a bad idea to bin")

# carbon_binned <- discretize(biomass_tr$carbon)
carbon_binned = discretize(biomass_tr['carbon'])

# table(predict(carbon_binned, biomass_tr$carbon))
preds = carbon_binned.predict(biomass_tr['carbon'])
counts = pd.Series(preds).value_counts().reindex(carbon_binned.levels).fillna(0).astype(int)

# Replicate R's table output
breaks_fmt_table = []
for b in carbon_binned.bins:
    if np.isinf(b):
        breaks_fmt_table.append("-Inf" if b < 0 else "Inf")
    else:
        s_val = f"{b:.1f}"
        if '.' in s_val:
            s_val = s_val.rstrip('0').rstrip('.')
        breaks_fmt_table.append(s_val)

print(f"      Breaks: {', '.join(breaks_fmt_table)}")
print(f"{' '.join(counts.index)} ")
print(f"{' '.join(map(str, counts.values()))}")

# carbon_no_infs <- discretize(biomass_tr$carbon, infs = FALSE)
carbon_no_infs = discretize(biomass_tr['carbon'], infs=False)

# predict(carbon_no_infs, c(50, 100))
final_preds = carbon_no_infs.predict([50, 100])
preds_str = " ".join([str(p) if pd.notnull(p) else "<NA>" for p in final_preds])
print(f"[1] {preds_str}")
print(f"Levels: {' '.join(carbon_no_infs.levels)}")