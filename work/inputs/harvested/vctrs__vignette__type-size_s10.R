# r2py crawler metadata
# package: vctrs
# source_type: vignette
# topic: type-size_s10
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\vctrs\doc\type-size.R
# lines: 6

suppressPackageStartupMessages(library(vctrs))
try({
vec_ptype_show(logical(), integer(), double())

vec_ptype_show(logical(), character())
})