# r2py crawler metadata
# package: recipes
# source_type: rd_example
# topic: summary.recipe.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\recipes\help
# lines: 7

suppressPackageStartupMessages(library(recipes))
rec <- recipe(~., data = USArrests)
summary(rec)
rec <- step_pca(rec, all_numeric(), num_comp = 3)
summary(rec) # still the same since not yet trained
rec <- prep(rec, training = USArrests)
summary(rec)