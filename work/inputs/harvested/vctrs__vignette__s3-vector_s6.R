# r2py crawler metadata
# package: vctrs
# source_type: vignette
# topic: s3-vector_s6
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\vctrs\doc\s3-vector.R
# lines: 4

suppressPackageStartupMessages(library(vctrs))
is_percent <- function(x) {
  inherits(x, "vctrs_percent")
}