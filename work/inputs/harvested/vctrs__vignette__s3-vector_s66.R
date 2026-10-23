# r2py crawler metadata
# package: vctrs
# source_type: vignette
# topic: s3-vector_s66
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\vctrs\doc\s3-vector.R
# lines: 17

suppressPackageStartupMessages(library(vctrs))
new_meter <- function(x) {
  stopifnot(is.double(x))
  new_vctr(x, class = "vctrs_meter")
}

format.vctrs_meter <- function(x, ...) {
  paste0(format(vec_data(x)), " m")
}

meter <- function(x) {
  x <- vec_cast(x, double())
  new_meter(x)
}

x <- meter(1:10)
x