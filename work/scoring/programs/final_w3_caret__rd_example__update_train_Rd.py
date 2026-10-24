import pandas as pd
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import cohen_kappa_score, accuracy_score
import warnings

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'caret__rd_example__update_train_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['iris']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

class CaretTrainModel:
    def __init__(self, method, trainingData, trainingClasses, finalModel, bestTune, results, control, preProcess):
        self.method = method
        self.trainingData = trainingData
        self.trainingClasses = trainingClasses
        self.finalModel = finalModel
        self.bestTune = bestTune
        self.results = results
        self.control = control
        self.preProcess = preProcess
        self.modelInfo = {
            'label': 'k-Nearest Neighbors',
            'parameters': {'parameter': 'k', 'class': 'numeric', 'label': '#Neighbors'},
            'type': ['Classification', 'Regression']
        }
        self.update = None

    def __str__(self):
        res = f"      {self.modelInfo['label']} \n\n"
        res += f"{len(self.trainingData)} samples\n"
        res += f"  {self.trainingData.shape[1]} predictor\n"
        classes = self.trainingClasses.unique()
        res += f"  {len(classes)} classes: {', '.join(map(repr, classes))} \n\n"
        res += f"Pre-processing: centered ({self.trainingData.shape[1]}), scaled ({self.trainingData.shape[1]}) \n"
        
        num_folds = self.control.get('number', 10)
        res += f"Resampling: Cross-Validated ({num_folds} fold) \n"
        
        # Compute sample sizes for each fold based on StratifiedKFold
        skf = StratifiedKFold(n_splits=num_folds, shuffle=False)
        fold_sizes = []
        for train_idx, _ in skf.split(self.trainingData, self.trainingClasses):
            fold_sizes.append(str(len(train_idx)))
        
        res += "Summary of sample sizes: " + ", ".join(fold_sizes) + ", ... \n"
        res += "Resampling results across tuning parameters:\n\n"
        res += self.results.to_string(index=False)
        return res

def train_caret(x, y, method="knn", preProcess=None, tuneLength=10, trControl=None):
    scaler = StandardScaler()
    x_scaled = scaler.fit_transform(x)
    
    # Caret's knn tuneLength sequence typically starts at 1 or 5 and increments by 2
    # For iris with tuneLength 10, R uses: 5, 7, 9, 11, 13, 15, 17, 19, 21, 23
    k_grid = np.arange(5, 5 + 2 * tuneLength, 2)
    
    num_folds = trControl.get('number', 10) if trControl else 10
    skf = StratifiedKFold(n_splits=num_folds, shuffle=False)
    
    results_list = []
    best_acc = -1
    best_k = None
    best_model = None

    for k in k_grid:
        accs = []
        kappas = []
        for train_idx, test_idx in skf.split(x_scaled, y):
            knn = KNeighborsClassifier(n_neighbors=k)
            knn.fit(x_scaled[train_idx], y.iloc[train_idx])
            preds = knn.predict(x_scaled[test_idx])
            
            accs.append(accuracy_score(y.iloc[test_idx], preds))
            kappas.append(cohen_kappa_score(y.iloc[test_idx], preds))
        
        mean_acc = np.mean(accs)
        mean_kappa = np.mean(kappas)
        results_list.append({'k': int(k), 'Accuracy': mean_acc, 'Kappa': mean_kappa})
        
        if mean_acc > best_acc:
            best_acc = mean_acc
            best_k = k
            best_model = knn

    results = pd.DataFrame(results_list)
    
    return CaretTrainModel(
        method=method,
        trainingData=x,
        trainingClasses=y,
        finalModel=best_model,
        bestTune={'k': best_k},
        results=results,
        control=trControl,
        preProcess={'method': preProcess}
    )

def update_caret(obj, param=None):
    if param is None:
        return obj
    
    # Handle '.k' or 'k' naming
    k_val = param.get('.k', param.get('k'))
    
    scaler = StandardScaler()
    x_scaled = scaler.fit_transform(obj.trainingData)
    
    final_knn = KNeighborsClassifier(n_neighbors=int(k_val))
    final_knn.fit(x_scaled, obj.trainingClasses)
    
    # Create a new object to maintain functional behavior (avoid in-place mutation of original)
    import copy
    new_obj = copy.deepcopy(obj)
    new_obj.finalModel = final_knn
    new_obj.bestTune = {'k': int(k_val)}
    new_obj.update = param
    return new_obj

# --- Main Execution ---

# data(iris)
# r2py:entity:data
iris_df = iris

# TrainData <- iris[,1:4]
# r2py:entity:TrainData
TrainData = iris_df.iloc[:, 0:4]

# TrainClasses <- iris[,5]
# r2py:entity:TrainClasses
TrainClasses = iris_df.iloc[:, 4]

# trainControl(method = "cv")
trControl = {'method': 'cv', 'number': 10}

# knnFit1 <- train(...)
# r2py:entity:knnFit1
knnFit1 = train_caret(
    TrainData, TrainClasses,
    method="knn",
    preProcess=["center", "scale"],
    tuneLength=10,
    trControl=trControl
)

# update(knnFit1, list(.k = 3))
# r2py:entity:update
update_res = update_caret(knnFit1, {'.k': 3})
print(update_res)