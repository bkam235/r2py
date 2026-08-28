# r2py crawler metadata
# package: tidyr
# source_type: vignette
# topic: programming_s2
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\tidyr\doc\programming.R
# lines: 4

import statsmodels.api as sm
import pandas as pd

iris = sm.datasets.get_rdataset("iris").data

nested = iris.groupby("Species").apply(
    lambda df: df.drop(columns="Species").reset_index(drop=True)
)
print(nested)
