# r2py crawler metadata
# package: vctrs
# source_type: vignette
# topic: s3-vector_chunk80
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\vctrs\doc\s3-vector.Rmd
# lines: 12

suppressPackageStartupMessages(library(vctrs))
#' @export
vec_ptype2.vctrs_percent.vctrs_percent <- function(x, y, ...) new_percent()
#' @export
vec_ptype2.double.vctrs_percent <- function(x, y, ...) double()

#' @export
vec_cast.pizza_percent.pizza_percent <- function(x, to, ...) x
#' @export
vec_cast.pizza_percent.double <- function(x, to, ...) percent(x)
#' @export
vec_cast.double.pizza_percent <- function(x, to, ...) vec_data(x)