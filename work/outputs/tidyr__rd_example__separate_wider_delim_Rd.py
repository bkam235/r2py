import pandas as pd
import numpy as np
import re

# Section 1
# r2py:entity:df
df = pd.DataFrame({'id': [1, 2, 3], 'x': ["m-123", "f-455", "f-123"]})

# separate_wider_delim
# r2py:entity:separate_wider_delim
split_cols = df['x'].str.split('-', expand=True)
res1 = pd.concat([df.drop(columns=['x']), split_cols], axis=1)
res1.columns = ['id', 'gender', 'unit']

# separate_wider_position
# R: separate_wider_position(x, c(gender = 1, 1, unit = 3))
# Widths: gender(1), unspecified(1), unit(3). 
# Note: The R example "c(gender = 1, 1, unit = 3)" implies 3 pieces. 
# Total length is 5. 1st char is gender, 2nd is dummy, 3rd-5th is unit.
# r2py:entity:separate_wider_position
gender = df['x'].str[0:1]
unit = df['x'].str[2:]
res2 = pd.concat([df.drop(columns=['x']), gender.rename('gender'), unit.rename('unit')], axis=1)

# separate_wider_regex
# R: c(gender = ".", ".", unit = "\\d+")
# The second "." is an unnamed capture group in R's regex logic here.
# r2py:entity:separate_wider_regex
res3_extracted = df['x'].str.extract(r'(?P<gender>.).(?P<unit>\d+)')
res3 = pd.concat([df.drop(columns=['x']), res3_extracted], axis=1)

# Section 2
# r2py:entity:df_1
df = pd.DataFrame({'var': ["race_1", "race_2", "age_bucket_1", "age_bucket_2"]})

# try(separate_wider_delim)
# r2py:entity:try
try:
    # separate_wider_delim without too_many="merge" fails if more than 2 pieces
    split_data = df['var'].str.split('_', expand=True)
    if split_data.shape[1] > 2:
        raise ValueError("Expected 2 pieces, found more")
    res4 = pd.concat([df.drop(columns=['var']), split_data], axis=1)
except Exception as e:
    # R's try() prints the error but continues
    print(f"Error caught: {e}")

# too_many = "merge"
# n=1 splits on first delimiter, effectively merging the rest into the second column
# r2py:entity:separate_wider_delim_1
split_data = df['var'].str.split('_', n=1, expand=True)
res5 = pd.concat([df.drop(columns=['var']), split_data], axis=1)
res5.columns = ['var1', 'var2']

# separate_wider_regex (greedy)
# r2py:entity:separate_wider_regex_1
res6_extracted = df['var'].str.extract(r'(?P<var1>.*)_(?P<var2>.*)')
res6 = pd.concat([df.drop(columns=['var']), res6_extracted], axis=1)

# separate_wider_regex (non-greedy)
# r2py:entity:separate_wider_regex_2
res7_extracted = df['var'].str.extract(r'(?P<var1>.*?)_(?P<var2>.*)')
res7 = pd.concat([df.drop(columns=['var']), res7_extracted], axis=1)

# Section 3
# r2py:entity:df_2
df = pd.DataFrame({'id': [1, 2, 3, 4], 'x': ["x", "x y", "x y z", np.nan]})

# separate_longer_delim
# r2py:entity:separate_longer_delim
res8 = df.assign(x=df['x'].str.split(' ')).explode('x')

# try(separate_wider_delim)
# r2py:entity:try_1
try:
    split_data = df['x'].str.split(' ', expand=True)
    # If some rows have too few pieces, separate_wider_delim fails by default
    # Check if any row has fewer than 2 pieces (excluding NAs)
    if (df['x'].str.count(' ') < 1).any():
        raise ValueError("too_few")
    res9 = pd.concat([df.drop(columns=['x']), split_data], axis=1)
except Exception as e:
    print(f"Error caught: {e}")

# too_few = "debug", too_many = "debug"
# Debug just shows the results including the problematic ones
# r2py:entity:separate_wider_delim_2
split_data = df['x'].str.split(' ', expand=True)
res10 = pd.concat([df.drop(columns=['x']), split_data], axis=1)

# too_few = "align_start", too_many = "merge"
# too_many="merge" -> n=1; too_few="align_start" -> pads with NaN at end
# r2py:entity:separate_wider_delim_3
split_data = df['x'].str.split(' ', n=1, expand=True)
res11 = pd.concat([df.drop(columns=['x']), split_data], axis=1)
res11.columns = ['id', 'a', 'b']

# names_sep = "", too_few = "align_start"
# r2py:entity:separate_wider_delim_4
split_data = df['x'].str.split(' ', expand=True)
# R's names_sep = "" with default separate_wider_delim creates "x1", "x2", etc.
# based on the column name 'x'
cols = [f'x{i+1}' for i in range(split_data.shape[1])]
split_data.columns = cols
res12 = pd.concat([df.drop(columns=['x']), split_data], axis=1)