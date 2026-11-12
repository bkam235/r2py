import pandas as pd
import numpy as np
import warnings

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'recipes__rd_example__discretize_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['biomass']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

class DiscretizeModel:
    def __init__(self, breaks, prefix="bin", keep_na=True):
        self.breaks = breaks
        self.prefix = prefix
        self.keep_na = keep_na
        self.num_bins = len(breaks) - 1
        self.levels = [f"{prefix}{i+1}" for i in range(self.num_bins)]
        if self.keep_na:
            # In R recipes, missing is often treated as a separate level if keep_na=True
            # However, for the purpose of this translation and based on R output, 
            # the levels are bin1, bin2, ...
            pass

    def predict(self, x):
        x = np.array(x)
        results = []
        for val in x:
            if pd.isna(val):
                results.append(np.nan)
                continue
            
            # R's discretize typically uses (low, high]
            # We check which bin the value falls into
            bin_idx = -1
            for i in range(self.num_bins):
                low = self.breaks[i]
                high = self.breaks[i+1]
                if i == 0:
                    # First bin usually includes the minimum: [low, high]
                    if low <= val <= high:
                        bin_idx = i
                        break
                else:
                    # Subsequent bins: (low, high]
                    if low < val <= high:
                        bin_idx = i
                        break
            
            if bin_idx != -1:
                results.append(self.levels[bin_idx])
            else:
                results.append(np.nan)
        return np.array(results, dtype=object)

def discretize(x, cuts=3, infs=True, keep_na=True, prefix="bin"):
    s = pd.Series(x)
    
    # Validate prefix as R would (simplification)
    if " " in prefix:
        # R warning: The prefix "..." is not a valid R name.
        warnings.warn(f'The prefix "{prefix}" is not a valid R name. It has been changed to "{prefix.replace(" ", ".")}".')
        prefix = prefix.replace(" ", ".")

    # Calculate quantiles for breaks
    # R's recipes::discretize uses quantile values
    qs = np.linspace(0, 1, cuts + 1)
    bins = np.quantile(s.dropna(), qs)
    
    if not infs:
        bins[0] = -np.inf
        bins[-1] = np.inf
    
    model = DiscretizeModel(bins, prefix=prefix, keep_na=keep_na)
    
    # Match R's printed output format
    # "Breaks: b1, b2, b3Bins: n (includes missing category)"
    breaks_fmt = ", ".join([str(b) if abs(b) == np.inf else f"{b:.2f}".rstrip('0').rstrip('.') for b in bins])
    missing_msg = " (includes missing category)" if keep_na else ""
    print(f"      Breaks: {breaks_fmt}Bins: {model.num_bins}{missing_msg}")
    
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
preds_binned = carbon_binned.predict(biomass_tr['carbon'])
unique_levels = carbon_binned.levels
counts = [np.sum(preds_binned == level) for level in unique_levels]

# Match R table output:
# Breaks: ...
# bin1 bin2 bin3
# 114 115 113
breaks_fmt_binned = ", ".join([str(b) if abs(b) == np.inf else f"{b:.1f}" for b in carbon_binned.breaks])
print(f"      Breaks: {breaks_fmt_binned}")
print(" ".join(unique_levels) + " ")
print(" ".join(map(str, counts)))

# carbon_no_infs <- discretize(biomass_tr$carbon, infs = FALSE)
carbon_no_infs = discretize(biomass_tr['carbon'], infs=False)

# predict(carbon_no_infs, c(50, 100))
final_preds = carbon_no_infs.predict([50, 100])
preds_str = " ".join([str(x) if pd.notnull(x) else "<NA>" for x in final_preds])
print(f"[1] {preds_str}")
print(f"Levels: {' '.join(carbon_no_infs.levels)}")