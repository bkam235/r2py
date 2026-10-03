# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 15

import pandas as pd
import numpy as np
from factor_analyzer import FactorAnalyzer

# set.seed(123)
# r2py:entity:set.seed
np.random.seed(123)

# generate data
# r2py:entity:m1
m1 = pd.DataFrame({
    'v1': [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3, 3, 3, 3, 4, 5, 6],
    'v2': [1, 2, 1, 1, 1, 1, 2, 1, 2, 1, 3, 4, 3, 3, 3, 4, 6, 5],
    'v3': [3, 3, 3, 3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 5, 4, 6],
    'v4': [3, 3, 4, 3, 3, 1, 1, 2, 1, 1, 1, 1, 2, 1, 1, 5, 6, 4],
    'v5': [1, 1, 1, 1, 1, 3, 3, 3, 3, 3, 1, 1, 1, 1, 1, 6, 4, 5],
    'v6': [1, 1, 1, 2, 1, 3, 3, 3, 4, 3, 1, 1, 1, 2, 1, 6, 5, 4]
})

# new data (map_dfr(m1, rev) reverses the order of rows for each column)
# r2py:entity:m2
m2 = m1.iloc[::-1].reset_index(drop=True)

# factor analysis objects
# R's factanal uses Maximum Likelihood by default. 
# Python's FactorAnalyzer uses different rotation/extraction methods.
# For parity with R's factanal (ML), we use rotation=None and similar logic.
# r2py:entity:fit1
fa1 = FactorAnalyzer(n_factors=3, rotation=None)
fa1.fit(m1)

# r2py:entity:fit2
fa2 = FactorAnalyzer(n_factors=3, rotation=None)
fa2.fit(m1)

# r2py:entity:tidy
def tidy_factanal(fa_model, data):
    loadings = fa_model.loadings_
    uniqueness = 1 - np.sum(loadings**2, axis=1)
    
    df_loadings = pd.DataFrame(loadings, index=data.columns)
    df_loadings.columns = [f'fl{i+1}' for i in range(df_loadings.shape[1])]
    
    tidy_df = pd.concat([df_loadings, pd.Series(uniqueness, index=data.columns, name='uniqueness')], axis=1)
    tidy_df.index.name = 'variable'
    return tidy_df.reset_index()

# r2py:entity:augment
def augment_factanal(fa_model, data, new_data=None):
    # Calculate factor scores
    # Bartlett vs Regression is handled by the scoring method in R. 
    # FactorAnalyzer's transform method provides the scores.
    scores = fa_model.transform(data if new_data is None else new_data)
    
    df_scores = pd.DataFrame(scores, columns=[f'.fs{i+1}' for i in range(scores.shape[1])])
    df_scores.insert(0, '.rownames', [str(i+1) for i in range(len(df_scores))])
    
    if new_data is None:
        target_data = data.copy()
    else:
        target_data = new_data.copy()
        
    target_data.insert(0, '.rownames', [str(i+1) for i in range(len(target_data))])
    
    # Join scores and data
    res = pd.merge(df_scores, target_data, on='.rownames', how='right')
    
    # Reorder columns: .rownames, then other data cols, then .fs cols
    cols = res.columns.tolist()
    fs_cols = [c for c in cols if c.startswith('.fs')]
    other_cols = [c for c in cols if c != '.rownames' and not c.startswith('.fs')]
    
    return res[['.rownames'] + other_cols + fs_cols]

# tidying the object
# r2py:entity:tidy
print(tidy_factanal(fa1, m1))
# r2py:entity:tidy_1
print(tidy_factanal(fa2, m1))

# augmented dataframe
# r2py:entity:augment
print(augment_factanal(fa1, m1))
# r2py:entity:augment_1
print(augment_factanal(fa2, m1))

# augmented dataframe (with new data)
# r2py:entity:augment_2
print(augment_factanal(fa1, m1, new_data=m2))
# r2py:entity:augment_3
print(augment_factanal(fa2, m1, new_data=m2))