# r2py crawler metadata
# package: vctrs
# source_type: vignette
# topic: s3-vector_s76
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\vctrs\doc\s3-vector.R
# lines: 15

suppressPackageStartupMessages(library(vctrs))
#' `percent` vector
#'
#' This creates a double vector that represents percentages so when it is
#' printed, it is multiplied by 100 and suffixed with `%`.
#'
#' @param x A numeric vector
#' @return An S3 vector of class `pizza_percent`.
#' @export
#' @examples
#' percent(c(0.25, 0.5, 0.75))
percent <- function(x = double()) {
  x <- vec_cast(x, double())
  new_percent(x)
}