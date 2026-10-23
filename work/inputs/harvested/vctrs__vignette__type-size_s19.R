# r2py crawler metadata
# package: vctrs
# source_type: vignette
# topic: type-size_s19
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\vctrs\doc\type-size.R
# lines: 16

suppressPackageStartupMessages(library(vctrs))
str(vec_cast_common(
  FALSE, 
  1:5, 
  2.5
))

str(vec_cast_common(
  factor("x"), 
  factor("y")
))

str(vec_cast_common(
  data.frame(x = 1),
  data.frame(y = 1:2)
))