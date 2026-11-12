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
from sklearn.model_selection import KFold, cross_val_score, GridSearchCV
from sklearn.pipeline import Pipeline

# Helper class to mimic caret's train object structure
class CaretTrainModel:
    def __init__(self, method, training_data, training_classes, pre_process, control, results, bestTune, finalModel):
        self.method = method
        self.trainingData = training_data
        self.trainingClasses = training_classes
        self.preProcess = pre_process
        self.control = control
        self.results = results
        self.bestTune = bestTune
        self.finalModel = finalModel

def update(model, params):
    """
    Mimics caret::update.train. 
    Updates the model with new tuning parameters.
    """
    k_val = params.get('.k')
    
    # Re-fit the model with the specific parameter provided
    pipeline = Pipeline([
        ('scaler', StandardScaler()),
        ('knn', KNeighborsClassifier(n_neighbors=k_val))
    ])
    pipeline.fit(model.trainingData, model.trainingClasses)
    
    # For the updated model, caret typically updates the finalModel and bestTune
    # The results table remains from the original tuning unless otherwise specified,
    # but we update the internal state to reflect the new 'best' parameter.
    updated_model = CaretTrainModel(
        method=model.method,
        training_data=model.trainingData,
        training_classes=model.trainingClasses,
        pre_process=model.preProcess,
        control=model.control,
        results=model.results,
        bestTune={'k': k_val},
        finalModel=pipeline
    )
    return updated_model

# R: data(iris)
# The data is provided by the shim as 'iris'
iris_df = iris

# R: TrainData <- iris[,1:4]
TrainData = iris_df.iloc[:, 0:4]

# R: TrainClasses <- iris[,5]
# Note: R's iris[,5] is a factor; Python's iloc returns a Series
TrainClasses = iris_df.iloc[:, 4]

# R: knnFit1 <- train(...)
# method = "knn", preProcess = c("center", "scale"), tuneLength = 10, trControl = trainControl(method = "cv")
# tuneLength = 10 means caret chooses 10 values for k. 
# For knn, these are typically sequences like 1, 3, 5... or similar.
k_values = np.arange(1, 20, 2) # Standard caret-like sequence for tuneLength=10
results_list = []

# Simulating the CV process to populate the 'results' object
cv = KFold(n_splits=10, shuffle=False)
best_acc = -1
best_k = None

for k in k_values:
    pipeline = Pipeline([
        ('scaler', StandardScaler()),
        ('knn', KNeighborsClassifier(n_neighbors=k))
    ])
    # Accuracy and AccuracySD
    scores = cross_val_score(pipeline, TrainData, TrainClasses, cv=cv, scoring='accuracy')
    acc = np.mean(scores)
    std = np.std(scores)
    results_list.append({'k': k, 'Accuracy': acc, 'AccuracySD': std})
    
    if acc > best_acc:
        best_acc = acc
        best_k = k

# Caret's results is a data frame
results_df = pd.DataFrame(results_list)

# Fit the final model using the best k
final_pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('knn', KNeighborsClassifier(n_neighbors=best_k))
])
final_pipeline.fit(TrainData, TrainClasses)

knnFit1 = CaretTrainModel(
    method='knn',
    training_data=TrainData,
    training_classes=TrainClasses,
    pre_process=['center', 'scale'],
    control={'method': 'cv'},
    results=results_df,
    bestTune={'k': best_k},
    finalModel=final_pipeline
)

# R: update(knnFit1, list(.k = 3))
# The result of update() is printed in R
updated_knn = update(knnFit1, {'.k': 3})
print(updated_knn)