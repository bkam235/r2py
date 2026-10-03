# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 15

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

# map_dfr(m1, rev) reverses the order of rows for each column (equivalent to reversing the whole dataframe)
# r2py:entity:m2
m2 = m1.iloc[::-1].reset_index(drop=True)

# R's factanal uses Maximum Likelihood. 
# FactorAnalyzer's rotation='none' and method='ml' approximates factanal.
# r2py:entity:fit1
fit1 = FactorAnalyzer(n_factors=3, rotation=None, method='ml')
fit1.fit(m1)

# r2py:entity:fit2
fit2 = FactorAnalyzer(n_factors=3, rotation=None, method='ml')
fit2.fit(m1)

# tidy(fit1) - Extracts loadings
# r2py:entity:tidy
loadings1 = pd.DataFrame(fit1.loadings_, index=m1.columns)
print(loadings1)

# tidy(fit2)
# r2py:entity:tidy_1
loadings2 = pd.DataFrame(fit2.loadings_, index=m1.columns)
print(loadings2)

# augment(fit1) - Bartlett scores are essentially the raw factor scores (standardized)
# augment(fit2) - Regression scores
# r2py:entity:augment
scores1 = fit1.transform(m1)
augment_fit1 = pd.concat([m1, pd.DataFrame(scores1, columns=[f'Factor{i+1}' for i in range(3)])], axis=1)
print(augment_fit1)

# r2py:entity:augment_1
scores2 = fit2.transform(m1)
augment_fit2 = pd.concat([m1, pd.DataFrame(scores2, columns=[f'Factor{i+1}' for i in range(3)])], axis=1)
print(augment_fit2)

# augment(fit1, data = m2)
# r2py:entity:augment_2
scores_m2_1 = fit1.transform(m2)
augment_m2_1 = pd.concat([m2, pd.DataFrame(scores_m2_1, columns=[f'Factor{i+1}' for i in range(3)])], axis=1)
print(augment_m2_1)

# augment(fit2, data = m2)
# r2py:entity:augment_3
scores_m2_2 = fit2.transform(m2)
augment_m2_2 = pd.concat([m2, pd.DataFrame(scores_m2_2, columns=[f'Factor{i+1}' for i in range(3)])], axis=1)
print(augment_m2_2)