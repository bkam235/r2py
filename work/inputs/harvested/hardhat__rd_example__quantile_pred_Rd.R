# r2py crawler metadata
# package: hardhat
# source_type: rd_example
# topic: quantile_pred.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\hardhat\help
# lines: 14

suppressPackageStartupMessages(library(hardhat))
.pred_quantile <- quantile_pred(matrix(rnorm(20), 5), c(.2, .4, .6, .8))

unclass(.pred_quantile)

# Access the underlying information
extract_quantile_levels(.pred_quantile)

# Matrix format
as.matrix(.pred_quantile)

# Tidy format
library(tibble)
as_tibble(.pred_quantile)