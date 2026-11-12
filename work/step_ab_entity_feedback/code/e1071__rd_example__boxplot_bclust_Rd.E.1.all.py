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
    
    all_centers = np.vstack(all_centers_list)
    
    # KNN to assign original data to the closest center
    knn = KNeighborsClassifier(n_neighbors=1).fit(all_centers, np.arange(len(all_centers)))
    all_cluster = knn.predict(x_mat)
    
    # Hierarchical clustering on centers
    d = pdist(all_centers, metric=dist_method)
    Z = linkage(d, method=hclust_method)
    
    # In R, hclust objects have a 'height' attribute
    hclust_obj = {'merge': Z, 'height': Z[:, 2]}
    
    # Cut tree for various levels
    members = np.zeros((len(all_centers), maxcluster - 1), dtype=int)
    for k_val in range(2, maxcluster + 1):
        members[:, k_val - 2] = fcluster(Z, k_val, criterion='maxclust')
    
    # For the specific 'centers' requested:
    # The 'cluster' assignment for the original data points
    current_members = members[:, centers - 2] if centers > 1 else np.ones(len(all_centers), dtype=int)
    # Map original data points (all_cluster) to the final clusters
    cluster_assignment = current_members[all_cluster]
    
    # Compute cluster centers as means of the centers assigned to that cluster
    final_centers = []
    for c in range(1, centers + 1):
        mask = current_members == c
        if np.any(mask):
            final_centers.append(np.mean(all_centers[mask], axis=0))
        else:
            final_centers.append(np.zeros(xc))
    
    return {
        'allcenters': all_centers,
        'allcluster': all_cluster,
        'hclust': hclust_obj,
        'members': members,
        'cluster': cluster_assignment,
        'centers': np.array(final_centers),
        'datamean': np.mean(x_mat, axis=0),
        'colnames': x.columns if hasattr(x, 'columns') else None,
        'dist.method': dist_method,
        'hclust.method': hclust_method,
        'maxcluster': maxcluster
    }

def boxplot_bclust(x, which=None, bycluster=True, oneplot=True):
    # The number of clusters is defined by the length of the 'centers' array
    n_clusters = len(x['centers'])
    if which is None:
        which = np.arange(1, n_clusters + 1)
    
    # R's boxplot.bclust uses members[, n-1] where n is the number of clusters
    # In our 0-indexed 'members', it's index [:, centers-2]
    memb = x['members'][:, n_clusters - 2] if n_clusters > 1 else np.ones(x['members'].shape[0], dtype=int)
    
    cendf = pd.DataFrame(x['allcenters'], columns=x['colnames'])
    y_min = np.min(x['allcenters'])
    y_max = np.max(x['allcenters'])
    
    if oneplot:
        plt.figure(figsize=(10, 6))
        # We create one plot and place boxplots side by side
        # For each cluster k in 'which', we plot the distribution of its centers across the 4 variables
        all_data = []
        all_labels = []
        
        for k in which:
            cluster_centers = cendf[memb == k]
            # R boxplots for bclust are organized by cluster, then by variable
            all_data.append(cluster_centers.values)
            
        # Flattening the data to plot them sequentially
        # R's boxplot(bc1) creates a set of boxplots for each variable for each cluster
        # We will use a custom approach to mirror the visual of 4 boxplots per cluster
        combined_data = [cluster_centers.values for k in which if (memb == k).any()]
        
        # To mimic R's layout:
        # We plot the centers for each variable, grouped by cluster
        # In Python's plt.boxplot, we can pass a list of arrays
        # We want: [Cluster1_Var1, Cluster1_Var2, Cluster1_Var3, Cluster1_Var4, Cluster2_Var1, ...]
        plot_data = []
        for k in which:
            cluster_centers = cendf[memb == k]
            for col in range(cendf.shape[1]):
                plot_data.append(cluster_centers.iloc[:, col].values)
        
        plt.boxplot(plot_data)
        plt.ylim(y_min, y_max)
        
        # Red line for overall mean
        # R plots the mean of the original data across the variables
        # The x-axis positions for the means are 1, 5, 9... (every 4th box)
        means = x['datamean']
        for i, m in enumerate(means):
            # The mean for variable i should be plotted across all clusters
            # But R usually just draws one set of mean lines or specific markers
            # a simple way is to plot a line through the means of the variables
            pass
        
        # R's boxplot.bclust actually plots a red line for the global mean of the original data
        # x-coords: 1, 2, 3, 4... then repeat for each cluster? 
        # No, it's one red line for the variables, repeated for each cluster or a single line.
        # Let's approximate by drawing the mean of variables 1-4.
        # The positions of the variables are 1, 2, 3, 4 in cluster 1, etc.
        for c_idx in range(len(which)):
            plt.plot(np.arange(c_idx*4 + 1, c_idx*4 + 5), means, color='red', linewidth=1)

        plt.title("Boxplots of Centers")
        plt.show()
    else:
        # Individual plots
        for k in which:
            plt.figure()
            data_for_cluster = cendf[memb == k]
            plt.boxplot(data_for_cluster.values)
            plt.ylim(y_min, y_max)
            plt.plot(range(1, 5), means, color='red')
            plt.title(f"Cluster {k}")
            plt.show()

# --- Execution ---
# iris is provided by the shim
iris_data = iris.iloc[:, 0:4]
bc1 = bclust(iris_data, centers=3, base_centers=5)
boxplot_bclust(bc1)