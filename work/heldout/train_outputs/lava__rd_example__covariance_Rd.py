import numpy as np
import pandas as pd

# r2py:entity:m
class LVM:
    """
    Python implementation of the lava::lvm model object.
    Focuses on tracking symbolic covariance parameters and structure.
    """
    def __init__(self):
        self.M = np.array([[]])
        self.par = np.array([[]])
        self.cov = np.array([[]])
        self.covpar = np.array([[]])
        self.fix = np.array([[]])
        self.covfix = np.array([[]])
        self.latent = []
        self.mean = {}
        self.index = {'vars': [], 'manifest': [], 'endogenous': [], 'exo.idx': [], 'endo.obsidx': [], 'obs.idx': [], 'endo.idx': []}
        self.attributes = {'parameter': {}}

    def add_var(self, var_names):
        for var in var_names:
            if var not in self.index['vars']:
                self.index['vars'].append(var)
                self.index['manifest'].append(var)
                self.index['endogenous'].append(var)
                
                # Expand matrices
                n = len(self.index['vars'])
                self.M = np.zeros((n, n))
                self.cov = np.eye(n)
                self.covpar = np.full((n, n), None)
                self.par = np.full((n, n), None)
                self.fix = np.full((n, n), None)
                self.covfix = np.full((n, n), None)
                self.mean[var] = None

    def set_covariance(self, formula):
        # formula is expected as "lhs ~ rhs"
        lhs_str, rhs_str = formula.split('~')
        lhs_vars = self._parse_vars(lhs_str)
        rhs_vars = self._parse_vars(rhs_str)
        
# r2py:entity:f
        # Handle f(v) special case for shared variance
        is_shared_var = "f(" in rhs_str
        param_name = None
        if is_shared_var:
            param_name = rhs_str[rhs_str.find("(")+1 : rhs_str.find(")")]
            rhs_vars = [] # The RHS is a parameter, not a variable

        for lv in lhs_vars:
            self.add_var([lv])
            if is_shared_var:
                idx = self.index['vars'].index(lv)
                self.covpar[idx, idx] = param_name
            else:
                for rv in rhs_vars:
                    self.add_var([rv])
                    li = self.index['vars'].index(lv)
                    ri = self.index['vars'].index(rv)
                    self.cov[li, ri] = self.cov[ri, li] = 1

# r2py:entity:c
    def _parse_vars(self, s):
        s = s.strip()
        if s.startswith('c(') and s.endswith(')'):
            inner = s[2:-1]
            return [v.strip() for v in inner.split(',')]
        return [s]

    def get_covariance_structure(self):
        vars_list = self.index['vars']
        df = pd.DataFrame(index=vars_list, columns=vars_list)
        for i, v1 in enumerate(vars_list):
            for j, v2 in enumerate(vars_list):
                # In lava, the print output shows symbols from covpar
                val = self.covpar[i, j]
                if val is None:
                    val = '*' if i != j and self.cov[i, j] != 0 else ''
                df.iloc[i, j] = val
        return df

def lvm():
    return LVM()

# r2py:entity:covariance(m)
def covariance(m, formula=None):
    if formula is not None:
        m.set_covariance(formula)
        return m
    else:
        # Simulation of print(covariance(m))
        struct = m.get_covariance_structure()
        print("      Covariance parameters:")
        print("      " + " ".join(struct.columns))
        for idx, row in struct.iterrows():
            print(f"   {idx} " + " ".join(map(str, row.values)))
        return struct

# --- Execution ---

# suppressPackageStartupMessages(library(lava))
# import_lava simulated by LVM class

# m <- lvm()
m = lvm()

# covariance(m) <- y1~y2
covariance(m, formula="y1~y2")

# covariance(m) <- c(y1,y2)~f(v)
# r2py:entity:covariance(m)_1
covariance(m, formula="c(y1,y2)~f(v)")

# covariance(m)
# r2py:entity:covariance
covariance(m)