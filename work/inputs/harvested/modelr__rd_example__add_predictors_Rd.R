# r2py crawler metadata
# package: modelr
# source_type: rd_example
# topic: add_predictors.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\modelr\help
# lines: 9

suppressPackageStartupMessages(library(modelr))
f <- lhs ~ rhs
add_predictors(f, ~var1, ~var2)

# Left-hand sides are ignored:
add_predictors(f, lhs1 ~ var1, lhs2 ~ var2)

# fun can also be set to a function like "*":
add_predictors(f, ~var1, ~var2, fun = "*")