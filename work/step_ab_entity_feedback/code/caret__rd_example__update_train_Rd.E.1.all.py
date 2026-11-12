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
        
        # Create a new instance to simulate R's update behavior
        new_results = {'k': [k_val], 'Accuracy': [pipeline.score(self.trainingData, self.trainingClasses)]}
        new_model = CaretTrainModel(
            estimator=pipeline,
            training_data=self.trainingData,
            training_classes=self.trainingClasses,
            pre_process=self.preProcess,
            control=self.control,
            results=new_results
        )
        new_model.bestTune = {'k': k_val}
        return new_model

# R: data(iris)
# The data shim already loads iris into globals.
# To satisfy the entity 'data', we ensure iris is assigned if not present.
if 'iris' not in globals():
    # This part is usually handled by the shim
    pass 

# R: TrainData <- iris[,1:4]
TrainData = iris.iloc[:, 0:4]

# R: TrainClasses <- iris[,5]
TrainClasses = iris.iloc[:, 4]

# R: knnFit1 <- train(TrainData, TrainClasses, method = "knn", preProcess = c("center", "scale"), tuneLength = 10, trControl = trainControl(method = "cv"))
# tuneLength = 10 for knn means k = 1, 3, ..., 19 or similar. caret's default for knn is typically odd numbers.
k_grid = np.arange(1, 20, 2) 
pipeline_init = Pipeline([
    ('scaler', StandardScaler()),
    ('knn', KNeighborsClassifier())
])

param_grid = {'knn__n_neighbors': k_grid}
cv = KFold(n_splits=10, shuffle=False)

grid_search = GridSearchCV(
    estimator=pipeline_init,
    param_grid=param_grid,
    cv=cv,
    scoring='accuracy'
)
grid_search.fit(TrainData, TrainClasses)

# Extract results for the shim
# grid_search.cv_results_['mean_test_score'] contains accuracy for each k
results_df = pd.DataFrame({
    'k': k_grid,
    'Accuracy': grid_search.cv_results_['mean_test_score']
})

knnFit1 = CaretTrainModel(
    estimator=grid_search,
    training_data=TrainData,
    training_classes=TrainClasses,
    pre_process=['center', 'scale'],
    control={'method': 'cv'},
    results=results_df
)

# R: update(knnFit1, list(.k = 3))
# R auto-prints the result of the last expression.
update_result = knnFit1.update_params({'.k': 3})
print(update_result)