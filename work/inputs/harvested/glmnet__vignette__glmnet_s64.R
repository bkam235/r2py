# r2py crawler metadata
# package: glmnet
# source_type: vignette
# topic: glmnet_s64
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\glmnet\doc\glmnet.R
# lines: 5

suppressPackageStartupMessages(library(glmnet))
sparsity <- function(fraction = 0.7) {
  function(x, ...) which(colMeans(x == 0) > fraction)
}
sparsity(0.5)