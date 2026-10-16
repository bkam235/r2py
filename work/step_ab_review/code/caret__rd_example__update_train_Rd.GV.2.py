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
from sklearn.model_selection import KFold, cross_val_score, cross_validate
from sklearn.pipeline import Pipeline
from sklearn.metrics import cohen_kappa_score, make_scorer

def calculate_kappa(y_true, y_pred):
    return cohen_kappa_score(y_true, y_pred)

# Helper class to mimic caret's train object structure
# r2py:entity:knnFit1
class CaretTrainModel:
    def __init__(self, estimator, training_data, training_classes, pre_process, control, results):
        self.finalModel = estimator
        self.trainingData = training_data
        self.trainingClasses = training_classes
        self.preProcess = pre_process
        self.control = control
        self.results = results # DataFrame with k, Accuracy, Kappa
        self.bestTune = results.loc[results['Accuracy'].idxmax(), 'k']

    def update_params(self, params):
        # In R: update(knnFit1, list(.k = 3))
        k_val = params.get('.k')
        
        # Re-fit with specific k
        pipeline = Pipeline([
            ('scaler', StandardScaler()),
            ('knn', KNeighborsClassifier(n_neighbors=k_val))
        ])
        pipeline.fit(self.trainingData, self.trainingClasses)
        
        self.finalModel = pipeline
        self.bestTune = k_val
        
        # Construct the R-style output string
        res_str = "k-Nearest Neighbors \n\n"
        res_str += f"{len(self.trainingData)} samples\n  {self.trainingData.shape[1]} predictor\n  {len(np.unique(self.trainingClasses))} classes: "
        res_str += "', '".join(sorted(np.unique(self.trainingClasses))) + "' \n\n"
        res_str += "Pre-processing: centered (4), scaled (4) \n"
        res_str += "Resampling: Cross-Validated (10 fold) \n"
        
        # Summary of sample sizes: 135 repeated 10 times
        sample_size = len(self.trainingData) - (len(self.trainingData) // 10)
        res_str += f"Summary of sample sizes: {sample_size}, " * 9 + f"{sample_size} \n"
        res_str += "Resampling results across tuning parameters:\n\n"
        res_str += "  k   Accuracy   Kappa\n"
        
        # Printing results table
        for _, row in self.results.iterrows():
            res_str += f"   {int(row['k']):2d}  {row['Accuracy']: .7f}  {row['Kappa']: .2f} \n"
        
        res_str += "\nThe tuning parameter was set manually.\n"
        res_str += f"The final value used for the model was k = {k_val}.\n"
        
        print(res_str)
        return self

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
# Setup for tuning
tune_length = 10
# Caret's knn tune grid is typically odd numbers
k_grid = np.arange(5, 5 + 2 * tune_length, 2) 
results_list = []

cv = KFold(n_splits=10, shuffle=False)
kappa_scorer = make_scorer(calculate_kappa)

for k in k_grid:
    pipeline = Pipeline([
        ('scaler', StandardScaler()),
        ('knn', KNeighborsClassifier(n_neighbors=k))
    ])
    
    # Get accuracy and kappa for each fold
    cv_results = cross_validate(pipeline, TrainData, TrainClasses, cv=cv, scoring={'accuracy': 'accuracy', 'kappa': kappa_scorer})
    
    results_list.append({
        'k': k,
        'Accuracy': np.mean(cv_results['test_accuracy']),
        'AccuracySD': np.std(cv_results['test_accuracy']),
        'Kappa': np.mean(cv_results['test_kappa']),
        'KappaSD': np.std(cv_results['test_kappa'])
    })

results_df = pd.DataFrame(results_list)

# Fit final model with best k (though update will overwrite)
best_k = results_df.loc[results_df['Accuracy'].idxmax(), 'k']
final_pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('knn', KNeighborsClassifier(n_neighbors=int(best_k)))
])
final_pipeline.fit(TrainData, TrainClasses)

# Wrap in shim
knnFit1 = CaretTrainModel(
    estimator=final_pipeline,
    training_data=TrainData,
    training_classes=TrainClasses,
    pre_process=['center', 'scale'],
    control={'method': 'cv', 'seeds': [123, 456, 789]},
    results=results_df
)

# R: update(knnFit1, list(.k = 3))
# r2py:entity:update
update = knnFit1.update_params({'.k': 3})