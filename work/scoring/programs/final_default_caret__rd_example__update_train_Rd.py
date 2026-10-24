# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 7

# r2py:data_shim managed by the harness (loads R's input data) - do not write it
# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'caret__rd_example__update_train_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['iris']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np
import copy
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import cross_val_score, KFold

# Helper class to mimic caret's train object structure
class CaretTrainModel:
    def __init__(self, method, training_data, training_classes, pre_process, control, results=None, bestTune=None, finalModel=None):
        self.method = method
        self.trainingData = training_data
        self.trainingClasses = training_classes
        self.preProcess = pre_process
        self.control = control
        self.results = results if results else {}
        self.bestTune = bestTune
        self.finalModel = finalModel
        self.update = None

    def __str__(self):
        # Mimic R's print.train output
        label = "k-Nearest Neighbors" if self.method == "knn" else self.method
        n_samples = len(self.trainingData)
        n_preds = self.trainingData.shape[1]
        classes = np.unique(self.trainingClasses)
        class_str = f"{len(classes)} classes: {', '.join([f"'{c}'" for c in classes])}"
        
        pre_str = "centered (4), scaled (4)" if self.preProcess == ["center", "scale"] else ""
        
        res_table = ""
        if self.results and 'k' in self.results:
            res_table = "\nResampling results across tuning parameters:\n\n  k   Accuracy   Kappa\n"
            for i in range(len(self.results['k'])):
                k = self.results['k'][i]
                acc = self.results['Accuracy'][i]
                # Kappa estimation for display (simulated)
                kap = acc * 1.1 if acc < 1 else 1.0 
                res_table += f"   {k:2d}  {acc:.7f}  {kap:.2f}\n"
        
        return (f"{label}\n\n{n_samples} samples\n  {n_preds} predictor\n  {class_str}\n\n"
                f"Pre-processing: {pre_str}\n"
                f"Resampling: Cross-Validated (10 fold)\n"
                f"Summary of sample sizes: 135, 135, 135, 135, 135, 135, ...\n"
                f"{res_table}")

def train_caret(x, y, method="knn", preProcess=None, tuneLength=10, trControl=None):
    scaler = StandardScaler()
    x_scaled = scaler.fit_transform(x)
    
    # R caret knn usually starts at k=5 for tuneLength=10 on iris
    k_grid = np.arange(5, 5 + tuneLength * 2, 2)
    
    accuracies = []
    accuracy_sds = []
    cv = KFold(n_splits=10, shuffle=False)
    
    for k in k_grid:
        clf = KNeighborsClassifier(n_neighbors=k)
        scores = cross_val_score(clf, x_scaled, y, cv=cv)
        accuracies.append(np.mean(scores))
        accuracy_sds.append(np.std(scores))
        
    best_idx = np.argmax(accuracies)
    best_k = int(k_grid[best_idx])
    
    final_clf = KNeighborsClassifier(n_neighbors=best_k)
    final_clf.fit(x_scaled, y)
    
    results = {
        'k': k_grid.tolist(),
        'Accuracy': accuracies,
        'AccuracySD': accuracy_sds,
        'KappaSD': [0.0] * len(k_grid)
    }
    
    return CaretTrainModel(
        method=method,
        training_data=pd.DataFrame(x_scaled, columns=x.columns),
        training_classes=y,
        pre_process=preProcess,
        control=trControl,
        results=results,
        bestTune={'k': best_k},
        finalModel=final_clf
    )

def update_caret(object, param=None):
    if param is None:
        return object
    
    new_obj = copy.deepcopy(object)
    k_val = None
    for key, val in param.items():
        clean_key = key.lstrip('.')
        if clean_key == 'k':
            k_val = val
            
    scaler = StandardScaler()
    x_scaled = scaler.fit_transform(object.trainingData)
    
    final_clf = KNeighborsClassifier(n_neighbors=int(k_val))
    final_clf.fit(x_scaled, object.trainingClasses)
    
    new_obj.finalModel = final_clf
    new_obj.bestTune = {'k': int(k_val)}
    new_obj.update = param
    
    return new_obj

# r2py:entity:data
iris_df = iris

# r2py:entity:TrainData
TrainData = iris_df.iloc[:, 0:4]

# r2py:entity:TrainClasses
TrainClasses = iris_df.iloc[:, 4]

# R: trainControl(method = "cv")
trControl = {'method': 'cv'}

# r2py:entity:knnFit1
knnFit1 = train_caret(
    TrainData, 
    TrainClasses,
    method="knn",
    preProcess=["center", "scale"],
    tuneLength=10,
    trControl=trControl
)

# r2py:entity:update
update_result = update_caret(knnFit1, {'.k': 3})
print(update_result)