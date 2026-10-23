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
    def __init__(self, bins, prefix=""):
        self.bins = bins
        self.prefix = prefix
        # R's recipes discretize labels bins as bin1, bin2...
        self.levels = [f"{prefix}bin{i+1}" for i in range(len(bins) - 1)]

    def predict(self, x):
        x = np.array(x)
        results = []
        for val in x:
            if pd.isna(val):
                results.append(np.nan)
                continue
            
            # R's discretize (quantile-based) typically uses (low, high] 
            # but the first bin is [min, high]
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
                # Handle values outside the calculated bins if infs=False
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

def discretize(x, cuts=3, infs=True, keep_na=True, prefix=""):
    s = pd.Series(x)
    # R's quantile is used for cuts
    qs = np.linspace(0, 1, cuts + 1)
    bins = np.quantile(s.dropna(), qs)
    
    if not infs:
        bins[0] = -np.inf
        bins[-1] = np.inf
    
    model = DiscretizeModel(bins, prefix=prefix)
    
    # Printing mimics the R object output
    breaks_str = ", ".join([f"{b}" if abs(b) == np.inf else f"{b:g}" for b in bins])
    print(f"      Breaks: {breaks_str}")
    print(f"Bins: {cuts}{' (includes missing category)' if keep_na else ''}")
    
    return model

# Setup data
biomass_tr = biomass[biomass['dataset'] == "Training"].copy()
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
unique_levels = carbon_binned.levels
counts = [np.sum(preds == level) for level in unique_levels]

print(f"{' '.join(unique_levels)}")
print(f"{' '.join(map(str, counts))}")

# carbon_no_infs <- discretize(biomass_tr$carbon, infs = FALSE)
carbon_no_infs = discretize(biomass_tr['carbon'], infs=False)

# predict(carbon_no_infs, c(50, 100))
final_preds = carbon_no_infs.predict([50, 100])
print(f"[1] {' '.join(map(str, final_preds))}")
print(f"Levels: {' '.join(carbon_no_infs.levels)}")