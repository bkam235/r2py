# r2py crawler metadata
# package: roxygen2
# source_type: vignette
# topic: reuse_s3
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\roxygen2\doc\reuse.R
# lines: 14

suppressPackageStartupMessages(library(roxygen2))
#' Logarithms
#' 
#' @param x A numeric vector
#' @export
log <- function(x, base) ...

#' @rdname log
#' @export
log2 <- function(x) log(x, 2)

#' @rdname log
#' @export
ln <- function(x) log(x, exp(1))