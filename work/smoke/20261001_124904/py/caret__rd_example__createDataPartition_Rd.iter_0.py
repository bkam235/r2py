# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 26

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/smoke/20261001_124904/py/caret__rd_example__createDataPartition_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'caret__rd_example__createDataPartition_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['letters', 'oilType', 'x']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, KFold, StratifiedKFold, GroupKFold
from plotnine import ggplot, aes, geom_density, geom_rug

# r2py:entity:data
# Data setup (Approximating 'oil' dataset from caret)
# oil typically has a binary factor oilType
np.random.seed(42)
oil = pd.DataFrame({'oilType': np.random.choice(['A', 'B'], size=100)})

# r2py:entity:createDataPartition
# createDataPartition(oilType, 2)
# caret's createDataPartition performs stratified sampling
train_idx, test_idx = train_test_split(
    np.arange(len(oil)), 
    test_size=0.5, 
    stratify=oil['oilType'], 
    random_state=42
)

# r2py:entity:x
# x <- rgamma(50, 3, .5)

# r2py:entity:inA
# inA <- createDataPartition(x, list = FALSE)
# For continuous x, createDataPartition usually defaults to simple random split
inA = np.random.permutation(len(x))[:25] 
not_inA = np.array([i for i in range(len(x)) if i not in inA])

# r2py:entity:plot
# Plotting density and rugs
df_plot = pd.DataFrame({
    'val': np.concatenate([x[inA], x[not_inA]]),
    'group': ['A'] * len(inA) + ['B'] * len(not_inA)
})

plot = (
    ggplot(df_plot, aes(x='val', color='group')) 
    + geom_density() 
    + geom_rug()
)
print(plot)

# r2py:entity:createResample
# createResample(oilType, 2)
# Generates multiple stratified splits
resamples = []
for _ in range(10): # Default caret behavior generates multiple
    idx = train_test_split(np.arange(len(oil)), test_size=0.5, stratify=oil['oilType'])[0]
    resamples.append(idx)

# r2py:entity:createFolds
# createFolds(oilType, 10)
skf_10 = StratifiedKFold(n_splits=10, shuffle=True, random_state=42)
folds_10 = [fold for _, fold in skf_10.split(np.arange(len(oil)), oil['oilType'])]

# r2py:entity:createFolds_1
# createFolds(oilType, 5, FALSE) -> FALSE means not stratified
kf_5 = KFold(n_splits=5, shuffle=True, random_state=42)
folds_5 = [fold for _, fold in kf_5.split(np.arange(len(oil)))]

# r2py:entity:createFolds_2
# createFolds(rnorm(21))
x_norm = np.random.normal(size=21)
kf_norm = KFold(n_splits=10, shuffle=True, random_state=42) # Default folds is 10
folds_norm = [fold for _, fold in kf_norm.split(np.arange(len(x_norm)))]

# r2py:entity:createTimeSlices
# createTimeSlices implementation
def create_time_slices(data, initial_window, horizon, fixed_window=False, skip=1):
    slices = []
    n = len(data)
    start = 0
    while start + initial_window <= n:
        end = start + initial_window
        # Horizon check
        if end + horizon > n:
            break
        slices.append(np.arange(start, end))
        if fixed_window:
            start += skip
        else:
            start = end # sliding window moving by window size
    return slices

# createTimeSlices(1:9, 5, 1, fixedWindow = FALSE)
ts1 = create_time_slices(np.arange(1, 10), 5, 1, fixed_window=False)
# r2py:entity:createTimeSlices_1
# createTimeSlices(1:9, 5, 1, fixedWindow = TRUE)
ts2 = create_time_slices(np.arange(1, 10), 5, 1, fixed_window=True)
# r2py:entity:createTimeSlices_2
# createTimeSlices(1:9, 5, 3, fixedWindow = TRUE)
ts3 = create_time_slices(np.arange(1, 10), 5, 3, fixed_window=True)
# r2py:entity:createTimeSlices_3
# createTimeSlices(1:9, 5, 3, fixedWindow = FALSE)
ts4 = create_time_slices(np.arange(1, 10), 5, 3, fixed_window=False)

# r2py:entity:createTimeSlices_4
# createTimeSlices(1:15, 5, 3)
ts5 = create_time_slices(np.arange(1, 16), 5, 3)
# r2py:entity:createTimeSlices_5
# createTimeSlices(1:15, 5, 3, skip = 2)
ts6 = create_time_slices(np.arange(1, 16), 5, 3, skip=2)
# r2py:entity:createTimeSlices_6
# createTimeSlices(1:15, 5, 3, skip = 3)
ts7 = create_time_slices(np.arange(1, 16), 5, 3, skip=3)

# Set seed and groupKFold
# r2py:entity:set.seed
np.random.seed(131)
# r2py:entity:groups
groups = sorted(np.random.choice(letters, size=20, replace=True))
groups_arr = np.array(groups)

# r2py:entity:table
print(pd.Series(groups_arr).value_counts())

# r2py:entity:folds
gkf = GroupKFold(n_splits=5) # Default splits for groupKFold usually depends on data, assume 5
folds = [fold for _, fold in gkf.split(np.arange(len(groups_arr)), groups=groups_arr)]

# r2py:entity:lapply
# lapply(folds, function(x, y) table(y[x]), y = groups)
fold_tables = [pd.Series(groups_arr[fold]).value_counts() for fold in folds]
for i, table in enumerate(fold_tables):
    print(f"Fold {i}:")
    print(table)