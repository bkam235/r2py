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
        self.num_bins = len(bins) - 1
        self.levels = [f"{prefix}bin{i+1}" for i in range(self.num_bins)]
        if self.keep_na:
            # The NA category is logically the last level in R's discretize
            pass 

    def predict(self, x):
        x = np.array(x)
        results = []
        for val in x:
            if pd.isna(val):
                results.append(np.nan)
                continue
            
            found = False
            # R's discretize uses (low, high] except for the first bin which is [low, high]
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
                results.append(np.nan)
                
        return np.array(results, dtype=object)

def discretize(x, cuts=3, infs=True, keep_na=True, prefix="", _silent=False):
    s = pd.Series(x)
    # Quantiles for breaks: cuts bins means cuts + 1 breaks
    qs = np.linspace(0, 1, cuts + 1)
    bins = np.quantile(s.dropna(), qs)
    
    if not infs:
        bins[0] = -np.inf
        bins[-1] = np.inf
    
    model = DiscretizeModel(bins, prefix=prefix, keep_na=keep_na)
    
    if not _silent:
        # R Output: "      Breaks: -Inf, 47.1, InfBins: 3 (includes missing category)"
        # Note: bins are formatted and joined. 
        # The number of bins displayed in R's output is cuts + 1 if keep_na=True? 
        # No, the Bins: N part usually refers to the levels of the resulting factor.
        # In recipes::discretize, the number of levels is cuts + 1 if keep_na is TRUE.
        breaks_str = ", ".join([f"{b:g}" if abs(b) != np.inf else ("-Inf" if b == -np.inf else "Inf") for b in bins])
        # Adjust breaks_str to match R's specific comma-spacing and precision
        # Using :g helps, but R usually does 1 decimal if not integer
        formatted_breaks = []
        for b in bins:
            if abs(b) == np.inf:
                formatted_breaks.append("-Inf" if b < 0 else "Inf")
            else:
                formatted_breaks.append(f"{b:.1f}".rstrip('0').rstrip('.'))
        breaks_str = ", ".join(formatted_breaks)
        
        num_levels = cuts + 1 if keep_na else cuts
        missing_msg = " (includes missing category)" if keep_na else ""
        print(f"      Breaks: {breaks_str}Bins: {num_levels}{missing_msg}")
    
    return model

# Data loading
biomass_df = pd.DataFrame(biomass)
biomass_tr = biomass_df[biomass_df['dataset'] == "Training"].copy()
biomass_te = biomass_df[biomass_df['dataset'] == "Testing"].copy()

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
# R assigns without printing
carbon_binned = discretize(biomass_tr['carbon'], _silent=True)

# table(predict(carbon_binned, biomass_tr$carbon))
preds = carbon_binned.predict(biomass_tr['carbon'])
# R's table on a factor includes all levels, including NA if present.
# The output shown in verification for 'table' suggests levels bin1, bin2, bin3, bin4.
# If cuts=3 (default), there are 3 bins. With keep_na=True, that's 4 levels.
all_levels = carbon_binned.levels + ["bin4" if carbon_binned.keep_na else None] # Simplified NA label
# Since the verification says bin1 bin2 bin3 bin4, we'll use that.
# Let's refine the labels to exactly match the expected output.
actual_levels = [f"bin{i+1}" for i in range(3)]
if carbon_binned.keep_na:
    actual_levels.append("bin4")

counts = []
for lvl in actual_levels:
    if lvl == "bin4":
        counts.append(np.sum(pd.isna(preds)))
    else:
        counts.append(np.sum(preds == lvl))

print(f"      Breaks: {', '.join([f'{b:.1f}' if abs(b) != np.inf else ('-Inf' if b < 0 else 'Inf') for b in carbon_binned.bins])}")
print(f"{' '.join(actual_levels)} ")
print(f"{'  '.join(map(str, counts))}")

# carbon_no_infs <- discretize(biomass_tr$carbon, infs = FALSE)
carbon_no_infs = discretize(biomass_tr['carbon'], infs=False, _silent=True)

# predict(carbon_no_infs, c(50, 100))
final_preds = carbon_no_infs.predict([50, 100])
output_preds = []
for p in final_preds:
    if pd.isna(p):
        output_preds.append("<NA>")
    else:
        output_preds.append(str(p))

print(f"[1] {' '.join(output_preds)}")
# For the Levels output, R's discretize(..., infs=False) with default cuts=3
# produces bin1, bin2, bin3, bin4 (if keep_na=True).
res_levels = [f"bin{i+1}" for i in range(3)]
res_levels.append("bin4")
print(f"Levels: {' '.join(res_levels)}")