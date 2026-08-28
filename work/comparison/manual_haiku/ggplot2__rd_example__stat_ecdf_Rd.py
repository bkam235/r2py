# r2py crawler metadata
# package: ggplot2
# source_type: rd_example
# topic: stat_ecdf.Rd
# Translated from R to Python

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

# Create sample data with two groups
np.random.seed(1)
df = pd.DataFrame({
    'x': np.concatenate([np.random.normal(0, 3, 100),
                         np.random.normal(0, 10, 100)]),
    'g': np.repeat(['1', '2'], 100)
})

# Create figure with subplots
fig, axes = plt.subplots(2, 2, figsize=(12, 10))

# Plot 1: ECDF with step geom
ax = axes[0, 0]
x_sorted = np.sort(df['x'])
ecdf = np.arange(1, len(x_sorted) + 1) / len(x_sorted)
ax.step(x_sorted, ecdf, where='post')
ax.set_xlabel('x')
ax.set_ylabel('ECDF')
ax.set_title('ECDF (step)')

# Plot 2: ECDF without padding to infinity
ax = axes[0, 1]
x_sorted = np.sort(df['x'])
ecdf = np.arange(1, len(x_sorted) + 1) / len(x_sorted)
ax.step(x_sorted, ecdf, where='post')
ax.set_xlim(x_sorted[0], x_sorted[-1])  # No padding
ax.set_xlabel('x')
ax.set_ylabel('ECDF')
ax.set_title('ECDF (no padding)')

# Plot 3: Multiple ECDFs by group
ax = axes[1, 0]
for group in df['g'].unique():
    group_data = df[df['g'] == group]['x']
    x_sorted = np.sort(group_data)
    ecdf = np.arange(1, len(x_sorted) + 1) / len(x_sorted)
    ax.step(x_sorted, ecdf, where='post', label=f'Group {group}')
ax.set_xlabel('x')
ax.set_ylabel('ECDF')
ax.set_title('Multiple ECDFs')
ax.legend()

# Plot 4: Weighted ECDF
ax = axes[1, 1]
weighted = pd.DataFrame({
    'x': np.arange(1, 11),
    'weights': np.concatenate([np.arange(1, 6), np.arange(5, 0, -1)])
})
plain = pd.DataFrame({
    'x': np.repeat(weighted['x'], weighted['weights'])
})

# ECDF without weights
x_sorted = np.sort(plain['x'])
ecdf = np.arange(1, len(x_sorted) + 1) / len(x_sorted)
ax.step(x_sorted, ecdf, where='post', linewidth=1)

# ECDF with weights
x_sorted_w = np.sort(weighted['x'])
ecdf_w = np.cumsum(weighted['weights']) / weighted['weights'].sum()
ax.step(x_sorted_w, ecdf_w, where='post', linewidth=1, color='green')

ax.set_xlabel('x')
ax.set_ylabel('ECDF')
ax.set_title('Weighted ECDF')

plt.tight_layout()
plt.show()
