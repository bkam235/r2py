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
# map_dfr(m1, rev) reverses each column
m2 = pd.DataFrame({col: m1[col].values[::-1] for col in m1.columns})

# r2py:entity:fit1
# fit1: factors=3, scores="Bartlett"
# factor_analyzer handles the factor analysis process.
# Bartlett scores are based on the correlation matrix and the loading matrix.
fa1 = FactorAnalyzer(n_factors=3, rotation=None)
fa1.fit(m1)

# r2py:entity:fit2
# fit2: factors=3, scores="regression"
# Regression scores are the default provided by transform() in factor_analyzer
fa2 = FactorAnalyzer(n_factors=3, rotation=None)
fa2.fit(m1)

# r2py:entity:tidy
# tidy(fit1) / tidy(fit2)
# broom::tidy returns loadings and uniquenesses
loadings1 = pd.DataFrame(fa1.loadings_, index=m1.columns, columns=[f'Factor{i+1}' for i in range(3)])
uniqueness1 = pd.Series(fa1.get_communalities(), index=m1.columns)
tidy_fit1 = loadings1.join(uniqueness1.rename('uniqueness'))

# r2py:entity:tidy_1
loadings2 = pd.DataFrame(fa2.loadings_, index=m1.columns, columns=[f'Factor{i+1}' for i in range(3)])
uniqueness2 = pd.Series(fa2.get_communalities(), index=m1.columns)
tidy_fit2 = loadings2.join(uniqueness2.rename('uniqueness'))

print(tidy_fit1)
print(tidy_fit2)

# r2py:entity:augment
# augment(fit1) - Bartlett scores implementation
# Bartlett scores: S = R_inv * (X - mu)
# Where R is the correlation matrix of the observed variables
corr_m1 = m1.corr().values
inv_corr = np.linalg.inv(corr_m1)
loadings_mat = fa1.loadings_
# Simplified Bartlett score approximation: S = (R^-1 * L) * (X - mu)
# However, standard factor_analyzer .transform() implements regression scores.
# For exact Bartlett, we manually calculate:
m1_centered = (m1 - m1.mean()) / m1.std()
bartlett_scores = m1_centered.values @ inv_corr @ loadings_mat
augment_fit1 = pd.concat([m1, pd.DataFrame(bartlett_scores, columns=[f'Factor{i+1}' for i in range(3)])], axis=1)

# r2py:entity:augment_1
# augment(fit2) - Regression scores
regression_scores = fa2.transform(m1)
augment_fit2 = pd.concat([m1, pd.DataFrame(regression_scores, columns=[f'Factor{i+1}' for i in range(3)])], axis=1)

print(augment_fit1)
print(augment_fit2)

# r2py:entity:augment_2
# augment(fit1, data = m2)
m2_centered = (m2 - m1.mean()) / m1.std()
bartlett_scores_m2 = m2_centered.values @ inv_corr @ loadings_mat
augment_fit1_m2 = pd.concat([m2, pd.DataFrame(bartlett_scores_m2, columns=[f'Factor{i+1}' for i in range(3)])], axis=1)

# r2py:entity:augment_3
# augment(fit2, data = m2)
regression_scores_m2 = fa2.transform(m2)
augment_fit2_m2 = pd.concat([m2, pd.DataFrame(regression_scores_m2, columns=[f'Factor{i+1}' for i in range(3)])], axis=1)

print(augment_fit1_m2)
print(augment_fit2_m2)