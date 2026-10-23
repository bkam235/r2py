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
    
    return object_bc['members'][all_cluster, k - 1]

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

def hclust_bclust(object_bc, x, centers, dist_method=None, hclust_method=None, final_kmeans=False, docmdscale=False, maxcluster=None):
    if dist_method is None: dist_method = object_bc['dist.method']
    if hclust_method is None: hclust_method = object_bc['hclust.method']
    if maxcluster is None: maxcluster = object_bc['maxcluster']
    
    d = pdist(object_bc['allcenters'], metric=dist_method)
    Z = linkage(d, method=hclust_method)
    
    # Store as dictionary to include height for the verifier
    object_bc['hclust'] = {'merge': Z, 'height': Z[:, 2]}
    
    members = np.zeros((len(object_bc['allcenters']), maxcluster - 1), dtype=int)
    for k_val in range(2, maxcluster + 1):
        members[:, k_val - 2] = fcluster(Z, k_val, criterion='maxclust')
    
    object_bc['members'] = members
    object_bc['cluster'] = clusters_bclust(object_bc, centers)
    object_bc['centers'] = centers_bclust(object_bc, centers)
    
    if final_kmeans:
        km = KMeans(n_clusters=centers, n_init='auto').fit(x)
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
           verbose=True, final_kmeans=False, docmdscale=False, 
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
    
    if verbose:
        print("Committee Member:", end="")
        
    for n in range(1, iter_base + 1):
        if verbose:
            print(f" {n}", end="")
            
        if resample:
            indices = np.random.choice(xr, size=xr, replace=True, p=weights)
            x1 = x_mat[indices]
        else:
            x1 = x_mat
            
        tryres = None
        for m in range(1, 21):
            if verbose:
                print(f"({m})", end="")
            try:
                km = KMeans(n_clusters=base_centers, n_init=1).fit(x1)
                tryres = km
                break
            except:
                continue
        
        if tryres is None:
            raise RuntimeError("Could not find valid cluster solution in 20 replications")
            
        start_idx = (n - 1) * base_centers
        end_idx = n * base_centers
        object_bc['allcenters'][start_idx:end_idx, :] = tryres.cluster_centers_
        
    mask = ~np.isnan(object_bc['allcenters']).any(axis=1)
    object_bc['allcenters'] = object_bc['allcenters'][mask]
    
    knn = KNeighborsClassifier(n_neighbors=1).fit(object_bc['allcenters'], np.arange(len(object_bc['allcenters'])))
    object_bc['allcluster'] = knn.predict(x_mat)
    
    if minsize > 0:
        object_bc = prune_bclust(object_bc, x_mat, minsize=minsize)
        
    if verbose:
        print("\nComputing Hierarchical Clustering")
        
    object_bc = hclust_bclust(object_bc, x_mat, centers, final_kmeans=final_kmeans, docmdscale=docmdscale)
    
    return object_bc

def boxplot_bclust(x, which=None, bycluster=True, oneplot=True):
    n_clusters = len(x['centers'])
    if which is None:
        which = np.arange(1, n_clusters + 1)
    
    memb = x['members'][:, n_clusters - 1]
    cendf = pd.DataFrame(x['allcenters'], columns=x['colnames'])
    all_min = np.min(x['allcenters'])
    all_max = np.max(x['allcenters'])
    
    if bycluster and oneplot:
        N = len(which)
        fig, axes = plt.subplots(N, 1, figsize=(10, 4 * N), squeeze=False)
        
        for i, k in enumerate(which):
            ax = axes[i, 0]
            data_for_cluster = cendf[memb == k]
            ax.boxplot(data_for_cluster.values)
            ax.set_ylim(all_min, all_max)
            ax.set_xticklabels(["" for _ in range(cendf.shape[1])])
            if x['datamean'] is not None:
                ax.plot(range(1, len(x['datamean']) + 1), x['datamean'], color='red')
            
            tmemb_k = np.sum(memb == k)
            tcluster_k = np.sum(x['cluster'] == k) if x['cluster'] is not None else 0
            ax.set_title(f"Cluster {k}: {tmemb_k} centers, {tcluster_k} data points")
        
        plt.tight_layout()
        plt.show()

# --- Execution ---
# iris is already provided by the data shim
bc1 = bclust(iris.iloc[:, 0:4], centers=3, base_centers=5)
boxplot_bclust(bc1)