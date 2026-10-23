# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 20

import pandas as pd
import numpy as np

# r2py:entity:x
x = [1, 2, 1, 4, 3]
# r2py:entity:y
y = [2, 5, 5, 1]

# Set operations for lists
# r2py:entity:vec_set_intersect
set_x = set(x)
set_y = set(y)

print(list(set_x.intersection(set_y)))
# r2py:entity:vec_set_difference
print(list(set_x.difference(set_y)))
# r2py:entity:vec_set_union
print(list(set_x.union(set_y)))
# r2py:entity:vec_set_symmetric_difference
print(list(set_x.symmetric_difference(set_y)))

# r2py:entity:x_1
x_df = pd.DataFrame({
    'a': [2, 3, 2, 2],
    'b': ['j', 'k', 'j', 'l']
})
# r2py:entity:y_1
y_df = pd.DataFrame({
    'a': [1, 2, 2, 2, 3],
    'b': ['j', 'l', 'j', 'l', 'j']
})

# For DataFrames, we drop duplicates to treat them as sets of rows
# r2py:entity:vec_set_intersect_1
x_uniq = x_df.drop_duplicates()
y_uniq = y_df.drop_duplicates()

# Intersection
print(pd.merge(x_uniq, y_uniq, how='inner'))

# r2py:entity:vec_set_difference_1
# Difference (x - y)
print(x_uniq[~x_uniq.apply(tuple, 1).isin(y_uniq.apply(tuple, 1))])

# r2py:entity:vec_set_union_1
# Union
print(pd.concat([x_uniq, y_uniq]).drop_duplicates())

# r2py:entity:vec_set_symmetric_difference_1
# Symmetric Difference
combined = pd.concat([x_uniq, y_uniq])
print(combined[combined.duplicated(keep=False)].drop_duplicates())

# r2py:entity:x_2
x_named = {'a': 1, 'b': 2, 'c': 2, 'd': 3}
# r2py:entity:y_2
y_named = {'c': 2, 'b': 1, 'a': 3, 'd': 3}

# r2py:entity:vec_set_intersect_2
# Intersection of named vectors (comparing key-value pairs)
intersect_named = {k: v for k, v in x_named.items() if k in y_named and y_named[k] == v}
print(intersect_named)

# r2py:entity:x_3
x_df_named = pd.DataFrame({'name': list(x_named.keys()), 'value': list(x_named.values())})
# r2py:entity:y_3
y_df_named = pd.DataFrame({'name': list(y_named.keys()), 'value': list(y_named.values())})

# r2py:entity:vec_set_intersect_3
print(pd.merge(x_df_named, y_df_named, how='inner'))