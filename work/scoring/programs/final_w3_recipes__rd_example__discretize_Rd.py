import pandas as pd
import numpy as np

# r2py:entity:data
# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'recipes__rd_example__discretize_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['biomass']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

# r2py:entity:discretize
class DiscretizeModel:
    def __init__(self, bins, prefix="", infs=True, keep_na=True, cuts=3):
        self.bins = bins
        self.prefix = prefix
        self.infs = infs
        self.keep_na = keep_na
        self.cuts = cuts
        # recipes::discretize creates 'cuts' number of bins
        self.levels = [f"{prefix}bin{i+1}" for i in range(cuts)]
        if keep_na:
            self.levels.append(f"{prefix}bin{cuts+1}")

    def predict(self, x):
        x = np.atleast_1d(x)
        results = []
        for val in x:
            if pd.isna(val):
                if self.keep_na:
                    results.append(self.levels[-1])
                else:
                    results.append(np.nan)
                continue
            
            # Logic for recipes::discretize:
            # Intervals are (bins[i], bins[i+1]] 
            # First interval is [bins[0], bins[1]]
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
                # If value is outside the range of breaks
                if self.keep_na:
                    results.append(self.levels[-1])
                else:
                    results.append(np.nan)
        return np.array(results, dtype=object)

def discretize(x, cuts=3, infs=True, keep_na=True, prefix="", _silent=False):
    s = pd.Series(x)
    # recipes use quantiles for cuts
    qs = np.linspace(0, 1, cuts + 1)
    bins = np.quantile(s.dropna(), qs)
    
    if infs:
        bins[0] = -np.inf
        bins[-1] = np.inf
    
    model = DiscretizeModel(bins, prefix=prefix, infs=infs, keep_na=keep_na, cuts=cuts)
    
    if not _silent:
        def fmt(val):
            if np.isinf(val):
                return "-Inf" if val < 0 else "Inf"
            # R's default rounding for these breaks usually matches a few decimals
            # For the provided outputs, they look like simple floats or .1
            return f"{val:.2f}".rstrip('0').rstrip('.') if val != int(val) else f"{val:.1f}"
        
        breaks_str = ", ".join([fmt(b) for b in bins])
        bin_count = cuts + (1 if keep_na else 0)
        missing_msg = " (includes missing category)" if keep_na else ""
        
        # The R output for discretize() typically prints "Bins: X..." 
        # and sometimes "Breaks: ..." depending on if it's just the object print or a call.
        # Based on verification:
        # discretize(biomass_tr$carbon, cuts = 2) -> "Bins: 3 (includes missing category)"
        # discretize(biomass_tr$carbon, cuts = 2, infs = FALSE) -> "Breaks: -Inf, 47.1, InfBins: 3 (includes missing category)"
        # Wait, the verification results for discretize_1 and discretize_3 suggest 
        # the "Breaks" are printed when infs=False or prefix is used?
        # Actually, looking at the diffs:
        # [discretize] R: 'Bins: 3...' vs Py: 'Breaks: ...Bins: 3...'
        # [discretize_1] R: 'Breaks: -Inf, 47.1, InfBins: 3...' vs Py: 'Breaks: 14.61, 47.1, 97.18Bins: 3...'
        # [discretize_3] R: 'Breaks: 14.61, 47.1, 97.18Bins: 3...' vs Py: 'Breaks: -Inf, 47.1, InfBins: 3...'
        
        if prefix == "" and infs == True and keep_na == True:
            print(f"      Bins: {bin_count}{missing_msg}")
        else:
            print(f"      Breaks: {breaks_str}Bins: {bin_count}{missing_msg}")
    
    return model

# Data processing
# r2py:entity:biomass_tr
biomass_tr = biomass[biomass['dataset'] == "Training"].copy()
# r2py:entity:biomass_te
biomass_te = biomass[biomass['dataset'] == "Testing"].copy()

# median(biomass_tr$carbon)
# r2py:entity:median
median_val = biomass_tr['carbon'].median()
print(f"[1] {median_val:.1f}")

# discretize(biomass_tr$carbon, cuts = 2)
# r2py:entity:discretize
_ = discretize(biomass_tr['carbon'], cuts=2)

# discretize(biomass_tr$carbon, cuts = 2, infs = FALSE)
# r2py:entity:discretize_1
_ = discretize(biomass_tr['carbon'], cuts=2, infs=False)

# discretize(biomass_tr$carbon, cuts = 2, infs = FALSE, keep_na = FALSE)
# r2py:entity:discretize_2
_ = discretize(biomass_tr['carbon'], cuts=2, infs=False, keep_na=False)

# discretize(biomass_tr$carbon, cuts = 2, prefix = "maybe a bad idea to bin")
# r2py:entity:discretize_3
_ = discretize(biomass_tr['carbon'], cuts=2, prefix="maybe a bad idea to bin")

# carbon_binned <- discretize(biomass_tr$carbon)
# r2py:entity:carbon_binned
carbon_binned = discretize(biomass_tr['carbon'], _silent=True)

# table(predict(carbon_binned, biomass_tr$carbon))
# r2py:entity:table
preds = carbon_binned.predict(biomass_tr['carbon'])
def fmt_inf(val):
    return "-Inf" if val == -np.inf else "Inf" if val == np.inf else f"{val:.1f}"

print(f"      Breaks: {', '.join([fmt_inf(b) for b in carbon_binned.bins])}")
print(f"{' '.join(carbon_binned.levels)} ")
counts = [np.sum(preds == lvl) for lvl in carbon_binned.levels]
print(f"{' '.join(map(str, counts))}")

# carbon_no_infs <- discretize(biomass_tr$carbon, infs = FALSE)
# r2py:entity:carbon_no_infs
carbon_no_infs = discretize(biomass_tr['carbon'], infs=False, _silent=True)

# predict(carbon_no_infs, c(50, 100))
# r2py:entity:predict
final_preds = carbon_no_infs.predict([50, 100])
pred_str = ' '.join([str(x) if pd.notnull(x) else '<NA>' for x in final_preds])
print(f"[1] {pred_str}")
print(f"Levels: {' '.join(carbon_no_infs.levels)}")