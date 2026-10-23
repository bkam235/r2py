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
            x_sample = x_mat[indices]
        else:
            x_sample = x_mat
            
        # Try up to 20 times to find a valid clustering
        km = None
        for m in range(20):
            try:
                # n_init=1 to mimic R's kmeans(..., nstart=1) behavior per iteration
                km = KMeans(n_clusters=base_centers, n_init=1, random_state=m).fit(x_sample)
                break
            except:
                continue
        
        if km is None:
            raise RuntimeError("Could not find valid cluster solution")
        all_centers_list.append(km.cluster_centers_)
        
    all_centers = np.vstack(all_centers_list)
    
    # Assign each observation to the nearest center (allcluster)
    from sklearn.neighbors import KNeighborsClassifier
    knn = KNeighborsClassifier(n_neighbors=1).fit(all_centers, np.arange(len(all_centers)))
    all_cluster = knn.predict(x_mat)
    
    # Hierarchical clustering of all_centers
    dist_matrix = pdist(all_centers, metric=dist_method)
    Z = linkage(dist_matrix, method=hclust_method)
    
    # Cut tree for levels 2 to maxcluster
    members = np.zeros((len(all_centers), maxcluster - 1), dtype=int)
    for k_val in range(2, maxcluster + 1):
        members[:, k_val - 2] = fcluster(Z, k_val, criterion='maxclust')
    
    # Current cluster assignments based on the requested 'centers' (k)
    # In R: members[, k-1]. Since members is 0-indexed, and k is 1-based
    k_idx = centers - 1
    member_assignments = members[:, k_idx]
    
    # Final cluster assignment for the data: mapping all_cluster to the clusters of their centers
    # all_cluster indices are 0-based center indices.
    # members is also 0-based center indices.
    cluster = member_assignments[all_cluster]
    
    # Calculate cluster centers
    final_centers = []
    for m in range(1, centers + 1):
        mask = (member_assignments == m)
        if np.any(mask):
            final_centers.append(np.mean(all_centers[mask], axis=0))
        else:
            final_centers.append(np.zeros(xc))
    
    res = {
        'allcenters': all_centers,
        'allcluster': all_cluster + 1, # 1-based to match R
        'hclust': Z,
        'members': members,
        'cluster': cluster,
        'centers': np.array(final_centers),
        'datamean': np.mean(x_mat, axis=0),
        'colnames': x.columns if hasattr(x, 'columns') else None,
        'dist.method': dist_method,
        'hclust.method': hclust_method,
        'maxcluster': maxcluster
    }
    
    return res

def boxplot_bclust(bc_obj, which=None, bycluster=True, oneplot=True):
    centers_count = len(bc_obj['centers'])
    if which is None:
        which = np.arange(1, centers_count + 1)
    
    # members mapping for the k-th clustering (where k = centers)
    # members is (n_centers, maxcluster-1). The index is centers - 1
    k_idx = centers_count - 1
    memb = bc_obj['members'][:, k_idx]
    
    cendf = pd.DataFrame(bc_obj['allcenters'], columns=bc_obj['colnames'])
    
    # Global y-axis limits
    ylim_min = np.min(bc_obj['allcenters'])
    ylim_max = np.max(bc_obj['allcenters'])
    
    if bycluster:
        # R's boxplot(bclust_obj) typically produces a set of boxplots per cluster
        for k in which:
            plt.figure()
            # Subset centers that belong to cluster k
            cluster_data = cendf[memb == k]
            
            plt.boxplot(cluster_data.values, tick_labels=["" for _ in range(cendf.shape[1])])
            plt.ylim(ylim_min, ylim_max)
            
            # Draw the mean line
            if bc_obj['datamean'] is not None:
                plt.plot(range(1, len(bc_obj['datamean']) + 1), bc_obj['datamean'], color='red')
            
            # Count data points assigned to this cluster
            tcluster_k = np.sum(bc_obj['cluster'] == k)
            tmemb_k = np.sum(memb == k)
            plt.title(f"Cluster {k}: {tmemb_k} centers, {tcluster_k} data points")
            plt.show()

# --- Execution ---
# r2py:entity:data
iris_df = iris

# r2py:entity:bc1
# R: bc1 <- bclust(iris[,1:4], 3, base.centers=5)
bc1 = bclust(iris_df.iloc[:, 0:4], centers=3, base_centers=5)

# r2py:entity:boxplot
boxplot_bclust(bc1)