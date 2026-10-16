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

# Helper class to mimic caret's train object structure
class CaretTrainModel:
    def __init__(self, method, results, final_model, training_data, training_classes, pre_process, control):
        self.method = method
        self.results = results
        self.finalModel = final_model
        self.trainingData = training_data
        self.trainingClasses = training_classes
        self.preProcess = pre_process
        self.control = control

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
# Mimicking caret's train(..., method="knn", tuneLength=10, trControl=trainControl(method="cv"))
# tuneLength=10 for knn typically tries k = 1, 3, 5, ..., 19 or similar. 
# R's caret knn default for tuneLength=10 usually results in k values like [5, 7, 9, 11, 13, 15, 17, 19, 21, 23] (approx)
ks = [5, 7, 9, 11, 13, 15, 17, 19, 21, 23]
accuracies = []

cv = KFold(n_splits=10, shuffle=False)

for k in ks:
    pipe = Pipeline([
        ('scaler', StandardScaler()),
        ('knn', KNeighborsClassifier(n_neighbors=k))
    ])
    # caret's cv uses accuracy by default for classification
    score = np.mean(cross_val_score(pipe, TrainData, TrainClasses, cv=cv))
    accuracies.append(score)

best_k = ks[np.argmax(accuracies)]
final_pipe = Pipeline([
    ('scaler', StandardScaler()),
    ('knn', KNeighborsClassifier(n_neighbors=best_k))
])
final_pipe.fit(TrainData, TrainClasses)

# r2py:entity:knnFit1
knnFit1 = CaretTrainModel(
    method="knn",
    results=pd.DataFrame({'k': ks, 'Accuracy': accuracies}),
    final_model=final_pipe,
    training_data=TrainData,
    training_classes=TrainClasses,
    pre_process=["center", "scale"],
    control={"method": "cv", "seeds": [123, 456, 789]}
)

def update(model, params):
    # R: update(knnFit1, list(.k = 3))
    # params is a dict like {'.k': 3}
    k_val = params.get('.k', 3)
    
    # Re-fit with the new parameter
    new_pipe = Pipeline([
        ('scaler', StandardScaler()),
        ('knn', KNeighborsClassifier(n_neighbors=k_val))
    ])
    new_pipe.fit(model.trainingData, model.trainingClasses)
    
    # Create a new instance mirroring the original but with updated model
    return CaretTrainModel(
        method=model.method,
        results=model.results, # Usually results are not re-calculated in a simple update()
        final_model=new_pipe,
        training_data=model.trainingData,
        training_classes=model.trainingClasses,
        pre_process=model.preProcess,
        control=model.control
    )

# R: update(knnFit1, list(.k = 3))
# r2py:entity:update
update_result = update(knnFit1, {'.k': 3})
print(update_result)