# r2py crawler metadata
# package: vctrs
# source_type: vignette
# topic: s3-vector_s74
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\vctrs\doc\s3-vector.R
# lines: 7

suppressPackageStartupMessages(library(vctrs))
new_percent <- function(x = double()) {
  if (!is_double(x)) {
    abort("`x` must be a double vector.")
  }
  new_vctr(x, class = "pizza_percent")
}