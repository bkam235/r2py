import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.neighbors import KNeighborsClassifier
from scipy.cluster.hierarchy import linkage, fcluster
from scipy.spatial.distance import pdist

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'e1071__rd_example__boxplot_bclust_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['iris']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

def bclust(x, centers=2, iter_base=10, minsize=0, dist_method="euclidean", 
           hclust_method="average", base_method="kmeans", base_centers=20, 
           verbose=False, final_kmeans=False, docmdscale=False, 
           resample=True, weights=None, maxcluster=None):
    
    x_mat = np.asarray(x)
    xr, xc = x_mat.shape
    if maxcluster is None:
        maxcluster = base_centers
        
    # Initialize the object structure to match R's bclust
    object_bc = {
        'allcenters': None,
        'allcluster': None,
        'hclust': None,
        'members': None,
        'cluster': None,
        'centers': None,
        'iter.base': iter_base,
        'base.centers': base_centers,
        'datamean': np.mean(x_mat, axis=0),
        'colnames': x.columns if hasattr(x, 'columns') else None,
        'dist.method': dist_method,
        'hclust.method': hclust_method,
        'maxcluster': maxcluster
    }
    
    all_centers_list = []
    for n in range(1, iter_base + 1):
        if resample:
            indices = np.random.choice(xr, size=xr, replace=True, p=weights)
            x1 = x_mat[indices]
        else:
            x1 = x_mat
            
        # R's kmeans is called with nstart=1 usually in this loop
        km = KMeans(n_clusters=base_centers, n_init=1, random_state=n).fit(x1)
        all_centers_list.append(km.cluster_centers_)
    
    all_centers = np.vstack(all_centers_list)
    object_bc['allcenters'] = all_centers
    
    # Nearest neighbor assignment of data points to the ensemble of centers
    knn = KNeighborsClassifier(n_neighbors=1).fit(all_centers, np.arange(len(all_centers)))
    object_bc['allcluster'] = knn.predict(x_mat)
    
    # Hierarchical clustering on the centers
    d = pdist(all_centers, metric=dist_method)
    Z = linkage(d, method=hclust_method)
    object_bc['hclust'] = Z
    
    # Memberships for different values of k
    # R's cutree(hclust, 2:maxcluster)
    members = np.zeros((len(all_centers), maxcluster - 1), dtype=int)
    for k_val in range(2, maxcluster + 1):
        members[:, k_val - 2] = fcluster(Z, k_val, criterion='maxclust')
    object_bc['members'] = members
    
    # Final cluster assignment for the requested 'centers' (k)
    k_idx = centers - 2 # 0-based index for the members matrix
    if k_idx < 0:
        # Handle k=1 case if necessary, though bclust typically centers >= 2
        current_members = np.ones(len(all_centers), dtype=int)
    else:
        current_members = members[:, k_idx]
        
    # Map data points to these clusters via their closest center
    # cluster[i] = members[allcluster[i]]
    object_bc['cluster'] = current_members[object_bc['allcluster']]
    
    # Compute the centers of the clusters
    cluster_centers = []
    for m in range(1, centers + 1):
        mask = current_members == m
        if np.any(mask):
            cluster_centers.append(np.mean(all_centers[mask], axis=0))
        else:
            cluster_centers.append(np.zeros(xc))
    object_bc['centers'] = np.array(cluster_centers)
    
    return object_bc

def boxplot_bclust(bc_obj, which=None, bycluster=True, oneplot=True):
    # R's boxplot.bclust usually plots the 'allcenters' that belong to each cluster
    k_requested = len(bc_obj['centers'])
    if which is None:
        which = np.arange(1, k_requested + 1)
    
    # members for the specified k
    memb = bc_obj['members'][:, k_requested - 2] if k_requested > 1 else np.ones(len(bc_obj['allcenters']), dtype=int)
    
    # Global y-axis limits based on all centers
    ylim_min = np.min(bc_obj['allcenters'])
    ylim_max = np.max(bc_obj['allcenters'])
    
    if bycluster:
        for k in which:
            # Only centers that belong to cluster k
            data_for_cluster = bc_obj['allcenters'][memb == k]
            
            plt.figure()
            plt.boxplot(data_for_cluster, tick_labels=["" for _ in range(data_for_cluster.shape[1])])
            plt.ylim(ylim_min, ylim_max)
            
            # Plot the overall mean as a red line
            if bc_obj['datamean'] is not None:
                plt.plot(range(1, len(bc_obj['datamean']) + 1), bc_obj['datamean'], color='red')
            
            # Calculate stats for title
            # tmemb: number of centers in this cluster
            tmemb_k = np.sum(memb == k)
            # tcluster: number of data points assigned to this cluster
            tcluster_k = np.sum(bc_obj['cluster'] == k)
            
            plt.title(f"Cluster {k}: {tmemb_k} centers, {tcluster_k} data points")
            plt.show()

# --- Execution ---
# r2py:entity:data
# iris is already available via data_shim

# r2py:entity:bc1
bc1 = bclust(iris.iloc[:, 0:4], centers=3, base_centers=5)

# r2py:entity:boxplot
boxplot_bclust(bc1)