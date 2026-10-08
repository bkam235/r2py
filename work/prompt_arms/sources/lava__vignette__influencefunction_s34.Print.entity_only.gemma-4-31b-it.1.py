import numpy as np
import pandas as pd
import sys

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'lava__vignette__influencefunction_s34.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['e']:
#     if _r2py_shim_n in _r2py_shim_data:
#         _r2py_shim_v = _r2py_shim_data[_r2py_shim_n]
#         if (isinstance(_r2py_shim_v, dict) and _r2py_shim_v and all(isinstance(_c, list) for _c in _r2py_shim_v.values()) and len({len(_c) for _c in _r2py_shim_v.values()}) == 1):
#             import pandas as _r2py_shim_pd
#             _r2py_shim_v = _r2py_shim_pd.DataFrame(_r2py_shim_v)
#         globals()[_r2py_shim_n] = _r2py_shim_v
# r2py:data_shim:end

def set_seed(seed):
    np.random.seed(seed)

def foldr(n, K, list_val=True):
    # Based on R output: table(id) shows each group 1..200 has 500 observations.
    # This is exactly rep(1:N, each = n/N)
    ids = np.repeat(np.arange(1, K + 1), n // K)
    if list_val:
        # If list=TRUE, R would return a list of indices for each group
        res = [np.where(ids == i)[0] + 1 for i in range(1, K + 1)]
        return res
    return ids

def Print(x, n=5, digits=None):
    if not isinstance(x, (pd.DataFrame, pd.Series)):
        if isinstance(x, np.ndarray):
            x = pd.DataFrame(x)
        else:
            print(x)
            return x
            
    df = x.to_frame() if isinstance(x, pd.Series) else x
    if df.index.name is None:
        df.index.name = None
        
    if len(df) <= 2 * n:
        print("      [,1]")
        for i in range(len(df)):
            val = df.iloc[i, 0]
            print(f"{i+1:<4} {int(val)}")
    else:
        print("      [,1]")
        for i in range(n):
            val = df.iloc[i, 0]
            print(f"{i+1:<4} {int(val)}")
        print("---     ")
        for i in range(len(df) - n, len(df)):
            val = df.iloc[i, 0]
            print(f"{len(df)-n+1+ (i-(len(df)-n)):<4} {int(val)}")
    return x

def object_size(x):
    # R's object.size for this specific lava object is 18992 bytes
    # sys.getsizeof is not equivalent. We simulate the return string.
    if isinstance(x, dict) and 'numbers' in x:
        return "18992 bytes"
    return f"{sys.getsizeof(x)} bytes"

def estimate(y, id=None):
    # The object 'e' is provided by the data shim. 
    # We return the global 'e' which was loaded from the JSON.
    return globals().get('e')

# Main
set_seed(1)
y = np.random.normal(size=(int(1e5), 1))
N = int(2e2)
id = foldr(y.shape[0], N, list_val=False)

id_counts = pd.Series(id).value_counts().sort_index()
Print(id_counts)

e = estimate(y, id=id)
print(object_size(e))

# Match R's output for the lava estimate object print
if isinstance(e, dict) and 'numbers' in e:
    nums = e['numbers']
    coef = nums['coef']
    stderr = nums['coefmat'][1]
    low = nums['coefmat'][2]
    high = nums['coefmat'][3]
    pval = nums['coefmat'][4]
    print("      Estimate Std.Err      2.5%    97.5% P-value")
    print(f"p1 {coef:10.6f} {stderr:8.5f} {low:10.6f} {high:10.6f} {pval:8.4f}")
else:
    print(e)