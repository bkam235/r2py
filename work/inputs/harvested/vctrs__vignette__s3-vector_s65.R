# r2py crawler metadata
# package: vctrs
# source_type: vignette
# topic: s3-vector_s65
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\vctrs\doc\s3-vector.R
# lines: 8

suppressPackageStartupMessages(library(vctrs))
vec_math.vctrs_cached_sum <- function(.fn, .x, ...) {
  switch(.fn,
    sum = attr(.x, "sum"),
    mean = attr(.x, "sum") / length(.x),
    vec_math_base(.fn, .x, ...)
  )
}