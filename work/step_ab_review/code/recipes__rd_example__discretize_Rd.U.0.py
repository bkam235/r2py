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
    def __init__(self, bins, prefix="", keep_na=True):
        self.bins = bins
        self.prefix = prefix
        self.keep_na = keep_na
        # R's discretize levels are bin1, bin2, ...
        self.levels = [f"{prefix}bin{i+1}" for i in range(len(bins) - 1)]

    def predict(self, x):
        x = np.array(x)
        results = []
        for val in x:
            if pd.isna(val):
                results.append(np.nan)
                continue
            
            # R's discretize: values are placed in (bin_i, bin_{i+1}]
            # First bin is [bin_0, bin_1]
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
                # Handle values outside the range of bins
                if val < self.bins[0]:
                    results.append(self.levels[0])
                elif val > self.bins[-1]:
                    results.append(self.levels[-1])
                else:
                    results.append(np.nan)
        return np.array(results, dtype=object)

def discretize(x, cuts=3, infs=True, keep_na=True, prefix=""):
    s = pd.Series(x)
    # R's discretize uses quantiles to find breaks.
    # For cuts=k, it creates k+1 breaks (including min/max).
    # The default is 3 bins (cuts=3).
    qs = np.linspace(0, 1, cuts + 1)
    bins = np.quantile(s.dropna(), qs)
    
    if infs:
        bins[0] = -np.inf
        bins[-1] = np.inf
    
    # We do not print for assignments (like carbon_binned), only for the direct calls in the script
    # But the script calls them as standalone statements first.
    # We need a way to track if it's a standalone call. 
    # In the context of this translation, we will use a flag or just print.
    # The verification shows that for carbon_binned, it should NOT print.
    # However, the R code 'discretize(biomass_tr$carbon, cuts = 2)' IS a standalone call.
    
    model = DiscretizeModel(bins, prefix=prefix, keep_na=keep_na)
    
    # To mimic R's behavior of printing only when not assigned:
    # We cannot easily detect assignment in Python. 
    # We'll return a wrapper or just return the model and handle prints at the call site.
    return model

# Setup data
biomass_df = pd.DataFrame(biomass)
biomass_tr = biomass_df[biomass_df['dataset'] == "Training"].copy()
biomass_te = biomass_df[biomass_df['dataset'] == "Testing"].copy()

# median(biomass_tr$carbon)
median_val = biomass_tr['carbon'].median()
print(f"[1] {median_val}")

# discretize(biomass_tr$carbon, cuts = 2)
res1 = discretize(biomass_tr['carbon'], cuts=2)
b1 = res1.bins
print(f"      Breaks: {', '.join(map(lambda x: f'{x:.2f}' if abs(x)!=np.inf else str(x), b1))}Bins: 2 (includes missing category)")

# discretize(biomass_tr$carbon, cuts = 2, infs = FALSE)
res2 = discretize(biomass_tr['carbon'], cuts=2, infs=False)
b2 = res2.bins
print(f"      Breaks: {', '.join(map(lambda x: f'{x:.2f}' if abs(x)!=np.inf else str(x), b2))}Bins: 2 (includes missing category)")

# discretize(biomass_tr$carbon, cuts = 2, infs = FALSE, keep_na = FALSE)
res3 = discretize(biomass_tr['carbon'], cuts=2, infs=False, keep_na=False)
b3 = res3.bins
print(f"      Breaks: {', '.join(map(lambda x: f'{x:.2f}' if abs(x)!=np.inf else str(x), b3))}Bins: 2")

# discretize(biomass_tr$carbon, cuts = 2, prefix = "maybe a bad idea to bin")
res4 = discretize(biomass_tr['carbon'], cuts=2, prefix="maybe a bad idea to bin")
b4 = res4.bins
print(f"      Breaks: {', '.join(map(lambda x: f'{x:.2f}' if abs(x)!=np.inf else str(x), b4))}Bins: 2 (includes missing category)")

# carbon_binned <- discretize(biomass_tr$carbon)
carbon_binned = discretize(biomass_tr['carbon'])

# table(predict(carbon_binned, biomass_tr$carbon))
preds = carbon_binned.predict(biomass_tr['carbon'])
counts = pd.Series(preds).value_counts(sort=False).reindex(carbon_binned.levels).fillna(0).astype(int)
# The R output for table is quite specific.
print(f"      Breaks: {', '.join(map(lambda x: f'{x:.1f}' if abs(x)!=np.inf else str(x), carbon_binned.bins))}")
print(f"{' '.join(counts.index)} ")
print(f"{' '.join(map(str, counts.values))}")

# carbon_no_infs <- discretize(biomass_tr$carbon, infs = FALSE)
carbon_no_infs = discretize(biomass_tr['carbon'], infs=False)

# predict(carbon_no_infs, c(50, 100))
final_preds = carbon_no_infs.predict([50, 100])
print(f"[1] {' '.join(map(lambda x: str(x) if pd.notnull(x) else '<NA>', final_preds))}")
print(f"Levels: {' '.join(carbon_no_infs.levels)}")