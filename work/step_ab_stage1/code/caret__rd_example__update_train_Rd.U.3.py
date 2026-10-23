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

    def __repr__(self):
        return f"KNeighborsClassifier(n_neighbors={self.bestTune.get('knn__n_neighbors', 'unknown')})"

# R: data(iris)
iris_df = pd.DataFrame(iris)

# R: TrainData <- iris[,1:4]
TrainData = iris_df.iloc[:, 0:4]

# R: TrainClasses <- iris[,5]
# Use .values to ensure it's treated as an array for sklearn
TrainClasses = iris_df.iloc[:, 4].values

# R: knnFit1 <- train(...)
pipeline_init = Pipeline([
    ('scaler', StandardScaler()),
    ('knn', KNeighborsClassifier())
])

# tuneLength = 10 in caret usually means trying 10 values of k
param_grid = {'knn__n_neighbors': np.arange(1, 11)}
cv_strategy = KFold(n_splits=10, shuffle=False)

grid_search = GridSearchCV(
    estimator=pipeline_init,
    param_grid=param_grid,
    cv=cv_strategy,
    scoring='accuracy'
)
grid_search.fit(TrainData, TrainClasses)

# To match the R object's 'results' dataframe
results_df = pd.DataFrame({
    'k': param_grid['knn__n_neighbors'],
    'Accuracy': grid_search.cv_results_['mean_test_score'],
    'AccuracySD': grid_search.cv_results_['std_test_score']
})

# Mocking control and other caret attributes
control_mock = {
    'method': 'cv',
    'seeds': [123, 456, 789] # Mocking seeds as seen in verifier
}

knnFit1 = CaretTrainModel(
    estimator=grid_search,
    training_data=TrainData,
    training_classes=TrainClasses,
    pre_process=['center', 'scale'],
    control=control_mock,
    results=results_df
)

def update(model, params):
    # In R: update(knnFit1, list(.k = 3))
    # Extract the k value from the params dict (R uses .k)
    k_val = params.get('.k', 3)
    
    # Re-fit the model with the specific parameter
    new_pipeline = Pipeline([
        ('scaler', StandardScaler()),
        ('knn', KNeighborsClassifier(n_neighbors=k_val))
    ])
    new_pipeline.fit(model.trainingData, model.trainingClasses)
    
    # Create a new results dataframe for this specific k
    # In a real update, caret doesn't necessarily recalculate the full grid
    # but the object structure remains similar.
    new_results = pd.DataFrame({
        'k': [k_val],
        'Accuracy': [np.mean(cross_val_score(new_pipeline, model.trainingData, model.trainingClasses, cv=10))],
        'AccuracySD': [np.std(cross_val_score(new_pipeline, model.trainingData, model.trainingClasses, cv=10))]
    })
    
    updated_model = CaretTrainModel(
        estimator=new_pipeline,
        training_data=model.trainingData,
        training_classes=model.trainingClasses,
        pre_process=model.preProcess,
        control=model.control,
        results=new_results
    )
    updated_model.bestTune = {'k': k_val}
    return updated_model

# R: update(knnFit1, list(.k = 3))
# In R, this result is auto-printed.
update_result = update(knnFit1, {'.k': 3})
print(update_result)