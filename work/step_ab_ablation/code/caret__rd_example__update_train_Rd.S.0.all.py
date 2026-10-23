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

# R: data(iris)
# The data shim already loads iris as a DataFrame.
# Just assigning for entity tracking.
data = iris

# R: TrainData <- iris[,1:4]
TrainData = iris.iloc[:, 0:4]

# R: TrainClasses <- iris[,5]
TrainClasses = iris.iloc[:, 4]

# R: knnFit1 <- train(TrainData, TrainClasses, method = "knn", preProcess = c("center", "scale"), tuneLength = 10, trControl = trainControl(method = "cv"))
# In caret, "knn" with preProcess "center", "scale" is equivalent to a Pipeline of StandardScaler and KNeighborsClassifier.
# tuneLength = 10 means it tests 10 values of k.
pipeline_init = Pipeline([
    ('scaler', StandardScaler()),
    ('knn', KNeighborsClassifier())
])

param_grid = {'knn__n_neighbors': list(range(1, 11))}
# caret's trainControl(method="cv") defaults to 10-fold CV.
cv = KFold(n_splits=10, shuffle=False)

grid_search = GridSearchCV(
    estimator=pipeline_init,
    param_grid=param_grid,
    cv=cv
)
grid_search.fit(TrainData, TrainClasses)
knnFit1 = grid_search

# R: update(knnFit1, list(.k = 3))
def update(model, params):
    # The update function in caret re-trains the model with updated parameters.
    # Extract .k and map to sklearn's n_neighbors
    k_val = params.get('.k', 3)
    
    # Re-create the pipeline with the specific k value
    new_pipeline = Pipeline([
        ('scaler', StandardScaler()),
        ('knn', KNeighborsClassifier(n_neighbors=k_val))
    ])
    new_pipeline.fit(TrainData, TrainClasses)
    return new_pipeline

update = update(knnFit1, {'.k': 3})