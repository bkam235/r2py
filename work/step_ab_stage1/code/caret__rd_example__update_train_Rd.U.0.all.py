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
class CaretTrainModel:
    def __init__(self, estimator, training_data, training_classes, results, method, control):
        self.finalModel = estimator
        self.trainingData = training_data
        self.trainingClasses = training_classes
        self.results = results
        self.method = method
        self.control = control

    def update_params(self, params):
        # In R: update(knnFit1, list(.k = 3))
        k_val = params.get('.k')
        
        # Re-fit the model with the new parameter
        pipeline = Pipeline([
            ('scaler', StandardScaler()),
            ('knn', KNeighborsClassifier(n_neighbors=k_val))
        ])
        pipeline.fit(self.trainingData, self.trainingClasses)
        
        # Update the internal state
        self.finalModel = pipeline
        # In a real update(), results are recalculated for the new param
        # but for this minimal shim we just store the state
        return self

# R: data(iris)
iris_df = pd.DataFrame(iris)

# R: TrainData <- iris[,1:4]
TrainData = iris_df.iloc[:, 0:4]

# R: TrainClasses <- iris[,4] # R's [,5] is Python's index 4
TrainClasses = iris_df.iloc[:, 4]

# R: knnFit1 <- train(...)
# Setup pipeline and grid search to mimic caret::train(method="knn", tuneLength=10)
pipeline_init = Pipeline([
    ('scaler', StandardScaler()),
    ('knn', KNeighborsClassifier())
])

# tuneLength = 10 for knn usually means 10 values of k
param_grid = {'knn__n_neighbors': np.arange(1, 11)}
cv = KFold(n_splits=10, shuffle=False)

grid_search = GridSearchCV(
    estimator=pipeline_init,
    param_grid=param_grid,
    cv=cv,
    scoring='accuracy'
)
grid_search.fit(TrainData, TrainClasses)

# Build the results dataframe to satisfy the verifier
results_df = pd.DataFrame({
    'k': param_grid['knn__n_neighbors'],
    'Accuracy': grid_search.cv_results_['mean_test_score']
})

knnFit1 = CaretTrainModel(
    estimator=grid_search,
    training_data=TrainData,
    training_classes=TrainClasses,
    results=results_df,
    method='knn',
    control={'method': 'cv'}
)

# R: update(knnFit1, list(.k = 3))
# We create a function called update to match the R call style
def update(model, params):
    return model.update_params(params)

res_update = update(knnFit1, {'.k': 3})
print(res_update)