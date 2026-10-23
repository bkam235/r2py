# r2py crawler metadata
# package: vctrs
# source_type: vignette
# topic: type-size_chunk17
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\vctrs\doc\type-size.Rmd
# lines: 6

suppressPackageStartupMessages(library(vctrs))
vec_ptype_show(
      data.frame(x = FALSE), 
      data.frame(x = 1L),
      data.frame(x = 2.5)
    )