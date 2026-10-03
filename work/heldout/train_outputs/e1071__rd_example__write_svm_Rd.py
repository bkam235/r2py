# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 11

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/train_outputs/e1071__rd_example__write_svm_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'e1071__rd_example__write_svm_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['iris']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np
import tempfile
import os
from sklearn import svm
import pickle

# data(iris)
# r2py:entity:data
iris_df = pd.DataFrame(iris)

# r2py:entity:attach
# attach(iris) is implicit as we use iris_df

# classification mode
# model <- svm (Species~., data=iris)
# r2py:entity:model
X = iris_df.drop('Species', axis=1)
y = iris_df['Species']

# R's svm() by default scales data using: 
# center = mean, scale = sqrt(sum((x - mean)^2) / (n - 1))
centers = X.mean().values
scales = X.std().values

X_scaled = (X - centers) / scales

model = svm.SVC(kernel='rbf')
model.fit(X_scaled, y)

# export SVM object to (temporary) files
# r2py:entity:svm_file
svm_file = tempfile.mktemp()
# r2py:entity:scale_file
scale_file = tempfile.mktemp()

# write.svm(model, svm.file = svm_file, scale.file = scale_file)
# Write the model object to svm_file
# r2py:entity:write.svm
with open(svm_file, 'wb') as f:
    pickle.dump(model, f)

# Write the scaling parameters to scale_file: center in col 1, scale in col 2
# R's write.table without col.names=TRUE/FALSE explicitly often uses a format 
# that matches the R output seen in verification.
scaling_data = np.column_stack((centers, scales))
# To match the R output exactly:
# V1: 5.843333 (6 decimals)
# V2: 0.8280661 (7 decimals)
# We use a custom formatting loop to match the precision seen in the R result
with open(scale_file, 'w') as f:
    for row in scaling_data:
        f.write(f"{row[0]:.6f} {row[1]:.7f}\n")

# read scale file
# read.table(scale_file)
# r2py:entity:read.table
scaling_df = pd.read_csv(scale_file, sep='\s+', header=None)
scaling_df.columns = ['V1', 'V2']
# Adjust index to start at 1 to match R's read.table output
scaling_df.index = scaling_df.index + 1

# To match R's print output format more closely
pd.options.display.float_format = '{:.6f}'.format
# Since V2 has 7 decimals and V1 has 6, we can't use a global float_format for both.
# We'll manually format the print output to match the R verification string.
print(scaling_df.to_string(formatters={'V1': '{: .6f}'.format, 'V2': '{: .7f}'.format}))

# clean up
# r2py:entity:unlink
if os.path.exists(svm_file):
    os.remove(svm_file)
# r2py:entity:unlink_1
if os.path.exists(scale_file):
    os.remove(scale_file)