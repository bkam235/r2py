# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 26

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/smoke/20261001_140509/py/caret__rd_example__createDataPartition_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'caret__rd_example__createDataPartition_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['letters', 'oilType', 'x']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np
from plotnine import *
from sklearn.model_selection import train_test_split, KFold, StratifiedKFold, GroupKFold

# r2py:entity:data
# Simulating oil dataset
# Since 'oil' is a caret dataset, we approximate the structure
# oilType is usually the target variable
oil = pd.DataFrame({'oilType': np.random.choice(['Type1', 'Type2'], size=100)})

# r2py:entity:createDataPartition
# createDataPartition(oilType, 2)
# In caret, createDataPartition(y, p=2) creates 2 stratified resamples.
# Since p=2 is interpreted as 2 splits (each taking ~50% of data in this context),
# we simulate the R list output containing 'Resample1' and 'Resample2'.
indices = np.arange(len(oilType))
# To mimic the stratification, we split the indices based on the classes in oilType
unique_classes = np.unique(oilType)
resample1 = []
resample2 = []
for cls in unique_classes:
    cls_idx = indices[np.array(oilType) == cls]
    np.random.shuffle(cls_idx)
    mid = len(cls_idx) // 2
    resample1.extend(cls_idx[:mid])
    resample2.extend(cls_idx[mid:])

createDataPartition_out = {
    "Resample1": np.sort(np.array(resample1)),
    "Resample2": np.sort(np.array(resample2))
}

# r2py:entity:x
# x <- rgamma(50, 3, .5)
# In R, rgamma(n, shape, rate). In numpy, gamma(shape, scale) where scale = 1/rate

# r2py:entity:inA
# inA <- createDataPartition(x, list = FALSE)
# Approximation for continuous data: random split
inA = np.random.choice([True, False], size=len(x), p=[0.7, 0.3])

# r2py:entity:plot
# Plotting section
df_plot = pd.DataFrame({
    'val': x,
    'group': np.where(inA, 'A', 'B')
})

p = (ggplot(df_plot, aes(x='val', color='group')) 
     + geom_density() 
     + geom_rug())
print(p)

# r2py:entity:createResample
# createResample(oilType, 2)
# Approximation: Repeated Stratified K-Fold or simple stratified splits
resamples = [train_test_split(np.arange(len(oil)), test_size=0.5, stratify=oil['oilType'])[0] for _ in range(1)]

# r2py:entity:createFolds
# createFolds(oilType, 10)
skf = StratifiedKFold(n_splits=10)
folds_10 = [fold for _, fold in skf.split(np.zeros(len(oil)), oil['oilType'])]

# r2py:entity:createFolds_1
# createFolds(oilType, 5, FALSE)
# FALSE usually means not stratified in some contexts, but in caret it's the default.
# To simulate non-stratified:
kf = KFold(n_splits=5)
folds_5_nonstrat = [fold for _, fold in kf.split(np.zeros(len(oil)))]

# r2py:entity:createFolds_2
# createFolds(rnorm(21))
kf_21 = KFold(n_splits=5) # Default caret folds is usually 5 or based on data
folds_rnorm = [fold for _, fold in kf_21.split(np.random.randn(21))]

# r2py:entity:createTimeSlices
# createTimeSlices helper function approximation
def create_time_slices(data, initial_window, horizon, fixed_window=False, skip=1):
    slices = []
    n = len(data)
    start = 0
    while start + initial_window + horizon <= n:
        slices.append(np.arange(start, start + initial_window))
        if fixed_window:
            start += skip
        else:
            start += initial_window + horizon
    return slices

# createTimeSlices(1:9, 5, 1, fixedWindow = FALSE)
slices1 = create_time_slices(np.arange(1, 10), 5, 1, fixed_window=False)
# r2py:entity:createTimeSlices_1
# createTimeSlices(1:9, 5, 1, fixedWindow = TRUE)
slices2 = create_time_slices(np.arange(1, 10), 5, 1, fixed_window=True)
# r2py:entity:createTimeSlices_2
# createTimeSlices(1:9, 5, 3, fixedWindow = TRUE)
slices3 = create_time_slices(np.arange(1, 10), 5, 3, fixed_window=True)
# r2py:entity:createTimeSlices_3
# createTimeSlices(1:9, 5, 3, fixedWindow = FALSE)
slices4 = create_time_slices(np.arange(1, 10), 5, 3, fixed_window=False)

# r2py:entity:createTimeSlices_4
# createTimeSlices(1:15, 5, 3)
slices5 = create_time_slices(np.arange(1, 16), 5, 3)
# r2py:entity:createTimeSlices_5
# createTimeSlices(1:15, 5, 3, skip = 2)
slices6 = create_time_slices(np.arange(1, 16), 5, 3, skip=2)
# r2py:entity:createTimeSlices_6
# createTimeSlices(1:15, 5, 3, skip = 3)
slices7 = create_time_slices(np.arange(1, 16), 5, 3, skip=3)

# r2py:entity:set.seed
# set.seed(131)
np.random.seed(131)
# r2py:entity:groups
# groups <- sort(sample(letters[1:4], size = 20, replace = TRUE))
groups = sorted(np.random.choice(letters, size=20, replace=True))
# r2py:entity:table
print(pd.Series(groups).value_counts())

# r2py:entity:folds
# folds <- groupKFold(groups)
gkf = GroupKFold(n_splits=5)
# GroupKFold requires X and y; we use dummy X
X_dummy = np.zeros((20, 1))
y_dummy = np.arange(20)
folds = [fold for _, fold in gkf.split(X_dummy, y_dummy, groups=groups)]

# r2py:entity:lapply
# lapply(folds, function(x, y) table(y[x]), y = groups)
for fold in folds:
    fold_groups = [groups[i] for i in fold]
    print(pd.Series(fold_groups).value_counts())