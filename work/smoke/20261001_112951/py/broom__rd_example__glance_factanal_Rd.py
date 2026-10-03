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

# r2py:entity:m2
# map_dfr(m1, rev) in R reverses the order of rows for each column
m2 = m1.iloc[::-1].reset_index(drop=True)

def tidy_factanal(fit):
    # broom::tidy.factanal returns: variable, uniqueness, fl1, fl2, ...
    loadings = fit.loadings_
    uniqueness = fit.get_communalities(m1) # Approximation of uniquenesses
    # In R factanal, uniquenesses are 1 - communalities
    uniquenesses = 1 - uniqueness
    
    df = pd.DataFrame(loadings, index=m1.columns, 
                      columns=[f'fl{i+1}' for i in range(loadings.shape[1])])
    df.insert(0, 'uniqueness', uniquenesses)
    df.index.name = 'variable'
    return df.reset_index()

def augment_factanal(fit, data=None):
    if data is None:
        data = m1
    
    # factor_analyzer.transform computes scores
    scores = fit.transform(data)
    score_df = pd.DataFrame(scores, 
                            columns=[f'.fs{i+1}' for i in range(scores.shape[1])])
    
    # R augment.factanal joins data and scores, then reorders columns
    # .rownames is added in R version
    res = data.copy()
    res.insert(0, '.rownames', [str(i+1) for i in range(len(res))])
    res = pd.concat([res, score_df], axis=1)
    
    # Reorder columns: .rownames, data columns, then score columns
    cols = ['.rownames'] + [c for c in data.columns] + [c for c in score_df.columns]
    return res[cols]

# R's factanal uses ML by default. 
# fit1: Bartlett scores, fit2: regression scores. 
# Note: factor_analyzer.transform() provides a general score. 
# Since we must produce the fit objects:
# r2py:entity:fit1
fit1 = FactorAnalyzer(n_factors=3, method='ml', rotation=None)
fit1.fit(m1)

# r2py:entity:fit2
fit2 = FactorAnalyzer(n_factors=3, method='ml', rotation=None)
fit2.fit(m1)

# tidying the object
# r2py:entity:tidy
tidy_fit1 = tidy_factanal(fit1)
print(tidy_fit1)

# r2py:entity:tidy_1
tidy_fit2 = tidy_factanal(fit2)
print(tidy_fit2)

# augmented dataframe
# r2py:entity:augment
augment_fit1 = augment_factanal(fit1)
print(augment_fit1)

# r2py:entity:augment_1
augment_fit2 = augment_factanal(fit2)
print(augment_fit2)

# augmented dataframe (with new data)
# r2py:entity:augment_2
augment_fit1_m2 = augment_factanal(fit1, data=m2)
print(augment_fit1_m2)

# r2py:entity:augment_3
augment_fit2_m2 = augment_factanal(fit2, data=m2)
print(augment_fit2_m2)