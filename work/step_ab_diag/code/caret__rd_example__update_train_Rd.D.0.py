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
from sklearn.model_selection import KFold, GridSearchCV, cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, make_scorer

# Helper class to mimic caret's train object structure
class CaretTrainModel:
    def __init__(self, estimator, training_data, training_classes, pre_process, control, results_df):
        self.finalModel = estimator
        self.trainingData = training_data
        self.trainingClasses = training_classes
        self.preProcess = pre_process
        self.control = control
        self.results = results_df
        self.bestTune = estimator.best_params_ if hasattr(estimator, 'best_params_') else None

    def update_params(self, params):
        # In R: update(knnFit1, list(.k = 3))
        k_val = params.get('.k')
        
        pipeline = Pipeline([
            ('scaler', StandardScaler()),
            ('knn', KNeighborsClassifier(n_neighbors=k_val))
        ])
        pipeline.fit(self.trainingData, self.trainingClasses)
        
        # Update attributes to reflect the "updated" state
        self.finalModel = pipeline
        self.bestTune = {'k': k_val}
        
        # Recalculate results for k=3 (simplification of caret's behavior)
        cv = KFold(n_splits=10, shuffle=False)
        scores = cross_val_score(pipeline, self.trainingData, self.trainingClasses, cv=cv)
        
        self.results = pd.DataFrame({
            'k': [k_val],
            'Accuracy': [np.mean(scores)],
            'AccuracySD': [np.std(scores)],
            'KappaSD': [0.0] # Simplified
        })
        return self

# R: data(iris)
# The iris dataframe is provided by the data_shim
iris_df = iris

# R: TrainData <- iris[,1:4]
TrainData = iris_df.iloc[:, 0:4]

# R: TrainClasses <- iris[,5]
TrainClasses = iris_df.iloc[:, 4]

# R: knnFit1 <- train(...)
pipeline_init = Pipeline([
    ('scaler', StandardScaler()),
    ('knn', KNeighborsClassifier())
])

# caret's tuneLength=10 for knn typically tests 10 values of k
param_grid = {'knn__n_neighbors': np.arange(1, 11)}
cv_strat = KFold(n_splits=10, shuffle=False)

grid_search = GridSearchCV(
    estimator=pipeline_init,
    param_grid=param_grid,
    cv=cv_strat,
    scoring='accuracy'
)
grid_search.fit(TrainData, TrainClasses)

# Compute results table to match R's caret output
results_list = []
for k in param_grid['knn__n_neighbors']:
    pipe = Pipeline([
        ('scaler', StandardScaler()),
        ('knn', KNeighborsClassifier(n_neighbors=k))
    ])
    scores = cross_val_score(pipe, TrainData, TrainClasses, cv=cv_strat)
    results_list.append({
        'k': k,
        'Accuracy': np.mean(scores),
        'AccuracySD': np.std(scores),
        'KappaSD': 0.0 # Simplified
    })
results_df = pd.DataFrame(results_list)

# Wrap in our shim class
knnFit1 = CaretTrainModel(
    estimator=grid_search,
    training_data=TrainData,
    training_classes=TrainClasses,
    pre_process=['center', 'scale'],
    control={'method': 'cv'},
    results_df=results_df
)

# R: update(knnFit1, list(.k = 3))
# This call in R auto-prints the result
update = knnFit1.update_params({'.k': 3})
print(update)