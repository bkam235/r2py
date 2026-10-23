# r2py crawler metadata
# package: modelr
# source_type: rd_example
# topic: formulas.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\modelr\help
# lines: 14

suppressPackageStartupMessages(library(modelr))
# Provide named arguments to create a named list of formulas:
models <- formulas(~lhs,
  additive = ~var1 + var2,
  interaction = ~var1 * var2
)
models$additive

# The formulas are created sequentially, so that you can refer to
# previously created formulas:
formulas(~lhs,
  linear = ~var1 + var2,
  hierarchical = add_predictors(linear, ~(1 | group))
)