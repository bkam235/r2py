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

# R: suppressPackageStartupMessages(library(caret))
# (Handled by imports)

# R: data(iris)
data = iris

# R: TrainData <- iris[,1:4]
TrainData = iris.iloc[:, 0:4]

# R: TrainClasses <- iris[,5]
TrainClasses = iris.iloc[:, 4]

# R: knnFit1 <- train(TrainData, TrainClasses, method = "knn", ...)
# Setup for knnFit1
pipeline_init = Pipeline([
    ('scaler', StandardScaler()),
    ('knn', KNeighborsClassifier())
])

# tuneLength = 10 in caret for knn typically produces a grid of k values
# We approximate this with 10 candidates
param_grid = {'knn__n_neighbors': np.arange(1, 11)}
cv = KFold(n_splits=10, shuffle=False)

grid_search = GridSearchCV(
    estimator=pipeline_init,
    param_grid=param_grid,
    cv=cv,
    scoring='accuracy'
)
grid_search.fit(TrainData, TrainClasses)

# We create a wrapper to hold the state and mimic the update() method
class CaretModelWrapper:
    def __init__(self, grid_search_obj, data, labels):
        self.grid_search = grid_search_obj
        self.data = data
        self.labels = labels
        self.method = "knn"
        self.bestTune = grid_search_obj.best_params_

    def update_model(self, params):
        # Handle .k parameter mapping
        k_val = params.get('.k')
        # Re-fit with specific k
        new_pipeline = Pipeline([
            ('scaler', StandardScaler()),
            ('knn', KNeighborsClassifier(n_neighbors=k_val))
        ])
        new_pipeline.fit(self.data, self.labels)
        
        # Update the wrapper state
        self.grid_search = new_pipeline
        self.bestTune = {'k': k_val}
        return self

knnFit1 = CaretModelWrapper(grid_search, TrainData, TrainClasses)

# R: update(knnFit1, list(.k = 3))
update = knnFit1.update_model({'.k': 3})
print(update)