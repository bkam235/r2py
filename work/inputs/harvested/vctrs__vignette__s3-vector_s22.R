# r2py crawler metadata
# package: vctrs
# source_type: vignette
# topic: s3-vector_s22
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\vctrs\doc\s3-vector.R
# lines: 4

suppressPackageStartupMessages(library(vctrs))
as_percent <- function(x) {
  vec_cast(x, new_percent())
}