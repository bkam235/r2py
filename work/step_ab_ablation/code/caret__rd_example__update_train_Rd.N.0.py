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

# R: TrainData <- iris[,1:4]
TrainData = iris.iloc[:, 0:4]

# R: TrainClasses <- iris[,5]
TrainClasses = iris.iloc[:, 4]

# Helper function to mimic caret::train
def train_knn(data, classes, method="knn", preProcess=None, tuneLength=10, trControl=None):
    # Pipeline for centering and scaling if requested
    steps = []
    if preProcess and "center" in preProcess and "scale" in preProcess:
        steps.append(('scaler', StandardScaler()))
    
    steps.append(('knn', KNeighborsClassifier()))
    pipeline = Pipeline(steps)
    
    # tuneLength in caret for knn usually defines the grid of k values
    param_grid = {'knn__n_neighbors': np.arange(1, tuneLength + 1)}
    
    # trControl(method = "cv") usually defaults to 10-fold CV in caret
    cv = KFold(n_splits=10, shuffle=False)
    
    grid = GridSearchCV(pipeline, param_grid, cv=cv, scoring='accuracy')
    grid.fit(data, classes)
    
    # Return a structure that holds the fit and the original parameters
    return {
        'model': grid,
        'data': data,
        'classes': classes,
        'preProcess': preProcess,
        'tuneLength': tuneLength,
        'trControl': trControl
    }

# R: knnFit1 <- train(...)
knnFit1 = train_knn(
    TrainData, 
    TrainClasses, 
    method="knn", 
    preProcess=["center", "scale"], 
    tuneLength=10, 
    trControl={"method": "cv"}
)

# Helper function to mimic caret::update
def update_model(model_obj, tune_list):
    # Extract new k from tune_list (R uses .k for knn)
    new_k = tune_list.get('.k')
    
    # Re-create pipeline with the specific k
    steps = []
    if model_obj['preProcess'] and "center" in model_obj['preProcess'] and "scale" in model_obj['preProcess']:
        steps.append(('scaler', StandardScaler()))
    
    steps.append(('knn', KNeighborsClassifier(n_neighbors=new_k)))
    pipeline = Pipeline(steps)
    
    # Fit the model with the fixed parameter
    pipeline.fit(model_obj['data'], model_obj['classes'])
    
    # Return an updated object
    updated_obj = model_obj.copy()
    updated_obj['model'] = pipeline
    return updated_obj

# R: update(knnFit1, list(.k = 3))
update = update_model(knnFit1, {'.k': 3})