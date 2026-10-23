# r2py crawler metadata
# package: vctrs
# source_type: vignette
# topic: type-size_chunk11
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\vctrs\doc\type-size.Rmd
# lines: 12

suppressPackageStartupMessages(library(vctrs))
vec_ptype_show(
      array(1, c(0, 1)), 
      array(1, c(0, 2))
    )
    
    vec_ptype_show(
      array(1, c(0, 1)), 
      array(1, c(0, 3)),
      array(1, c(0, 3, 4)),
      array(1, c(0, 3, 4, 5))
    )