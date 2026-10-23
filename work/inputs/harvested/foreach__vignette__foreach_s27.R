# r2py crawler metadata
# package: foreach
# source_type: vignette
# topic: foreach_s27
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\foreach\doc\foreach.R
# lines: 14

suppressPackageStartupMessages(library(foreach))
qsort <- function(x) {
  n <- length(x)
  if (n == 0) {
    x
  } else {
    p <- sample(n, 1)
    smaller <- foreach(y=x[-p], .combine=c) %:% when(y <= x[p]) %do% y
    larger  <- foreach(y=x[-p], .combine=c) %:% when(y >  x[p]) %do% y
    c(qsort(smaller), x[p], qsort(larger))
  }
}

qsort(runif(12))