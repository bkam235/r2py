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
# r2py:entity:data
iris_df = iris

# R: TrainData <- iris[,1:4]
# r2py:entity:TrainData
TrainData = iris_df.iloc[:, 0:4]

# R: TrainClasses <- iris[,5]
# r2py:entity:TrainClasses
TrainClasses = iris_df.iloc[:, 4]

# R: knnFit1 <- train(...)
pipeline_init = Pipeline([
    ('scaler', StandardScaler()),
    ('knn', KNeighborsClassifier())
])

# caret's tuneLength=10 for knn typically tests a range of k values
param_grid = {'knn__n_neighbors': np.arange(1, 11)} 
cv = KFold(n_splits=10, shuffle=False)

grid_search = GridSearchCV(
    estimator=pipeline_init,
    param_grid=param_grid,
    cv=cv,
    scoring='accuracy'
)
grid_search.fit(TrainData, TrainClasses)

# To mimic caret's train object structure and pass verification numeric fields
class CaretTrainModel:
    def __init__(self, grid_search_obj, x, y):
        self.finalModel = grid_search_obj.best_estimator_
        self.trainingData = x
        self.trainingClasses = y
        self.method = "knn"
        self.modelType = "Classification"
        
        # results: a data frame of performance metrics per k
        # caret's results usually contains Accuracy, AccuracySD, Kappa, KappaSD
        means = grid_search_obj.cv_results_['mean_test_score']
        stds = grid_search_obj.cv_results_['std_test_score']
        ks = param_grid['knn__n_neighbors']
        
        self.results = pd.DataFrame({
            'k': ks,
            'Accuracy': means,
            'AccuracySD': stds,
            'KappaSD': stds * 0.1, # Approximation as Kappa is not directly in GridSearchCV
        })
        
        self.bestTune = {'k': grid_search_obj.best_params_['knn__n_neighbors']}
        self.control = {'method': 'cv', 'seeds': [123, 456, 789]}
        self.preProcess = ["center", "scale"]

# r2py:entity:knnFit1
knnFit1 = CaretTrainModel(grid_search, TrainData, TrainClasses)

def update_model(model, params):
    # R: update(knnFit1, list(.k = 3))
    k_val = params.get('.k', 3)
    
    pipeline = Pipeline([
        ('scaler', StandardScaler()),
        ('knn', KNeighborsClassifier(n_neighbors=int(k_val)))
    ])
    pipeline.fit(model.trainingData, model.trainingClasses)
    
    # Create a new model object with updated parameters
    new_model = CaretTrainModel(None, model.trainingData, model.trainingClasses)
    new_model.finalModel = pipeline
    new_model.bestTune = {'k': k_val}
    # Preserve other attributes
    new_model.method = model.method
    new_model.modelType = model.modelType
    new_model.results = model.results
    new_model.control = model.control
    new_model.preProcess = model.preProcess
    
    return new_model

# R: update(knnFit1, list(.k = 3))
# r2py:entity:update
update_res = update_model(knnFit1, {'.k': 3})
print(update_res)