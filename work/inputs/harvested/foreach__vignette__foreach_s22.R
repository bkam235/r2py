# r2py crawler metadata
# package: foreach
# source_type: vignette
# topic: foreach_s22
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\foreach\doc\foreach.R
# lines: 6

suppressPackageStartupMessages(library(foreach))
applyKernel <- function(newX, FUN, d2, d.call, dn.call=NULL, ...) {
  foreach(i=1:d2) %dopar%
    FUN(array(newX[,i], d.call, dn.call), ...)
}
applyKernel(matrix(1:16, 4), mean, 4, 4)