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

def clusters_bclust(object_bc, k, x=None):
    if x is None:
        all_cluster = object_bc['allcluster']
    else:
        knn = KNeighborsClassifier(n_neighbors=1).fit(object_bc['allcenters'], np.arange(len(object_bc['allcenters'])))
        all_cluster = knn.predict(x)
    
    return object_bc['members'][:, k - 1] # Simplified mapping

def centers_bclust(object_bc, k):
    all_centers = object_bc['allcenters']
    members = object_bc['members']
    n_cols = all_centers.shape[1]
    centers = np.zeros((k, n_cols))
    for m in range(1, k + 1):
        mask = members[:, k - 1] == m
        if np.any(mask):
            centers[m-1, :] = np.mean(all_centers[mask], axis=0)
        else:
            centers[m-1, :] = 0
    return centers

def hclust_bclust(object_bc, x, centers_val, dist_method=None, hclust_method=None, final_kmeans=False, docmdscale=False, maxcluster=None):
    if dist_method is None: dist_method = object_bc['dist.method']
    if hclust_method is None: hclust_method = object_bc['hclust.method']
    if maxcluster is None: maxcluster = object_bc['maxcluster']
    
    d = pdist(object_bc['allcenters'], metric=dist_method)
    Z = linkage(d, method=hclust_method)
    
    # R's hclust object contains 'height' (the distances at which clusters were merged)
    # In scipy.cluster.hierarchy.linkage, the height is the 4th column (index 3)
    object_bc['hclust'] = {'merge': Z, 'height': Z[:, 3]}
    
    members = np.zeros((len(object_bc['allcenters']), maxcluster - 1), dtype=int)
    for k_val in range(2, maxcluster + 1):
        members[:, k_val - 2] = fcluster(Z, k_val, criterion='maxclust')
    
    object_bc['members'] = members
    
    # The cluster assignment for the specific k requested
    # Note: R bclust assigns cluster based on distance to the computed centers
    if centers_val > 1:
        # Basic assignment based on the centers of the last hierarchical level
        # For the example, we simplify to the centers_bclust result
        curr_centers = centers_bclust(object_bc, centers_val)
        knn = KNeighborsClassifier(n_neighbors=1).fit(curr_centers, np.arange(1, centers_val + 1))
        object_bc['cluster'] = knn.predict(x)
        object_bc['centers'] = curr_centers
    
    if final_kmeans:
        km = KMeans(n_clusters=centers_val, n_init='auto').fit(x)
        object_bc['centers'] = km.cluster_centers_
        object_bc['cluster'] = km.labels_ + 1
        
    return object_bc

def prune_bclust(object_bc, x, minsize=1, dohclust=False):
    while True:
        knn = KNeighborsClassifier(n_neighbors=1).fit(object_bc['allcenters'], np.arange(len(object_bc['allcenters'])))
        object_bc['allcluster'] = knn.predict(x)
        counts = np.bincount(object_bc['allcluster'], minlength=len(object_bc['allcenters']))
        ok = counts >= minsize
        valid_indices = np.where(ok)[0]
        if len(valid_indices) == len(object_bc['allcenters']):
            break
        object_bc['allcenters'] = object_bc['allcenters'][valid_indices]
    
    if dohclust:
        object_bc = hclust_bclust(object_bc, x, len(object_bc['centers']))
    return object_bc

def bclust(x, centers=2, iter_base=10, minsize=0, dist_method="euclidean", 
           hclust_method="average", base_method="kmeans", base_centers=20, 
           verbose=False, final_kmeans=False, docmdscale=False, 
           resample=True, weights=None, maxcluster=None):
    
    x_mat = np.asarray(x)
    xr, xc = x_mat.shape
    if maxcluster is None:
        maxcluster = base_centers
        
    object_bc = {
        'allcenters': np.zeros((iter_base * base_centers, xc)),
        'allcluster': None,
        'hclust': None,
        'members': None,
        'cluster': None,
        'centers': None,
        'iter.base': iter_base,
        'base.centers': base_centers,
        'prcomp': None,
        'datamean': np.mean(x_mat, axis=0),
        'colnames': x.columns if hasattr(x, 'columns') else None,
        'dist.method': dist_method,
        'hclust.method': hclust_method,
        'maxcluster': maxcluster
    }
    
    for n in range(1, iter_base + 1):
        if resample:
            indices = np.random.choice(xr, size=xr, replace=True, p=weights)
            x1 = x_mat[indices]
        else:
            x1 = x_mat
            
        tryres = None
        for m in range(1, 21):
            try:
                km = KMeans(n_clusters=base_centers, n_init=1).fit(x1)
                tryres = km
                break
            except:
                continue
        
        if tryres is None:
            raise RuntimeError("Could not find valid cluster solution")
            
        start_idx = (n - 1) * base_centers
        end_idx = n * base_centers
        object_bc['allcenters'][start_idx:end_idx, :] = tryres.cluster_centers_
        
    mask = ~np.isnan(object_bc['allcenters']).any(axis=1)
    object_bc['allcenters'] = object_bc['allcenters'][mask]
    
    knn = KNeighborsClassifier(n_neighbors=1).fit(object_bc['allcenters'], np.arange(len(object_bc['allcenters'])))
    object_bc['allcluster'] = knn.predict(x_mat)
    
    if minsize > 0:
        object_bc = prune_bclust(object_bc, x_mat, minsize=minsize)
        
    object_bc = hclust_bclust(object_bc, x_mat, centers, final_kmeans=final_kmeans, docmdscale=docmdscale)
    
    return object_bc

def boxplot_bclust(x, which=None, bycluster=True, oneplot=True):
    # In R, the centers count is derived from the 'centers' array
    k_val = len(x['centers'])
    if which is None:
        which = np.arange(1, k_val + 1)
    
    # memb is the cluster assignment of each 'allcenter' for the requested k
    memb = x['members'][:, k_val - 1]
    
    cendf = pd.DataFrame(x['allcenters'], columns=x['colnames'])
    # Calculate global ylim across all centers
    all_vals = x['allcenters'].flatten()
    ylim = (np.min(all_vals), np.max(all_vals))
    
    N = len(which)
    if bycluster:
        if oneplot:
            fig, axes = plt.subplots(N, 1, figsize=(8, 3 * N), squeeze=False)
            axes = axes.flatten()
        
        for i, k in enumerate(which):
            ax = axes[i] if oneplot else plt.gca()
            if not oneplot: plt.figure()
            
            data_for_cluster = cendf[memb == k]
            ax.boxplot(data_for_cluster.values, tick_labels=["" for _ in range(cendf.shape[1])])
            ax.set_ylim(ylim)
            
            if x['datamean'] is not None:
                ax.plot(range(1, len(x['datamean']) + 1), x['datamean'], color='red')
            
            tcluster_k = len(x['cluster'][x['cluster'] == k]) if x['cluster'] is not None else 0
            tmemb_k = np.sum(memb == k)
            ax.set_title(f"Cluster {k}: {tmemb_k} centers, {tcluster_k} data points")
            
        if not oneplot:
            plt.show()
        else:
            plt.tight_layout()
            plt.show()
    else:
        pass

# --- Execution ---
# r2py:entity:data
iris_df = iris
# r2py:entity:bc1
bc1 = bclust(iris_df.iloc[:, 0:4], centers=3, base_centers=5)
# r2py:entity:boxplot
boxplot_bclust(bc1)