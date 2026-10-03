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
# map_dfr(m1, rev) reverses each column of the dataframe
m2 = m1.iloc[::-1].reset_index(drop=True)

# r2py:entity:fit1
# R's factanal performs Maximum Likelihood estimation by default.
# We use FactorAnalyzer and assign the result to fit1 to match R's variable name.
# Note: FactorAnalyzer.fit returns the instance itself.
fit1 = FactorAnalyzer(n_factors=3, rotation=None, method='ml')
fit1.fit(m1)

# r2py:entity:tidy
# tidy(fit1) equivalent: Extract loadings
loadings1 = pd.DataFrame(fa1.loadings_, index=m1.columns, columns=[f'Factor{i+1}' for i in range(3)])
print(loadings1)

# r2py:entity:fit2
# fit2: regression scores
fa2 = FactorAnalyzer(n_factors=3, rotation=None)
fa2.fit(m1)
# r2py:entity:tidy_1
loadings2 = pd.DataFrame(fa2.loadings_, index=m1.columns, columns=[f'Factor{i+1}' for i in range(3)])
print(loadings2)

# r2py:entity:augment
# augment(fit1) - Calculate factor scores for original data
# Using regression method (standard in Python factor_analyzer)
scores1 = fa1.transform(m1)
augment_fit1 = pd.concat([m1, pd.DataFrame(scores1, columns=[f'Factor{i+1}' for i in range(3)])], axis=1)
print(augment_fit1)

# r2py:entity:augment_1
# augment(fit2)
scores2 = fa2.transform(m1)
augment_fit2 = pd.concat([m1, pd.DataFrame(scores2, columns=[f'Factor{i+1}' for i in range(3)])], axis=1)
print(augment_fit2)

# r2py:entity:augment_2
# augment(fit1, data = m2)
scores_m2_1 = fa1.transform(m2)
augment_m2_fit1 = pd.concat([m2, pd.DataFrame(scores_m2_1, columns=[f'Factor{i+1}' for i in range(3)])], axis=1)
print(augment_m2_fit1)

# r2py:entity:augment_3
# augment(fit2, data = m2)
scores_m2_2 = fa2.transform(m2)
augment_m2_fit2 = pd.concat([m2, pd.DataFrame(scores_m2_2, columns=[f'Factor{i+1}' for i in range(3)])], axis=1)
print(augment_m2_fit2)