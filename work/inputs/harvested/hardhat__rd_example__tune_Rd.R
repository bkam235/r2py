# r2py crawler metadata
# package: hardhat
# source_type: rd_example
# topic: tune.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\hardhat\help
# lines: 13

suppressPackageStartupMessages(library(hardhat))
if (rlang::is_installed(c("recipes"))) (if (getRversion() >= "3.4") withAutoprint else force)({ # examplesIf
tune()
tune("your name here")

# In practice, `tune()` is used alongside recipes or parsnip to mark
# specific arguments for tuning
library(recipes)

recipe(mpg ~ ., data = mtcars) |>
  step_normalize(all_numeric_predictors()) |>
  step_pca(all_numeric_predictors, num_comp = tune())
}) # examplesIf