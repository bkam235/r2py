# r2py crawler metadata
# package: foreach
# source_type: vignette
# topic: foreach_s24
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\foreach\doc\foreach.R
# lines: 18

suppressPackageStartupMessages(library(foreach))
iblkcol <- function(a, chunks) {
  n <- ncol(a)
  i <- 1

  nextElem <- function() {
    if (chunks <= 0 || n <= 0) stop('StopIteration')
    m <- ceiling(n / chunks)
    r <- seq(i, length=m)
    i <<- i + m
    n <<- n - m
    chunks <<- chunks - 1
    a[,r, drop=FALSE]
  }

  structure(list(nextElem=nextElem), class=c('iblkcol', 'iter'))
}
nextElem.iblkcol <- function(obj) obj$nextElem()