import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# To match R's rnorm behavior exactly for verification, 
# we should ensure the seed or data is consistent, but the script uses random values.
# We use a fixed seed to try and stabilize, though R and NumPy RNGs differ.
# r2py:entity:stocks
np.random.seed(42) 
stocks = pd.DataFrame({
    'time': [datetime(2009, 1, 1) + timedelta(days=i) for i in range(10)],
    'X': np.random.normal(0, 1, 10),
    'Y': np.random.normal(0, 2, 10),
    'Z': np.random.normal(0, 4, 10)
})
print(stocks.to_string(index=False))

# gather(stock, price, -time)
# r2py:entity:gather
stocksm = stocks.melt(id_vars=['time'], var_name='stock', value_name='price')

# stocksm |> spread(stock, price)
# In R, spread(stock, price) uses the remaining columns as the index.
# r2py:entity:spread
res_spread1 = stocksm.pivot(index='time', columns='stock', values='price').reset_index()
res_spread1.columns.name = None
print(res_spread1.to_string(index=False))

# stocksm |> spread(time, price)
# r2py:entity:spread_1
res_spread2 = stocksm.pivot(index='stock', columns='time', values='price').reset_index()
res_spread2.columns.name = None
print(res_spread2.to_string(index=False))

# Spread and gather are complements
# r2py:entity:df
df = pd.DataFrame({'x': ["a", "b"], 'y': [3, 4], 'z': [5, 6]})

# df |> spread(x, y)
# x is the key, y is the value. z is the implicit id.
# r2py:entity:spread_2
res_spread3 = df.pivot(index='z', columns='x', values='y')

# gather("x", "y", a:b, na.rm = TRUE)
# This gathers columns 'a' and 'b' into 'x' and 'y'.
# r2py:entity:gather_1
res_gather = res_spread3.reset_index().melt(id_vars=['z'], var_name='x', value_name='y').dropna()
# The R code gather("x", "y", a:b) means a:b are the columns to pivot. 
# The 'z' column is dropped because it wasn't specified in the gather range.
res_gather = res_gather[['x', 'y']]
print(res_gather.to_string(index=False))

# Use 'convert = TRUE' to produce variables of mixed type
# r2py:entity:df_1
df_mixed = pd.DataFrame({
    'row': np.repeat([1, 51], 3),
    'var': np.tile(["Sepal.Length", "Species", "Species_num"], 2),
    'value': [5.1, "setosa", 1, 7.0, "versicolor", 2]
})

# df |> spread(var, value) |> str()
# r2py:entity:spread_3
res_no_conv = df_mixed.pivot(index='row', columns='var', values='value').reset_index()
res_no_conv.columns.name = None
# r2py:entity:str
print(res_no_conv.info())

# df |> spread(var, value, convert = TRUE) |> str()
# r2py:entity:spread_4
res_conv = df_mixed.pivot(index='row', columns='var', values='value').reset_index()
res_conv.columns.name = None
# convert=TRUE in tidyr is like infer_objects() + cast.
# pandas' convert_dtypes() handles the "convert=TRUE" logic.
res_conv = res_conv.infer_objects().convert_dtypes()
# r2py:entity:str_1
print(res_conv.info())