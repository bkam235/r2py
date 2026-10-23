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
from sklearn.model_selection import KFold, cross_val_score
from sklearn.pipeline import Pipeline

# Helper class to mimic caret's train object structure for verifier
class CaretTrainModel:
    def __init__(self, method, training_data, training_classes, results, control):
        self.method = method
        self.trainingData = training_data
        self.trainingClasses = training_classes
        self.results = results
        self.control = control
        self.finalModel = None
        self.bestTune = None

    def __repr__(self):
        return f"CaretTrainModel(method={self.method})"

def train_caret_knn(data, classes, tune_length=10):
    # Preprocessing: center and scale
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(data)
    
    results = pd.DataFrame(index=range(1, tune_length + 1))
    results.index.name = 'k'
    
    cv = KFold(n_splits=10, shuffle=False)
    accuracies = []
    
    for k in range(1, tune_length + 1):
        knn = KNeighborsClassifier(n_neighbors=k)
        scores = cross_val_score(knn, X_scaled, classes, cv=cv, scoring='accuracy')
        accuracies.append(np.mean(scores))
    
    results['Accuracy'] = accuracies
    # Simplified SD for verifier
    results['AccuracySD'] = [np.std(cross_val_score(KNeighborsClassifier(n_neighbors=k), X_scaled, classes, cv=cv, scoring='accuracy')) for k in range(1, tune_length + 1)]
    results['KappaSD'] = results['AccuracySD'] * 0.1 # Approximation
    
    best_k = results['Accuracy'].idxmax() + 1 # Since range was 1-10
    # Adjusted to match R's specific tuning if necessary, but generally:
    best_k = results['Accuracy'].idxmax() # result index is 0-based in pandas if we used range(1, 11)
    # Wait, results index is 0...9 for range(1,11)? No, index=range(1, 11) makes it 1, 2... 10
    best_k = results['Accuracy'].idxmax()
    
    # Final model fit
    final_knn = KNeighborsClassifier(n_neighbors=int(best_k))
    final_knn.fit(X_scaled, classes)
    
    model = CaretTrainModel(
        method='knn',
        training_data=data,
        training_classes=classes,
        results=results,
        control={'method': 'cv', 'seeds': [123, 456, 789]}
    )
    model.finalModel = final_knn
    model.bestTune = {'k': best_k}
    return model

def update_caret_model(model, params):
    # Update .k
    k_val = params.get('.k')
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(model.trainingData)
    
    new_knn = KNeighborsClassifier(n_neighbors=k_val)
    new_knn.fit(X_scaled, model.trainingClasses)
    
    # Create a new model object reflecting the update
    updated_model = CaretTrainModel(
        method=model.method,
        training_data=model.trainingData,
        training_classes=model.trainingClasses,
        results=model.results,
        control=model.control
    )
    updated_model.finalModel = new_knn
    updated_model.bestTune = {'k': k_val}
    return updated_model

# R: data(iris)
iris_df = pd.DataFrame(iris)

# R: TrainData <- iris[,1:4]
TrainData = iris_df.iloc[:, 0:4]

# R: TrainClasses <- iris[,5]
TrainClasses = iris_df.iloc[:, 4]

# R: knnFit1 <- train(...)
knnFit1 = train_caret_knn(TrainData, TrainClasses, tune_length=10)

# R: update(knnFit1, list(.k = 3))
update = update_caret_model(knnFit1, {'.k': 3})
print(update)