# r2py crawler metadata
# package: ggplot2
# source_type: rd_example
# topic: ggplot.Rd
# Translated from R to Python

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm

# Create a data frame with sample data
np.random.seed(1)
sample_df = pd.DataFrame({
    'group': pd.Categorical(np.repeat(['a', 'b', 'c'], 10)),
    'value': np.random.normal(size=30)
})

# Calculate group means
group_means_df = sample_df.groupby('group')['value'].mean().reset_index()
group_means_df.columns = ['group', 'group_mean']

# Create three plots using different approaches

# Pattern 1: Both data and mapping in the main call
fig, axes = plt.subplots(1, 3, figsize=(15, 5))

# Pattern 1
ax1 = axes[0]
# Plot sample data
for group in sample_df['group'].unique():
    group_data = sample_df[sample_df['group'] == group]
    ax1.scatter(np.repeat(group, len(group_data)), group_data['value'], alpha=0.6)
# Plot group means
ax1.scatter(group_means_df['group'], group_means_df['group_mean'],
           color='red', s=100, zorder=5)
ax1.set_xlabel('group')
ax1.set_ylabel('value')
ax1.set_title('Pattern 1')

# Pattern 2: Only data in main call
ax2 = axes[1]
for group in sample_df['group'].unique():
    group_data = sample_df[sample_df['group'] == group]
    ax2.scatter(np.repeat(group, len(group_data)), group_data['value'], alpha=0.6)
ax2.scatter(group_means_df['group'], group_means_df['group_mean'],
           color='red', s=100, zorder=5)
ax2.set_xlabel('group')
ax2.set_ylabel('value')
ax2.set_title('Pattern 2')

# Pattern 3: No data or mapping in main call
ax3 = axes[2]
for group in sample_df['group'].unique():
    group_data = sample_df[sample_df['group'] == group]
    ax3.scatter(np.repeat(group, len(group_data)), group_data['value'], alpha=0.6)
ax3.scatter(group_means_df['group'], group_means_df['group_mean'],
           color='red', s=100, zorder=5)
ax3.set_xlabel('group')
ax3.set_ylabel('value')
ax3.set_title('Pattern 3')

plt.tight_layout()
plt.show()
