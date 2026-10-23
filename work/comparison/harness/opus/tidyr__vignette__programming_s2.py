# Translated from <R script> by r2py v0.3.0
# Model: claude-opus-4-6  ScriptMap entities: 2

import pandas as pd
import warnings
warnings.filterwarnings('ignore')

iris = pd.read_csv("https://raw.githubusercontent.com/mwaskom/seaborn-data/master/iris.csv")
iris.columns = ['Sepal.Length', 'Sepal.Width', 'Petal.Length', 'Petal.Width', 'Species']

# r2py:entity:nest
nested_dict = {species: group.drop(columns='Species').reset_index(drop=True) for species, group in iris.groupby('Species', sort=False)}

result = pd.DataFrame({
    'Species': list(nested_dict.keys()),
    'data': list(nested_dict.values())
})

# Print in R tibble style
print(f"# A tibble: {len(result)} \u00d7 {len(result.columns)}")

# Column header
species_values = result['Species'].tolist()
max_species_len = max(len(str(s)) for s in species_values)
max_species_len = max(max_species_len, len('Species'))

print(f"  {'Species':<{max_species_len}} {'data':<17}")
print(f"  {'<fct>':<{max_species_len}} {'<list>':<17}")

for i, row in result.iterrows():
    df = row['data']
    nrow = len(df)
    ncol = len(df.columns)
    data_repr = f"<tibble [{nrow} \u00d7 {ncol}]>"
    print(f"{i+1} {str(row['Species']):<{max_species_len}} {data_repr:<17}")