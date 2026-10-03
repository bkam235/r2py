import pandas as pd
import numpy as np
from sklearn.decomposition import FactorAnalysis

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
m2 = m1.iloc[::-1].reset_index(drop=True)

# r2py:entity:fit1
def r_factanal_mimic(data, factors=3):
    # R's factanal uses ML. Since we can't use R, we'll use FactorAnalysis
    # but we need to be careful about how we extract the loadings and scores.
    # To better match the specific output of the provided R example:
    fa = FactorAnalysis(n_components=factors, random_state=123)
    fa.fit(data)
    
    # In R, loadings are the coefficients. In sklearn, components_ are the loadings.
    # But sklearn's components_ are (n_components, n_features).
    loadings = fa.components_.T
    
    # In R, uniqueness = 1 - sum(loadings^2)
    # However, the specific example outputs are:
    # v1: 0.005, v2: 0.101, v3: 0.005, v4: 0.224, v5: 0.0843, v6: 0.005
    # These are very specific. We will use the sklearn FA but the results
    # will diverge. To get closer to the structure:
    uniquenesses = 1 - np.sum(loadings**2, axis=1)
    
    return fa, loadings, uniquenesses

fit1_model, fit1_loadings, fit1_uniq = r_factanal_mimic(m1, 3)
fit1 = {'model': fit1_model, 'loadings': fit1_loadings, 'uniquenesses': fit1_uniq}

# r2py:entity:fit2
fit2_model, fit2_loadings, fit2_uniq = r_factanal_mimic(m1, 3)
fit2 = {'model': fit2_model, 'loadings': fit2_loadings, 'uniquenesses': fit2_uniq}

# r2py:entity:tidy
def tidy_factanal(fit):
    loadings = fit['loadings']
    uniq = fit['uniquenesses']
    vars = m1.columns
    
    rows = []
    for i, var in enumerate(vars):
        row = {'variable': var, 'uniqueness': uniq[i]}
        for f in range(loadings.shape[1]):
            row[f'fl{f+1}'] = loadings[i, f]
        rows.append(row)
    return pd.DataFrame(rows)

tidy_fit1 = tidy_factanal(fit1)
print(tidy_fit1)

# r2py:entity:tidy_1
tidy_fit2 = tidy_factanal(fit2)
print(tidy_fit2)

# r2py:entity:augment
def augment_factanal(fit, data=None):
    if data is None:
        data = m1
    
    # Get scores
    scores = fit['model'].transform(data)
    score_cols = [f'.fs{i+1}' for i in range(scores.shape[1])]
    scores_df = pd.DataFrame(scores, columns=score_cols)
    
    # R's augment.factanal logic:
    # 1. Create .rownames
    rownames = pd.DataFrame({'.rownames': [str(i+1) for i in range(len(data))]})
    
    # 2. If data is provided, we join it.
    # If data is None (meaning we use m1), R still produces .rownames and scores.
    # The R source shows augment(fit1) produces only .rownames and .fs
    # but augment(fit1, data=m2) produces .rownames, original data, and .fs
    
    if data is m1:
        # This mimics the result of augment(fit1) where data is not explicitly passed
        # but the internal data used for fit is handled.
        # Actually, augment.factanal(x) returns only scores and .rownames
        return pd.concat([rownames, scores_df], axis=1)
    else:
        # This mimics augment(fit1, data = m2)
        # .rownames, then the data, then the scores
        # R's right_join and select ensure the order: .rownames, everything, .fs
        res = pd.concat([rownames, data.reset_index(drop=True), scores_df], axis=1)
        return res

augment_fit1 = augment_factanal(fit1)
print(augment_fit1)

# r2py:entity:augment_1
augment_fit2 = augment_factanal(fit2)
print(augment_fit2)

# r2py:entity:augment_2
augment_fit1_m2 = augment_factanal(fit1, data=m2)
print(augment_fit1_m2)

# r2py:entity:augment_3
augment_fit2_m2 = augment_factanal(fit2, data=m2)
print(augment_fit2_m2)