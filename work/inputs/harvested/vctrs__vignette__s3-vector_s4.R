# r2py crawler metadata
# package: vctrs
# source_type: vignette
# topic: s3-vector_s4
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\vctrs\doc\s3-vector.R
# lines: 5

suppressPackageStartupMessages(library(vctrs))
percent <- function(x = double()) {
  x <- vec_cast(x, double())
  new_percent(x)
}