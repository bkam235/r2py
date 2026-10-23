# r2py crawler metadata
# package: foreach
# source_type: vignette
# topic: foreach_s21
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\foreach\doc\foreach.R
# lines: 10

suppressPackageStartupMessages(library(foreach))
applyKernel <- function(newX, FUN, d2, d.call, dn.call=NULL, ...) {
  ans <- vector("list", d2)
  for(i in 1:d2) {
    tmp <- FUN(array(newX[,i], d.call, dn.call), ...)
    if(!is.null(tmp)) ans[[i]] <- tmp
  }
  ans
}
applyKernel(matrix(1:16, 4), mean, 4, 4)