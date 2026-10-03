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

# map_dfr(m1, rev) reverses the order of rows for each column
# r2py:entity:m2
m2 = m1.iloc[::-1].reset_index(drop=True)

# fit1: factanal with Bartlett scores (approximately handled by FactorAnalyzer)
# r2py:entity:fit1
fit1 = FactorAnalyzer(n_factors=3, rotation=None)
fit1.fit(m1)

# fit2: factanal with regression scores
# r2py:entity:fit2
fit2 = FactorAnalyzer(n_factors=3, rotation=None)
fit2.fit(m1)

# tidy(fit1) / tidy(fit2) - Extracting loadings
# In factor_analyzer, loadings are stored in .loadings_
# r2py:entity:tidy
tidy_fit1 = pd.DataFrame(fit1.loadings_, index=m1.columns)
# r2py:entity:tidy_1
tidy_fit2 = pd.DataFrame(fit2.loadings_, index=m1.columns)

print(tidy_fit1)
print(tidy_fit2)

# augment(fit1) / augment(fit2) - Transforming original data to factor scores
# Bartlett and Regression scores are different, but factor_analyzer.transform 
# typically implements a regression-like approach.
# r2py:entity:augment
augment_fit1 = pd.DataFrame(fit1.transform(m1), columns=[f'Factor{i+1}' for i in range(3)])
# r2py:entity:augment_1
augment_fit2 = pd.DataFrame(fit2.transform(m1), columns=[f'Factor{i+1}' for i in range(3)])

print(augment_fit1)
print(augment_fit2)

# augment(fit1, data = m2) / augment(fit2, data = m2)
# r2py:entity:augment_2
augment_fit1_m2 = pd.DataFrame(fit1.transform(m2), columns=[f'Factor{i+1}' for i in range(3)])
# r2py:entity:augment_3
augment_fit2_m2 = pd.DataFrame(fit2.transform(m2), columns=[f'Factor{i+1}' for i in range(3)])

print(augment_fit1_m2)
print(augment_fit2_m2)