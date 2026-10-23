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
# r2py:entity:knnFit1
class CaretTrainModel:
    def __init__(self, estimator, training_data, training_classes, pre_process, control, results=None):
        self.finalModel = estimator
        self.trainingData = training_data
        self.trainingClasses = training_classes
        self.preProcess = pre_process
        self.control = control
        self.results = results if results is not None else pd.DataFrame()
        self.bestTune = estimator.best_params_ if hasattr(estimator, 'best_params_') else None

    def update_params(self, params):
        # In R: update(knnFit1, list(.k = 3))
        k_val = params.get('.k')
        
        # Re-fit the model with the new parameter
        pipeline = Pipeline([
            ('scaler', StandardScaler()),
            ('knn', KNeighborsClassifier(n_neighbors=int(k_val)))
        ])
        pipeline.fit(self.trainingData, self.trainingClasses)
        
        # Create a simplified results df for the updated single k
        # In a real update, caret would re-run the train logic or just fix the param
        new_results = pd.DataFrame({'k': [k_val], 'Accuracy': [pipeline.score(self.trainingData, self.trainingClasses)]})
        
        # Create a new instance of CaretTrainModel to return
        return CaretTrainModel(
            estimator=pipeline,
            training_data=self.trainingData,
            training_classes=self.trainingClasses,
            pre_process=self.preProcess,
            control=self.control,
            results=new_results
        )

# In R: data(iris)
# r2py:entity:data
iris_df = pd.DataFrame(iris)

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

# caret's tuneLength = 10 for knn usually tries a sequence of k values
# based on the verification output, R tried [5, 7, 9, 11, 13, 15, 17, 19, 21, 23]
param_grid = {'knn__n_neighbors': [5, 7, 9, 11, 13, 15, 17, 19, 21, 23]}
cv = KFold(n_splits=10, shuffle=False)

grid_search = GridSearchCV(
    estimator=pipeline_init,
    param_grid=param_grid,
    cv=cv,
    scoring='accuracy'
)
grid_search.fit(TrainData, TrainClasses)

# Extract results to mimic caret's results table
cv_results = pd.DataFrame(grid_search.cv_results_)
results_df = pd.DataFrame({
    'k': cv_results['param_knn__n_neighbors'],
    'Accuracy': cv_results['mean_test_score'],
    'AccuracySD': cv_results['std_test_score']
})

# Wrap in our shim class
knnFit1 = CaretTrainModel(
    estimator=grid_search,
    training_data=TrainData,
    training_classes=TrainClasses,
    pre_process=['center', 'scale'],
    control={'method': 'cv'},
    results=results_df
)

# R: update(knnFit1, list(.k = 3))
# r2py:entity:update
update_res = knnFit1.update_params({'.k': 3})
print(update_res)