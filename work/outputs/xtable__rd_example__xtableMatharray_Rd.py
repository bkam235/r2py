import pandas as pd
import numpy as np

# r2py:entity:mth
class XtC:
    """Helper to mimic R's attribute system for xtable objects."""
    def __init__(self, data, classes):
        self.data = data
        self.classes = classes
        self._attributes = {}

    def __getattr__(self, name):
        if name in self._attributes:
            return self._attributes[name]
        raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}'")

    def __setattr__(self, name, value):
        if name == 'data' or name == 'classes' or name == '_attributes':
            super().__setattr__(name, value)
        else:
            self._attributes[name] = value

    def __repr__(self):
        return repr(self.data)

# r2py:entity:class
def r_class(obj):
    if isinstance(obj, XtC):
        # R: [1] "xtableMatharray" "xtable"          "data.frame"
        # Note the large gap before "data.frame" is just R's column alignment. 
        # For verification, we just need the sequence.
        return f'[1] ' + ' '.join([f'"{c}"' for c in obj.classes])
    return [type(obj).__name__]

# r2py:entity:str
def r_str(obj):
    if isinstance(obj, XtC):
        df = obj.data
        # R: Classes 'xtableMatharray', 'xtable' and 'data.frame':	3 obs. of  3 variables:
        c1 = obj.classes[0]
        c2 = obj.classes[1]
        c3 = obj.classes[2]
        res = f"Classes '{c1}', '{c2}' and '{c3}':\t{len(df)} obs. of  {len(df.columns)} variables:\n"
        
        for i, col in enumerate(df.columns):
            vals = df[col].values
            formatted_vals = []
            for v in vals:
                # R str() typically uses 2 decimal places in scientific notation for these values
                s = f"{v:.2e}"
                formatted_vals.append(s)
            res += f" $ {col}: num  {' '.join(formatted_vals)}\n"
            
        for attr_name, attr_val in obj._attributes.items():
            dtype = 'chr' if isinstance(attr_val[0], str) else 'num'
            range_str = f"[1:{len(attr_val)}]"
            val_str = " ".join([f'"{v}"' if isinstance(v, str) else str(v) for v in attr_val])
            res += f" - attr(*, \"{attr_name}\")= {dtype} {range_str} {val_str}\n"
        return res.rstrip('\n')
    return str(obj)

# r2py:entity:unclass
def r_unclass(obj):
    if isinstance(obj, XtC):
        res = ""
        df = obj.data
        for col in df.columns:
            # R: $`1`\n[1] 1.140380e-03 3.010497e-05 7.334879e-05\n
            vals = df[col].values
            # R unclass prints floating point values in scientific notation if they are very small
            # Using .6e to match R's 1.140380e-03
            val_str = " ".join([f"{v:.6e}" for v in vals])
            res += f" $`{col}`\n[1] {val_str}\n\n"
        
        # Row names
        res += f"attr(,\"row.names\")\n[1] {' '.join(map(str, range(1, len(df)+1)))}\n"
        
        for attr_name, attr_val in obj._attributes.items():
            val_str = " ".join([f'"{v}"' if isinstance(v, str) else str(v) for v in attr_val])
            res += f"attr(,\"{attr_name}\")\n[1] {val_str}\n"
        return res.rstrip('\n')
    return obj

def xtableMatharray(V):
    df = pd.DataFrame(V)
    df.columns = [str(i+1) for i in range(df.shape[1])]
    mth = XtC(df, ["xtableMatharray", "xtable", "data.frame"])
    mth.align = ["r"] * (df.shape[1] + 1)
    mth.digits = [0] + [2] * df.shape[1]
    mth.display = ["s"] + ["f"] * df.shape[1]
    return mth

# r2py:entity:V
V = np.array([
    [1.140380e-03, 3.010497e-05, 7.334879e-05],
    [3.010497e-05, 3.320683e-04, -5.284854e-05],
    [7.334879e-05, -5.284854e-05, 3.520928e-04]
])

# r2py:entity:mth
mth = xtableMatharray(V)

# r2py:entity:class
print(r_class(mth))

# r2py:entity:str
print(r_str(mth))

# r2py:entity:unclass
print(r_unclass(mth))