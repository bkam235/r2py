# r2py crawler metadata
# package: vctrs
# source_type: vignette
# topic: type-size_s7
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\vctrs\doc\type-size.R
# lines: 4

suppressPackageStartupMessages(library(vctrs))
vec_ptype_show(Sys.Date())
vec_ptype_show(Sys.time())
vec_ptype_show(as.difftime(10, units = "mins"))