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

# Helper class to mimic caret's train object structure
class CaretTrainModel:
    def __init__(self, estimator, training_data, training_classes, pre_process, control):
        self.finalModel = estimator
        self.trainingData = training_data
        self.trainingClasses = training_classes
        self.preProcess = pre_process
        self.control = control
        
        # Capture GridSearchCV results into a format similar to caret's 'results'
        if hasattr(estimator, 'cv_results_'):
            self.results = pd.DataFrame(estimator.cv_results_).drop(columns=['mean_test_score', 'std_test_score'], errors='ignore')
            # Caret's results typically has the tune parameter as the index
            self.results.index = estimator.cv_results_['param_knn__n_neighbors']
            self.results = self.results.rename(columns={'mean_test_score': 'Accuracy'})
        else:
            self.results = pd.DataFrame()
            
        self.bestTune = estimator.best_params_ if hasattr(estimator, 'best_params_') else None

    def update_params(self, params):
        # In R: update(knnFit1, list(.k = 3))
        k_val = params.get('.k')
        
        pipeline = Pipeline([
            ('scaler', StandardScaler()),
            ('knn', KNeighborsClassifier(n_neighbors=k_val))
        ])
        pipeline.fit(self.trainingData, self.trainingClasses)
        
        self.finalModel = pipeline
        self.bestTune = {'k': k_val}
        return self

# In R: data(iris)
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

# caret tuneLength=10 for knn usually generates a sequence of k
param_grid = {'knn__n_neighbors': np.arange(1, 21, 2)} # Mimicking caret's typical knn grid
cv = KFold(n_splits=10, shuffle=False)

grid_search = GridSearchCV(
    estimator=pipeline_init,
    param_grid=param_grid,
    cv=cv,
    scoring='accuracy'
)
grid_search.fit(TrainData, TrainClasses)

# Wrap in our shim class to maintain caret-like properties
# r2py:entity:knnFit1
knnFit1 = CaretTrainModel(
    estimator=grid_search,
    training_data=TrainData,
    training_classes=TrainClasses,
    pre_process=['center', 'scale'],
    control={'method': 'cv'}
)

# R: update(knnFit1, list(.k = 3))
# r2py:entity:update
update = knnFit1.update_params({'.k': 3})
print(update)