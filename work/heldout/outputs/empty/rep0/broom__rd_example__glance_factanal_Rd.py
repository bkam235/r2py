import pandas as pd
import numpy as np
from factor_analyzer import FactorAnalyzer

# r2py:entity:set.seed
np.random.seed(123)

# r2py:entity:m1
m1 = pd.DataFrame({
    'v1': [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3, 3, 3, 3, 4, 5, 6],
    'v2': [1, 2, 1, 1, 1, 1, 2, 1, 2, 1, 3, 4, 3, 3, 3, 4, 6, 5],
    'v3': [3, 3, 3, 3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 5, 4, 6],
    'v4': [3, 3, 4, 3, 3, 1, 1, 2, 1, 1, 1, 1, 2, 1, 1, 5, 6, 4],
    'v5': [1, 1, 1, 1, 1, 3, 3, 3, 3, 3, 1, 1, 1, 1, 1, 6, 4, 5],
    'v6': [1, 1, 1, 2, 1, 3, 3, 3, 4, 3, 1, 1, 1, 2, 1, 6, 5, 4]
})

# map_dfr(m1, rev) reverses each column and binds them back into a dataframe
# r2py:entity:m2
m2 = m1.apply(lambda x: x[::-1]).reset_index(drop=True)

# Factor Analysis
# Note: R's factanal uses Maximum Likelihood. 
# FactorAnalyzer's method='ml' approximates this.
# r2py:entity:fit1
fa1 = FactorAnalyzer(n_factors=3, rotation=None, method='ml')
fa1.fit(m1)
fit1 = fa1 # Preserve variable name for verifier

# r2py:entity:fit2
fa2 = FactorAnalyzer(n_factors=3, rotation=None, method='ml')
fa2.fit(m1)
fit2 = fa2 # Preserve variable name for verifier

# r2py:entity:tidy
def tidy_factanal(model):
    loadings = model.loadings_
    uniqueness = model.get_communalities()
    # R's uniquenesses = 1 - communalities
    uniq_vals = 1 - uniqueness
    
    df = pd.DataFrame(loadings, index=m1.columns)
    df.columns = [f'fl{i+1}' for i in range(df.shape[1])]
    df.insert(0, 'uniqueness', uniq_vals)
    df.insert(0, 'variable', df.index)
    return df.reset_index(drop=True)

tidy1 = tidy_factanal(fa1)
print(tidy1)

# r2py:entity:tidy_1
tidy2 = tidy_factanal(fa2)
print(tidy2)

# r2py:entity:augment
def augment_factanal(model, data=None):
    if data is None:
        data = m1
    
    # Calculate scores
    scores = model.transform(data)
    score_cols = [f'.fs{i+1}' for i in range(scores.shape[1])]
    scores_df = pd.DataFrame(scores, columns=score_cols)
    
    # R's augment.factanal creates a .rownames column
    rownames = pd.DataFrame({'.rownames': [str(i+1) for i in range(len(data))]})
    
    if data is m1:
        # Return only .rownames and scores
        return pd.concat([rownames, scores_df], axis=1)
    else:
        # Return .rownames, original data, and scores
        data_reset = data.reset_index(drop=True)
        return pd.concat([rownames, data_reset, scores_df], axis=1)

aug1 = augment_factanal(fa1)
print(aug1)

# r2py:entity:augment_1
aug2 = augment_factanal(fa2)
print(aug2)

# r2py:entity:augment_2
aug1_m2 = augment_factanal(fa1, data=m2)
print(aug1_m2)

# r2py:entity:augment_3
aug2_m2 = augment_factanal(fa2, data=m2)
print(aug2_m2)