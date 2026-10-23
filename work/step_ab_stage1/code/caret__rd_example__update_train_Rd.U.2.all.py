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

# R: data(iris)
iris_df = pd.DataFrame(iris)

# R: TrainData <- iris[,1:4]
TrainData = iris_df.iloc[:, 0:4]

# R: TrainClasses <- iris[,5]
TrainClasses = iris_df.iloc[:, 4]

# caret::train(..., method="knn", preProcess=c("center", "scale"), tuneLength=10, trControl=trainControl(method="cv"))
# tuneLength=10 for knn usually means k from 1 to 10 (or a range)
# We must implement the centering and scaling and the CV loop to get the results
scaler = StandardScaler()
X_scaled = scaler.fit_transform(TrainData)

k_values = np.arange(1, 11)
accuracies = []
cv = KFold(n_splits=10, shuffle=False)

for k in k_values:
    clf = KNeighborsClassifier(n_neighbors=k)
    scores = cross_val_score(clf, X_scaled, TrainClasses, cv=cv, scoring='accuracy')
    accuracies.append(np.mean(scores))

# Build the knnFit1 object to mimic caret's structure
knnFit1 = {
    'method': 'knn',
    'modelType': 'Classification',
    'results': pd.DataFrame({
        'k': k_values,
        'Accuracy': accuracies
    }),
    'trainingData': TrainData,
    'trainingClasses': TrainClasses,
    'preProcess': ['center', 'scale'],
    'control': {'method': 'cv'},
    'bestTune': {'k': k_values[np.argmax(accuracies)]},
    'finalModel': KNeighborsClassifier(n_neighbors=k_values[np.argmax(accuracies)]).fit(X_scaled, TrainClasses)
}

# R: update(knnFit1, list(.k = 3))
def update_train(model, params):
    # In R, update() re-runs the train call with modified parameters
    # Here we mimic re-fitting with the specific .k value
    k_val = params.get('.k', 3)
    
    # Re-apply preprocessing
    scaler_upd = StandardScaler()
    X_upd_scaled = scaler_upd.fit_transform(model['trainingData'])
    
    clf_upd = KNeighborsClassifier(n_neighbors=k_val)
    clf_upd.fit(X_upd_scaled, model['trainingClasses'])
    
    # Create a new object similar to knnFit1
    updated_model = model.copy()
    updated_model['bestTune'] = {'k': k_val}
    updated_model['finalModel'] = clf_upd
    
    # Update results for the specific k if we want to be thorough, 
    # but for this specific update call in R, it just returns the new train object
    return updated_model

# R auto-prints the result of update()
update_result = update_train(knnFit1, {'.k': 3})
print(update_result)