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
from sklearn.model_selection import KFold, GridSearchCV
from sklearn.pipeline import Pipeline

# Mimic caret's train object structure
class CaretTrainModel:
    def __init__(self, estimator, training_data, training_classes, pre_process, control, results):
        self.finalModel = estimator
        self.trainingData = training_data
        self.trainingClasses = training_classes
        self.preProcess = pre_process
        self.control = control
        self.results = results
        self.bestTune = results['k'][np.argmax(results['Accuracy'])] if 'Accuracy' in results else None

    def update_model(self, params):
        # Extract .k
        k_val = params.get('.k')
        
        # Re-fit the model with the new parameter
        pipeline = Pipeline([
            ('scaler', StandardScaler()),
            ('knn', KNeighborsClassifier(n_neighbors=k_val))
        ])
        pipeline.fit(self.trainingData, self.trainingClasses)
        
        # Update the object
        self.finalModel = pipeline
        # When update() is called with a specific k, results effectively collapse to that k
        self.results = {'k': [k_val], 'Accuracy': [pipeline.score(self.trainingData, self.trainingClasses)]}
        self.bestTune = k_val
        return self

# R: data(iris)
# The data shim already provides 'iris'
data = iris 

# R: TrainData <- iris[,1:4]
TrainData = iris.iloc[:, 0:4]

# R: TrainClasses <- iris[,5]
TrainClasses = iris.iloc[:, 4]

# R: knnFit1 <- train(...)
# caret's tuneLength = 10 for knn means it tests 10 values of k (usually 1, 3, 5, ..., 19)
k_values = np.arange(1, 20, 2)
param_grid = {'knn__n_neighbors': k_values}

pipeline_init = Pipeline([
    ('scaler', StandardScaler()),
    ('knn', KNeighborsClassifier())
])

cv = KFold(n_splits=10, shuffle=False)

grid_search = GridSearchCV(
    estimator=pipeline_init,
    param_grid=param_grid,
    cv=cv,
    scoring='accuracy'
)
grid_search.fit(TrainData, TrainClasses)

# Construct the results dictionary to match caret's format
# We need Accuracy for each k in the grid
accuracies = grid_search.cv_results_['mean_test_score']
results_dict = {
    'k': k_values.tolist(),
    'Accuracy': accuracies.tolist()
}

knnFit1 = CaretTrainModel(
    estimator=grid_search,
    training_data=TrainData,
    training_classes=TrainClasses,
    pre_process=['center', 'scale'],
    control={'method': 'cv'},
    results=results_dict
)

# R: update(knnFit1, list(.k = 3))
update_result = knnFit1.update_model({'.k': 3})
print(update_result)