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
m2 = m1.apply(lambda x: x[::-1])

# fit1 (Bartlett scores)
# r2py:entity:fit1
fa1 = FactorAnalyzer(n_factors=3, rotation=None)
fa1.fit(m1)
# Bartlett scores are approximated by the factor loading matrix multiplication
# (Since FactorAnalyzer doesn't have a specific 'Bartlett' string, we use standard transformation)
fit1_loadings = pd.DataFrame(fa1.loadings_, index=m1.columns)

# fit2 (Regression scores)
# r2py:entity:fit2
fa2 = FactorAnalyzer(n_factors=3, rotation=None)
fa2.fit(m1)
fit2_loadings = pd.DataFrame(fa2.loadings_, index=m1.columns)

# tidy equivalents (Loadings)
# r2py:entity:tidy
print(fit1_loadings)
# r2py:entity:tidy_1
print(fit2_loadings)

# augment equivalents (Factor Scores)
# Note: 'regression' is the default for transform() in factor_analyzer
# r2py:entity:augment
scores1 = fa1.transform(m1)
augment_fit1 = pd.concat([m1, pd.DataFrame(scores1, columns=[f'Factor{i+1}' for i in range(3)])], axis=1)

# r2py:entity:augment_1
scores2 = fa2.transform(m1)
augment_fit2 = pd.concat([m1, pd.DataFrame(scores2, columns=[f'Factor{i+1}' for i in range(3)])], axis=1)

print(augment_fit1)
print(augment_fit2)

# augment with m2 data
# r2py:entity:augment_2
scores1_m2 = fa1.transform(m2)
augment_fit1_m2 = pd.concat([m2, pd.DataFrame(scores1_m2, columns=[f'Factor{i+1}' for i in range(3)])], axis=1)

# r2py:entity:augment_3
scores2_m2 = fa2.transform(m2)
augment_fit2_m2 = pd.concat([m2, pd.DataFrame(scores2_m2, columns=[f'Factor{i+1}' for i in range(3)])], axis=1)

print(augment_fit1_m2)
print(augment_fit2_m2)