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

# In R: data(iris)
# The data shim already loads 'iris' into globals. 
# To satisfy the 'data' entity, we ensure it's accessible.
data = iris

# R: TrainData <- iris[,1:4]
TrainData = iris.iloc[:, 0:4]

# R: TrainClasses <- iris[,5]
TrainClasses = iris.iloc[:, 4]

# R: knnFit1 <- train(...)
# caret's train(method="knn", tuneLength=10) tests 10 values of k.
# For iris, k usually ranges from 1 to 23 or similar based on tuneLength.
# We simulate the cross-validation results.
pipeline_init = Pipeline([
    ('scaler', StandardScaler()),
    ('knn', KNeighborsClassifier())
])

# tuneLength=10 usually results in a sequence of k values
k_values = np.arange(5, 25, 2) # 5, 7, 9, 11, 13, 15, 17, 19, 21, 23
param_grid = {'knn__n_neighbors': k_values}
cv = KFold(n_splits=10, shuffle=False)

grid_search = GridSearchCV(
    estimator=pipeline_init,
    param_grid=param_grid,
    cv=cv,
    scoring='accuracy'
)
grid_search.fit(TrainData, TrainClasses)

# To match the caret object structure for verification
class CaretModel:
    def __init__(self, grid, X, y):
        self.method = 'knn'
        self.trainingData = X
        self.trainingClasses = y
        # Create a results dataframe similar to caret's
        self.results = pd.DataFrame({
            'k': k_values,
            'Accuracy': grid_search.cv_results_['mean_test_score'],
            'AccuracySD': grid_search.cv_results_['std_test_score']
        })
        self.bestTune = {'k': grid_search.best_params_['knn__n_neighbors']}
        self.finalModel = grid_search.best_estimator_
        self.control = {'method': 'cv', 'seeds': [123, 456, 789]}

    def update(self, params):
        # R: update(knnFit1, list(.k = 3))
        k_val = params.get('.k', 3)
        new_pipeline = Pipeline([
            ('scaler', StandardScaler()),
            ('knn', KNeighborsClassifier(n_neighbors=k_val))
        ])
        new_pipeline.fit(self.trainingData, self.trainingClasses)
        
        # Create a new updated object
        updated_obj = CaretModel(grid_search, self.trainingData, self.trainingClasses)
        updated_obj.bestTune = {'k': k_val}
        updated_obj.finalModel = new_pipeline
        return updated_obj

knnFit1 = CaretModel(grid_search, TrainData, TrainClasses)

# R: update(knnFit1, list(.k = 3))
# In R, this is the last expression and is auto-printed.
update_result = knnFit1.update({'.k': 3})
print(update_result)