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

# R: knnFit1 <- train(TrainData, TrainClasses, method = "knn", 
#                    preProcess = c("center", "scale"), tuneLength = 10, 
#                    trControl = trainControl(method = "cv"))
pipeline = Pipeline([
    ('preProcess', StandardScaler()),
    ('knn', KNeighborsClassifier())
])

# tuneLength = 10 in caret for knn typically means trying 10 values of k
param_grid = {'knn__n_neighbors': list(range(1, 11))}
cv = KFold(n_splits=10, shuffle=False)

grid_search = GridSearchCV(
    estimator=pipeline,
    param_grid=param_grid,
    cv=cv
)
grid_search.fit(TrainData, TrainClasses)

# We store the model and parameters to mimic caret's train object
class CaretTrainShim:
    def __init__(self, model, data, classes):
        self.model = model
        self.data = data
        self.classes = classes

    def update(self, params):
        # R: update(knnFit1, list(.k = 3))
        # Create a new pipeline with the updated k value
        k_val = params.get('.k', self.model.best_params_['knn__n_neighbors'])
        
        new_pipeline = Pipeline([
            ('preProcess', StandardScaler()),
            ('knn', KNeighborsClassifier(n_neighbors=k_val))
        ])
        new_pipeline.fit(self.data, self.classes)
        
        # Update the state
        self.model = new_pipeline
        return self

knnFit1 = CaretTrainShim(grid_search, TrainData, TrainClasses)

# R: update(knnFit1, list(.k = 3))
update = knnFit1.update({'.k': 3})