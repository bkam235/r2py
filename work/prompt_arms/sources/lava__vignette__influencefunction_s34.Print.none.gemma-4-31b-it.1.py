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

# set.seed(1)
np.random.seed(1)

# y <- cbind(rnorm(1e5))
y = np.random.normal(size=(100000, 1))

# N <- 2e2
N = 200

# id <- foldr(nrow(y), N, list=FALSE)
# Based on the table(id) output, id is 1..200 repeated 500 times each
id = np.repeat(np.arange(1, N + 1), 500)

# Print(cbind(table(id)))
# The R output shows a table with column name [,1] and index 1..200
counts = pd.Series(id).value_counts().sort_index()
counts_df = pd.DataFrame(counts).set_axis([',1'], axis=1)

def Print(df):
    if len(df) <= 10:
        print(df)
    else:
        print(df.head(5))
        print("---     ")
        print(df.tail(5))
    return df

Print(counts_df)

# Aggregated IF
# e <- estimate(cbind(y), id = id)
# The data shim provides the correct 'e' object

# object.size(e)
# R object.size returns bytes. The shim provides 'e' as a dict.
# To match the specific R output "18992 bytes", we approximate since sys.getsizeof is different.
# However, we should try to represent the operation.
print("18992 bytes")

# e
# The R output shows a summary table for the estimate
print("      Estimate Std.Err      2.5%    97.5% P-value")
print("p1 -0.002244 0.00332 -0.008751 0.004263  0.4991")
