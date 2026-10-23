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

# Helper class to mimic caret's train object structure
# r2py:entity:knnFit1
class CaretTrainModel:
    def __init__(self, estimator, training_data, training_classes, pre_process, control, results, seeds):
        self.finalModel = estimator
        self.trainingData = training_data
        self.trainingClasses = training_classes
        self.preProcess = pre_process
        self.control = control
        self.results = results
        self.seeds = seeds
        self.bestTune = estimator.best_params_ if hasattr(estimator, 'best_params_') else None

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
        # In a real update, results would be re-calculated, but for this shim we maintain the object
        return self

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

# caret tuneLength=10 for knn usually tries k = 1, 3, 5, ... 19 or similar.
# We'll use 1 to 19 to be safe or just range(1, 11) as before.
param_grid = {'knn__n_neighbors': np.arange(1, 21, 2)} 
cv = KFold(n_splits=10, shuffle=False)

grid_search = GridSearchCV(
    estimator=pipeline_init,
    param_grid=param_grid,
    cv=cv,
    scoring='accuracy'
)
grid_search.fit(TrainData, TrainClasses)

# Mimic the 'results' dataframe in caret
results_df = pd.DataFrame({
    'k': param_grid['knn__n_neighbors'],
    'Accuracy': grid_search.cv_results_['mean_test_score'],
    'AccuracySD': grid_search.cv_results_['std_test_score'],
    'KappaSD': np.zeros(len(param_grid['knn__n_neighbors'])) # Approximation
})

# Caret typically stores seeds in the control object
seeds = [123, 456, 789] # Placeholder as these are internal R seeds

knnFit1 = CaretTrainModel(
    estimator=grid_search,
    training_data=TrainData,
    training_classes=TrainClasses,
    pre_process=['center', 'scale'],
    control={'method': 'cv', 'seeds': seeds},
    results=results_df,
    seeds=seeds
)

# R: update(knnFit1, list(.k = 3))
# r2py:entity:update
update = knnFit1.update_params({'.k': 3})
print(update)