import pandas as pd
import numpy as np

# suppressPackageStartupMessages(library(dplyr))
# Handled by imports

# r2py:entity:rescale01
def rescale01(x):
    # rng <- range(x, na.rm = TRUE)
    # (x - rng[1]) / (rng[2] - rng[1])
    rng = np.nanmin(x), np.nanmax(x)
    return (x - rng[0]) / (rng[1] - rng[0])

# df <- tibble(x = 1:4, y = rnorm(4))
# r2py:entity:df
df = pd.DataFrame({
    'x': np.arange(1, 5),
    'y': np.random.randn(4)
})

# df |> mutate(across(where(is.numeric), rescale01))
# In Python/pandas, we select numeric columns and apply the function
# r2py:entity:mutate
numeric_cols = df.select_dtypes(include=[np.number]).columns
df_res = df.copy()
df_res[numeric_cols] = df[numeric_cols].apply(rescale01)

# The R code auto-prints the result of the pipeline
print(df_res)