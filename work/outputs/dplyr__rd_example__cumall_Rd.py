# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 11

import pandas as pd
import numpy as np

# r2py:entity:x
x = np.array([1, 3, 5, 2, 2])

# cummean(x)
# r2py:entity:cummean
cummean_x = np.cumsum(x) / np.arange(1, len(x) + 1)
print(cummean_x)

# cumsum(x) / seq_along(x)
# r2py:entity:seq_along
cumsum_div_seq = np.cumsum(x) / np.arange(1, len(x) + 1)
print(cumsum_div_seq)

# cumall(x < 5)
# r2py:entity:cumall
cumall_x = np.cumprod((x < 5).astype(int))
print(cumall_x.astype(bool))

# cumany(x == 3)
# r2py:entity:cumany
cumany_x = np.maximum.accumulate((x == 3).astype(int))
print(cumany_x.astype(bool))

# r2py:entity:df
df = pd.DataFrame({
    'date': pd.to_datetime("2020-01-01") + pd.to_timedelta(np.arange(7), unit='D'),
    'balance': [100, 50, 25, -25, -50, 30, 120]
})

# df |> filter(cumany(balance < 0))
# r2py:entity:filter
df_filter1 = df[np.maximum.accumulate((df['balance'] < 0).astype(int)).astype(bool)]
print(df_filter1)

# df |> filter(cumall(!(balance < 0)))
# r2py:entity:filter_1
df_filter2 = df[np.cumprod((~(df['balance'] < 0)).astype(int)).astype(bool)]
print(df_filter2)