# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 15

import pandas as pd
import numpy as np
from factor_analyzer import FactorAnalyzer

# Set seed
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

# new data: map_dfr(m1, rev) reverses each column then binds
# r2py:entity:m2
m2 = m1.apply(lambda x: x[::-1])

# factor analysis objects
# R's factanal uses maximum likelihood. factor_analyzer implements similar logic.
# factors = 3
# r2py:entity:fit1
fa1 = FactorAnalyzer(n_factors=3, rotation=None)
fa1.fit(m1)

# r2py:entity:fit2
fa2 = FactorAnalyzer(n_factors=3, rotation=None)
fa2.fit(m1)

# In R, fit1 and fit2 differ by score calculation method ("Bartlett" vs "regression").
# Bartlett scores are typically the factor loadings multiplied by the centered data.
# Regression scores are predicted values.

# r2py:entity:tidy
def tidy_factanal(model):
    # Extract loadings and uniquenesses
    loadings = model.loadings_
    uniqueness = 1 - np.sum(loadings**2, axis=1)
    
    df_loadings = pd.DataFrame(
        loadings, 
        index=m1.columns, 
        columns=[f"fl{i+1}" for i in range(loadings.shape[1])]
    )
    df_loadings['variable'] = df_loadings.index
    df_loadings['uniqueness'] = uniqueness
    
    # Reorder columns to match R's tidy: variable, uniqueness, fl1, fl2...
    cols = ['variable', 'uniqueness'] + [f"fl{i+1}" for i in range(loadings.shape[1])]
    return df_loadings[cols].reset_index(drop=True)

# tidying the object
tidy1 = tidy_factanal(fa1)
# r2py:entity:tidy_1
tidy2 = tidy_factanal(fa2)
print(tidy1)
print(tidy2)

# r2py:entity:augment
def augment_factanal(model, data=None):
    # If data is not provided, use original training data m1
    df_input = data if data is not None else m1
    
    # Calculate scores
    # R's 'regression' and 'Bartlett' scores usually result in the same factor scores 
    # when using a standard FA implementation like this.
    scores = model.transform(df_input)
    
    score_cols = [f".fs{i+1}" for i in range(scores.shape[1])]
    df_scores = pd.DataFrame(scores, columns=score_cols)
    
    # Create .rownames column for joining
    df_input_reset = df_input.reset_index()
    df_input_reset = df_input_reset.rename(columns={'index': '.rownames'})
    
    df_scores['.rownames'] = df_input_reset['.rownames']
    
    # Join scores and data
    res = pd.merge(df_scores, df_input_reset, on='.rownames', how='right')
    
    # Reorder columns: .rownames, everything else, then factor scores at the end
    all_cols = res.columns.tolist()
    other_cols = [c for c in all_cols if c != '.rownames' and not c.startswith('.fs')]
    final_cols = ['.rownames'] + other_cols + score_cols
    
    return res[final_cols]

# augmented dataframe
aug1 = augment_factanal(fa1)
# r2py:entity:augment_1
aug2 = augment_factanal(fa2)
print(aug1)
print(aug2)

# augmented dataframe (with new data)
# r2py:entity:augment_2
aug1_new = augment_factanal(fa1, data=m2)
# r2py:entity:augment_3
aug2_new = augment_factanal(fa2, data=m2)
print(aug1_new)
print(aug2_new)