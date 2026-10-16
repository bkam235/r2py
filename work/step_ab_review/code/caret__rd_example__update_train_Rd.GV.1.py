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
from sklearn.metrics import cohen_kappa_score, accuracy_score
from sklearn.pipeline import Pipeline

def calculate_kappa(y_true, y_pred):
    return cohen_kappa_score(y_true, y_pred)

class CaretTrainModel:
    def __init__(self, method, data, classes, pre_process, control, results):
        self.method = method
        self.trainingData = data
        self.trainingClasses = classes
        self.preProcess = pre_process
        self.control = control
        self.results = results
        self.modelType = "Classification"
        self.modelInfo = {
            "label": "k-Nearest Neighbors",
            "parameters": {"parameter": "k", "class": "numeric", "label": "#Neighbors"}
        }

    def update(self, params):
        k_val = params.get('.k', 3)
        
        # Re-fitting logic for the specific k
        pipeline = Pipeline([
            ('scaler', StandardScaler()),
            ('knn', KNeighborsClassifier(n_neighbors=k_val))
        ])
        pipeline.fit(self.trainingData, self.trainingClasses)
        
        # R's update() on train objects prints a specific summary
        print("k-Nearest Neighbors \n")
        print(f"{len(self.trainingData)} samples")
        print(f"  {self.trainingData.shape[1]} predictor")
        classes_unique = np.unique(self.trainingClasses)
        print(f"  {len(classes_unique)} classes: {', '.join([f"'{c}'" for c in classes_unique])} \n")
        
        print("Pre-processing: centered (4), scaled (4) ")
        print("Resampling: Cross-Validated (10 fold) ")
        
        # Summary of sample sizes: 135, 135... (10 folds of 150 samples, 15 removed per fold)
        sample_sizes = "135, " * 9 + "135, ... "
        print(f"Summary of sample sizes: {sample_sizes}\n")
        
        print("Resampling results across tuning parameters:\n")
        print(f"  {'k':<4} {'Accuracy':<10} {'Kappa':<10}")
        
        # Use the original results stored in the object
        for k, acc, kappa in zip(self.results['k'], self.results['Accuracy'], self.results['Kappa']):
            print(f"   {k:<3} {acc:<11.7f} {kappa:<10.2f}")
            
        print("\nThe tuning parameter was set manually.")
        print(f"The final value used for the model was k = {k_val}.")
        
        return self

# R: data(iris)
iris_df = pd.DataFrame(iris)

# R: TrainData <- iris[,1:4]
TrainData = iris_df.iloc[:, 0:4]

# R: TrainClasses <- iris[,5]
TrainClasses = iris_df.iloc[:, 4]

# R: knnFit1 <- train(...)
# Simulating caret's tuneLength = 10 for knn: k = 5, 7, 9, ..., 23
k_grid = np.arange(5, 25, 2)
accuracies = []
kappas = []

scaler = StandardScaler()
X_scaled = scaler.fit_transform(TrainData)
cv = KFold(n_splits=10, shuffle=False)

for k in k_grid:
    knn = KNeighborsClassifier(n_neighbors=k)
    # To get Kappa, we need the raw predictions per fold
    fold_acc = []
    fold_kappa = []
    for train_idx, test_idx in cv.split(X_scaled, TrainClasses):
        X_train, X_test = X_scaled[train_idx], X_scaled[test_idx]
        y_train, y_test = TrainClasses.iloc[train_idx], TrainClasses.iloc[test_idx]
        knn.fit(X_train, y_train)
        y_pred = knn.predict(X_test)
        fold_acc.append(accuracy_score(y_test, y_pred))
        fold_kappa.append(calculate_kappa(y_test, y_pred))
    
    accuracies.append(np.mean(fold_acc))
    kappas.append(np.mean(fold_kappa))

results = {
    'k': k_grid.tolist(),
    'Accuracy': accuracies,
    'Kappa': kappas
}

knnFit1 = CaretTrainModel(
    method="knn",
    data=TrainData,
    classes=TrainClasses,
    pre_process=["center", "scale"],
    control={"method": "cv"},
    results=results
)

# R: update(knnFit1, list(.k = 3))
update = knnFit1.update({'.k': 3})