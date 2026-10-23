import pandas as pd
import numpy as np

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/outputs/dplyr__rd_example__mutate_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'dplyr__rd_example__mutate_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['starwars']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

# Initialize starwars as DataFrame from shim
starwars = pd.DataFrame(starwars)

# Newly created variables are available immediately
# starwars |> select(name, mass) |> mutate(mass2 = mass * 2, mass2_squared = mass2 * mass2)
# r2py:entity:select
res1 = starwars[['name', 'mass']].copy()
# r2py:entity:mutate
res1['mass2'] = res1['mass'] * 2
res1['mass2_squared'] = res1['mass2'] * res1['mass2']
print(res1)

# As well as adding new variables, you can use mutate() to remove variables and modify existing variables.
# starwars |> select(name, height, mass, homeworld) |> mutate(mass = NULL, height = height * 0.0328084)
# r2py:entity:select_1
res2 = starwars[['name', 'height', 'mass', 'homeworld']].copy()
# r2py:entity:mutate_1
res2 = res2.drop(columns=['mass'])
res2['height'] = res2['height'] * 0.0328084
print(res2)

# Use across() with mutate() to apply a transformation to multiple columns in a tibble.
# starwars |> select(name, homeworld, species) |> mutate(across(!name, as.factor))
# r2py:entity:select_2
res3 = starwars[['name', 'homeworld', 'species']].copy()
# r2py:entity:mutate_2
cols_to_factor = [col for col in res3.columns if col != 'name']
res3[cols_to_factor] = res3[cols_to_factor].astype('category')
print(res3)

# Window functions are useful for grouped mutates:
# starwars |> select(name, mass, homeworld) |> group_by(homeworld) |> mutate(rank = min_rank(desc(mass)))
# r2py:entity:select_3
res4 = starwars[['name', 'mass', 'homeworld']].copy()
# r2py:entity:mutate_3
res4['rank'] = res4.groupby('homeworld')['mass'].rank(method='min', ascending=False).astype('Int64')
print(res4)

# By default, new columns are placed on the far right.
# r2py:entity:df
df = pd.DataFrame({'x': [1], 'y': [2]})
# df |> mutate(z = x + y)
# r2py:entity:mutate_4
res5_1 = df.assign(z = df['x'] + df['y'])
print(res5_1)
# df |> mutate(z = x + y, .before = 1)
# r2py:entity:mutate_5
res5_2 = df.assign(z = df['x'] + df['y'])
cols5_2 = ['z'] + [c for c in res5_2.columns if c != 'z']
res5_2 = res5_2[cols5_2]
print(res5_2)
# df |> mutate(z = x + y, .after = x)
# r2py:entity:mutate_6
res5_3 = df.assign(z = df['x'] + df['y'])
cols5_3 = list(res5_3.columns)
z_idx = cols5_3.index('z')
val = cols5_3.pop(z_idx)
cols5_3.insert(cols5_3.index('x') + 1, val)
res5_3 = res5_3[cols5_3]
print(res5_3)

# By default, mutate() keeps all columns from the input data.
# r2py:entity:df_1
df = pd.DataFrame({'x': [1], 'y': [2], 'a': ["a"], 'b': ["b"]})
# df |> mutate(z = x + y, .keep = "all")
# r2py:entity:mutate_7
res6_1 = df.assign(z = df['x'] + df['y'])
print(res6_1)
# df |> mutate(z = x + y, .keep = "used")
# r2py:entity:mutate_8
res6_2 = df[['x', 'y']].assign(z = df['x'] + df['y'])
print(res6_2)
# df |> mutate(z = x + y, .keep = "unused")
# r2py:entity:mutate_9
res6_3 = df.drop(columns=['x', 'y']).assign(z = df['x'] + df['y'])
print(res6_3)
# df |> mutate(z = x + y, .keep = "none")
# r2py:entity:mutate_10
res6_4 = df.assign(z = df['x'] + df['y'])[['z']]
print(res6_4)

# Grouping ----------------------------------------
# The following normalises `mass` by the global average:
# r2py:entity:select_4
res7 = starwars[['name', 'mass', 'species']].copy()
# r2py:entity:mutate_11
res7['mass_norm'] = res7['mass'] / res7['mass'].mean()
print(res7)

# Whereas this normalises `mass` by the averages within species levels:
# r2py:entity:select_5
res8 = starwars[['name', 'mass', 'species']].copy()
# r2py:entity:mutate_12
res8['mass_norm'] = res8.groupby('species')['mass'].transform(lambda x: x / x.mean())
print(res8)

# Indirection ----------------------------------------
# r2py:entity:vars
vars = ["mass", "height"]
# mutate(starwars, prod = .data[[vars[[1]]]] * .data[[vars[[2]]]])
# r2py:entity:mutate_13
res9 = starwars.assign(prod = starwars[vars[0]] * starwars[vars[1]])
print(res9)