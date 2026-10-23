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
        
    # Initialize result object
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
            # Simplified weights handling
            p = weights if weights is not None else None
            indices = np.random.choice(xr, size=xr, replace=True, p=p)
            x1 = x_mat[indices]
        else:
            x1 = x_mat
            
        # Try to fit KMeans (up to 20 attempts as per R source)
        tryres = None
        for m in range(1, 21):
            try:
                km = KMeans(n_clusters=base_centers, n_init=1, random_state=m).fit(x1)
                tryres = km.cluster_centers_
                break
            except:
                continue
        
        if tryres is None:
            raise RuntimeError("Could not find valid cluster solution")
        all_centers_list.append(tryres)
        
    all_centers = np.vstack(all_centers_list)
    object_bc['allcenters'] = all_centers
    
    # allcluster: which center is closest to each point in x
    knn = KNeighborsClassifier(n_neighbors=1).fit(all_centers, np.arange(len(all_centers)))
    object_bc['allcluster'] = knn.predict(x_mat) + 1 # 1-based
    
    # Hierarchical clustering of centers
    d = pdist(all_centers, metric=dist_method)
    Z = linkage(d, method=hclust_method)
    object_bc['hclust'] = Z # This contains the heights in the 3rd column
    
    # members: cluster assignment for each center for k in 2:maxcluster
    members = np.zeros((len(all_centers), maxcluster - 1), dtype=int)
    for k_val in range(2, maxcluster + 1):
        members[:, k_val - 2] = fcluster(Z, k_val, criterion='maxclust')
    object_bc['members'] = members
    
    # Final clustering for the requested 'centers' (which is 'k' in R's bclust)
    # R uses: object$members[, centers - 1]
    # members is 0-indexed, and we want the (centers-1)-th column if centers >= 2
    if centers < 2:
        # Special case for 1 cluster, but usually centers >= 2
        bc_cluster_assignment = np.ones(len(all_centers), dtype=int)
    else:
        # centers-1 is the index for the k-th cluster set in members
        # But members was filled from k=2 to maxcluster.
        # So k=2 is index 0, k=3 is index 1... k=centers is index centers-2
        bc_cluster_assignment = members[:, centers - 2]
    
    # Assign each observation to a cluster based on the closest center's cluster
    # R: object$cluster <- object$members[object$allcluster, centers-1]
    # Python: members[allcluster-1, centers-2]
    object_bc['cluster'] = members[object_bc['allcluster'] - 1, centers - 2] if centers >= 2 else np.ones(xr, dtype=int)
    
    # Calculate centers of the final clusters
    centers_final = np.zeros((centers, xc))
    for m_idx in range(1, centers + 1):
        mask = (bc_cluster_assignment == m_idx)
        if np.any(mask):
            centers_final[m_idx-1, :] = np.mean(all_centers[mask], axis=0)
    object_bc['centers'] = centers_final
    
    return object_bc

def boxplot_bclust(x, which=None, bycluster=True, oneplot=True):
    # x is the result of bclust
    # R's boxplot(bc1) by default uses the current 'centers' value (k)
    # The number of clusters is determined by the length of x['centers']
    k_val = len(x['centers'])
    if which is None:
        which = np.arange(1, k_val + 1)
    
    # Membership of centers for the k_val-th clustering
    # R: memb <- x$members[, k_val - 1]
    # In our Python, members index for k_val is k_val - 2
    if k_val >= 2:
        memb = x['members'][:, k_val - 2]
    else:
        memb = np.ones(len(x['allcenters']), dtype=int)
        
    cendf = pd.DataFrame(x['allcenters'], columns=x['colnames'])
    
    # Set overall ylim based on all centers
    all_vals = x['allcenters'].flatten()
    ylim = (np.min(all_vals), np.max(all_vals))
    
    if bycluster and oneplot:
        plt.figure(figsize=(10, 6))
        # We need to group boxplots by cluster and then by variable
        # Each cluster has 'xc' variables.
        xc = cendf.shape[1]
        all_data_to_plot = []
        labels = []
        
        for k in which:
            cluster_mask = (memb == k)
            cluster_data = cendf[cluster_mask].values # (n_centers_in_k, xc)
            
            # For each variable in the cluster
            for var_idx in range(xc):
                all_data_to_plot.append(cluster_data[:, var_idx])
                labels.append(f"C{k} V{var_idx+1}")
        
        plt.boxplot(all_data_to_plot)
        plt.ylim(ylim)
        plt.xticks(range(1, len(all_data_to_plot) + 1), labels, rotation=90)
        
        if x['datamean'] is not None:
            # The red line in R is the global mean of the original data
            # It's drawn across the plot. We need to replicate the point for each group.
            mean_vals = x['datamean']
            # In R, the red line is actually a line connecting the means of the variables
            # across the boxplots.
            # For each cluster k, plot the mean vector.
            for k in which:
                # Calculate shift to align with the boxplots for cluster k
                offset = (which.tolist().index(k)) * xc
                plt.plot(np.arange(offset + 1, offset + xc + 1), mean_vals, color='red')
        
        plt.title(f"Boxplot of centers for bclust (k={k_val})")
        plt.show()

# --- Execution ---
# r2py:entity:data
iris_df = iris # iris is provided by the data shim

# r2py:entity:bc1
# R: bc1 <- bclust(iris[,1:4], 3, base.centers=5)
bc1 = bclust(iris_df.iloc[:, 0:4], centers=3, base_centers=5)

# r2py:entity:boxplot
# R: boxplot(bc1)
boxplot_bclust(bc1)