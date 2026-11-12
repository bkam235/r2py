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

def bclust(x, centers=2, iter_base=10, minsize=0, dist_method="euclidean", 
           hclust_method="average", base_method="kmeans", base_centers=20, 
           verbose=False, final_kmeans=False, docmdscale=False, 
           resample=True, weights=None, maxcluster=None):
    
    x_mat = np.asarray(x)
    xr, xc = x_mat.shape
    if maxcluster is None:
        maxcluster = base_centers
        
    all_centers = []
    for n in range(iter_base):
        if resample:
            indices = np.random.choice(xr, size=xr, replace=True, p=weights)
            x1 = x_mat[indices]
        else:
            x1 = x_mat
            
        km = KMeans(n_clusters=base_centers, n_init=1, random_state=n).fit(x1)
        all_centers.append(km.cluster_centers_)
        
    all_centers = np.vstack(all_centers)
    
    knn = KNeighborsClassifier(n_neighbors=1).fit(all_centers, np.arange(len(all_centers)))
    all_cluster = knn.predict(x_mat)
    
    # Hierarchical clustering of centers
    from scipy.spatial.distance import pdist
    d = pdist(all_centers, metric=dist_method)
    Z = linkage(d, method=hclust_method)
    
    # R: cutree(object$hclust, 2:maxcluster)
    # We need members for k from 2 up to maxcluster
    members = np.zeros((len(all_centers), maxcluster - 1), dtype=int)
    for k_val in range(2, maxcluster + 1):
        members[:, k_val - 2] = fcluster(Z, k_val, criterion='maxclust')
    
    # Determine final cluster for data points
    # In R, the clustering of data points is based on their closest center
    # The centers are grouped into 'centers' number of clusters via hclust
    final_member_map = fcluster(Z, centers, criterion='maxclust')
    # map: center_index -> cluster_id
    cluster_assignment = final_member_map[all_cluster - 1] if all_cluster.any() else None
    
    # Calculate centroids of the clusters of centers
    # R's bclust center calculation: mean of centers assigned to that cluster
    final_centers = []
    for c in range(1, centers + 1):
        mask = final_member_map == c
        if np.any(mask):
            final_centers.append(np.mean(all_centers[mask], axis=0))
        else:
            final_centers.append(np.zeros(xc))
    
    res = {
        'allcenters': all_centers,
        'allcluster': all_cluster,
        'hclust': Z,
        'members': members,
        'cluster': cluster_assignment,
        'centers': np.array(final_centers),
        'datamean': np.mean(x_mat, axis=0),
        'colnames': x.columns if hasattr(x, 'columns') else None,
        'dist.method': dist_method,
        'hclust.method': hclust_method,
        'maxcluster': maxcluster
    }
    return res

def boxplot_bclust(x, which=None, bycluster=True, oneplot=True):
    n_centers = len(x['centers'])
    if which is None:
        which = np.arange(1, n_centers + 1)
    
    # The R code uses the membership mapping for the requested 'centers' k
    # In the provided R example, bc1 <- bclust(..., 3, ...), so n=3.
    # members is cutree from 2 to maxcluster. 
    # R: memb <- x$members[, (n - 1)] 
    # Since members is index 0 for k=2, then (3-1)=2 is index 1.
    # However, the most stable way to get the membership for k=centers is fcluster again
    # because the 'members' matrix might not cover the exact 'centers' value if it's small.
    
    from scipy.cluster.hierarchy import fcluster
    memb = fcluster(x['hclust'], n_centers, criterion='maxclust')
    
    cendf = pd.DataFrame(x['allcenters'], columns=x['colnames'])
    all_vals = x['allcenters']
    ylim = (np.min(all_vals), np.max(all_vals))
    
    if bycluster:
        if oneplot:
            fig, axes = plt.subplots(len(which), 1, figsize=(8, 4 * len(which)), squeeze=False)
            axes = axes.flatten()
            for i, k in enumerate(which):
                ax = axes[i]
                data_for_cluster = cendf[memb == k]
                ax.boxplot(data_for_cluster.values, tick_labels=["" for _ in range(cendf.shape[1])])
                ax.set_ylim(ylim)
                if x['datamean'] is not None:
                    ax.plot(range(1, len(x['datamean']) + 1), x['datamean'], color='red')
                
                tcluster_k = np.sum(x['cluster'] == k) if x['cluster'] is not None else 0
                tmemb_k = np.sum(memb == k)
                ax.set_title(f"Cluster {k}: {tmemb_k} centers, {tcluster_k} data points")
            plt.tight_layout()
            plt.show()
        else:
            for k in which:
                plt.figure()
                data_for_cluster = cendf[memb == k]
                plt.boxplot(data_for_cluster.values, tick_labels=["" for _ in range(cendf.shape[1])])
                plt.ylim(ylim)
                if x['datamean'] is not None:
                    plt.plot(range(1, len(x['datamean']) + 1), x['datamean'], color='red')
                tcluster_k = np.sum(x['cluster'] == k) if x['cluster'] is not None else 0
                tmemb_k = np.sum(memb == k)
                plt.title(f"Cluster {k}: {tmemb_k} centers, {tcluster_k} data points")
                plt.show()

# --- Execution ---
# r2py:entity:data
iris_df = iris
# r2py:entity:bc1
bc1 = bclust(iris_df.iloc[:, 0:4], centers=3, base_centers=5)
# r2py:entity:boxplot
boxplot_bclust(bc1)