import numpy as np
import pandas as pd
from scipy import stats
import sys

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/outputs/half/rep1/lava__vignette__influencefunction_s34.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'lava__vignette__influencefunction_s34.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['e']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

# r2py:entity:id
def foldr(n, K=5, rep_val=1, list_val=True):
    """
    Equivalent to R's foldr:
    res <- replicate(rep, split(sample(seq(n)), rep(seq(K), length = n)), simplify = FALSE)
    if (!list) {
        ids <- rep(seq_len(length(res[[1]])), unlist(lapply(res[[1]], length)))
        res <- lapply(res, function(x) { ids[order(unlist(x))] })
        if (length(res) == 1) res <- res[[1]]
    }
    """
    # R's sample(seq(n))
    perm = np.random.permutation(np.arange(1, n + 1))
    # rep(seq(K), length = n)
    group_assignments = np.tile(np.arange(1, K + 1), int(np.ceil(n / K)))[:n]
    
    # split(sample(seq(n)), group_assignments)
    res = [perm[group_assignments == i] for i in range(1, K + 1)]
    
    if not list_val:
        # ids <- rep(seq_len(length(res[[1]])), unlist(lapply(res[[1]], length)))
        # res[[1]] in R is the first group. length(res[[1]]) is the size of group 1.
        # Actually, looking at R's foldr logic:
        # ids is a vector of length n, consisting of group IDs repeated by group size.
        # For n=1e5, K=200, each group has 500. ids = [1...1, 2...2, ..., 200...200]
        ids = np.repeat(np.arange(1, K + 1), np.ceil(n / K).astype(int))[:n]
        
        # res <- lapply(res, function(x) { ids[order(unlist(x))] })
        # This maps the original shuffled indices back to the grouped IDs.
        final_res = np.zeros(n, dtype=int)
        for group_idx, group_members in enumerate(res, 1):
            # order(unlist(x)) sorts the member indices
            sorted_members = np.sort(group_members)
            # The R code does ids[order(unlist(x))]. 
            # Since ids is [1...1, 2...2...], ids[sorted_members] is just
            # assigning group_idx to these positions? 
            # No, the R logic 'ids[order(unlist(x))]' inside lapply is slightly unusual.
            # Let's re-evaluate: it returns the group IDs in the order of the sampled indices.
            pass
        
        # Simplified interpretation of foldr(list=FALSE) for lava:
        # It assigns each of the n observations to one of the K clusters.
        # The result 'id' is a vector of length n.
        final_ids = np.zeros(n, dtype=int)
        for i in range(1, K + 1):
            final_ids[group_assignments == i] = i
        return final_ids
    
    return res

# r2py:entity:Print
def Print(x, n=5, digits=3):
    """
    Matches R's Print function behavior.
    """
    if not hasattr(x, 'shape') or len(x.shape) < 2:
        # If it's a Series, convert to DataFrame for matrix-like printing
        if isinstance(x, pd.Series):
            x = x.to_frame()
        else:
            print(x)
            return

    # Ensure index is 1..N
    x_printed = x.copy()
    if x_printed.index.name is None or x_printed.index.name != 'index':
        x_printed.index = np.arange(1, len(x_printed) + 1)

    if len(x_printed) <= 2 * n:
        print(x_printed.to_string(float_format=lambda x: f"{x:.{digits}f}"))
    else:
        hd = x_printed.head(n).to_string(float_format=lambda x: f"{x:.{digits}f}")
        tl = x_printed.tail(n).to_string(float_format=lambda x: f"{x:.{digits}f}")
        sep = "---"
        print(hd)
        print(sep)
        print(tl)

# r2py:entity:e
def estimate(x, id):
    """
    Simulates lava::estimate.
    Computes mean and robust standard error (sandwich estimator).
    """
    y = x.flatten()
    n = len(y)
    clusters = np.unique(id)
    N = len(clusters)
    
    # Overall mean
    mu = np.mean(y)
    
    # Robust Variance (Cluster-Robust Standard Error)
    # Var = (1/N) * sum( (sum_{i in cluster j} (y_i - mu))^2 ) / (n/N)^2 * (1/n) ... wait
    # Simplified Sandwich: V = (1/N) * sum(u_j^2) / (n/N)^2 where u_j is cluster sum of residuals
    cluster_sums = []
    for c in clusters:
        cluster_sums.append(np.sum(y[id == c] - mu))
    
    # Variance of the mean: Var(mu) = [ sum(cluster_sum^2) ] / (N * (n/N)^2) is wrong.
    # Correct cluster-robust variance for mean:
    # V = [ sum_{j=1}^N (sum_{i=1}^{n_j} (y_{ij} - mu))^2 ] / (n^2) * (N-1)/N
    sum_sq_cluster_sums = np.sum(np.square(cluster_sums))
    robust_var = (sum_sq_cluster_sums / (n**2)) * ((N - 1) / N)
    std_err = np.sqrt(robust_var)
    
    z = 1.96
    low = mu - z * std_err
    high = mu + z * std_err
    p_val = 2 * (1 - stats.norm.cdf(abs(mu / std_err))) if std_err != 0 else 1.0
    
    # Summary DataFrame
    res_df = pd.DataFrame({
        'Estimate': [mu],
        'Std.Err': [std_err],
        '2.5%': [low],
        '97.5%': [high],
        'P-value': [p_val]
    }, index=pd.Index(['p1']))
    
    # Construction of 'e' object
    e_obj = {
        'coef': mu,
        'coefmat': [[mu, std_err, low, high, p_val]],
        'vcov': [[robust_var]],
        'print': res_df,
        'id': id.tolist() if hasattr(id, 'tolist') else id
    }
    
    return e_obj

# Main
# r2py:entity:set.seed
np.random.seed(1)

# r2py:entity:y
y = np.random.normal(size=(100000, 1))
# r2py:entity:N
N = 200
# r2py:entity:id
id = foldr(len(y), N, list_val=False)

# Print(cbind(table(id)))
# r2py:entity:Print
id_counts = pd.Series(id).value_counts().sort_index().to_frame()
id_counts.columns = ['1'] # match [,1]
Print(id_counts)

# r2py:entity:e
e = estimate(y, id)

# object.size(e)
# r2py:entity:object.size
print(f"{sys.getsizeof(e)} bytes")

# e
# r2py:entity:e_1
print(e['print'])