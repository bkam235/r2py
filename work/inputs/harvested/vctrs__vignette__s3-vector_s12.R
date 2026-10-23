# r2py crawler metadata
# package: vctrs
# source_type: vignette
# topic: s3-vector_s12
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\vctrs\doc\s3-vector.R
# lines: 6

suppressPackageStartupMessages(library(vctrs))
try({
vec_ptype2("bogus", percent())
vec_ptype2(percent(), NA)
vec_ptype2(NA, percent())
})