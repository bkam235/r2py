# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'bit64__rd_example__benchmark64_data_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['benchmark64.data']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# The data shim loads 'benchmark64.data' as a list or similar structure.
# R's benchmark64.data is a matrix/dataframe.
# We need to ensure it's a DataFrame with proper index and columns.
# r2py:entity:data
if 'benchmark64.data' in globals():
    # If the shim loaded it as a list of lists/dicts, convert to DataFrame
    # R's benchmark64.data usually has row names and col names.
    # Based on R output: rows are tasks, cols are contexts.
    raw_data = globals()['benchmark64.data']
    if isinstance(raw_data, dict):
        # Handle case where it might be a dict representing a dataframe
        benchmark64_data = pd.DataFrame(raw_data)
    else:
        # Handle list/array representation
        benchmark64_data = pd.DataFrame(raw_data)
else:
    # Fallback if shim fails (though it shouldn't)
    benchmark64_data = pd.DataFrame()

# In R: data(benchmark64.data)
# print(benchmark64.data)
# r2py:entity:print
print(benchmark64_data)

# R: matplot(log2(benchmark64.data[-1,1]/benchmark64.data[-1,]), ...)
# benchmark64.data[-1, 1] is the first column excluding the first row.
# benchmark64.data[-1, ] is the entire matrix excluding the first row.

# r2py:entity:matplot
# Extract values excluding the first row
subset_data = benchmark64_data.iloc[1:, :].values
first_col = subset_data[:, 0]
relative_speed = np.log2(first_col[:, np.newaxis] / subset_data)

# First plot
plt.figure()
# R pch=c("3", "6", "h", "s", "o", "a") 
# Python approximations: '3'->'v', '6'->'^', 'h'->'H', 's'->'s', 'o'->'o', 'a'->'.'
markers = ['v', '^', 'H', 's', 'o', '.']
for i in range(relative_speed.shape[1]):
    plt.plot(range(1, relative_speed.shape[0] + 1), relative_speed[:, i], 
             marker=markers[i] if i < len(markers) else 'o', linestyle='None')
plt.xlabel("tasks [last=session]")
plt.ylabel("log2(relative speed) [bigger is better]")

# r2py:entity:matplot_1
# Second plot: matplot(t(log2(benchmark64.data[-1,1]/benchmark64.data[-1,])), ...)
plt.figure()
relative_speed_t = relative_speed.T
# R: lwd=c(rep(1, 14), 3) -> first 14 lines width 1, 15th width 3
# Note: The number of lines depends on the number of columns in original data.
lwd_vals = [1] * 14 + [3]

for i in range(relative_speed_t.shape[0]):
    lw = lwd_vals[i] if i < len(lwd_vals) else 1
    plt.plot(range(1, relative_speed_t.shape[1] + 1), relative_speed_t[i, :], 
             marker='o', markerfacecolor='none', linewidth=lw)

# axis(1, labels=c("32-bit", "64-bit", "hash", "sortorder", "order", "hash+sortorder"), at=1:6)
# r2py:entity:axis
plt.xticks(
    ticks=range(1, 7), 
    labels=["32-bit", "64-bit", "hash", "sortorder", "order", "hash+sortorder"]
)
# r2py:entity:axis_1
# axis(2)
plt.ylabel("log2(relative speed) [bigger is better]")
plt.xlabel("context")

plt.show()