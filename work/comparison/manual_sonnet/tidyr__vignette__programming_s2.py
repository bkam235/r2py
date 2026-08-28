# r2py crawler metadata
# package: tidyr
# source_type: vignette
# topic: programming_s2
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\tidyr\doc\programming.R
# lines: 4

import pandas as pd
from sklearn.datasets import load_iris

iris_data = load_iris()
iris = pd.DataFrame(iris_data.data, columns=["Sepal.Length", "Sepal.Width", "Petal.Length", "Petal.Width"])
iris["Species"] = pd.Categorical.from_codes(iris_data.target, iris_data.target_names)

# nest(data = !Species): group by Species, nest all other columns into a "data" sub-dataframe
nested = (
    iris.groupby("Species", observed=True)
    .apply(lambda x: x.drop(columns="Species").reset_index(drop=True), include_groups=False)
    .reset_index(name="data")
)
print(nested)
