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
    def __init__(self, breaks, prefix=""):
        self.breaks = breaks
        self.prefix = prefix
        self.levels = [f"{prefix}bin{i+1}" for i in range(len(breaks) - 1)]

    def predict(self, x):
        x = np.atleast_1d(x)
        results = []
        for val in x:
            if pd.isna(val):
                results.append(np.nan)
                continue
            
            # Logic: (break[i], break[i+1]]
            # Except for the first bin which is [break[0], break[1]]
            found = False
            for i in range(len(self.breaks) - 1):
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
                # Outside ranges
                if val <= self.breaks[0]:
                    results.append(self.levels[0])
                elif val > self.breaks[-1]:
                    results.append(self.levels[-1])
                else:
                    results.append(np.nan)
        return np.array(results)

def discretize(x, cuts=3, infs=True, keep_na=True, prefix=""):
    s = pd.Series(x).dropna()
    # R's recipes::discretize uses quantiles
    # cuts=3 means 4 break points (0, 1/3, 2/3, 1)
    qs = np.linspace(0, 1, cuts + 1)
    breaks = np.quantile(s, qs)
    
    if infs:
        breaks[0] = -np.inf
        breaks[-1] = np.inf
    
    # Simulation of the printout that R's discretize() produces
    # This is essentially a summary of the object created
    # "      Breaks: -Inf, 47.1, 100.5, Inf"
    breaks_fmt = ", ".join([str(b) if np.isinf(b) else f"{b:.1f}" for b in breaks])
    # In R, the output shows the breaks and then a message about bins
    # We mimic the implied print from the R example script
    # print(f"      Breaks: {breaks_fmt}") # Often printed in RL's discretize if printed
    
    return DiscretizeModel(breaks, prefix=prefix)

# Data Processing
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
# R's table() prints levels and counts
unique_levels = carbon_binned.levels
counts = [np.sum(preds == lvl) for lvl in unique_levels]
print(" ".join(unique_levels))
print(" ".join(map(str, counts)))

# carbon_no_infs <- discretize(biomass_tr$carbon, infs = FALSE)
carbon_no_infs = discretize(biomass_tr['carbon'], infs=False)

# predict(carbon_no_infs, c(50, 100))
final_preds = carbon_no_infs.predict([50, 100])
print(f"[1] {' '.join(final_preds)}")
print(f"Levels: {' '.join(carbon_no_infs.levels)}")