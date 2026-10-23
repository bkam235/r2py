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
        self.levels = [f"{prefix}bin{i+1}" for i in range(len(bins) - 1)]

    def predict(self, x):
        x = np.array(x)
        results = []
        for val in x:
            if pd.isna(val):
                results.append(np.nan)
                continue
            
            # R's discretize uses (low, high] for all but the first bin [min, high]
            # This is similar to pandas qcut logic
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
                # Handle values outside the range if bins aren't -inf/inf
                if val < self.bins[0]:
                    results.append(self.levels[0])
                elif val > self.bins[-1]:
                    results.append(self.levels[-1])
                else:
                    results.append(np.nan)
        return np.array(results, dtype=object)

def discretize(x, cuts=3, infs=True, keep_na=True, prefix=""):
    s = pd.Series(x)
    # Calculate quantiles
    qs = np.linspace(0, 1, cuts + 1)
    bins = np.quantile(s.dropna(), qs)
    
    if not infs:
        # In R's discretize, infs=FALSE means the ends are -Inf and Inf
        # Wait, actually in recipes::discretize, infs=TRUE (default) means it replaces
        # the outer edges with -Inf and Inf. Let's check.
        # Actually, looking at the R code for discretize:
        # if (infs) { breaks[1] <- -Inf; breaks[length(breaks)] <- Inf }
        # So infs=TRUE is the default that adds infinities.
        pass
    else:
        bins[0] = -np.inf
        bins[-1] = np.inf
    
    model = DiscretizeModel(bins, prefix=prefix)
    
    # Format output for R's print method of a discretize object
    breaks_str = ", ".join([f"{b:.1f}" if abs(b) != np.inf else str(b) for b in bins])
    num_bins = len(bins) - 1
    missing_msg = " (includes missing category)" if keep_na else ""
    print(f"      Breaks: {breaks_str}\nBins: {num_bins}{missing_msg}")
    
    return model

# Data loading
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
# Calculate counts for each level
counts = pd.Series(preds).value_counts().reindex(carbon_binned.levels).fillna(0).astype(int)
print(f"{' '.join(counts.index)} ")
print(f"{' '.join(map(str, counts.values))}")

# carbon_no_infs <- discretize(biomass_tr$carbon, infs = FALSE)
carbon_no_infs = discretize(biomass_tr['carbon'], infs=False)

# predict(carbon_no_infs, c(50, 100))
final_preds = carbon_no_infs.predict([50, 100])
print(f"[1] {' '.join(map(lambda x: str(x) if pd.notnull(x) else '<NA>', final_preds))}")