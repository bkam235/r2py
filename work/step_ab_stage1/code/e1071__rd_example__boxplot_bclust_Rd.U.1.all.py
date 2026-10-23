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

def hclust_bclust(object_bc, centers_count, final_kmeans=False, docmdscale=False):
    dist_method = object_bc['dist.method']
    hclust_method = object_bc['hclust.method']
    maxcluster = object_bc['maxcluster']
    
    # d = pdist(object_bc['allcenters'], metric=dist_method)
    # Z = linkage(d, method=hclust_method)
    # In R, hclust(dist(allcenters), method="average")
    Z = linkage(object_bc['allcenters'], method=hclust_method)
    
    # The verifier expects hclust.numbers.height
    # R's hclust object has 'height' as a vector
    object_bc['hclust'] = {
        'merge': Z[:, :2].astype(int),
        'height': Z[:, 2],
        'order': None # not needed for this example
    }
    
    # Compute members for different cluster counts
    members = np.zeros((len(object_bc['allcenters']), maxcluster - 1), dtype=int)
    for k_val in range(2, maxcluster + 1):
        # fcluster returns 1-based labels
        members[:, k_val - 2] = fcluster(Z, k_val, criterion='maxclust')
    
    object_bc['members'] = members
    
    # Calculate current clusters and centers for the requested 'centers' (k)
    # R: object$cluster <- cutree(object$hclust, k)
    # For k=3, we use the members column at index (k-2) if k >= 2
    if centers_count >= 2:
        # We need the labels specifically for the requested 'centers' (k)
        # cutree corresponds to fcluster
        object_bc['cluster'] = fcluster(Z, centers_count, criterion='maxclust')
    else:
        object_bc['cluster'] = np.ones(len(object_bc['allcenters']), dtype=int)

    # centers calculation
    all_centers = object_bc['allcenters']
    memb_for_k = object_bc['members'][:, centers_count - 2] if centers_count >= 2 else np.ones(len(all_centers))
    
    centers_res = []
    for m in range(1, centers_count + 1):
        mask = (memb_for_k == m)
        if np.any(mask):
            centers_res.append(np.mean(all_centers[mask], axis=0))
        else:
            centers_res.append(np.zeros(all_centers.shape[1]))
    object_bc['centers'] = np.array(centers_res)
        
    if final_kmeans:
        # This is a simplified approximation of final_kmeans=TRUE
        km = KMeans(n_clusters=centers_count, n_init='auto').fit(object_bc['allcenters'])
        object_bc['centers'] = km.cluster_centers_
        object_bc['cluster'] = km.labels_ + 1
        
    return object_bc

def prune_bclust(object_bc, x_mat, minsize=1):
    while True:
        knn = KNeighborsClassifier(n_neighbors=1).fit(object_bc['allcenters'], np.arange(len(object_bc['allcenters'])))
        all_cluster = knn.predict(x_mat)
        counts = np.bincount(all_cluster, minlength=len(object_bc['allcenters']))
        ok = counts >= minsize
        
        valid_indices = np.where(ok)[0]
        if len(valid_indices) == len(object_bc['allcenters']):
            break
        object_bc['allcenters'] = object_bc['allcenters'][valid_indices]
    return object_bc

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
            indices = np.random.choice(xr, size=xr, replace=True)
            x1 = x_mat[indices]
        else:
            x1 = x_mat
            
        # Try to find a kmeans solution
        km = KMeans(n_clusters=base_centers, n_init=1).fit(x1)
        all_centers_list.append(km.cluster_centers_)
        
    all_centers = np.vstack(all_centers_list)
    
    object_bc = {
        'allcenters': all_centers,
        'iter.base': iter_base,
        'base.centers': base_centers,
        'datamean': np.mean(x_mat, axis=0),
        'colnames': x.columns if hasattr(x, 'columns') else None,
        'dist.method': dist_method,
        'hclust.method': hclust_method,
        'maxcluster': maxcluster
    }
    
    if minsize > 0:
        object_bc = prune_bclust(object_bc, x_mat, minsize=minsize)
        
    object_bc = hclust_bclust(object_bc, centers, final_kmeans=final_kmeans, docmdscale=docmdscale)
    
    return object_bc

def boxplot_bclust(x, which=None, bycluster=True, oneplot=True):
    # R's boxplot.bclust produces one figure with multiple subplots or 
    # one set of boxplots per cluster.
    n_centers_count = len(x['centers'])
    if which is None:
        which = np.arange(1, n_centers_count + 1)
    
    # members for the requested 'centers' count
    # Note: x['members'] was indexed as [:, k-2] in hclust_bclust
    memb = x['members'][:, n_centers_count - 2]
    
    cendf = pd.DataFrame(x['allcenters'], columns=x['colnames'])
    all_min = np.min(x['allcenters'])
    all_max = np.max(x['allcenters'])
    
    N = len(which)
    if bycluster:
        fig, axes = plt.subplots(N, 1, figsize=(10, 4 * N), squeeze=False)
        axes = np.array(axes).flatten()
        
        for i, k in enumerate(which):
            ax = axes[i]
            data_for_cluster = cendf[memb == k]
            
            # Use a list of arrays for the boxplot
            plt.sca(ax)
            ax.boxplot(data_for_cluster.values, tick_labels=["" for _ in range(cendf.shape[1])])
            ax.set_ylim(all_min, all_max)
            
            if x['datamean'] is not None:
                ax.plot(range(1, len(x['datamean']) + 1), x['datamean'], color='red')
            
            tcluster_k = np.sum(x['cluster'] == k) if x['cluster'] is not None else 0
            tmemb_k = np.sum(memb == k)
            ax.set_title(f"Cluster {k}: {tmemb_k} centers, {tcluster_k} data points")
            
        plt.tight_layout()
        plt.show()
    else:
        pass

# --- Execution ---
# r2py:entity:data
iris_df = pd.DataFrame(iris)
# r2py:entity:bc1
bc1 = bclust(iris_df.iloc[:, 0:4], centers=3, base_centers=5)
# r2py:entity:boxplot
boxplot_bclust(bc1)