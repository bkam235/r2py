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
    def __init__(self, estimator, training_data, training_classes, pre_process, control, results):
        self.finalModel = estimator
        self.trainingData = training_data
        self.trainingClasses = training_classes
        self.preProcess = pre_process
        self.control = control
        self.results = results
        self.bestTune = results.iloc[results['Accuracy'].idxmax()]['k'] if 'Accuracy' in results.columns else None

    def update_params(self, params):
        # Extract the specific parameter (e.g., .k -> n_neighbors)
        k_val = params.get('.k')
        
        # Re-fit the model with the new parameter
        pipeline = Pipeline([
            ('scaler', StandardScaler()),
            ('knn', KNeighborsClassifier(n_neighbors=int(k_val)))
        ])
        pipeline.fit(self.trainingData, self.trainingClasses)
        
        self.finalModel = pipeline
        # In R, update() returns the updated train object
        return self

# R: data(iris)
# r2py:entity:data
iris_df = pd.DataFrame(iris)

# R: TrainData <- iris[,1:4]
# r2py:entity:TrainData
TrainData = iris_df.iloc[:, 0:4]

# R: TrainClasses <- iris[,5]
# r2py:entity:TrainClasses
TrainClasses = iris_df.iloc[:, 4]

# R: knnFit1 <- train(...)
# We need to simulate the 'tuneLength = 10' and 'method = "cv"'
# caret's knn tuneLength = 10 typically selects 10 values of k
k_values = np.linspace(1, 23, 10, dtype=int) # Approximation of caret's tuneLength for knn
results_list = []

pipeline_init = Pipeline([
    ('scaler', StandardScaler()),
    ('knn', KNeighborsClassifier())
])

cv = KFold(n_splits=10, shuffle=False)

for k in k_values:
    pipeline_init.set_params(knn__n_neighbors=int(k))
    scores = cross_val_score(pipeline_init, TrainData, TrainClasses, cv=cv, scoring='accuracy')
    results_list.append({'k': k, 'Accuracy': np.mean(scores), 'AccuracySD': np.std(scores)})

results_df = pd.DataFrame(results_list)

# Re-fit the best model for finalModel
best_k = results_df.loc[results_df['Accuracy'].idxmax(), 'k']
pipeline_init.set_params(knn__n_neighbors=int(best_k))
pipeline_init.fit(TrainData, TrainClasses)

# r2py:entity:knnFit1
knnFit1 = CaretTrainModel(
    estimator=pipeline_init,
    training_data=TrainData,
    training_classes=TrainClasses,
    pre_process=['center', 'scale'],
    control={'method': 'cv'},
    results=results_df
)

# R: update(knnFit1, list(.k = 3))
# r2py:entity:update
update_result = knnFit1.update_params({'.k': 3})
print(update_result)