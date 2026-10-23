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
# Since iris is provided by data_shim, we just use it.
# r2py:entity:data
iris_df = iris

# R: TrainData <- iris[,1:4]
# r2py:entity:TrainData
TrainData = iris_df.iloc[:, 0:4]

# R: TrainClasses <- iris[,5]
# r2py:entity:TrainClasses
TrainClasses = iris_df.iloc[:, 4]

# R: knnFit1 <- train(...)
# In caret, train() performs cross-validation to find the best tune parameters.
# preProcess = c("center", "scale") is equivalent to StandardScaler().
pipeline_init = Pipeline([
    ('scaler', StandardScaler()),
    ('knn', KNeighborsClassifier())
])

# tuneLength = 10 for knn usually means testing k from 1 to 10.
param_grid = {'knn__n_neighbors': np.arange(1, 11)}
# trainControl(method = "cv") defaults to 10-fold CV in caret.
cv_strategy = KFold(n_splits=10, shuffle=False)

grid_search = GridSearchCV(
    estimator=pipeline_init,
    param_grid=param_grid,
    cv=cv_strategy,
    scoring='accuracy'
)
grid_search.fit(TrainData, TrainClasses)

# To mimic the caret object, we store the grid search result and the data used.
# r2py:entity:knnFit1
knnFit1 = {
    'model': grid_search,
    'train_data': TrainData,
    'train_classes': TrainClasses,
    'preProcess': ['center', 'scale'],
    'trControl': {'method': 'cv'}
}

# R: update(knnFit1, list(.k = 3))
# r2py:entity:update
def update(model_obj, params):
    # In R, update() re-fits the model with new hyperparameters.
    # .k maps to n_neighbors in sklearn.
    k_val = params.get('.k')
    
    # Re-create the pipeline with the specific k value.
    new_pipeline = Pipeline([
        ('scaler', StandardScaler()),
        ('knn', KNeighborsClassifier(n_neighbors=k_val))
    ])
    
    # Fit the model on the original training data.
    new_pipeline.fit(model_obj['train_data'], model_obj['train_classes'])
    
    # Return a new model object similar to the original structure.
    return {
        'model': new_pipeline,
        'train_data': model_obj['train_data'],
        'train_classes': model_obj['train_classes'],
        'preProcess': model_obj['preProcess'],
        'trControl': model_obj['trControl'],
        'bestTune': {'k': k_val}
    }

update = update(knnFit1, {'.k': 3})