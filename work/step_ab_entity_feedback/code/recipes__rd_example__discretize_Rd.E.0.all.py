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
    def __init__(self, breaks, prefix="bin", keep_na=True):
        self.breaks = breaks
        self.prefix = prefix
        self.keep_na = keep_na
        # R's recipes discretize creates cuts + 1 bins
        self.num_bins = len(breaks) - 1
        self.levels = [f"{prefix}{i+1}" for i in range(self.num_bins)]

    def predict(self, x):
        x = np.array(x)
        results = []
        for val in x:
            if pd.isna(val):
                results.append(np.nan)
                continue
            
            # Binning logic: (break[i], break[i+1]]
            # However, for the first bin, it's usually [break[0], break[1]]
            found = False
            for i in range(self.num_bins):
                low = self.breaks[i]
                high = self.breaks[i+1]
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

def discretize(x, cuts=3, infs=True, keep_na=True, prefix="bin"):
    s = pd.Series(x)
    # recipes::discretize uses quantiles to find breaks
    # For cuts=k, it creates k internal cuts, resulting in k+1 bins.
    # The breaks are the 1/(k+1), 2/(k+1) ... k/(k+1) quantiles.
    # But actually, looking at R's output: cuts=2 -> 3 bins.
    # Quantiles are based on the data.
    q = np.linspace(0, 1, cuts + 2) # This is not quite right for R's 'cuts'
    # In recipes, cuts is the number of bins.
    # If cuts=3, we want 3 bins, so 2 internal cuts + 2 boundaries.
    
    # Correct logic for recipes::discretize:
    # breaks = quantile(x, prob = seq(0, 1, length.out = cuts + 1))
    probs = np.linspace(0, 1, cuts + 1)
    bins = np.quantile(s.dropna(), probs)
    
    if infs:
        bins[0] = -np.inf
        bins[-1] = np.inf
    
    model = DiscretizeModel(bins, prefix=prefix, keep_na=keep_na)
    
    # Formatting stdout
    # R: "      Breaks: -Inf, 47.1, InfBins: 3 (includes missing category)"
    b_str = ", ".join([str(b) if abs(b) == np.inf else f"{b:.1f}".rstrip('0').rstrip('.') for b in bins])
    # The "Bins: X" part matches the number of bins created
    missing_msg = " (includes missing category)" if keep_na else ""
    # Note: R's output for cuts=2 (discretize_1) showed 'Bins: 3' because it counts the bins
    # But in the verification, discretize_1 with cuts=2 produced "Bins: 3". 
    # This means bins = cuts + 1. Let's adjust.
    
    # Wait, looking at the verification: 
    # discretize(cuts=2) -> "Bins: 3" (Wait, 2+1=3)
    # carbon_binned (default cuts=3) -> "Bins: 4" (3+1=4)
    # So the logic is: number of bins = cuts + 1.
    
    # Let's refine:
    probs = np.linspace(0, 1, cuts + 2) 
    bins = np.quantile(s.dropna(), probs)
    if infs:
        bins[0] = -np.inf
        bins[-1] = np.inf
    model = DiscretizeModel(bins, prefix=prefix, keep_na=keep_na)
    
    b_str = ", ".join([str(b) if abs(b) == np.inf else f"{b:.1f}".rstrip('0').rstrip('.') for b in bins])
    print(f"      Breaks: {b_str}Bins: {model.num_bins}{missing_msg}")
    
    return model

# Data processing
biomass_tr = biomass[biomass['dataset'] == "Training"].copy()
biomass_te = biomass[biomass['dataset'] == "Testing"].copy()

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
carbon_binned = discretize(biomass_tr['carbon'])

# table(predict(carbon_binned, biomass_tr$carbon))
preds = carbon_binned.predict(biomass_tr['carbon'])
# R table: bins as columns, counts as rows
# R output: bin1 bin2 bin3 bin4 / 114 115 113 114
# We need to count each level
counts = []
for level in carbon_binned.levels:
    counts.append(np.sum(preds == level))

# Output for table
b_str_table = ", ".join([str(b) if abs(b) == np.inf else f"{b:.1f}".rstrip('0').rstrip('.') for b in carbon_binned.breaks])
print(f"Breaks: {b_str_table}")
print(f"{' '.join(carbon_binned.levels)} ")
print(f" {' '.join(map(str, counts))}")

# carbon_no_infs <- discretize(biomass_tr$carbon, infs = FALSE)
carbon_no_infs = discretize(biomass_tr['carbon'], infs=False)

# predict(carbon_no_infs, c(50, 100))
final_preds = carbon_no_infs.predict([50, 100])
print(f"[1] {' '.join(map(lambda x: str(x) if pd.notnull(x) else '<NA>', final_preds))}")
print(f"Levels: {' '.join(carbon_no_infs.levels)}")