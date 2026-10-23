# r2py crawler metadata
# package: glmnet
# source_type: vignette
# topic: glmnet_s67
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\glmnet\doc\glmnet.R
# lines: 18

suppressPackageStartupMessages(library(glmnet))
ut.test <- function(x, y, s0 = 0) {
  ni <- table(y); n <- sum(ni)
  if(length(ni) != 2) stop("Only two-sample t-test here")
  index <- seq(n)
  mv <- tapply(index, y, function(i, x) uvar(x[i, ], means = TRUE), x = x)
  ss <- ((ni[1] - 1) * mv[[1]]$var  + (ni[2] - 1) * mv[[2]]$var)
  sd <- sqrt(ss * (1 / ni[[1]] + 1 / ni[[2]]) / (n - 2))
  numer <- mv[[1]]$mean - mv[[2]]$mean
  numer / (sd + s0)
}

tfilter <- function(q = 0.3, s0 = 0) {
  function(x, y, ...) {
    abs_tstats <- abs(ut.test(x, y, s0 = s0))
    which(abs_tstats < quantile(abs_tstats, q))
  }
}