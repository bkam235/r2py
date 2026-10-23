# r2py crawler metadata
# package: glmnet
# source_type: vignette
# topic: glmnet_s66
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\glmnet\doc\glmnet.R
# lines: 17

suppressPackageStartupMessages(library(glmnet))
uvar <- function(x, means = FALSE) {
  # if means = TRUE, the means and variances are returned, 
  # otherwise just the variances
  m <- colMeans(x)
  n <- nrow(x)
  x <- x - outer(rep(1,n),m)
  v <- colSums(x^2) / (n - 1)
  if (means) list(mean = m, var = v) else v
}

vfilter <- function(q = 0.3) {
  function(x,...) {
    v <- uvar(x)
    which(v < quantile(v, q))
  }
}