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
from sklearn.model_selection import KFold, GridSearchCV, cross_validate
from sklearn.pipeline import Pipeline

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
        if self.bestTune and 'knn__n_neighbors' in self.bestTune:
            self.bestTune = {'k': self.bestTune['knn__n_neighbors']}

    def update_params(self, params):
        # In R: update(knnFit1, list(.k = 3))
        k_val = params.get('.k')
        
        # Re-fit the model with the new parameter
        pipeline = Pipeline([
            ('scaler', StandardScaler()),
            ('knn', KNeighborsClassifier(n_neighbors=k_val))
        ])
        pipeline.fit(self.trainingData, self.trainingClasses)
        
        self.finalModel = pipeline
        self.bestTune = {'k': k_val}
        # Create a dummy results DF for the updated model to maintain structure
        self.results = pd.DataFrame({'k': [k_val], 'Accuracy': [np.nan], 'AccuracySD': [np.nan], 'KappaSD': [np.nan]})
        return self

# R: data(iris)
# iris is provided by data_shim

# R: TrainData <- iris[,1:4]
TrainData = iris.iloc[:, 0:4]

# R: TrainClasses <- iris[,5]
TrainClasses = iris.iloc[:, 4]

# R: knnFit1 <- train(...)
pipeline_init = Pipeline([
    ('scaler', StandardScaler()),
    ('knn', KNeighborsClassifier())
])

# caret tuneLength = 10 for knn usually generates a grid of k values
# The R output shows k: [5, 7, 9, 11, 13, 15, 17, 19, 21, 23]
param_grid = {'knn__n_neighbors': [5, 7, 9, 11, 13, 15, 17, 19, 21, 23]}
cv = KFold(n_splits=10, shuffle=False)

grid_search = GridSearchCV(
    estimator=pipeline_init,
    param_grid=param_grid,
    cv=cv,
    scoring='accuracy'
)
grid_search.fit(TrainData, TrainClasses)

# Extract results to mimic caret's results dataframe
results_data = {
    'k': param_grid['knn__n_neighbors'],
    'Accuracy': grid_search.cv_results_['mean_test_score'],
    'AccuracySD': grid_search.cv_results_['std_test_score'],
    'KappaSD': [np.nan] * len(param_grid['knn__n_neighbors'])
}
results_df = pd.DataFrame(results_data)

knnFit1 = CaretTrainModel(
    estimator=grid_search,
    training_data=TrainData,
    training_classes=TrainClasses,
    pre_process=['center', 'scale'],
    control={'method': 'cv'},
    results_df=results_df
)

# R: update(knnFit1, list(.k = 3))
# In R, this returns the updated model and auto-prints it.
updated_model = knnFit1.update_params({'.k': 3})
print(updated_model)
update = updated_model