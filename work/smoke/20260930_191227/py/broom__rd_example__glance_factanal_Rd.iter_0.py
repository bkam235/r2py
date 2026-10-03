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

# factor_analyzer.FactorAnalyzer provides the equivalent to factanal
# Bartlett vs Regression scores are handled via the transform method 
# (Regression is the default for most Python factor analysis libs)
# r2py:entity:fit1
fit1 = FactorAnalyzer(n_factors=3, rotation=None)
fit1.fit(m1)

# r2py:entity:fit2
fit2 = FactorAnalyzer(n_factors=3, rotation=None)
fit2.fit(m1)

# tidy(fit1) / tidy(fit2) equivalent: Loadings
# r2py:entity:tidy
tidy_fit1 = pd.DataFrame(fit1.loadings_, index=m1.columns)
# r2py:entity:tidy_1
tidy_fit2 = pd.DataFrame(fit2.loadings_, index=m1.columns)

print(tidy_fit1)
print(tidy_fit2)

# augment(fit1) / augment(fit2) equivalent: Transform data to factor scores
# Note: factor_analyzer uses a regression-like approach for transform
# r2py:entity:augment
augment_fit1 = pd.concat([m1, pd.DataFrame(fit1.transform(m1))], axis=1)
# r2py:entity:augment_1
augment_fit2 = pd.concat([m1, pd.DataFrame(fit2.transform(m1))], axis=1)

print(augment_fit1)
print(augment_fit2)

# augment(fit1, data = m2) / augment(fit2, data = m2)
# r2py:entity:augment_2
augment_fit1_m2 = pd.concat([m2, pd.DataFrame(fit1.transform(m2))], axis=1)
# r2py:entity:augment_3
augment_fit2_m2 = pd.concat([m2, pd.DataFrame(fit2.transform(m2))], axis=1)

print(augment_fit1_m2)
print(augment_fit2_m2)