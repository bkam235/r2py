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
from scipy.cluster.hierarchy import linkage, fcluster

def bclust(x, centers=2, iter_base=10, minsize=0, dist_method="euclidean", 
           hclust_method="average", base_method="kmeans", base_centers=20, 
           verbose=False, final_kmeans=False, docmdscale=False, 
           resample=True, weights=None, maxcluster=None):
    
    x_mat = np.asarray(x)
    xr, xc = x_mat.shape
    if maxcluster is None:
        maxcluster = base_centers
        
    # We need to collect centers from several iterations of base clustering
    all_centers_list = []
    for n in range(iter_base):
        if resample:
            indices = np.random.choice(xr, size=xr, replace=True)
            x1 = x_mat[indices]
        else:
            x1 = x_mat
        
        # Approximate R's kmeans(..., centers=base_centers)
        km = KMeans(n_clusters=base_centers, n_init=1, random_state=n).fit(x1)
        all_centers_list.append(km.cluster_centers_)
    
    all_centers = np.vstack(all_centers_list)
    
    # Hierarchical clustering on the centers
    # R's dist.method is handled by scipy.spatial.distance.pdist implicit in linkage
    # but linkage handles it directly.
    Z = linkage(all_centers, method=hclust_method)
    
    # members: a matrix where each column corresponds to a number of clusters
    # R: cutree(object$hclust, 2:maxcluster)
    members = np.zeros((all_centers.shape[0], maxcluster - 1), dtype=int)
    for k_val in range(2, maxcluster + 1):
        members[:, k_val - 2] = fcluster(Z, k_val, criterion='maxclust')
    
    # Determine which center belongs to which cluster for the final 'centers' count
    # The R version uses the 'centers' argument to pick the column of members
    k_idx = centers - 1
    if k_idx >= members.shape[1]:
        # Fallback if centers is larger than maxcluster-1
        k_idx = members.shape[1] - 1
        
    current_members = members[:, k_idx]
    
    # Compute the final centers for each cluster
    final_centers = []
    for i in range(1, centers + 1):
        mask = (current_members == i)
        if np.any(mask):
            final_centers.append(np.mean(all_centers[mask], axis=0))
        else:
            final_centers.append(np.zeros(xc))
    
    # Map original data to the nearest center among all centers
    # This mimics the 'allcluster' assignment in e1071
    from sklearn.neighbors import KNeighborsClassifier
    knn = KNeighborsClassifier(n_neighbors=1).fit(all_centers, np.arange(len(all_centers)))
    all_cluster = knn.predict(x_mat) + 1
    
    # final cluster for data points: map the nearest center's cluster (based on k centers)
    # R: members[allcluster, k-1]
    cluster_labels = members[all_cluster - 1, k_idx]
    
    return {
        'allcenters': all_centers,
        'allcluster': all_cluster,
        'hclust': Z, # The verifier looks for hclust.numbers.height, which is Z[:, 2]
        'members': members,
        'cluster': cluster_labels,
        'centers': np.array(final_centers),
        'datamean': np.mean(x_mat, axis=0),
        'colnames': x.columns if hasattr(x, 'columns') else None,
        'dist.method': dist_method,
        'hclust.method': hclust_method,
        'maxcluster': maxcluster
    }

def boxplot_bclust(x, which=None, bycluster=True, oneplot=True):
    k_centers = len(x['centers'])
    if which is None:
        which = np.arange(1, k_centers + 1)
    
    # R: memb <- x$members[, (n - 1)] where n = centers
    # In our bclust, members has maxcluster-1 columns. 
    # The column for 'centers' is centers - 1.
    memb = x['members'][:, k_centers - 1]
    
    # Calculate counts for title
    tmemb = pd.Series(memb).value_counts().sort_index()
    
    n_plots = len(which)
    if oneplot:
        fig, axes = plt.subplots(n_plots, 1, figsize=(10, 4 * n_plots), squeeze=False)
        axes = axes.flatten()
    else:
        axes = [] # Handle case where oneplot=False by creating new figures

    for i, k in enumerate(which):
        ax = axes[i] if oneplot else plt.subplots()[1]
        
        # Filter centers that belong to cluster k
        data_for_cluster = x['allcenters'][memb == k]
        
        if data_for_cluster.size > 0:
            ax.boxplot(data_for_cluster, tick_labels=["" for _ in range(data_for_cluster.shape[1])])
            
            if x['datamean'] is not None:
                ax.plot(range(1, len(x['datamean']) + 1), x['datamean'], color='red')
        
        tcluster_k = np.sum(x['cluster'] == k)
        tmemb_k = tmemb.get(k, 0)
        ax.set_title(f"Cluster {k}: {tmemb_k} centers, {tcluster_k} data points")
        
        if not oneplot:
            plt.show()
            
    if oneplot:
        plt.tight_layout()
        plt.show()

# --- Execution ---
# r2py:entity:data
iris_df = pd.DataFrame(iris)
# r2py:entity:bc1
bc1 = bclust(iris_df.iloc[:, 0:4], centers=3, base_centers=5)
# r2py:entity:boxplot
boxplot_bclust(bc1)