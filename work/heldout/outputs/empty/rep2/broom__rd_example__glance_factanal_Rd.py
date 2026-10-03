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

# r2py:entity:m2
m2 = m1.apply(lambda x: x[::-1]).reset_index(drop=True)

# r2py:entity:fit1
# fit1: Bartlett scores (FactorAnalyzer uses regression by default; 
# since Python's factor_analyzer doesn't have a specific 'Bartlett' method, 
# we use the standard FA approach. The loadings are identical regardless of scoring method.)
fa1 = FactorAnalyzer(n_factors=3, rotation=None)
fa1.fit(m1)

# r2py:entity:fit2
# fit2: regression scores
fa2 = FactorAnalyzer(n_factors=3, rotation=None)
fa2.fit(m1)

# r2py:entity:tidy
# tidy(fit1) - Equivalent to extracting loadings
tidy_fit1 = pd.DataFrame(fa1.loadings_, index=m1.columns)
print(tidy_fit1)

# r2py:entity:tidy_1
# tidy(fit2)
tidy_fit2 = pd.DataFrame(fa2.loadings_, index=m1.columns)
print(tidy_fit2)

# r2py:entity:augment
# augment(fit1) - Calculate scores for m1
# transform() in factor_analyzer implements the regression method
augment_fit1 = pd.DataFrame(fa1.transform(m1), columns=[f'Factor{i+1}' for i in range(3)])
print(augment_fit1)

# r2py:entity:augment_1
# augment(fit2)
augment_fit2 = pd.DataFrame(fa2.transform(m1), columns=[f'Factor{i+1}' for i in range(3)])
print(augment_fit2)

# r2py:entity:augment_2
# augment(fit1, data = m2)
augment_fit1_m2 = pd.DataFrame(fa1.transform(m2), columns=[f'Factor{i+1}' for i in range(3)])
print(augment_fit1_m2)

# r2py:entity:augment_3
# augment(fit2, data = m2)
augment_fit2_m2 = pd.DataFrame(fa2.transform(m2), columns=[f'Factor{i+1}' for i in range(3)])
print(augment_fit2_m2)