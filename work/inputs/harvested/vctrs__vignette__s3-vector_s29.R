# r2py crawler metadata
# package: vctrs
# source_type: vignette
# topic: s3-vector_s29
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\vctrs\doc\s3-vector.R
# lines: 6

suppressPackageStartupMessages(library(vctrs))
try({
vec_cast(c(1, 2, 10), to = integer())

vec_cast(c(1.5, 2, 10.5), to = integer())
})