# r2py crawler metadata
# package: glmnet
# source_type: vignette
# topic: glmnetFamily_s3
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\glmnet\doc\glmnetFamily.R
# lines: 4

suppressPackageStartupMessages(library(glmnet))
set.seed(1)
x <- matrix(rnorm(500), ncol = 5)
y <- rowSums(x[, 1:2]) + rnorm(100)