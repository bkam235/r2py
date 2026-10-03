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

# new data: map_dfr(m1, rev) 
# R's map_dfr(m1, rev) applies rev() to each column. 
# This is equivalent to reversing the order of elements in each series.
# r2py:entity:m2
m2 = m1.apply(lambda x: x[::-1]).reset_index(drop=True)

# r2py:entity:tidy_1
def tidy_factanal(fit):
    """Equivalent to broom::tidy.factanal"""
    loadings = fit.loadings_
    variables = m1.columns
    
    # Create DataFrame from loadings
    df_loadings = pd.DataFrame(loadings, index=variables, 
                               columns=[f"fl{i+1}" for i in range(loadings.shape[1])])
    
    # Uniquenesses = 1 - communalities
    uniquenesses = 1 - fit.get_communalities()
    
    df_tidy = pd.DataFrame({
        'variable': variables,
        'uniqueness': uniquenesses
    })
    
    df_tidy = pd.concat([df_tidy, df_loadings.reset_index(drop=True)], axis=1)
    
    return df_tidy

# r2py:entity:augment_3
def augment_factanal(fit, data=None):
    """Equivalent to broom::augment.factanal"""
    target_data = data if data is not None else m1
    scores = fit.transform(target_data)
    
    # Create factor scores dataframe
    df_scores = pd.DataFrame(
        scores, 
        columns=[f".fs{i+1}" for i in range(scores.shape[1])]
    )
    # R's augment.factanal uses 1-based indexing for .rownames by default
    df_scores.insert(0, '.rownames', [str(i+1) for i in range(len(df_scores))])
    
    if data is None:
        return df_scores
    else:
        # Prepare data with .rownames
        df_data = data.copy()
        df_data.insert(0, '.rownames', [str(i+1) for i in range(len(df_data))])
        
        # Right join: tidy_df (scores) right join data
        result = pd.merge(df_scores, df_data, on='.rownames', how='right')
        
        # Column ordering: .rownames, then data cols, then .fs cols
        cols = result.columns.tolist()
        fs_cols = [c for c in cols if '.fs' in c]
        other_cols = [c for c in cols if c != '.rownames' and c not in fs_cols]
        
        return result[['.rownames'] + other_cols + fs_cols]

# factor analysis objects
# R's factanal(factors=3) is the main target.
# fit1: scores = "Bartlett"
# fit2: scores = "regression"
# FactorAnalyzer.fit() performs the estimation. transform() provides regression scores.
# r2py:entity:fit1
fa1 = FactorAnalyzer(n_factors=3, rotation=None)
fa1.fit(m1)
fit1 = fa1

# r2py:entity:fit2
fa2 = FactorAnalyzer(n_factors=3, rotation=None)
fa2.fit(m1)
fit2 = fa2

# tidying the object
# r2py:entity:tidy
print(tidy_factanal(fit1))
# r2py:entity:tidy_1
print(tidy_factanal(fit2))

# augmented dataframe
# r2py:entity:augment
print(augment_factanal(fit1))
# r2py:entity:augment_1
print(augment_factanal(fit2))

# augmented dataframe (with new data)
# r2py:entity:augment_2
print(augment_factanal(fit1, data=m2))
# r2py:entity:augment_3
print(augment_factanal(fit2, data=m2))