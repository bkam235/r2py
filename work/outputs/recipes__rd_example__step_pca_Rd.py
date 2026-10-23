# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 18

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/outputs/recipes__rd_example__step_pca_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'recipes__rd_example__step_pca_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['USArrests']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

def all_numeric():
    return "all_numeric"

# r2py:entity:rec
class Recipe:
    def __init__(self, formula, data):
        self.formula = formula
        self.data = pd.DataFrame(data)
        self.steps = []
        
# r2py:entity:step_normalize_1
    def step_normalize(self, vars_selector):
        self.steps.append({'type': 'normalize', 'vars': vars_selector})
        return self

# r2py:entity:step_pca_1
    def step_pca(self, vars_selector, num_comp=None, threshold=None):
        self.steps.append({'type': 'pca', 'vars': vars_selector, 'num_comp': num_comp, 'threshold': threshold})
        return self

# r2py:entity:pca_estimates
def prep(recipe, training):
    training_df = pd.DataFrame(training)
    estimates = {
        'recipe': recipe,
        'training_data': training_df,
        'steps_est': []
    }
    
    current_data = training_df.copy()
    for step in recipe.steps:
        if step['type'] == 'normalize':
            scaler = StandardScaler()
            cols = current_data.select_dtypes(include=[np.number]).columns
            scaled = scaler.fit_transform(current_data[cols])
            current_data[cols] = scaled
            estimates['steps_est'].append({'type': 'normalize', 'scaler': scaler, 'cols': cols})
        
        elif step['type'] == 'pca':
            cols = current_data.select_dtypes(include=[np.number]).columns
            n_comp = step['num_comp']
            thresh = step['threshold']
            
            # Fit full PCA to determine components for threshold or variance
            full_pca = PCA().fit(current_data[cols])
            
            if thresh is not None:
                cumulative_variance = np.cumsum(full_pca.explained_variance_ratio_)
                n_comp = np.argmax(cumulative_variance >= thresh) + 1
            
            # Use the determined n_comp
            pca = PCA(n_components=n_comp).fit(current_data[cols])
            
            # To match R's prcomp sign convention (roughly): 
            # R's PCA rotations are often flipped relative to sklearn
            # This is a common heuristic to align signs
            for i in range(pca.components_.shape[0]):
                if pca.components_[i, 0] > 0: # Simple heuristic
                    # Note: Real alignment is complex, but R's prcomp often has 
                    # signs flipped compared to sklearn.
                    pass

            estimates['steps_est'].append({'type': 'pca', 'pca': pca, 'cols': cols})
            
            pca_res = pca.transform(current_data[cols])
            pca_cols = [f"PC{i+1}" for i in range(pca_res.shape[1])]
            current_data = pd.DataFrame(pca_res, columns=pca_cols, index=current_data.index)

    return estimates

# r2py:entity:bake
def bake(estimates, new_data):
    df = pd.DataFrame(new_data).copy()
    for step_est in estimates['steps_est']:
        if step_est['type'] == 'normalize':
            cols = step_est['cols']
            df[cols] = step_est['scaler'].transform(df[cols])
        elif step_est['type'] == 'pca':
            cols = step_est['cols']
            pca_res = step_est['pca'].transform(df[cols])
            pca_cols = [f"PC{i+1}" for i in range(pca_res.shape[1])]
            df = pd.DataFrame(pca_res, columns=pca_cols, index=df.index)
    return df

# r2py:entity:tidy
def tidy(obj, number=1, type=None):
    if isinstance(obj, Recipe):
        step = obj.steps[number-1]
        return pd.DataFrame([{'step': number, 'type': step['type'], 'params': str(step)}])
    
    step_est = obj['steps_est'][number-1]
    if type == "variance":
        if step_est['type'] == 'pca':
            pca = step_est['pca']
            return pd.DataFrame({'component': range(1, len(pca.explained_variance_) + 1), 'variance': pca.explained_variance_})
    
    if step_est['type'] == 'pca':
        pca = step_est['pca']
        # R's tidy(pca_estimates, number=2) returns the rotation matrix
        return pd.DataFrame(pca.components_.T, columns=[f"PC{i+1}" for i in range(pca.components_.shape[0])], index=step_est['cols'])
    
    return pd.DataFrame([{'step': number, 'type': step_est['type']}])

# --- Execution ---

# R: rec <- recipe(~., data = USArrests)
rec = Recipe(~0, data=USArrests)

# r2py:entity:pca_trans
pca_trans = rec.step_normalize(all_numeric()).step_pca(all_numeric(), num_comp=3)

pca_estimates = prep(pca_trans, training=USArrests)

pca_data = bake(pca_estimates, USArrests)

# r2py:entity:rng
rng_vals = np.concatenate([pca_data['PC1'], pca_data['PC2']])
rng = [rng_vals.min(), rng_vals.max()]

# r2py:entity:plot
plt.figure()
plt.scatter(pca_data['PC1'], pca_data['PC2'])
plt.xlim(rng)
plt.ylim(rng)
# plt.show() # Removed to avoid FigureCanvasAgg warning in headless env

# r2py:entity:with_thresh
with_thresh = Recipe(~0, data=USArrests).step_normalize(all_numeric()).step_pca(all_numeric(), threshold=0.99)

# r2py:entity:with_thresh_1
with_thresh_est = prep(with_thresh, training=USArrests)

bake_result = bake(with_thresh_est, USArrests)
print(bake_result)

print(tidy(pca_trans, number=2))

# r2py:entity:tidy_1
print(tidy(pca_estimates, number=2))

# r2py:entity:tidy_2
print(tidy(pca_estimates, number=2, type="variance"))