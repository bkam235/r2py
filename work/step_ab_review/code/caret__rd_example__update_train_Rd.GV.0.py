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
from sklearn.model_selection import KFold, cross_validate
from sklearn.metrics import accuracy_score, cohen_kappa_score
from sklearn.pipeline import Pipeline

# r2py:entity:knnFit1
class CaretTrainModel:
    def __init__(self, TrainData, TrainClasses, method="knn", preProcess=None, tuneLength=10, trControl=None):
        self.method = method
        self.preProcess = preProcess
        self.tuneLength = tuneLength
        self.trControl = trControl
        self.trainingData = TrainData
        self.trainingClasses = TrainClasses
        
        # Setup pipeline
        self.pipeline = Pipeline([
            ('scaler', StandardScaler()),
            ('knn', KNeighborsClassifier())
        ])
        
        # Caret's knn defaults to a grid of k values
        # For tuneLength=10, it typically picks 10 values starting from 5, usually by 2s
        self.k_grid = np.arange(5, 5 + 2 * tuneLength, 2)
        self.results = pd.DataFrame(columns=['k', 'Accuracy', 'Kappa'])
        
        kf = KFold(n_splits=10, shuffle=False)
        accs, kappas = [], []
        
        for k in self.k_grid:
            self.pipeline.set_params(knn__n_neighbors=k)
            cv_results = cross_validate(self.pipeline, TrainData, TrainClasses, cv=kf, scoring='accuracy')
            acc = np.mean(cv_results['test_score'])
            
            # Calculate Kappa manually for each fold to get the mean Kappa
            fold_kappas = []
            for train_idx, test_idx in kf.split(TrainData):
                p = Pipeline([('scaler', StandardScaler()), ('knn', KNeighborsClassifier(n_neighbors=k))])
                p.fit(TrainData.iloc[train_idx], TrainClasses.iloc[train_idx])
                preds = p.predict(TrainData.iloc[test_idx])
                fold_kappas.append(cohen_kappa_score(TrainClasses.iloc[test_idx], preds))
            
            accs.append(acc)
            kappas.append(np.mean(fold_kappas))
            
        self.results = pd.DataFrame({'k': self.k_grid, 'Accuracy': accs, 'Kappa': kappas})
        self.bestTune = {'k': self.results.loc[self.results['Accuracy'].idxmax(), 'k'].astype(int)}

# r2py:entity:update
def update(model, params):
    # In R: update(knnFit1, list(.k = 3))
    k_val = params.get('.k', 3)
    
    # Set manual parameter
    model.bestTune = {'k': k_val}
    
    # Final fit with the updated parameter
    model.pipeline.set_params(knn__n_neighbors=k_val)
    model.pipeline.fit(model.trainingData, model.trainingClasses)
    
    # Print R-style output
    print("k-Nearest Neighbors \n")
    print(f"{len(model.trainingData)} samples")
    print(f"  {model.trainingData.shape[1]} predictor")
    classes = np.unique(model.trainingClasses)
    print(f"  {len(classes)} classes: {', '.join([f"'{c}'" for c in classes])} \n")
    print(f"Pre-processing: centered ({model.trainingData.shape[1]}), scaled ({model.trainingData.shape[1]}) ")
    print(f"Resampling: Cross-Validated (10 fold) ")
    
    # Summary of sample sizes: for 150 samples, 10-fold CV is 135 per fold
    sample_size = len(model.trainingData) // 10 * 9
    print(f"Summary of sample sizes: {', '.join([str(sample_size)] * 10 + ['... '])} \n")
    
    print("Resampling results across tuning parameters:\n")
    print(f"  {'k':<4} {'Accuracy':<10} {'Kappa':<8}")
    for _, row in model.results.iterrows():
        print(f"   {int(row['k']):<2}  {row['Accuracy']:<10.7f}  {row['Kappa']:<8.2f}")
    
    print("\nThe tuning parameter was set manually.")
    print(f"The final value used for the model was k = {k_val}.")
    
    return model

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
# r2py:entity:knnFit1
knnFit1 = CaretTrainModel(
    TrainData=TrainData, 
    TrainClasses=TrainClasses,
    method="knn", 
    preProcess=["center", "scale"], 
    tuneLength=10, 
    trControl={"method": "cv"}
)

# R: update(knnFit1, list(.k = 3))
# r2py:entity:update
update(knnFit1, {'.k': 3})