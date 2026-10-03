# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 9

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/train_outputs/caret__rd_example__knn3_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'caret__rd_example__knn3_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['iris', 'iris3']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np
from sklearn.neighbors import KNeighborsClassifier

# irisFit1 <- knn3(Species ~ ., iris)
# r2py:entity:irisFit1
iris_df = pd.DataFrame(iris)
X1 = iris_df.drop('Species', axis=1)
y1 = iris_df['Species']
irisFit1 = KNeighborsClassifier().fit(X1, y1)

# irisFit2 <- knn3(as.matrix(iris[, -5]), iris[,5])
# r2py:entity:irisFit2
X2 = iris_df.iloc[:, :4].values
y2 = iris_df.iloc[:, 4].values
irisFit2 = KNeighborsClassifier().fit(X2, y2)

# data(iris3) is already loaded via shim
# R: train <- rbind(iris3[1:25,,1], iris3[1:25,,2], iris3[1:25,,3])
# iris3 is 50x4x3. R index 1:25 is Python 0:25.
# iris3[1:25,,1] means rows 1 to 25, all columns, slice 1.
# r2py:entity:train
train = np.vstack([
    np.array(iris3)[0:25, :, 0],
    np.array(iris3)[0:25, :, 1],
    np.array(iris3)[0:25, :, 2]
])

# test <- rbind(iris3[26:50,,1], iris3[26:50,,2], iris3[26:50,,3])
# r2py:entity:test
test = np.vstack([
    np.array(iris3)[25:50, :, 0],
    np.array(iris3)[25:50, :, 1],
    np.array(iris3)[25:50, :, 2]
])

# cl <- factor(c(rep("s",25), rep("c",25), rep("v",25)))
# r2py:entity:cl
cl = np.array(["s"] * 25 + ["c"] * 25 + ["v"] * 25)

# r2py:entity:knn3Train
def knn3Train_impl(train_val, test_val, cl_val, k=1, l=0, prob=True, use_all=True):
    # Fit the model on train_val with labels cl_val
    knn = KNeighborsClassifier(n_neighbors=k)
    knn.fit(train_val, cl_val)
    
    # Predict classes
    preds = knn.predict(test_val)
    
    if prob:
        probs = knn.predict_proba(test_val)
        # In R, the result is a factor with a 'prob' attribute.
        # We return a custom object to mimic this attribute.
        class Result:
            def __init__(self, value, prob_val):
                self.value = value
                self.prob = prob_val
            def __repr__(self):
                return repr(self.value)
            def __len__(self):
                return len(self.value)
            def __getitem__(self, key):
                return self.value[key]
        
        return Result(preds, probs)
    
    return preds

# knn3Train(train, test, cl, k = 5, prob = TRUE)
# r2py:entity:knn3Train
knn3Train = knn3Train_impl(train, test, cl, k=5, prob=True)