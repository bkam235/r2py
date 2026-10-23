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
        
    all_centers_list = []
    
    for n in range(iter_base):
        if resample:
            indices = np.random.choice(xr, size=xr, replace=True, p=weights)
            x1 = x_mat[indices]
        else:
            x1 = x_mat
            
        km = KMeans(n_clusters=base_centers, n_init=1, random_state=n).fit(x1)
        all_centers_list.append(km.cluster_centers_)
        
    allcenters = np.vstack(all_centers_list)
    
    # Mapping data to centers
    knn = KNeighborsClassifier(n_neighbors=1).fit(allcenters, np.arange(len(allcenters)))
    allcluster = knn.predict(x_mat)
    
    # Hierarchical clustering of centers
    d = pdist(allcenters, metric=dist_method)
    Z = linkage(d, method=hclust_method)
    
    # Generate members for clusters from 1 to maxcluster
    members = np.zeros((len(allcenters), maxcluster), dtype=int)
    for k_val in range(1, maxcluster + 1):
        # fcluster returns 1-based labels
        members[:, k_val-1] = fcluster(Z, k_val, criterion='maxclust')
    
    # For the requested 'centers' number of clusters
    # R: members[, centers]
    current_members = members[:, centers-1]
    
    # Calculate centers for these clusters
    cluster_centers = []
    for m in range(1, centers + 1):
        mask = (current_members == m)
        if np.any(mask):
            cluster_centers.append(np.mean(allcenters[mask], axis=0))
        else:
            cluster_centers.append(np.zeros(xc))
    
    # Assign data points to the centers of the final clusters
    final_centers_mat = np.array(cluster_centers)
    knn_final = KNeighborsClassifier(n_neighbors=1).fit(final_centers_mat, np.arange(1, centers + 1))
    cluster = knn_final.predict(x_mat)
    
    return {
        'allcenters': allcenters,
        'allcluster': allcluster,
        'hclust': Z,
        'members': members,
        'cluster': cluster,
        'centers': final_centers_mat,
        'datamean': np.mean(x_mat, axis=0),
        'colnames': x.columns if hasattr(x, 'columns') else None
    }

def boxplot_bclust(bc_obj, which=None, bycluster=True, oneplot=True):
    centers_count = len(bc_obj['centers'])
    if which is None:
        which = np.arange(1, centers_count + 1)
    
    # R uses (n-1) index because members is 1-based in R, but we stored it 0-indexed for k
    # The 'centers' requested is the index in the members array
    n_requested = centers_count
    memb = bc_obj['members'][:, n_requested - 1]
    
    all_centers = bc_obj['allcenters']
    col_names = bc_obj['colnames']
    datamean = bc_obj['datamean']
    
    # Global y-limits
    ylim_min = np.min(all_centers)
    ylim_max = np.max(all_centers)
    
    for k in which:
        plt.figure()
        # Indices where the cluster is k
        mask = (memb == k)
        data_for_cluster = all_centers[mask]
        
        plt.boxplot(data_for_cluster, tick_labels=["" for _ in range(all_centers.shape[1])])
        plt.ylim(ylim_min, ylim_max)
        
        if datamean is not None:
            plt.plot(range(1, len(datamean) + 1), datamean, color='red')
        
        # Calculate stats for title
        tmemb_k = np.sum(mask)
        tcluster_k = np.sum(bc_obj['cluster'] == k)
        plt.title(f"Cluster {k}: {tmemb_k} centers, {tcluster_k} data points")
        plt.show()

# --- Execution ---
# r2py:entity:bc1
bc1 = bclust(iris.iloc[:, 0:4], centers=3, base_centers=5)
# r2py:entity:boxplot
boxplot_bclust(bc1)