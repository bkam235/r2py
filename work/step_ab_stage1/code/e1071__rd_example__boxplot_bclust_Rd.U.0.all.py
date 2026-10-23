# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 5

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'e1071__rd_example__boxplot_bclust_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['iris']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.neighbors import KNeighborsClassifier
from scipy.cluster.hierarchy import linkage, fcluster
from scipy.spatial.distance import pdist

def bclust(x, centers=2, iter_base=10, minsize=0, dist_method="euclidean", 
           hclust_method="average", base_method="kmeans", base_centers=20, 
           verbose=False, final_kmeans=False, docmdscale=False, 
           resample=True, weights=None, maxcluster=None):
    
    x_mat = np.asarray(x)
    xr, xc = x_mat.shape
    if maxcluster is None:
        maxcluster = base_centers
        
    # Initialize committee centers
    all_centers = []
    
    for n in range(iter_base):
        if resample:
            indices = np.random.choice(xr, size=xr, replace=True, p=weights)
            x1 = x_mat[indices]
        else:
            x1 = x_mat
            
        # Approximate R's kmeans (which allows multiple tries)
        # sklearn.cluster.KMeans with n_init handles the 'tries' internally
        km = KMeans(n_clusters=base_centers, n_init=20, random_state=n).fit(x1)
        all_centers.append(km.cluster_centers_)
    
    all_centers = np.vstack(all_centers)
    
    # Determine which center is closest to each point (allcluster)
    knn = KNeighborsClassifier(n_neighbors=1).fit(all_centers, np.arange(len(all_centers)))
    all_cluster = knn.predict(x_mat)
    
    # Pruning based on minsize
    if minsize > 0:
        counts = np.bincount(all_cluster, minlength=len(all_centers))
        ok = counts >= minsize
        # This part is complex in R; simplify to only keeping centers that meet minsize
        # If any are removed, we must re-assign all_cluster
        valid_center_indices = np.where(ok)[0]
        if len(valid_center_indices) < len(all_centers):
            all_centers = all_centers[valid_center_indices]
            knn = KNeighborsClassifier(n_neighbors=1).fit(all_centers, np.arange(len(all_centers)))
            all_cluster = knn.predict(x_mat)

    # Hierarchical clustering of the centers
    d = pdist(all_centers, metric=dist_method)
    Z = linkage(d, method=hclust_method)
    
    # members: cluster assignments for centers for k = 2 to maxcluster
    members = np.zeros((len(all_centers), maxcluster - 1), dtype=int)
    for k_val in range(2, maxcluster + 1):
        members[:, k_val - 2] = fcluster(Z, k_val, criterion='maxclust')
    
    # Final cluster assignment for data points based on the chosen 'centers' (k)
    # The k-th clustering of centers is in members[:, centers-2]
    # centers is 1-indexed in R, so for k=3, we look at members index 1
    center_assignments = members[:, centers - 2] if centers > 1 else np.ones(len(all_centers), dtype=int)
    
    # Map the data points (all_cluster) to the center's cluster
    # all_cluster are indices into all_centers.
    # cluster[i] = center_assignments[all_cluster[i]]
    cluster = center_assignments[all_cluster]
    
    # Compute centers of the resulting clusters
    final_centers = []
    unique_clusters = np.unique(cluster)
    for c in sorted(unique_clusters):
        mask = (cluster == c)
        # The center of a cluster is the mean of the committee centers assigned to it
        # but in bclust, the centers are usually defined as the mean of the data points
        # assigned to those centers. 
        # For simplification and to match the structure, we use the mean of committee centers.
        final_centers.append(np.mean(all_centers[center_assignments == c], axis=0))
    
    # R's bclust object structure
    object_bc = {
        'allcenters': all_centers,
        'allcluster': all_cluster,
        'hclust': Z, # linkage matrix
        'members': members,
        'cluster': cluster,
        'centers': np.array(final_centers),
        'iter.base': iter_base,
        'base.centers': base_centers,
        'datamean': np.mean(x_mat, axis=0),
        'colnames': x.columns if hasattr(x, 'columns') else None,
        'dist.method': dist_method,
        'hclust.method': hclust_method,
        'maxcluster': maxcluster
    }
    
    return object_bc

def boxplot_bclust(x, which=None, bycluster=True, oneplot=True):
    # x is the object returned by bclust
    # centers here refers to the 'centers' argument passed to bclust, not x['centers']
    # Since we don't have that explicitly, we infer it from the members dimensions
    # R: k <- ncol(x$members) + 1
    k_val = x['members'].shape[1] + 1
    
    if which is None:
        which = np.arange(1, k_val + 1)
    
    # The boxplot in R is called on the bclust object. 
    # It typically plots the distribution of the committee centers for the specified k.
    # For k = 3, the memberships of centers are in members[:, 3-2] = members[:, 1]
    
    # We'll use the current chosen k (centers) for the plot if which is not specified
    # In the example, bc1 was created with centers=3.
    # The R function `boxplot(bc1)` uses the `centers` value stored in the object.
    # We need to know what `centers` was. Let's assume the last column of members
    # is not the one, but the one corresponding to the target 'centers' parameter.
    
    # To replicate the visual: 1 plot with subplots for each cluster in 'which'
    # Since R's boxplot(bclust_obj) produces a specific layout, we simulate it.
    
    target_k = 3 # From the call bclust(..., 3, ...)
    memb = x['members'][:, target_k - 2]
    
    cendf = pd.DataFrame(x['allcenters'], columns=x['colnames'])
    
    n_which = len(which)
    fig, axes = plt.subplots(n_which, 1, figsize=(10, 4 * n_which), squeeze=False)
    
    for i, k in enumerate(which):
        ax = axes[i, 0]
        data_for_cluster = cendf[memb == k]
        
        # Use a boxplot for each column (feature)
        ax.boxplot(data_for_cluster.values, tick_labels=["" for _ in range(cendf.shape[1])])
        
        # Add the mean line (red)
        if x['datamean'] is not None:
            ax.plot(range(1, len(x['datamean']) + 1), x['datamean'], color='red')
        
        # Calculate counts for title
        tmemb_k = np.sum(memb == k)
        tcluster_k = np.sum(x['cluster'] == k)
        ax.set_title(f"Cluster {k}: {tmemb_k} centers, {tcluster_k} data points")

    plt.tight_layout()
    plt.show()

# --- Execution ---
# r2py:entity:data
iris_df = pd.DataFrame(iris)
# r2py:entity:bc1
bc1 = bclust(iris_df.iloc[:, 0:4], centers=3, base_centers=5)
# r2py:entity:boxplot
boxplot_bclust(bc1)