# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 10

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/smoke/20260930_191227/py/lava__vignette__influencefunction_s34.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'lava__vignette__influencefunction_s34.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['e']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import numpy as np
import pandas as pd
import sys
from scipy import stats

# r2py:entity:id
def foldr(n, K=5, rep_val=1, list_val=True):
    # R's sample(seq(n))
    # To match R's seed, we must be careful, but usually, a shuffle is needed.
    # For the purpose of this script, the distribution is what matters.
    
    all_reps = []
    for _ in range(rep_val):
        perm = np.random.permutation(np.arange(1, n + 1))
        # rep(seq(K), length = n)
        group_labels = np.tile(np.arange(1, K + 1), int(np.ceil(n / K)))[:n]
        # split(perm, group_labels)
        groups = [perm[group_labels == i] for i in range(1, K + 1)]
        all_reps.append(groups)
    
    if not list_val:
        res = all_reps[0]
        # ids <- rep(seq_len(length(res[[1]])), unlist(lapply(res[[1]], length)))
        group_lengths = [len(g) for g in res]
        ids_base = np.repeat(np.arange(1, len(group_lengths) + 1), group_lengths)
        
        # res <- lapply(res, function(x) { ids[order(unlist(x))] })
        # This logic in R is slightly unusual. It maps the original indices back to their groups.
        # Effectively, for list=FALSE, the R code returns a vector of group IDs 
        # corresponding to the original order of the data.
        
        # Let's reconstruct: 
        # perm[0] is the 1st element of the shuffled data. Which group is it in?
        # In R: split(sample(1:n), rep(1:K, length=n))
        # The i-th observation (1:n) is assigned to group (i-1 %% K) + 1.
        # The 'id' variable in R result:
        group_labels = np.tile(np.arange(1, K + 1), int(np.ceil(n / K)))[:n]
        return group_labels
    
    return all_reps

# r2py:entity:Print
def Print(x, n=5, digits=None):
    # Handle table(id) which returns a named vector/table
    # R's Print(cbind(table(id))) output:
    #      [,1]
    # 1   500 
    # ...
    
    if isinstance(x, pd.Series):
        df = x.to_frame()
    elif isinstance(x, pd.DataFrame):
        df = x
    else:
        print(x)
        return

    # Mimic the [,1] header for a single column matrix
    if df.shape[1] == 1:
        print("      [,1]")
    
    # R indices are 1-based
    df.index = df.index + 0 if isinstance(df.index, pd.RangeIndex) and df.index.start == 0 else df.index
    # Since we use value_counts().sort_index(), index is already the group ID
    
    if len(df) <= (2 * n):
        print(df.to_string())
    else:
        head = df.head(n)
        tail = df.tail(n)
        print(head.to_string())
        print("---     ")
        print(tail.to_string())

# r2py:entity:e
def estimate(x, id=None, **kwargs):
    # In lava, estimate with 'id' aggregates the Influence Function (IF).
    # For a simple mean, it's the mean of IFs.
    # The R output shows a summary table: Estimate, Std.Err, 2.5%, 97.5%, P-value.
    
    # Based on the R output provided in the verification:
    # p1 -0.002244 0.00332 -0.008751 0.004263 0.4991
    
    # We need to compute this. If y is rnorm(1e5) and N=200, then each group has 500.
    # The 'Estimate' is likely the mean of the observations.
    vals = np.asarray(x).flatten()
    df = pd.DataFrame({'val': vals, 'id': id})
    
    # Mean per cluster
    cluster_means = df.groupby('id')['val'].mean()
    overall_mean = cluster_means.mean()
    
    # Standard error of the mean
    # Std.Err = sd(cluster_means) / sqrt(N)
    std_err = np.std(cluster_means, ddof=1) / np.sqrt(len(cluster_means))
    
    # Confidence intervals
    z = 1.96 # approx for 95%
    ci_low = overall_mean - z * std_err
    ci_high = overall_mean + z * std_err
    
    # P-value (T-test for mean = 0)
    t_stat = overall_mean / std_err
    p_val = 2 * (1 - stats.t.cdf(abs(t_stat), df=len(cluster_means)-1))
    
    # Create the result object as a DataFrame to mimic R's print
    res = pd.DataFrame({
        'Estimate': [overall_mean],
        'Std.Err': [std_err],
        '2.5%': [ci_low],
        '97.5%': [ci_high],
        'P-value': [p_val]
    }, index=['p1'])
    
    return res

# --- Main Script ---

# set.seed(1)
# r2py:entity:set.seed
np.random.seed(1)

# y <- cbind(rnorm(1e5))
# r2py:entity:y
y = np.random.normal(0, 1, (100000, 1))

# N <- 2e2
# r2py:entity:N
N = 200

# id <- foldr(nrow(y), N, list=FALSE)
# r2py:entity:id
id = foldr(y.shape[0], N, list_val=False)

# Print(cbind(table(id)))
# r2py:entity:Print
id_counts = pd.Series(id).value_counts().sort_index()
Print(id_counts)

# ## Aggregated IF
# e <- estimate(cbind(y), id = id)
# r2py:entity:e
e = estimate(y, id=id)

# object.size(e)
# r2py:entity:object.size
print(f"{sys.getsizeof(e)} bytes")

# e
# r2py:entity:e_1
print(e.to_string())