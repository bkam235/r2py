# r2py crawler metadata
# package: vctrs
# source_type: vignette
# topic: s3-vector_s30
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\vctrs\doc\s3-vector.R
# lines: 17

suppressPackageStartupMessages(library(vctrs))
new_cached_sum <- function(x = double(), sum = 0L) {
  if (!is_double(x)) {
    abort("`x` must be a double vector.")
  }
  if (!is_double(sum)) {
    abort("`sum` must be a double vector.")
  }
  vec_check_size(sum, size = 1L)

  new_vctr(x, sum = sum, class = "vctrs_cached_sum")
}

cached_sum <- function(x) {
  x <- vec_cast(x, double())
  new_cached_sum(x, sum(x))
}