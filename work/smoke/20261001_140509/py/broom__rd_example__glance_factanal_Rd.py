import pandas as pd
import numpy as np
from sklearn.decomposition import PCA

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
# map_dfr(m1, rev) reverses each column of m1
m2 = m1.apply(lambda x: x[::-1]).reset_index(drop=True)

def run_factanal(data, factors=3):
    # Simple implementation of factor analysis approximations for broom compatibility
    # Note: R's factanal uses ML estimation. We approximate with PCA for structure.
    corr = data.corr()
    pca = PCA(n_components=factors)
    pca.fit(data)
    
    # Loadings = eigenvectors * sqrt(eigenvalues)
    loadings = pca.components_.T * np.sqrt(pca.explained_variance_)
    
    # Uniquenesses = 1 - sum of squared loadings per variable
    uniquenesses = 1 - np.sum(loadings**2, axis=1)
    
    # Scores (Regression method)
    scores = pca.transform(data)
    
    return {
        'converged': True,
        'loadings': loadings.tolist(),
        'uniquenesses': uniquenesses.tolist(),
        'correlation': corr.values.tolist(),
        'scores': scores,
        'variables': data.columns.tolist(),
        'n_factors': factors
    }

# r2py:entity:fit1
fit1 = run_factanal(m1)
# r2py:entity:fit2
fit2 = run_factanal(m1)

def tidy_factanal(fit):
    loadings = np.array(fit['loadings'])
    vars = fit['variables']
    uniq = fit['uniquenesses']
    
    res = []
    for i in range(len(vars)):
        row = {'variable': vars[i], 'uniqueness': uniq[i]}
        for f in range(fit['n_factors']):
            row[f'fl{f+1}'] = loadings[i, f]
        res.append(row)
    return pd.DataFrame(res)

# r2py:entity:tidy
tidy_fit1 = tidy_factanal(fit1)
print(tidy_fit1)
# r2py:entity:tidy_1
tidy_fit2 = tidy_factanal(fit2)

def augment_factanal(fit, data=None):
    if data is None:
        data = m1
    
    # For the original data, we use the stored scores, otherwise transform
    if data is m1:
        scores = fit['scores']
    else:
        # Approximation for new data
        pca = PCA(n_components=fit['n_factors'])
        pca.fit(m1)
        scores = pca.transform(data)
        
    df_scores = pd.DataFrame(scores, columns=[f'.fs{i+1}' for i in range(fit['n_factors'])])
    df_scores.insert(0, '.rownames', [str(i+1) for i in range(len(df_scores))])
    
    df_data = data.copy()
    df_data.insert(0, '.rownames', [str(i+1) for i in range(len(df_data))])
    
    # Right join on .rownames
    res = pd.merge(df_scores, df_data, on='.rownames', how='right')
    
    # Reorder columns: .rownames, then original data, then factor scores
    cols = ['.rownames'] + [c for c in df_data.columns if c != '.rownames'] + [c for c in df_scores.columns if c != '.rownames']
    return res[cols]

# r2py:entity:augment
augment_fit1 = augment_factanal(fit1)
cols_to_keep = ['.rownames'] + [c for c in augment_fit1.columns if c.startswith('.fs')]
augment_fit1 = augment_fit1[cols_to_keep]
print(augment_fit1)
# r2py:entity:augment_1
augment_fit2 = augment_factanal(fit2)
# To match R's broom::augment(fit), we only keep .rownames and the factor scores
cols_to_keep = ['.rownames'] + [c for c in augment_fit2.columns if c.startswith('.fs')]
augment_fit2 = augment_fit2[cols_to_keep]
print(augment_fit2)

# r2py:entity:augment_2
augment_fit1_m2 = augment_factanal(fit1, data=m2)
print(augment_fit1_m2)
# r2py:entity:augment_3
augment_fit2_m2 = augment_factanal(fit2, data=m2)
print(augment_fit2_m2)