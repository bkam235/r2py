# r2py crawler metadata
# package: vctrs
# source_type: vignette
# topic: s3-vector_s55
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\vctrs\doc\s3-vector.R
# lines: 9

suppressPackageStartupMessages(library(vctrs))
poly <- function(...) {
  x <- vec_cast_common(..., .to = integer())
  x <- new_poly(x)
  new_rcrd(list(data = x), class = "vctrs_poly")
}
format.vctrs_poly <- function(x, ...) {
  format(field(x, "data"))
}