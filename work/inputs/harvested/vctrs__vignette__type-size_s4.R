# r2py crawler metadata
# package: vctrs
# source_type: vignette
# topic: type-size_s4
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\vctrs\doc\type-size.R
# lines: 4

suppressPackageStartupMessages(library(vctrs))
vec_ptype_show(array(logical(), c(2, 3)))
vec_ptype_show(array(integer(), c(2, 3, 4)))
vec_ptype_show(array(character(), c(2, 3, 4, 5)))