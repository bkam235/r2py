# r2py crawler metadata
# package: roxygen2
# source_type: vignette
# topic: roxygen2_s3
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\roxygen2\doc\roxygen2.R
# lines: 12

suppressPackageStartupMessages(library(roxygen2))
#' Add together two numbers
#'
#' @param x A number.
#' @param y A number.
#' @return A number.
#' @examples
#' add(1, 1)
#' add(10, 1)
add <- function(x, y) {
  x + y
}