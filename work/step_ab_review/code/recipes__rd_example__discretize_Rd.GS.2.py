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
    def __init__(self, x, cuts=3, infs=True, keep_na=True, prefix=""):
        self.prefix = prefix
        self.keep_na = keep_na
        self.infs = infs
        
        s = pd.Series(x).dropna()
        qs = np.linspace(0, 1, cuts + 1)
        self.bins = np.quantile(s, qs)
        
        if self.infs:
            self.bins[0] = -np.inf
            self.bins[-1] = np.inf
            
        self.levels = [f"{prefix}bin{i+1}" for i in range(cuts)]
        if self.keep_na:
            # R recipes discretize often adds a bin for NAs as the last level
            self.levels.append(f"{prefix}bin{cuts+1}")

    def predict(self, x):
        x = np.array(x)
        results = []
        for val in x:
            if pd.isna(val):
                if self.keep_na:
                    results.append(self.levels[-1])
                else:
                    results.append(np.nan)
                continue
            
            found = False
            for i in range(len(self.bins) - 1):
                low = self.bins[i]
                high = self.bins[i+1]
                
                # Standard R binning for discretize: 
                # First bin is inclusive of low, others are (low, high]
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
                if self.keep_na:
                    # If it falls outside the defined bins, R often puts it in a 'missing/out' bin
                    # but usually, the +/- inf handles it.
                    results.append(self.levels[-1])
                else:
                    results.append(np.nan)
                    
        return np.array(results, dtype=object)

def discretize(x, cuts=3, infs=True, keep_na=True, prefix=""):
    model = DiscretizeModel(x, cuts=cuts, infs=infs, keep_na=keep_na, prefix=prefix)
    
    # Mimicking R's print output for the discretize function call
    breaks_str = ", ".join([f"{b:g}" if abs(b) != np.inf else ("-Inf" if b < 0 else "Inf") for b in model.bins])
    bins_count = cuts if not model.keep_na else cuts + 1
    missing_msg = " (includes missing category)" if model.keep_na else ""
    
    # The R output format is quite specific
    print(f"      Breaks: {breaks_str}Bins: {bins_count}{missing_msg}")
    return model

# Data loading
biomass_df = pd.DataFrame(biomass)
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
carbon_binned = discretize(biomass_tr['carbon'])

# table(predict(carbon_binned, biomass_tr$carbon))
preds = carbon_binned.predict(biomass_tr['carbon'])
unique_levels = carbon_binned.levels
counts = [np.sum(preds == level) for level in unique_levels]

# R Table format
print(f"      Breaks: {', '.join([f'{b:g}' if abs(b) != np.inf else ('-Inf' if b < 0 else 'Inf') for b in carbon_binned.bins])}")
print(f"{' '.join(unique_levels)} ")
print(f"{' '.join(map(str, counts))}")

# carbon_no_infs <- discretize(biomass_tr$carbon, infs = FALSE)
carbon_no_infs = discretize(biomass_tr['carbon'], infs=False)

# predict(carbon_no_infs, c(50, 100))
final_preds = carbon_no_infs.predict([50, 100])
print(f"[1] {' '.join(map(lambda x: str(x) if pd.notnull(x) else '<NA>', final_preds))}")
print(f"Levels: {' '.join(carbon_no_infs.levels)}")