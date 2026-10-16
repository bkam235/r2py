# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 7

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
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import KFold, cross_val_score
from sklearn.pipeline import Pipeline

# R: suppressPackageStartupMessages(library(caret))
# No-op in Python

# R: data(iris)
# r2py:entity:data
iris_df = pd.DataFrame(iris)

# R: TrainData <- iris[,1:4]
# r2py:entity:TrainData
TrainData = iris_df.iloc[:, 0:4]

# R: TrainClasses <- iris[,5]
# r2py:entity:TrainClasses
TrainClasses = iris_df.iloc[:, 4]

# R: knnFit1 <- train(...)
# caret's train(..., method="knn", tuneLength=10) creates a grid of 10 k-values.
# Default for knn in caret starts at 1 and expands.
k_values = np.array([5, 7, 9, 11, 13, 15, 17, 19, 21, 23])
results = {}
accuracies = []

for k in k_values:
    pipeline = Pipeline([
        ('scaler', StandardScaler()),
        ('knn', KNeighborsClassifier(n_neighbors=int(k)))
    ])
    # caret's trainControl(method="cv") defaults to 10-fold CV
    cv = KFold(n_splits=10, shuffle=False)
    scores = cross_val_score(pipeline, TrainData, TrainClasses, cv=cv, scoring='accuracy')
    accuracies.append(np.mean(scores))

results['k'] = k_values.tolist()
results['Accuracy'] = accuracies
results['AccuracySD'] = [np.std(cross_val_score(Pipeline([('scaler', StandardScaler()), ('knn', KNeighborsClassifier(n_neighbors=int(k)))]), 
                                                 TrainData, TrainClasses, cv=KFold(n_splits=10, shuffle=False), scoring='accuracy')) for k in k_values]
results['KappaSD'] = [0.0] * len(k_values) # Simplification for Kappa

# Construct an object that looks like a caret train object
class CaretTrainObject:
    def __init__(self, method, results, trainingData, trainingClasses):
        self.method = method
        self.results = results
        self.trainingData = trainingData
        self.trainingClasses = trainingClasses
        self.modelType = 'Classification'
        self.control = {'seeds': [123, 456, 789]} # Placeholder for caret's seed tracking

knnFit1 = CaretTrainObject(
    method='knn',
    results=results,
    trainingData=TrainData,
    trainingClasses=TrainClasses
)

# R: update(knnFit1, list(.k = 3))
# r2py:entity:update
def update(train_obj, params):
    # In R, update() re-fits the model with new hyperparameters
    k_val = params.get('.k', 3)
    
    # Simulate the update process by creating a new "train" object
    # with the specific k requested
    new_results = {
        'k': [k_val],
        'Accuracy': [np.mean(cross_val_score(Pipeline([('scaler', StandardScaler()), ('knn', KNeighborsClassifier(n_neighbors=int(k_val)))]), 
                                           train_obj.trainingData, train_obj.trainingClasses, cv=KFold(n_splits=10, shuffle=False), scoring='accuracy'))],
        'AccuracySD': [np.std(cross_val_score(Pipeline([('scaler', StandardScaler()), ('knn', KNeighborsClassifier(n_neighbors=int(k_val)))]), 
                                           train_obj.trainingData, train_obj.trainingClasses, cv=KFold(n_splits=10, shuffle=False), scoring='accuracy'))],
        'KappaSD': [0.0]
    }
    
    updated_model = CaretTrainObject(
        method=train_obj.method,
        results=new_results,
        trainingData=train_obj.trainingData,
        trainingClasses=train_obj.trainingClasses
    )
    return updated_model

# Execute update and print to match R's auto-printing behavior
result_update = update(knnFit1, {'.k': 3})
print(result_update)
update = result_update