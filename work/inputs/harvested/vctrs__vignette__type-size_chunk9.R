# r2py crawler metadata
# package: vctrs
# source_type: vignette
# topic: type-size_chunk9
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\vctrs\doc\type-size.Rmd
# lines: 4

suppressPackageStartupMessages(library(vctrs))
df <- data.frame(x = FALSE)
    df$y <- data.frame(a = 1L, b = 2.5)
    vec_ptype_show(df)