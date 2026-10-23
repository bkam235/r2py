# r2py crawler metadata
# package: vctrs
# source_type: vignette
# topic: s3-vector_s36
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\vctrs\doc\s3-vector.R
# lines: 11

suppressPackageStartupMessages(library(vctrs))
new_rational <- function(n = integer(), d = integer()) {
  if (!is_integer(n)) {
    abort("`n` must be an integer vector.")
  }
  if (!is_integer(d)) {
    abort("`d` must be an integer vector.")
  }

  new_rcrd(list(n = n, d = d), class = "vctrs_rational")
}